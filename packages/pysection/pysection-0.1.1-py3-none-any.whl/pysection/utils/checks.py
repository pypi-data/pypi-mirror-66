import numpy as np
import pandas as pd
import json
import os
import io
from datetime import datetime
from .slns import SLN

def run_check(sec_dir="data_sec", sln_dir="data_sln", res_dir="data_res", data_hdf="data.h5", data_set=0, types=None, groups=None, LC_af=None, LC_st=None):
    '''
    check ULS strength (NTC-2018).
        sec_dir = directory where design section files (.json) saved;
        sln_dir = directory where sln (from sofistik) files (.json) saved;
        res_dir = directory where to save the resutls;
        data_hdf = data file (.h5) of beam forces;
        data_set = number of set (in list of res_xls) to be checked, [default=0, first set], see function "read_fem(res_xls=[...])";
        types   = list of types  of sln to be checked [default=None, check all];
        groups  = list of groups of sln to be checked [default=None, check all];
        LC_af   = list of loadcases to be checked with axial-flexure [default=None, check all];
        LC_st   = list of loadcases to be checked with shear-torsion [default=None, check all].
    '''
    try:
        sec_index = json.load(open(f"{sec_dir}/_index.json","r"))
    except:
        print(f"{sec_dir}/_index.json not valid!")
        raise
    try:
        sln_index = json.load(open(f"{sln_dir}/_index.json","r"))
    except:
        print(f"{sln_dir}/_index.json not valid!")
        raise
    try:
        df_bfor = pd.read_hdf(data_hdf, f"res{data_set}", mode="r")
    except:
        print(f"{data_hdf} or its set {data_set} not valid!")
        raise
    # ----------
    res_dir = f"{res_dir}_{data_set}"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    # ----------
    print("\nchecking cross sections of sln...")
    sln_f = pd.DataFrame(sln_index["sln"]).T
    # ----
    # filterring
    sln_f = sln_f.loc[sln_f["ID"].isin(sec_index["sec"]["ID"]),:]
    sln_checked = []
    sln_summary = []
    res_df = pd.DataFrame()
    for ind,row in sln_f.iterrows():
        # --- read data
        sln_data = json.load(open(f"{sln_dir}/{row['file']}","r"))
        _ind = sec_index["sec"]["ID"].index(row["ID"])
        sec_data = json.load(open(f"{sec_dir}/{sec_index['sec']['file'][_ind]}","r"))
        # --- assemble cross sections to SLN
        # print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] ...", end="\r", flush=True)
        sln = SLN().from_dict(sln_data)
        sln.type  = sec_data["type"]
        if sec_data["grp"]>=0:
            sln.group = sec_data["grp" ]
            for sec in sln.sections:
                sec["ref_nq"] = sln.group
        else:
            sln.group = int(sln.sections[0]["ref_nq"]/abs(sec_data["grp"]))
        for i,sec in enumerate(sln.sections):
            if (types is None or sln.type in types) and (groups is None or sec["ref_nq"] in groups):
                if sec["id"]>=0:
                    if sec_data[sec["name"]] is not None:
                        sec_data[sec["name"]]["ref_beam"] = sec["ref_beam"]
                        sec_data[sec["name"]]["ref_x"   ] = sec["ref_x"   ]
                        sec.update(sec_data[sec["name"]])
                        sln.has_sections = True
        # --- checks
        if sln.has_sections:
            sln.get_forces(bfor=df_bfor)
            sln.check(groups=groups, LC_af=LC_af, LC_st=LC_st)
            if not all([r["data"] is None for r in sln.results]):
                rho_max = max([r['rho'] for r in sln.results])
                if rho_max<=1:
                    print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] -> {rho_max:5.3f}", end="\r", flush=True)
                else:
                    print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] -> {rho_max:5.3f}")
                filename = f'{res_dir}/{sln.id}.json'
                with open(filename,"w") as f:
                    json.dump(sln.__dict__, f, indent=4)
                sln_checked += [f'{sln.id}.json']
                # -----
                df1 = pd.DataFrame(sln.summary)
                df1["SLN"  ] = [sln.id   ]*len(df1)
                df1["sec"  ] = [sln.name ]*len(df1)
                df1["type" ] = [sln.type ]*len(df1)
                df1["group"] = [sln.group]*len(df1)
                res_df = pd.concat([res_df, df1],ignore_index=True) 
                # sln_summary += [{"id":sln.id, "sec":sln.name, "type":sln.type, "group":sln.group, "sum":sln.summary}]
    print(f"checking SLN {ind:>4} [total checked {len(sln_checked):>4}] completed.")
    # ----
    print("saving results...")
    res_df["rho_max"] = res_df[["rho_flexure","rho_shear"]].max(axis=1)
    res_df["weak"] = res_df[["rho_flexure","rho_shear"]].idxmax(axis=1)
    res_df["weak"] = res_df["weak"].str.replace("rho_", "") 
    res_df.to_hdf(f"{res_dir}/_results.h5","res",mode='w')
    sum_df = res_df.loc[res_df.groupby('SLN')['rho_max'].idxmax(), ["SLN","sec","type","group","rho_max","LC","station","weak"]]
    log={
        "date": f"{datetime.today():%d/%m/%Y}",
        "time": f"{datetime.now():%H:%M:%S}",
        "sln": sln_checked,
        "summary":sum_df.to_dict('list')
    }
    with open(f"{res_dir}/_summary.json", "w") as f:
            json.dump(log,f,indent=4)
    print("done.")

