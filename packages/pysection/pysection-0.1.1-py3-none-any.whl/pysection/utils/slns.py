## imports
import numpy as np
import pandas as pd
import json
import os
import io
import datetime
from ..core.sections import Section


class Sect(Section):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.ref_beam = 0
        self.ref_x    = 0
        self.ref_nq   = -1
    
    def check(self, forces=[(0,0,0,0,0,0)], flexure=None, shear=None):
        '''
        forces = [(Nx,Vy,Vz,Mt,My,Mz),...] in kN,m
        '''
        Ncd = self.axial_resistances["Nc"]
        Ntd = self.axial_resistances["Nt"]
        # Myd = self.domains["My"]
        # Mzd = self.domains["Mz"]
        Nxd = [None]*len(forces)
        Myd = [None]*len(forces)
        Mzd = [None]*len(forces)
        alpha = [None]*len(forces)
        Vyd = [None]*len(forces)
        Vzd = [None]*len(forces)
        Vyt = [None]*len(forces)
        Vzt = [None]*len(forces)
        rho_flexure = [None]*len(forces)
        rho_shear   = [None]*len(forces)
        for i in range(len(forces)):
            Nx,Vy,Vz,Mt,My,Mz = forces[i]
            # axial flexure
            if flexure is None or flexure[i]:
                Nxd[i] = Ntd if Nx>0 else -Ncd
                Myd[i], Mzd[i] = self.get_flexure_resistance(Nx=min(0,Nx), sign_My=My, sign_Mz=Mz)
                rho_My = My/Myd[i]
                rho_Mz = Mz/Mzd[i]
                v = max(-Nx,0)*1000 / (self.A-self.As) / self.mat["fcd"]
                alpha[i] = 1
                if v>0.1 and v<0.7:
                    alpha[i] = 1+(v-0.1)/(0.7-0.1)*0.5
                elif v>0.7:
                    alpha[i] = 1.5+(v-0.7)/(1.0-0.7)*0.5
                alpha[i] = min(alpha[i], 2)
                if self.shape_inputs["shape"] in ["circ"]:
                    alpha[i] = 2
                rho_flexure[i] = (rho_My**alpha[i] + rho_Mz**alpha[i])**(1/alpha[i])
            # shear torsion
            if shear is None or shear[i]:
                Vyd[i], Vzd[i] = self.get_shear_resistance(Nx=Nx)
                Vyt[i] = abs(Mt)*1000/(self.stirr["bw"][0]/2)*2
                Vzt[i] = abs(Mt)*1000/(self.stirr["bw"][1]/2)*2
                rho_Vy = (abs(Vy)+Vyt[i])/Vyd[i]
                rho_Vz = (abs(Vz)+Vzt[i])/Vzd[i]
                rho_shear[i] = max(rho_Vy, rho_Vz)
        return {
            "Nxd": Nxd, "Myd":Myd, "Mzd":Mzd, "alpha":alpha, "Vyd":Vyd,"Vzd":Vzd,"Vyt":Vyt,"Vzt":Vzt,
            "rho_flexure":rho_flexure,"rho_shear":rho_shear
        }


class SLN:
    def __init__(self, id=0, name="Line"):
        self.id = id
        self.name = name
        self.type = "T"
        self.group  = 0
        self.length = 0
        self.node1 = {"nr":0,"x":0,"y":0,"z":0}
        self.node2 = {"nr":0,"x":0,"y":0,"z":0}
        self.stations = []
        self.sections = []
        self.forces   = []
        self.results  = []
        self.is_checked = False
        self.has_sections = False
        self.has_nodes = False
        self.summary  = {}

    def __repr__(self):
        return f"<SLN - {self.id}>"
    
    def from_dict(self, vdict):
        self.__dict__.update(vdict)
        return self
    
    def get_forces(self, bfor):
        self.forces = [None]*len(self.stations)
        bfor["X"] = np.round(bfor["X"],5)
        for i,sec in enumerate(self.sections):
            df2 = bfor.loc[(bfor["Beam"]==sec["ref_beam"])&(bfor["X"]==round(sec["ref_x"],5)), ["LC","N","VY","VZ","MT","MY","MZ"]]
            if len(df2):
                self.forces[i] = df2.to_dict('list')


    def check(self, groups=None, LC_af=None, LC_st=None):
        results = [None]*len(self.stations)
        res_df = pd.DataFrame()
        for i,sec in enumerate(self.sections):
            if sec["A"]>0 and (groups is None or sec["ref_nq"] in groups) and self.forces[i] is not None:
                sect = Sect().from_dict(sec)
                forc = pd.DataFrame(self.forces[i])
                # -- loadcases
                if LC_af is None:
                    flexure = None
                else:
                    flexure = forc["LC"].isin(LC_af).to_list()
                if LC_st is None:
                    shear = None
                else:
                    shear = forc["LC"].isin(LC_st).to_list()
                # -- check
                res = pd.DataFrame(sect.check(forc[["N","VY","VZ","MT","MY","MZ"]].to_numpy().tolist(), flexure=flexure, shear=shear))
                res["LC"] = forc["LC"]
                idx_flexure = res["rho_flexure"].idxmax()
                idx_shear   = res["rho_shear"  ].idxmax()
                rho_flexure = res["rho_flexure"][idx_flexure]
                rho_shear   = res["rho_shear"  ][idx_shear  ]
                LC_flexure = int(res["LC"][idx_flexure])
                LC_shear   = int(res["LC"][idx_shear  ])
                self.is_checked = True
                rho = max(rho_flexure, rho_shear)
                results[i] = {"data":res.to_dict('list'),"rho":rho,"rho_flexure":rho_flexure,"rho_shear":rho_shear,"LC_flexure":LC_flexure,"LC_shear":LC_shear}
                res1 = pd.DataFrame({"station":[self.stations[i]]*len(res)})
                res1 = pd.concat([res1, res[["LC","rho_flexure","rho_shear"]]], axis=1, sort=False)
                # res1.columns = pd.MultiIndex.from_tuples([(f"s={self.stations[i]:5.3f}m",f"{k}") for k in ["flexure","shear"]], names=["station","rho"])
                res_df = pd.concat([res_df, res1], axis=0, sort=False, ignore_index=True)
            else:
                results[i] = {"data":None,"rho":0,"rho_flexure":0,"rho_shear":0,"LC_flexure":0,"LC_shear":0}
        self.results = results
        self.summary = res_df.to_dict('list')
