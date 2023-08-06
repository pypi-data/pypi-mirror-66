## imports
import os
import numpy as np
import pandas as pd
import json
import sqlite3
from datetime import datetime

from ..core.materials import Concrete, Steel
from ..core.sections import Section
from .slns import SLN, Sect

def get_sec(src="20_007_map_sezioni.xlsx", sec_dir="data_sec"):
    '''
    read design sections.
        src     = source file (.xlsx)
        sec_dir = directory where sections files (.json) to be saved.
    '''
    print(f"\nreading design cross sections...")
    df_mat = pd.read_excel(src, sheet_name="Materials", usecols=range(7),  skiprows=[1])
    df_sec = pd.read_excel(src, sheet_name="Sections",  usecols=range(32), skiprows=[1,2,3])
    # materials
    mat = {}
    for _,row in df_mat.iterrows():
        if row["type"].lower() in ["concrete","calcestruzzo"]:
            m = Concrete(fck=row["fk"], gamma=row["gamma"], LC=row["LC"], alpha_cc=row["alpha_cc"], v1=row["v1"])
        elif row["type"].lower() in ["steel","acciaio"]:
            m = Steel(fyk=row["fk"], gamma=row["gamma"], LC=row["LC"])
        else:
            m = Concrete()
        m.id = row["id"]
        mat.update({row["id"]: m})
    # dir
    if not os.path.exists(sec_dir):
        os.mkdir(sec_dir)
    ## create sections
    df_sec["span"] = False
    df_sec["end1"] = False
    df_sec["end2"] = False
    df_sec["file"] = "-"
    for ind,row in df_sec.iterrows():
        b  = row["B"]*10  # mm
        d  = row["H"]*10  # mm
        c  = row["C"]*10  # mm
        sec = {"id":row["ID"],"type":row["type"],"grp":row["grp"]}
        # 3 input sections 
        st = [None]*3
        print(f"creating cross section {row['ID']:20}  [{ind+1:4.0f}/{len(df_sec)}] ...", end="\r", flush=True)
        for j in range(3):
            dim = row[[f"d1_{j}",f"n1_{j}",f"d2_{j}",f"n2_{j}",f"ds_{j}",f"ns_{j}",f"ss_{j}"]]
            dim = dim.replace("-",np.nan)
            if any(dim[[f"d1_{j}",f"n1_{j}",f"ds_{j}",f"ns_{j}",f"ss_{j}"]].isna()):
                continue
            dim = dim.fillna(0)
            d1 = float(dim[f"d1_{j}"])
            n1 =   int(dim[f"n1_{j}"])
            d2 = float(dim[f"d2_{j}"])
            n2 =   int(dim[f"n2_{j}"])
            ds = float(dim[f"ds_{j}"])
            ns =   int(dim[f"ns_{j}"])
            ss = float(dim[f"ss_{j}"])
            # ---------
            if row["type"].lower() in ["t","mz","b"]:
                # layer1 = upper side; layer2 = lower side
                rebar = {
                    'y': [-b/2+c+(b-2*c)*i/(n1-1) for i in range(n1)] + [-b/2+c+(b-2*c)*i/(n2-1) for i in range(n2)],
                    'z': [-d/2+c]*n1 + [d/2-c]*n2,
                    'd': [d1]*n1   + [d2]*n2
                }
            else:
                # layer1 = upper/lower sym.; layer2 = left/right sym. (excl. corners of layer1)
                _y1 = [-b/2+c+(b-2*c)*i/(n1-1) for i in range(n1)]*2
                _z1 = [-d/2+c]*n1 + [d/2-c]*n1
                _d1 = [d1]*n1*2
                _y2 = [-b/2+c]*n2 + [b/2-c]*n2
                _z2 = [-d/2+c+(d-2*c)*(i+1)/(n2+1) for i in range(n2)]*2
                _d2 = [d2]*n2*2
                rebar = {'y': _y1 + _y2, 'z': _z1 + _z2, 'd': _d1 + _d2}
            stirr = {'d': ds, 's': ss, 'nx': ns, 'ny': ns}
            # ---------
            sect = Sect(name=str(j), mat=mat[row["mat"]], mrf=mat[row["mrf"]], shape='rect', d=d, b=b, rebar=rebar, stirr=stirr)
            sect.id = j
            st[j] = sect.__dict__
        # assign for check
        for j,k in enumerate(["span","end1","end2"]):
            ref = row[f"ref_{j}"]
            if pd.isna(ref) or ref<0:
                sec.update({k: None})
            else:
                ref = min(int(ref), 2)
                sec.update({k: st[ref]})
                df_sec.loc[ind,k] = True
        # ---------
        df_sec.loc[ind,"file"] = f'{row["ID"]}.json'
        with open(f'{sec_dir}/{row["ID"]}.json',"w") as f:
            json.dump(sec, f, indent=4)
    print(f"creating cross section  {row['ID']:20}  [{ind+1:4.0f}/{len(df_sec)}] completed.")
    log = {
        "date": f"{datetime.today():%d/%m/%Y}",
        "time": f"{datetime.now():%H:%M:%S}",
        "source": src,
        "sec": df_sec[["ID","type","grp","span","end1","end2","file"]].to_dict('list')
    }
    with open(f'{sec_dir}/_index.json',"w") as f:
            json.dump(log, f, indent=4)
    print('done.')


def read_fem(fem_xls="model_data.xlsx", res_xls=["result_slu.xlsx","result_slv.xlsx"], save_to="data.h5"):
    '''
    read fem data (sofistik).
        fem_xls = model data file (.xlsx), exported from sofistik, with sheets ["SLN_ID"]["SLN-Beams"]["Beams"]["Nodes"];
        res_xls = list of result files (.xlsx), exported from sofistik, with sheet ["Beam-Forces"];
        save_to = save to data file (.h5) for checks, see function "get_sln()".
    '''
    # dir
    if not os.path.exists(os.path.dirname(save_to)):
        os.mkdir(os.path.dirname(save_to))
    log = {
        "date": f"{datetime.today():%d/%m/%Y}",
        "time": f"{datetime.now():%H:%M:%S}",
    }
    # ----
    sheets = ["Nodes","Beams","SLN-Beams","SLN_ID"]
    tables = ["node" ,"beam" ,"slnb"   ,"slnt"]
    # Nodes: "NR "	"X [m]"	"Y [m]"	"Z [m]"
    # Beams: "NR "	"group "	"DL [m]"	"node1 "	"node2 "
    # SLN-Beams: "NR "	"S "	"SubSln "	"SubS "	"Beam "	"X [m]"
    # SLN_ID: "NR "	"Text "
    if fem_xls is not None:
        for i,sht in enumerate(sheets):
            print(f"updating model table {sht} in {save_to}...")
            df_fem = pd.read_excel(fem_xls, sheet_name=sht)
            df_fem.columns = df_fem.columns.str.replace(' ', '')
            df_fem.columns = df_fem.columns.str.replace('[m]', '', regex=False)
            if sht in ["Nodes","Beams","SLN_ID"]:
                df_fem = df_fem.set_index("NR")
            df_fem.to_hdf(save_to, tables[i] , mode="a" if i>0 else "w")
        log.update({"fem":fem_xls})
    # ---------
    # Beam-Forces: "LC "	"NR "	"X [m]"	"N [kN]"	"VY [kN]"	"VZ [kN]"	"MT [kNm]"	"MY [kNm]"	"MZ [kNm]"
    if res_xls is not None:
        for i,xls in enumerate(res_xls):
            print(f"updating forces set {i} from {xls}...")
            df_res  = pd.read_excel(xls, sheet_name="Beam-Forces").rename(
                columns={"LC ":"LC","NR ":"Beam","X [m]":"X","N [kN]":"N","VY [kN]":"VY","VZ [kN]":"VZ","MT [kNm]":"MT","MY [kNm]":"MY","MZ [kNm]":"MZ"}
            )
            df_res.to_hdf(save_to, f"res{i}" ,mode="a")
        log.update({"res":res_xls})
    # ---------
    print(f"saved into {save_to}.")
    with open(f'{os.path.splitext(save_to)[0]}.json',"w") as f:
        json.dump(log, f, indent=4)
    print("done.")


def update_db(database, fem_xls=None, res_xls=[]):
    connection = sqlite3.connect(database)
    cur = connection.cursor()
    # fem_xls="model_data.xlsx"
    # res_xls=["result_slu.xlsx","result_slv.xlsx"]
    sheets = ["Nodes","Beams","SLN-Beams","SLN_ID"]
    tables = ["node" ,"beam" ,"slnb"   ,"slnt"]
    for i,sht in enumerate(sheets):
        print(f"updating model table {sht} in {database}...")
        df_fem = pd.read_excel(fem_xls, sheet_name=sht)
        df_fem.columns = df_fem.columns.str.replace(' ', '')
        df_fem.columns = df_fem.columns.str.replace('[m]', '', regex=False)
        df_fem.to_sql(name=tables[i], con=connection, if_exists="replace", index=False)

    for i,s in enumerate(res_xls):
        if s is not None:
            print(f"updating result set {i} in {database}...")
            df_res  = pd.read_excel(s, sheet_name="Beam-Forces").rename(
                            columns={"LC ":"LC","NR ":"Beam","X [m]":"X","N [kN]":"N","VY [kN]":"VY","VZ [kN]":"VZ","MT [kNm]":"MT","MY [kNm]":"MY","MZ [kNm]":"MZ"}
                        )
            df_res.to_sql(name=f"forces_{i}", con=connection, if_exists="replace", index=False)

    # cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cur.fetchall())
    cur.close()


def get_sln(src="data.h5", sln_dir="data_sln"):
    '''
    read sln data (sofistik fem).
        src     = source file (.h5), see function "read_fem()"
        sln_dir = directory where sln files (.json) to be saved.
    '''
    print("\nreading sln data...")
    # dir
    if not os.path.exists(sln_dir):
        os.mkdir(sln_dir)
    # ---
    df_sln  = pd.read_hdf(src, "slnt", mode="r")
    df_slnb = pd.read_hdf(src, "slnb", mode="r")
    df_node = pd.read_hdf(src, "node", mode="r")
    df_beam = pd.read_hdf(src, "beam", mode="r")
    # ----
    sln = df_sln.sort_index().rename(columns={"Text":"ID"})
    for k in ["ndiv", "node1","x1","y1","z1", "node2","x2","y2","z2", "forces", "file"]:
        sln[k] = 0
    # ----
    for ind,row in sln.iterrows():
        print(f"creating SLN {ind:4.0f}/{sln.index.max()}...", end="\r", flush=True)
        s = SLN(ind, row["ID"])
        # beam sections
        df1 = df_slnb.loc[df_slnb["SubSln"]==ind, :]
        df1["SubS"] = np.round(df1["SubS"], 5)
        df1 = df1.drop_duplicates(["SubSln","SubS"],'last').sort_values(["SubS"], ignore_index=True)
        sln.loc[ind,"ndiv"] = int(len(df1)/2)
        s.length = df1["SubS"].max()
        df1["mid"] = np.abs(df1["SubS"]-s.length/2)
        df1["sec"] = 0
        df1.loc[df1["SubS"]<s.length*1/4,"sec"]=1   # from 0 to 1/4
        df1.loc[df1["SubS"]>s.length*3/4,"sec"]=2   # from 3/4 to 1 
        s.stations = []
        s.sections = []
        for _ind,_row in df1.iterrows():
            sec = Sect()
            sec.id       = int(_row["sec" ])
            sec.name     = f"end{sec.id}" if sec.id>0 else "span"
            sec.ref_beam = int(_row["Beam"])
            sec.ref_x    = _row["X"   ]
            if sec.ref_beam in df_beam.index:
                sec.ref_nq = int(df_beam.loc[sec.ref_beam,"group"])
            s.stations += [_row["SubS"]]
            s.sections += [sec.__dict__]
        # nodes
        if len(df1)<2:
            continue
        if df1.loc[0,"Beam"] in df_beam.index:
            n1 = df_beam.loc[df1.loc[0,"Beam"], "node1" if df1.loc[0,"X"]==0 else "node2"].item()
            s.node1 = {"nr":n1, "x":df_node.loc[n1, "X"], "y":df_node.loc[n1, "Y"], "z":df_node.loc[n1, "Z"]}
            sln.loc[ind,["node1","x1","y1","z1"]] = s.node1.values()
        if df1.loc[len(df1)-1,"Beam"] in df_beam.index:
            n2 = df_beam.loc[df1.loc[len(df1)-1,"Beam"], "node1" if df1.loc[len(df1)-1,"X"]==0 else "node2"].item()
            s.node2 = {"nr":n2, "x":df_node.loc[n2, "X"], "y":df_node.loc[n2, "Y"], "z":df_node.loc[n2, "Z"]}
            sln.loc[ind,["node2","x2","y2","z2"]] = s.node2.values()
        if min(s.node1["nr"],s.node2["nr"])>0:
            s.has_nodes = True
        # # forces
        # s.forces = []
        # for i in range(len(s.stations)):
        #     sec = s.sections[i]
        #     df2 = df_bfor.loc[(df_bfor["NR"]==sec["ref_beam"])&(df_bfor["X"]==sec["ref_x"]), ["LC","N","VY","VZ","MT","MY","MZ"]]
        #     s.forces += [df2.to_dict('list')]
        #     sln.loc[ind,"forces"] = int(df2["LC"].nunique())
        # ---------
        sln.loc[ind, "file"] = f'{s.id}.json'
        with open(f'{sln_dir}/{s.id}.json',"w") as f:
            json.dump(s.__dict__, f, indent=4)
    print(f"creating SLN {ind:4.0f}/{sln.index.max()} completed.")
    log = {
        "date": f"{datetime.today():%d/%m/%Y}",
        "time": f"{datetime.now():%H:%M:%S}",
        "source": src,
        "sln": sln.loc[sln["ndiv"]>0,:].to_dict('index')
    }
    with open(f'{sln_dir}/_index.json',"w") as f:
        json.dump(log, f, indent=4)
    print("done.")