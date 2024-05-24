from math import sqrt

from corematmaconnerie import *
from corematbetonarme import * 
from corematacierarmature import *
from coresituationprojet import *
from coreconstante import ES

class CisaillementMurChaine:
    
    def __init__(self, bloc, beton, acier, lt, l, Zv, d, MEd, NEd, VEd, Ac, As, position):
        self.bloc = bloc
        self.beton = beton
        self.acier = acier
        self.lt = lt
        self.l = l
        self.Zv = Zv
        self.d = d
        self.MEd = MEd
        self.NEd = NEd
        self.VEd = VEd
        self.Ac = Ac
        self.As = As
        self.position = position
        
    # def VRd(self):
    #     Ac = self.Ac
    #     fvd = self.bloc.fvd()
    #     fcvk = self.fcvk()
    #     gamma_c = self.beton.situation.gamma_c()
    #     t = self.bloc.t
    #     l = self.l
    #     return fvd * t * l + Ac * fcvk / gamma_c
    
    def VRd(self):
        fvd = self.bloc.fvd()
        t = self.bloc.t
        d = self.d
        return fvd * t * d
    
    def VRdlt(self):
        fd = self.bloc.fd
        t = self.bloc.t
        d = self.d
        return 0.3 * fd * t * d
    
    def MRd(self):
        As = self.As
        fyd = self.acier.fyd()
        d = self.d
        x = self.x()
        NEd = self.NEd
        l = self.l
        return As * fyd * (d - 0.4 * x) + NEd * (l / 2 - 0.4 * x)
    
    def x(self):
        emu = self.bloc.emu()
        epsilon_yd = self.acier.epsilon_yd()
        d = self.d
        return emu / (emu + epsilon_yd) * d
        
    def lc(self):
        lt = self.lt
        Ma = self.Ma()
        fd = self.bloc.fd
        fip = self.fip()
        t = self.bloc.t
        d = self.d
        return lt * (1 - sqrt(1 - (2 * Ma) / (fd * fip * d**2 * t)))
    
    def ea(self):
        Ma = self.Ma()
        NEd = self.NEd
        return Ma / NEd
    
    def Ma(self):
        MEd = self.MEd
        NEd = self.NEd
        VEd = self.VEd
        lt = self.lt
        Zv = self.Zv
        return MEd + NEd * lt / 2 + VEd * Zv
    
    def sigmad(self):
        NEd = self.NEd
        lt = self.lt
        t = self.bloc.t
        return NEd / (lt * t)
    
    def ASVcalc(self):
        lc = self.lc()
        t = self.bloc.t
        fip = self.fip()
        fd = self.bloc.fd
        NEd = self.NEd
        esu = self.esu()
        return ((lc * t * fip * fd) - NEd) / (ES * esu)
    
    def esu(self):
        emu = self.bloc.emu()
        d = self.d
        lc = self.lc()
        fyd = self.acier.fyd()
        esu1 = emu * (d - 1.25 * lc) / (1.25 * lc)
        esu2 = fyd / ES
        return min(esu1, esu2)
    
    # def isBasculement(self):
    #     Zv = self.Zv
    #     VEd = self.VEd
    #     NEd = self.NEd
    #     l = self.l
    #     ea = self.ea()
    #     if Zv * VEd / NEd > l - ea:
    #         return True
    #     else:
    #         return False
    
    def fcvk(self):
        classeResistance = self.beton.classeresistance
        dict_fcvk = {"C12/15" : 0.27,
                     "C16/20" : 0.33,
                     "C20/25" : 0.39,
                     "C25/30" : 0.45,
                     "C30/37" : 0.45,
                     "C35/45" : 0.45,
                     "C40/50" : 0.45,
                     "C45/55" : 0.45,
                     "C50/60" : 0.45,
                     "C55/67" : 0.45,
                     "C60/75" : 0.45,
                     "C70/85" : 0.45,
                     "C80/95" : 0.45,
                     "C90/105" : 0.45}
        return dict_fcvk[classeResistance]
    
    def fip(self):
        position = self.position
        dict_fip = {"Façade" : 0.6,
                    "Rive" : 0.6,
                    "Intérieur" : 0.8,
                    "Refend" : 0.8}
        return dict_fip[position]
        
    
if __name__ == "__main__":
    
    situation = "Accidentelle"
    situation = SituationProjet(situation)
    
    classe_exposition = "XC3"
    classe_resistance = "C16/20"
    classe_ciment = "N"
    acc = 1
    act = 1
    ae = 15
    fiinft0 = 2
    age = 28
    beton = BetonArme(situation, classe_exposition, classe_resistance,acc, act, age, classe_ciment, ae, fiinft0)
    
    nuance = "S500B"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
        
    t = 20 / 100 # m
    fvk = 0.32 # MPa
    gammaM = 1.5
    fb = 5.43 # MPa
    fd = 1.74 # MPa
    groupe = 3
    bloc = BlocMaconnerie(groupe, t, fvk, fb, fd, gammaM)
        
    lt = 300 / 100 # m
    l = 285 / 100 # m
    d = 293 / 100 # m
    Zv = 450 /100 # m
    MEd = 0 # MN.m
    VEd = 6.5 / 100 # MN
    NEd = 17.5 / 100 # MN
    Ac = 15 / 100 * t
    As = 3.14 / 1e4
    position = "Façade"
    mcs = CisaillementMurChaine(bloc, beton, acier, lt, l, d, Zv, MEd, NEd, VEd, Ac, As, position)
    
    print(f"fvd = {mcs.bloc.fvd():.2f} MPa")
    print(f"Ma = {mcs.Ma()*100} T.m")
    print(f"ea = {mcs.ea()*100:.0f} cm")
    print(f"lc = {mcs.lc()*100:.0f} cm")
    print(f"Sigmad = {mcs.sigmad():.2f} MPa")
    print(f"VRd = {mcs.VRd()*100:.2f} T")
    print(f"VRdlt = {mcs.VRdlt()*100:.2f} T")
    print(f"fcvk = {mcs.fcvk():.2f} MPa")
    print(f"fip = {mcs.fip():.2f} MPa")
    # print(f"Baculement ? = {mcs.isBasculement()}")
    print(f"emu = {mcs.bloc.emu()}")
    print(f"esu = {mcs.esu()}")
    print(f"ASVcalc = {mcs.ASVcalc()*1e4:.2f} cm2")
    print(f"MRd = {mcs.MRd()*100:.2f} T.m")
    print(f"x = {mcs.x()*100:.2f} cm")