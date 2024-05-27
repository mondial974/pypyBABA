from math import *

from rich.table import Table
from rich.console import Console

from coreconstante import *
from coresituationprojet import *
from utilsprint import *


class BetonArme:

    def __init__(self, situation, classe_exposition='XC3', classe_resistance='C25/30', alpha_cc=1, alpha_ct=1, age=28, classe_ciment='N', alpha_e=0, fi_infini_t0=2,
                 h=0, maitrise_fissuration=True):
        
        self.situation = situation
        self.classe_exposition = classe_exposition
        self.classe_resistance = classe_resistance
        self.alpha_cc = alpha_cc
        self.alpha_ct = alpha_ct
        self.gamma_c = self.situation.gamma_c()
        self.age = age
        self.classe_ciment = classe_ciment
        self.alpha_e = alpha_e
        self.fi_infini_t0 = fi_infini_t0
        self.h = h
        self.maitrise_fissuration = maitrise_fissuration

    def fck(self):
        classe_resistance = self.classe_resistance
        #---
        fck = DICT_FCK[classe_resistance]
        return fck

    def fck_cube(self):
        classe_resistance = self.classe_resistance
        #---
        fck_cube = DICT_FCK_CUBE[classe_resistance]
        return fck_cube

    def fcm(self):
        """Calcul fcm"""
        fck = self.fck()
        #---
        fcm = fck + 8.
        return fcm

    def fctm(self):
        fck = self.fck()
        fcm = self.fcm()
        #---
        if fck <= 50.:
            return 0.3 * pow(fck, 2./3.)
        else:
            return 2.12 * log10(1. + fcm / 10.)
    
    def fctm_fl(self):
        fctm = self.fctm()
        h = self.h
        #---
        fctm_fl = max(fctm, (1.6 - h / 1000.) * fctm)
        return fctm_fl
    
    def fct_eff(self):
        fctm = self.fctm()
        fctm_fl = self.fctm_fl()
        maitrise_fissuration = self.maitrise_fissuration
        #---
        if maitrise_fissuration == True:
            fct_eff = fctm
        else:
            fct_eff = fctm_fl
        return fct_eff

    def fctk_005(self):
        fctm = self.fctm()
        #---
        fctk_005 = 0.7 * fctm
        return fctk_005

    def fctk_005_t(self):
        fctm_t = self.fctm_t()
        #---
        fctk_005_t = 0.7 * fctm_t
        return fctk_005_t
        
    def fctk_095(self):
        fctm = self.fctm()
        #---
        fctk_095 = 1.3 * fctm
        return fctk_095

    def Ecm(self):
        fcm = self.fcm()
        #---
        Ecm = 22000. * pow(fcm / 10., 0.3)
        return Ecm

    def Eceff(self):
        Ecm = self.Ecm()
        fi_infini_t0 = self.fi_infini_t0
        #---
        Eceff = Ecm / (1 + fi_infini_t0)
        return Eceff

    def get_alpha_e(self):
        Eceff = self.Eceff()
        #---
        if self.alpha_e == 0:
            alpha_e = ES / Eceff
        else:
            alpha_e = self.alpha_e
        return alpha_e
            
    def s_ciment(self):
        classe_ciment = self.classe_ciment
        #---
        s = DICT_S_CIMENT[classe_ciment]
        return s
        
    def beta_cc_t(self):
        age = self.age
        s = self.s_ciment()
        #---
        beta_cc_t = exp(s * (1. - sqrt(28. / age)))
        return beta_cc_t

    def fck_t(self):
        age = self.age
        fcm_t = self.fcm_t()
        fck = self.fck()
        #---
        if age < 28:
            fck_t = fcm_t - 8.
        else:
            fck_t = fck
        return fck_t

    def fcm_t(self):
        beta_cc_t = self.beta_cc_t()
        fcm = self.fcm()
        #---
        fcm_t = beta_cc_t * fcm
        return fcm_t

    def fctm_t(self):
        age = self.age
        beta_cc_t = self.beta_cc_t()
        fctm = self.fctm()
        #---
        if age < 28:
            alpha = 1.
        else:
            alpha = 2./3.
        fctm_t = pow(beta_cc_t, alpha) * fctm
        return fctm_t

    def Ecm_t(self):
        Ecm = self.Ecm()
        fcm_t = self.fcm_t()
        fcm = self.fcm()
        #---
        Ecm_t = Ecm * pow(fcm_t / fcm, 0.3)
        return Ecm_t

    def fcd(self):
        """Calcul fcd"""
        eta = self.eta()
        alpha_cc = self.alpha_cc
        fck_t = self.fck_t()
        gamma_c = self.gamma_c
        #---
        fcd = eta * alpha_cc * fck_t / gamma_c
        return fcd

    def fctd(self):
        alpha_ct = self.alpha_ct
        fctk_005_t = self.fctk_005_t()
        gamma_c = self.gamma_c
        #---
        fctd = alpha_ct * fctk_005_t / gamma_c
        return fctd

    def k1(self):
        classe_exposition = self.classe_exposition
        #---
        k1 = DICT_K1[classe_exposition]
        return k1

    def Scbar(self):
        k1 = self.k1()
        fck = self.fck()
        #---
        Scbar = self.k1() * self.fck()
        return Scbar

    def lmbda(self):
        fck = self.fck()
        #---
        if fck <= 50.:
            lmbda =  0.8
        else:
            lmbda = 0.8 - (fck() - 50.) / 400.
        return lmbda

    def eta(self):
        fck = self.fck()
        #---
        if fck <= 50.:
            eta = 1.
        else:
            eta = 1. - (fck() - 50.) / 100.
        return eta

    def resultatdetail(self):
        w = 40
        tableau = Table(title="PARAMETRE BETON ARME")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="left")
        tableau.add_column("Valeur", justify="right")
        tableau.add_column("unité", justify="left")
        tableau.add_row("Classe d'exposition", "-", f"{self.classe_exposition}", "-")
        tableau.add_row("Classe de résistance", "-", f"{self.classe_resistance}", "-")
        tableau.add_row("Classe de ciment", "-", f"{self.classe_ciment}", "-")
        tableau.add_row("", "s", f"{self.s_ciment()}", "-")
        tableau.add_row("Résistance caractéritique en compression", "fck", f"{self.fck():.0f}", "MPa")
        tableau.add_row("", "fck_cube", f"{self.fck_cube():.0f}", "MPa")
        tableau.add_row("", "fcm", f"{self.fcm():.0f}", "MPa")
        tableau.add_row("Résistance caractéristique en traction", "fctm", f"{self.fctm():.2f}", "MPa")
        tableau.add_row("", "fctk_095", f"{self.fctk_095():.2f}", "MPa")
        tableau.add_row("", "fctk_005", f"{self.fctk_005():.2f}", "MPa")
        tableau.add_row("Coefficient de fluage", "fiinft0", f"{self.fiinft0}", "-")
        tableau.add_row("Module d'elacticité sécant", "Ecm", f"{self.Ecm():.0f}", "MPa")
        tableau.add_row("Module d'élasticité effectif", "Eceff", f"{self.Eceff():.0f}", "MPa")
        tableau.add_row("Coefficient d'équivalence", "alpha_e", f"{self.alphae():.0f}", "-")
        tableau.add_row("", "", "", "")
        tableau.add_row("Age du béton", "age", f"{self.age}", "jours")
        tableau.add_row("", "betacc(t)", f"{self.beta_cc_t():.2f}", "-")
        tableau.add_row("Résistance caractéritique en compression", "fck(t)", f"{self.fck_t():.2f}", "MPa")
        tableau.add_row("", "fcm(t)", f"{self.fcm_t():.2f}", "MPa")
        tableau.add_row("Résistance caractéristique en traction", "fctm(t)", f"{self.fctm_t():.2f}", "MPa")
        tableau.add_row("Module d'elacticité sécant", "Ecm(t)", f"{self.Ecm_t():.0f}", "MPa")
        tableau.add_row("", "", "", "")
        tableau.add_row("", "acc", f"{self.acc}", "-")
        tableau.add_row("", "act", f"{self.act}", "-")
        tableau.add_row("", "gamma_c", f"{self.gamma_c}", "-")
        tableau.add_row("Résistance de calcul en compression", "fcd", f"{self.fcd():.2f}", "MPa")
        tableau.add_row("Résistance de calcul en traction", "fctd", f"{self.fctd():.2f}", "MPa")
        console = Console()
        console.print(tableau)

    def __repr__(self):
        printentete()
        printligne("Classe d'exposition", "-", "-", f'{self.classe_exposition}')
        printligne("Classe de résistance", "-", "-", f'{self.classe_resistance}')
        printligne("Classe de ciment    ", "-", "-", f'{self.classe_ciment}')
        printligne("", "s", "-", f"{self.s_ciment():.2f}")
        printligne("Résistance caractéritique en compression", "fck", "MPa", f'{self.fck():.0f}')
        printligne("", "fck_cube", "MPa", f'{self.fck_cube():.0f}')
        printligne("", "fcm", "MPa", f'{self.fcm():.0f}')
        printligne("Résistance caractéristique en traction", "fctm", "MPa", f'{self.fctm():.2f}')
        printligne("", "fctm_fl", "MPa", f'{self.fctm_fl():.2f}')
        printligne("", "fct_eff", "MPa", f'{self.fct_eff():.2f}')
        printligne("", "fctk_095", "MPa", f'{self.fctk_095():.2f}')
        printligne("", "fctk_005", "MPa", f'{self.fctk_005():.2f}')
        printligne("Coefficient de fluage", "fi_infini_t0", "-", f'{self.fi_infini_t0:.2f}')
        printligne("Module d'elacticité sécant", "Ecm", "MPa", f'{self.Ecm():.0f}')
        printligne("Module d'élasticité effectif", "Eceff", "MPa", f'{self.Eceff():.0f}')
        printligne("Coefficient d'équivalence", "alpha_e", "-", f'{self.get_alpha_e():.0f}')
        printsep()
        printligne("Age du béton", "age", "jour", f'{self.age:.0f}')
        printligne("", "beta_cc(t)", "-", f'{self.beta_cc_t():.3f}')
        printligne("Résistance caractéritique en compression", "fck(t)", "MPa", f'{self.fck_t():.2f}')
        printligne("", "fcm(t)", "MPa", f'{self.fcm_t():.2f}')
        printligne("Résistance caractéristique en traction", "fctm(t)", "MPa", f'{self.fctm_t():.2f}')
        printligne("Module d'elacticité sécant", "Ecm(t)", "MPa", f'{self.Ecm_t():.0f}')
        printsep()
        print("A l'ELU")
        printligne("", "alpha_cc", "-", f'{self.alpha_cc:.2f}')
        printligne("", "alpha_ct", "-", f'{self.alpha_ct:.2f}')
        printligne("", "gamma_c", "-", f'{self.gamma_c:.2f}')
        printligne("", "eta", "-", f'{self.eta():.2f}')
        printligne("", "lambda", "-", f'{self.lmbda():.2f}')
        printligne("Résistance de calcul en compression", "fcd", "MPa", f'{self.fcd():.2f}')
        printligne("Résistance de calcul en traction", "fctd", "MPa", f'{self.fctd():.2f}')
        printsep()
        print("A l'ELS")
        printligne("", "k1", "MPa", f'{self.k1():.2f}')
        printligne("", "Scbar", "MPa", f'{self.Scbar():.2f}')
        printsep()


if __name__ == '__main__':
    situation = SituationProjet('Durable')
    beton = BetonArme(situation, classe_exposition='XS1', classe_resistance='C30/37', alpha_cc=1, alpha_ct=1, age=28, classe_ciment="N", _alpha_e=15, fi_infini_t0=2,
                      h=0.5, maitrise_fissuration=True)
    beton.__repr__()