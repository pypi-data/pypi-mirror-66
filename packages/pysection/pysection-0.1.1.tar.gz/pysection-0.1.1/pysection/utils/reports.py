import numpy as np
import pandas as pd
import json
import os
import io
from datetime import datetime
from ..core.sections import Section

# ------------------------------------
# html report generation
# ------------------------------------
css_style = '''
<style type="text/css">
    html * {
        font-family: consolas;
    }
    body {
        font-size: 10pt;
    }
    .navpanel {
        height:100%;
        width:270px;
        position:fixed;
        z-index:1;
        top:0;
        left:0;
        background-color: #E8E8E8;
        overflow-x: hidden;
        padding: 10px 10px;
    }
    .navpanel ul {
        list-style:none;
		padding:0;
		margin:0;
    }
	.navpanel ul ul {
        list-style:none;
		padding:10px;
    }
    .navpanel a {
        text-decoration: none;
        display: block;
    }
    .navpanel a:hover {
        color: #2196F3;
    }
    .contents {
        margin-left:300px;
        padding: 0px 10px;
    }
    h1 {font-size: 13pt; }
    h2 {font-size: 12pt; background: #E8E8E8; page-break-before: always;}
    h3 {font-size: 12pt; }
    h4 {font-size: 11pt; }
    h5 {font-size: 10pt; font-style: italic;}
    h6 {font-size: 10pt; }
    table {
        font-size: 10pt;
        border: none;
        text-align: right;
    }
    caption {
        text-align: left;
    }
    thead, th {
        font-weight: bold;
    }
    th, td {
        width: 60px;
        overflow: hidden;
        white-space: nowrap;
    }
    @media print {
        body {padding:15px;}
		.navpanel {position:static; height:auto; width:100%; border-bottom: 1px solid black; font-size:100px}
        .navpanel ul {display:none;}
        .contents {margin-left:0;}
        /* h2 {page-break-before: always;} */
    }
</style>
'''

class Report:
    def __init__(self, title="", css=None):
        self.title = title
        self.css = css or css_style
        self.contents = ""
        self.headers = []
        self.navpanel = "<div class='navpanel'><hl><strong>PY-SECTION</strong></hl><p>report</p></div>\n"
    
    def add_contents(self, contents):
        self.contents += contents
    
    def add_headline(self, level, id, headline):
        self.contents += f"<h{level} id='{id}'>{headline}</h{level}>\n"
        self.headers += [(level, id, headline)]

    def get_navpanel(self, title):
        nav = f'''<hl><strong>PY-SECTION</strong></hl><p>{title}</p>\n<ul>\n'''
        for i,h in enumerate(self.headers):
            hi = h[0]
            if i==len(self.headers)-1:
                hj = self.headers[0][0]
            else:
                hj = self.headers[i+1][0]
            nav += f'''<li><a href="#{h[1]}">{h[2]}</a>'''
            if hj<hi:
                nav += f"{'</ul>'*(hi-hj)}\n</li>\n"
            elif hj>hi:
                nav += f"\n{'<ul>'*(hj-hi)}\n"
            else:
                nav += "</li>\n" 
        nav += "</ul>\n"
        self.navpanel = nav

    def get_html(self, nav_title="report"):
        self.get_navpanel(nav_title)
        self.html = f'''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="chrome=1">
        <title>{self.title}</title>
        {self.css}
    </head>
    <body>
        <div class="navpanel">\n{self.navpanel}\n</div>
        <div class="contents">\n{self.contents}\n</div>
    </body>
</html>'''

    def write_html(self, filename, sub_title="report"):
        self.get_html(sub_title)
        with open(f"{filename}.html", "w", encoding="utf-8") as f:
            f.write(self.html)

    def add_table(self, df, rho_cols=None, max_cols=10, max_rows=50):
        '''
        convert DataFrame to html tables
            rho_cols = values to be formatted and highlight for max
            max_cols = max columns in one sub-table
            max_rows = max rows (of all sub-tables) in one page (for printing)
        '''
        ntab = int(np.ceil(len(df.columns)/max_cols)) # number of tables
        html = ""
        if rho_cols is None:
            rho_cols=df.columns
        rmax = df[rho_cols].replace(to_replace="-",value=-1).max().max()
        df.index.name = df.index.name or " "
        # print(f"max rho = {rmax:5.3}")
        ntpp = max(1, int(np.floor(max_rows/(len(df)+3)))) # tables per pages
        for i in range(ntab):
            df1 = df.iloc[:, (i*max_cols):(min(len(df.columns), (i+1)*max_cols))]
            if i>1 and i%ntpp==0:
                html += "<p style='page-break-before:always;'></p><br>\n" 
            html += "<table>\n"
            html += f"<caption>tab.{i+1}/{ntab}</caption>\n"
            # ---- headers
            html += "<thead>\n"
            if isinstance(df1.columns[0], tuple):
                for j in range(len(df1.columns[0])):
                    html += f"<tr><th>{df1.index.name if j==0 else ' '}</th>"
                    nc = 1
                    for k in range(len(df1.columns)):
                        h1 = df1.columns[k][j]
                        if k<len(df1.columns)-1:
                            h2 = df1.columns[k+1][j]
                            if h1==h2:
                                nc+=1
                            else:
                                html += f"<th colspan={nc}>{h1}</th>"
                                nc = 1
                        else:
                            html += f"<th colspan={nc}>{h1}</th>"
                    html += "</tr>\n"
            else:
                html += f"<tr><th>{df1.index.name}</th>"
                for j in range(len(df1.columns)):
                    html += f"<th>{df1.columns[j]}</th>"
                html += "</tr>\n"
            html += "</thead>\n"
            # ----
            for ind,_ in df1.iterrows():
                html += f"<tr><td style='font-weight:bold;'>{ind}</td>\n"
                for j in range(len(df1.columns)):
                    val = df1.loc[ind,df1.columns[j]]
                    if pd.isna(val):
                        html += "<td>-</td>"
                    else:
                        if df1.columns[j] in rho_cols:
                            try:
                                rho = float(val)
                                attr = ''
                                if rho==rmax:
                                    attr += f'font-weight:bold;text-decoration:underline;'
                                    # attr = f'background-color:red;color:white;'
                                if rho>1:
                                    attr += f'color:red;'
                                html += f"<td style={attr}>{rho:5.3f}</td>"
                            except:
                                html += "<td>-</td>"
                        else:
                            html += f"<td>{val}</td>"
                html += "</tr>\n"
            html += "</table><br>\n"
        self.contents += html


# ------------------------------------
# ------------------------------------
# ------------------------------------
def report_summary(res_dir="data_res", filename=None, types=None, groups=None, max_cols=12, detailed=False):
    '''
    generate summary tables (in html file) from results.
        res_dir    = directory where results files (.json) saved, see function "run_check()";
        filename   = filename of report html file to be saved;
        types      = list of types  of sln to be reported [default=None, report all];
        groups     = list of groups of sln to be reported [default=None, report all];
        max_cols   = maximum number of columns to be shown in one table (for printing page width);
    '''
    # ---- check results log
    try:
        with open(f"{res_dir}/_summary.json","r") as f:
            log = json.load(f)
    except:
        print("results not valid!")
        raise
    # -----
    filename = filename or "report_summary"
    # ----
    print("\ngetting summary data ...")
    report = Report(title=f"Summary of {res_dir}")
    all_df = pd.DataFrame(log["summary"])
    all_df["file"] = log["sln"]
    if types is not None:
        all_df = all_df.loc[all_df["type" ].isin(types ),:]
    if groups is not None:
        all_df = all_df.loc[all_df["group"].isin(groups),:]
    # ---
    sum_df = all_df.drop(columns=["file"])
    sum1 = sum_df.set_index("SLN")
    sum1 = sum1.loc[(sum1["rho_max"]>=0.9) | (sum1["rho_max"]>=0.9*sum1["rho_max"].max()),:]
    sum1 = sum1.sort_values(by=["rho_max"], ascending=False)
    report.add_headline(2,"criticals","Critical SLNs")
    report.add_table(sum1, rho_cols=["rho_max"])
    # ---
    idx = sum_df.groupby(['sec'])['rho_max'].transform(max) == sum_df['rho_max']
    sum2 = sum_df.loc[idx]
    sum2 = sum2.drop_duplicates('sec')
    sum2 = sum2[["sec","rho_max","SLN","LC","station","weak"]].set_index("sec")
    sum3 = pd.pivot_table(sum_df, values='rho_max', index='group', columns='type', aggfunc='max')
    report.add_headline(2,"sections","Maximum by sections")
    report.add_table(sum2, rho_cols=["rho_max"])
    report.add_headline(2,"types_groups","Maximum by type and group")
    report.add_table(sum3, rho_cols=sum3.columns)
    # ---
    if detailed:
        print(f"preparing detailed tables ...")
        res_df = pd.read_hdf(f"{res_dir}/_results.h5","res")
        resf = res_df.drop(res_df[pd.isna(res_df["rho_flexure"])].index)
        ress = res_df.drop(res_df[pd.isna(res_df["rho_shear"  ])].index)
        # ---- by section
        resf1 = resf.loc[resf.groupby('sec')['rho_flexure'].idxmax(),["sec","rho_flexure","LC","SLN","station"]].set_index('sec')
        ress1 = ress.loc[ress.groupby('sec')['rho_shear'  ].idxmax(),["sec","rho_shear"  ,"LC","SLN","station"]].set_index('sec')
        report.add_headline(2,"detailed","Detailed Summary Tables")
        report.add_headline(3,"section2","Maximum by sections")
        report.add_headline(4,"sect_f","Flexure checks (ductile failure)")
        report.add_table(resf1, rho_cols=["rho_flexure"])
        report.add_headline(4,"sect_s","Shear checks (fragile failure)")
        report.add_table(ress1, rho_cols=["rho_shear"  ])
        # ---- by type/group
        tt = res_df["type"].unique()
        for t in tt:
            resf2 = resf.loc[resf['type']==t,:]
            ress2 = ress.loc[ress['type']==t,:]
            resf3 = resf2.loc[resf2.groupby('group')['rho_flexure'].idxmax(),["group","rho_flexure","sec","LC","SLN","station"]].set_index('group')
            ress3 = ress2.loc[ress2.groupby('group')['rho_shear'  ].idxmax(),["group","rho_shear"  ,"sec","LC","SLN","station"]].set_index('group')
            report.add_headline(3,f"type_{t}",f"Maximum of Type: '{t}'")
            report.add_headline(4,f"type_{t}_f","Flexure checks (ductile failure)")
            report.add_table(resf3, rho_cols=["rho_flexure"])
            report.add_headline(4,f"type_{t}_s","Shear checks (fragile failure)")
            report.add_table(ress3, rho_cols=["rho_shear"  ])
    # ---
    report.write_html(filename=filename, sub_title="Summary Tables")
    print("html report generated.")
    # ---- statistics
    # resf4 = resf2.loc[resf2["rho_flexure"]>0.90,:]
    # html += f"<p>rho statistics: (only where rho>0.90)</p>\n"
    # html += f'''<table>
    # <tr><td>count =              </td> <td>{resf4["rho_flexure"].count() }</td></tr>
    # <tr><td>maximum =            </td> <td>{resf4["rho_flexure"].max()   :5.3f}</td></tr>
    # <tr><td>minimum =            </td> <td>{resf4["rho_flexure"].min()   :5.3f}</td></tr>
    # <tr><td>average =            </td> <td>{resf4["rho_flexure"].mean()  :5.3f}</td></tr>
    # <tr><td>standard deviation = </td> <td>{resf4["rho_flexure"].std()   :5.3f}</td></tr>
    # <tr><td>median figure =      </td> <td>{resf4["rho_flexure"].median():5.3f}</td></tr>
    # </table>
    # '''
    # plt.style.use('seaborn')
    # plt.hist([resf2["rho_flexure"],ress2["rho_shear"]], 20, label=["flexure","shear"])
    # plt.legend(loc='upper right')
    # plt.show()
        

def report_single(res_dir="data_res", sln_id=120, filename=None):
    '''
    generate report (in html file) for single sln results.
        res_dir    = directory where results files (.json) saved, see function "run_check()";
        sln_id     = sln id (file name without .json);
        filename   = filename of report html file to be saved.
    '''
    filename = filename  or f"report_SLN_{sln_id}"
    print("\npreparing data for report...")
    data = None
    try:
        with open(f"{res_dir}/{sln_id}.json","r") as f:
            data = json.load(f)
    except:
        print(f"data file {res_dir}/{sln_id}.json not valid!")
        raise
    # ----
    if data is not None:
        print(f"generating report for SLN {data['id']}...")
        report = Report(title=f"SLN {data['id']} of {res_dir}")
        # --- nodes
        nodes = f'''<table><thead><tr><td> </td>
            <td>No.  </td> <td>X [m]</td> <td>Y [m]</td> <td>Z [m]</td>
            </tr></thead> \n'''
        for sv in ["node1","node2"]:
            nodes += f'''<tr><td>{sv}</td> 
            <td>{data[sv]["nr"]:7.0f}</td> 
            <td>{data[sv]["x" ]:8.3f}</td> 
            <td>{data[sv]["y" ]:8.3f}</td> 
            <td>{data[sv]["z" ]:8.3f}</td> </tr>\n'''
        nodes += "</table>\n"
        report.add_headline(2, "nodes", "SLN End-Nodes")
        report.add_contents(nodes)
        # --- checks
        for i in range(len(data["stations"])):
            if data["results"][i]["data"]:    
                rs = f"s_{data['stations'][i]:5.3f}"
                report.add_headline(2, rs, f"Resistance Checks - s = {data['stations'][i]:5.3f} / {data['length']:6.3f}")
                # --- cross section
                sec = Section().from_dict(data["sections"][i])
                sects = f'''<table><tr> 
                    <td>  concrete:      </td>
                    <td style="width:150px">  f<sub>cd</sub>  = {sec.mat["fcd"]:5.2f}  MPa  </td>  
                    <td style="width:150px">  f<sub>cvd</sub> = {sec.mat["fcvd"]:5.2f} MPa  </td>  
                    <td style="width:100px"> ( &gamma; = {sec.mat["gamma"]:4.2f}  </td> 
                    <td style="width:100px">  FC = {sec.mat["FC"]} )</td> 
                    </tr><tr> 
                    <td>  reinforcement:  </td>
                    <td style="width:150px">  f<sub>yd</sub>  = {sec.mrf["fyd"]:5.1f}  MPa  </td>  
                    <td style="width:150px">  f<sub>ywd</sub> = {sec.mrf["fywd"]:5.1f} MPa  </td>  
                    <td style="width:100px"> ( &gamma; = {sec.mrf["gamma"]:4.2f}  </td> 
                    <td style="width:100px">  FC = {sec.mrf["FC"]} )</td> 
                    </tr></table> \n'''
                fig1 = io.StringIO()
                sec.plot_geometry(fig1,rebar=True, stirr=False, z_inversed=True, figsize=(12/2.54,12/2.54))
                fig2 = io.StringIO()
                sec.plot_geometry(fig2,rebar=False, stirr=True, z_inversed=True, figsize=(12/2.54,12/2.54))
                sects +='<figure>\n' + fig1.getvalue() + fig2.getvalue() + '\n<figcaption>section geometry</figcaption>\n</figure>\n'
                fig3 = io.StringIO()
                sec.plot_domains(fig3)
                sects +='<figure>\n' + fig3.getvalue() + '\n<figcaption>N-M domains</figcaption>\n</figure>\n'
                report.add_headline(3, f"{rs}_sec", f"Cross section: {sec.name}")
                report.add_contents(sects)
                # --- forces, check and results
                ff  = data["forces"][i]
                for j in range(len(ff['LC'])):
                    lccks = f'''
                    <h5>Design Forces</h5>
                    <table>
                    <tr> <td>N<sub>Ed</sub>   =</td> <td style="width:80px">{ff["N" ][j]:10.0f} kN </td> </tr>
                    <tr> <td>V<sub>y,Ed</sub> =</td> <td style="width:80px">{ff["VY"][j]:10.0f} kN </td> </tr>
                    <tr> <td>V<sub>z,Ed</sub> =</td> <td style="width:80px">{ff["VZ"][j]:10.0f} kN </td> </tr>
                    <tr> <td>T<sub>Ed</sub>   =</td> <td style="width:80px">{ff["MT"][j]:10.0f} kNm</td> </tr>
                    <tr> <td>M<sub>y,Ed</sub> =</td> <td style="width:80px">{ff["MY"][j]:10.0f} kNm</td> </tr>
                    <tr> <td>M<sub>z,Ed</sub> =</td> <td style="width:80px">{ff["MZ"][j]:10.0f} kNm</td> </tr>
                    </table>
                    '''
                    res = data["results"][i]["data"]
                    if not pd.isna(res["rho_flexure"][j]):
                        lccks += f'''
                        <h5>Flexure and Axial Loads check</h5>
                        <i> the stengths are calculated according to Clause 4.1.2.3.4, NTC-2018</i><br>
                        <i> the biaxial flexure-compression combined effect is checked according to Eq.[4.1.19], NTC-2018</i><br><br>
                        <strong>[ ( M<sub>y,Ed</sub> / M<sub>y,Rd</sub> )<sup>&alpha;</sup> + ( M<sub>z,Ed</sub> / M<sub>z,Rd</sub> )<sup>&alpha;</sup> ]<sup>1/&alpha;</sup>
                            = {res["rho_flexure"][j]:5.3f} {"≤" if res["rho_flexure"][j]<=1 else ">"} 1 </strong><br><br>
                        where,<ul>
                        <li>M<sub>y,Rd</sub> = {res["Myd"][j]:10.0f} kNm = uniaxial flexure resistance in y-direction</li>
                        <li>M<sub>z,Rd</sub> = {res["Mzd"][j]:10.0f} kNm = uniaxial flexure resistance in z-direction</li>
                        <li>&alpha; = {res["alpha"][j]:10.2f} = index evaluated according to geometry and compression level </li>
                        </ul>
                        <em>verification {"" if res["rho_flexure"][j]<=1 else "NOT "}satisfied.</em><br><br>
                        '''
                    if not pd.isna(res["rho_shear"][j]):
                        lccks += f'''
                        <h5>Shear and Torsion check</h5>
                        <i> the stengths are calculated according to Clause 4.1.2.3.5, NTC-2018</i><br><br>
                        <strong> max[ ( V<sub>y,Ed</sub> + V<sub>y,T</sub> ) / V<sub>y,Rd</sub>, ( V<sub>z,Ed</sub> + V<sub>z,T</sub> ) / V<sub>z,Rd</sub> ]
                            = {res["rho_shear"][j]:5.3f} {"≤" if res["rho_shear"][j]<=1 else ">"} 1</strong> <br><br>
                        where,<ul>
                        <li>V<sub>y,T</sub>  = {res["Vyt"][j]:10.0f} kN = torsion T<sub>Ed</sub> induced shear in y-direction</li>
                        <li>V<sub>z,T</sub>  = {res["Vzt"][j]:10.0f} kN = torsion T<sub>Ed</sub> induced shear in z-direction</li>
                        <li>V<sub>y,Rd</sub> = {res["Vyd"][j]:10.0f} kN = shear resistance in y-direction</li>
                        <li>V<sub>z,Rd</sub> = {res["Vzd"][j]:10.0f} kN = shear resistance in z-direction</li>
                        </ul>
                        <em>verification {"" if res["rho_shear"][j]<=1 else "NOT "}satisfied.</em><br><br>
                        '''
                    report.add_headline(3, f"{rs}_lc_{ff['LC'][j]}", f"Checks Loadcase LC.{ff['LC'][j]}")
                    report.add_contents(lccks)
                # --------------
        # --------------
        sum_df = pd.DataFrame(data["summary"])
        sum_df = sum_df.pivot(index='LC', columns='station')
        sum_df.columns = pd.MultiIndex.from_tuples([(f"s={c[1]:.5f}",c[0][4:]) for c in sum_df.columns]) #.swaplevel(0, 1)
        sum_df.sort_index(axis=1, level=0, inplace=True)
        report.add_headline(2, "summary", f"Summary of checks - SLN {data['id']}")
        report.add_table(sum_df)
        # -------------
        report.write_html(filename=filename, sub_title=f"SLN {data['id']} Checks")
        print(f"html report for SLN {data['id']} generated.")
    return None

