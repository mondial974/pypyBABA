from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *


class BlocMaconnerie:
    
    def __init__(self, groupe, t, fb, fk1, fk2, fxk1, fxk2, fvk0, gamma_M):
        self.groupe = groupe
        self.t = t
        self.fb = fb
        self.fk1 = fk1
        self.fk2 = fk2
        self.fxk1 = fxk1
        self.fxk2 = fxk2
        self.fvk0 = fvk0
        self.gamma_M = gamma_M
    
    def fd1(self):
        return self.fk1 / self.gamma_M
    
    def fd2(self):
        return self.fk2 / self.gamma_M    
    
    def fxd1(self):
        return self.fxk1 / self.gamma_M
    
    def fxd2(self):
        return self.fxk2 / self.gamma_M
    
    def reslong(self):
        def printligne(designation, symbole, unite, valeur):
            print(f'{designation:45} {symbole:<10} {valeur:>10} {"   "} {unite:<10}')
        
        def printsep():
            print("-"*77)
        
        def printentete():
            print("="*77)
            print(f'{"DESIGNATION":45} {"SYMBOLE":<10} {"VALEUR":^10} {" "} {"UNITE":^10}')
            print("="*77)
        
        printentete()  
        print("Bloc de maconnerie")
        printligne("Groupe"         , "-"           , ""       , f'{self.groupe}')
        printligne("Epaisseur"               , "t"           , "cm"       , f'{self.t*100}')
        print("")
        print("Résistance caractéristique")
        printligne("-"               , "fb"           , "MPa"       , f'{self.fb:.2f}')
        printligne("-"               , "fk1"           , "MPa"       , f'{self.fk1:.2f}')
        printligne("-"               , "fxk1"           , "MPa"       , f'{self.fxk1:.2f}')
        printligne("-"               , "fxk2"           , "MPa"       , f'{self.fxk2:.2f}')
        printligne("-"               , "fvk0"           , "MPa"       , f'{self.fvk0:.2f}')
        printligne("-"               , "gamma_M"           , "MPa"       , f'{self.gamma_M:.2f}')
        print("")
        print("Résistance de calcul")
        printligne("-"               , "fd1"           , "MPa"       , f'{self.fd1():.2f}')        
        printligne("-"               , "fd2"           , "MPa"       , f'{self.fd2():.2f}')        
        printligne("-"               , "fxd1"           , "MPa"       , f'{self.fxd1():.2f}')        
        printligne("-"               , "fxd2"           , "MPa"       , f'{self.fxd2():.2f}')        
        printsep()

class MurChargementLateral:
    
    def __init__(self,situation, bloc, acier, h, l, liaison, WEd, NEd, b, Asv1, d1, Ash2, d2, Ash2joint, d2joint, alpha2_025, alpha2_mu):
        self.situation = situation
        self.bloc = bloc
        self.acier = acier
        self.h = h
        self.l = l
        self.liason = liaison
        self.WEd = WEd
        self.NEd = NEd
        self.b = b
        self.Asv1 = Asv1
        self.d1 = d1
        self.Ash2 = Ash2 
        self.d2 = d2 
        self.Ash2joint = Ash2joint 
        self.d2joint = d2joint 
        self.alpha2_025 = alpha2_025
        self.alpha2_mu = alpha2_mu        
        
    def rho2(self):
        return 1
    
    def rho(self):
        if self.liason == "Tenu en tête, en pied et sur un bord vertical":
            if self.h / self.l <= 3.5:
                return self.rho2() / (1 + ((self.rho2() * self.h) / (3 * self.l))**2)
            else:
                return max(1.5 * self.l / self.h, 0.3)
        
        if self.liason == "Tenu en tête, en pied et sur deux bords verticaux":
            if self.h / self.l <= 1.15:
                return self.rho2() / (1 + ((self.rho2() * self.h) / (self.l))**2)
            else:
                return 0.5 * self.l /  self.h  
    
    def hef(self):
        return self.rho() * self.h
            
    def ismurtreslong(self):
        if self.h / self.l < 0.3:
            return True
        else:
            return False
    
    def ismurtreshaut(self):
        if self.h / self.l > 2:
            return True
        else:
            return False
    
    def ismursur3ou4appui(self):
        if 0.3 <= self.h / self.l and self.h / self.l <= 2:
            return True
        else:
            return False
    
    def ismursanschargement(self):
        if self.NEd == 0 and self.Ash2 == 0:
            return True
        else:
            return False
    
    def ismuravecchargeverticale(self):
        if self.NEd != 0:
            return True
        else:
            return False
    
    def ismuravecchargehorizontale(self):
        if self.Ash2joint != 0:
            return True
        else:
            return False
    
    def sigma_d(self):
        return self.NEd / (self.bloc.t * self.h)        
    
    def fxd1(self):
        return self.bloc.fxd1()
    
    def fxd2(self):
        return self.bloc.fxd2()
    
    def fxd1app(self):
        if self.NEd == 0:
            return self.fxd1()
        else:
            return self.fxd1() + self.sigma_d()
    
    def fxd2app(self):
        if self.Ash2joint == 0:
            return self.fxd2()
        else:
            return 6 * self.Ash2joint * self.acier.fyd() * self.z2fxd2jointarme() / self.bloc.t**2 
        
    def mu(self):
        return self.fxd1app() / self.fxd2app()
   
    def alpha1_025(self):
        return 0.25 * self.alpha2_025
    
    def alpha1_mu(self):
        return self.mu() * self.alpha2_mu        
            
    def MEd1(self):
        if self.ismurtreslong():
            return 1/8 * self.WEd * self.hef()**2
        if self.ismurtreshaut():
            return 0
        if self.ismursur3ou4appui():
            return self.alpha1_025() * self.WEd * self.l**2
    
    def MEd2(self):
        if self.ismurtreslong():
            return 0
        if self.ismurtreshaut():
            return 1/8 * self.WEd * self.l**2
        if self.ismursur3ou4appui():
            return self.alpha2_025 * self.WEd * self.l**2
    
    def MEd1jointarme(self):
        if self.ismurtreslong():
            return 1/8 * self.WEd * self.hef()**2
        if self.ismurtreshaut():
            return 0
        if self.ismursur3ou4appui():
            return self.alpha1_mu() * self.WEd * self.l**2
    
    def MEd2jointarme(self):
        if self.ismurtreslong():
            return 0
        if self.ismurtreshaut():
            return 1/8 * self.WEd * self.l**2
        if self.ismursur3ou4appui():
            return self.alpha2_mu * self.WEd * self.l**2
    
    def MRd1nonarme(self):
        if self.ismursanschargement:
            return self.fxd1() * self.bloc.t**2 / 6
        if self.ismuravecchargeverticale:
            return self.fxd1app() * self.bloc.t**2 / 6
    
    def MRd2nonarme(self):
        return self.fxd2() * self.bloc.t**2 / 6 
    
    def phi(self):
        dict_phi = {'1': 0.4, '2': 0.3, '2': 0.3, '3': 0.3}
        return dict_phi[self.bloc.groupe]
    
    def MRd1jointarme(self):
        if self.Ash2joint == 0:
            return 0
        else:
            return self.MRd1nonarme()
    
    def z2fxd2jointarme(self):
        if self.bloc.fd2() == 0:
            return 0
        else:
            return min(self.d2joint - 0.5 * self.Ash2joint * self.acier.fyd() / (1000 * self.bloc.fd2()),
                       0.95 * self.d2joint) 
    
    def MRd2jointarme(self):
        if self.Ash2joint == 0:
            return 0
        else:
            return min(self.Ash2joint * self.acier.fyd() * self.z2fxd2jointarme(),
                       self.phi() * self.bloc.fd2() * self.d2joint**2)   
    
    def z1SectionRectArme(self):
        if self.d1 == 0:
            return 0
        else:
            return min(self.d1 * (1 - 0.5 * self.Asv1 * self.acier.fyd() / (self.b * self.d1 * self.bloc.fd1())),
                       0.95 * self.d1)
    
    def z2SectionRectArme(self):
        if self.d2 == 0:
            return 0
        else:
            return min(self.d2 * (1 - 0.5 * self.Ash2 * self.acier.fyd() / (self.b * self.d2 * self.bloc.fd2())),
                       0.95 * self.d2)
        
    def MRd1SectionRectArme(self):
        return max(self.Asv1 * self.acier.fyd() * self.z1SectionRectArme(),
                   self.phi() * self.bloc.fd1() * self.b * self.d1**2)
    
    def MRd2SectionRectArme(self):
        if self.Ash2 == 0:
            return self.MEd2jointarme()
        else:
            return max(self.Ash2 * self.acier.fyd() * self.z2SectionRectArme(),
                   self.phi() * self.bloc.fd2() * self.b * self.d2**2)             
                
    def reslong(self):
        def printligne(designation, symbole, unite, valeur):
            print(f'{designation:45} {symbole:<10} {valeur:>10} {"   "} {unite:<10}')
        
        def printsep():
            print("-"*77)
        
        def printentete():
            print("="*77)
            print(f'{"DESIGNATION":45} {"SYMBOLE":<10} {"VALEUR":^10} {" "} {"UNITE":^10}')
            print("="*77)
        
        printentete()  
        print("Bloc de maconnerie")
        printligne("Groupe"                                     , "-"           , ""        , f'{self.bloc.groupe}')
        printligne("Epaisseur"                                  , "t"           , "cm"      , f'{self.bloc.t*100}')
        print("")
        print("Résistance caractéristique en compression")
        printligne("Résistance moyenne"                         , "fb"          , "MPa"      , f'{self.bloc.fb:.2f}')
        printligne("Résistance caractéristique"                 , "fk1"          , "MPa"      , f'{self.bloc.fk1:.2f}')
        printligne("-"                                          , "fk2"          , "MPa"      , f'{self.bloc.fk2:.2f}')
        printligne("Résistance en flexion // lit de pose"       , "fxk1"        , "MPa"      , f'{self.bloc.fxk1:.2f}')
        printligne("Résistance en flexion ⟂ au lit de pose"     , "fxk2"        , "MPa"      , f'{self.bloc.fxk2:.2f}')
        printligne("Coefficient de sécurité sur maçonnerie"     , "gamma_M"     , "MPa"      , f'{self.bloc.gamma_M:.2f}')
        print("")
        print("Résistance de calcul")
        printligne("Résistance de calcul"                       , "fd1"          , "MPa"      , f'{self.bloc.fd1():.2f}')        
        printligne("-"                                          , "fd2"          , "MPa"      , f'{self.bloc.fd2():.2f}')        
        printligne("-"                                          , "fxd1"        , "MPa"      , f'{self.bloc.fxd1():.2f}')        
        printligne("-"                                          , "fxd2"        , "MPa"      , f'{self.bloc.fxd2():.2f}')        
        printsep()
        print("Géométrie mur")   
        printligne("Longueur"                                   , "l"           , "cm"       , f'{self.l*100:.0f}')     
        printligne("Hauteur"                                    , "h"           , "cm"       , f'{self.h*100:.0f}')        
        printligne("-"                                          , "h/l"         , "-"       , f'{self.h / self.l:.3f}')        
        printligne("Hauteur effective"                          , "hef"         , "cm"       , f'{self.hef()*100:.0f}')
        printligne("-"                                          , "rho2"        , "-"        , f'{self.rho2():.3f}')
        printligne("-"                                          , "rho"         , "-"        , f'{self.rho():.3f}')
        
        print("")
        print("Sollicitation")
        printligne("Pression laterale"                          , "WEd"           , "daN/m2"    , f'{self.WEd*1e5:.0f}')
        printligne("Effort vertical en tête"                    , "NEd"           , "T"         , f'{self.NEd*100:.3f}')
        printligne("Contrainte de compression"                  , "Sigma_d"       , "MPa"       , f'{self.sigma_d():.2f}')
        printligne("-"                                          , "alpha1_025"        , "-"         , f'{self.alpha1_025():.4f}')
        printligne("-"                                          , "alpha2_025"        , "-"         , f'{self.alpha2_025:.4f}')
        printligne("MEd rupture // joint de pose"               , "MEd1"          , "daN.m"     , f'{self.MEd1()*1e5:.0f}')
        printligne("MEd rupture ⟂ joint de pose"                , "MEd2"          , "daN.m"     , f'{self.MEd2()*1e5:.0f}')
        print("")
        print("Cas du mur non armé")
        printligne("MEd rupture // joint de pose"               , "MEd1"          , "daN.m"     , f'{self.MEd1()*1e5:.0f}')
        printligne("MEd rupture ⟂ joint de pose"                , "MEd2"          , "daN.m"     , f'{self.MEd2()*1e5:.0f}')
        printligne("MRd rupture // joint de pose"              , "MRd1"           , "daN.m"     , f'{self.MRd1nonarme()*1e5:.0f}')
        printligne("MRd rupture ⟂ joint de pose"               , "MRd2"           , "daN.m"     , f'{self.MRd2nonarme()*1e5:.0f}')
        print("")
        print("Cas du mur avec armatures dans joint de pose")
        printligne("-"                                          , "phi"             , "-"           , f'{self.phi():.2f}')
        printligne("Résistance de calcul"                       , "fd2"             , "MPa"         , f'{self.bloc.fd2():.2f}')
        printligne("-"                                          , "fxd1app"         , "MPa"         , f'{self.fxd1app():.2f}')
        printligne("-"                                          , "fxd2app"         , "MPa"         , f'{self.fxd2app():.2f}')
        printligne("-"                                          , "mu"              , "-"           , f'{self.mu():.2f}')        
        printligne("-"                                          , "alpha1_mu"       , "-"           , f'{self.alpha1_mu():.4f}')        
        printligne("-"                                          , "alpha2_mu"       , "-"           , f'{self.alpha2_mu:.4f}') 
        printligne("MEd rupture // joint de pose"                , "MEd1"           , "daN.m"       , f'{self.MEd1jointarme()*1e5:.0f}')       
        printligne("MEd rupture ⟂ joint de pose"                , "MEd2"            , "daN.m"       , f'{self.MEd2jointarme()*1e5:.0f}')       
        printligne("MRd rupture // joint de pose"                , "MRd1"           , "daN.m"       , f'{self.MRd1jointarme()*1e5:.0f}')
        printligne("MRd rupture ⟂ joint de pose"                , "MRd2"            , "daN.m"       , f'{self.MRd2jointarme()*1e5:.0f}')
        printligne("Bras de levier"                             , "z2"              , "cm"          , f'{self.z2fxd2jointarme()*100:.1f}')
        print("")
        print("Moment résistant mur armé Section rectangulaire")
        printligne("MEd rupture // joint de pose"                , "MEd1"            , "daN.m"       , f'{self.MEd1jointarme()*1e5:.0f}') 
        printligne("MEd rupture ⟂ joint de pose"                , "MEd2"            , "daN.m"       , f'{self.MEd2jointarme()*1e5:.0f}')  
        printligne("MRd rupture // joint de pose"               , "MRd1"            , "daN.m"       , f'{self.MRd1SectionRectArme()*1e5:.0f}')
        printligne("MRd rupture ⟂ joint de pose"                , "MRd2"            , "daN.m"       , f'{self.MRd2SectionRectArme()*1e5:.0f}')
        printligne("Bras de levier z1"                          , "z1"              , "cm"          , f'{self.z1SectionRectArme()*100:.1f}')
        printsep()
          
       
if __name__ == '__main__':
    situation = SituationProjet(situation="Durable")
    acier = AcierArmature(situation, nuance='S500A', diagramme='Palier horizontal', diametre=8)
    bloc = BlocMaconnerie(groupe="2", t=20/100, fb=6, fk1=2.6, fk2=1.04, fxk1=0.60, fxk2=0.48, fvk0=0.19, gamma_M=2.7)
    #bloc.reslong()       
    mur = MurChargementLateral(situation=situation, bloc=bloc, acier=acier, h=400/100, l=976/100,
                               liaison="Tenu en tête, en pied et sur deux bords verticaux",
                               WEd = 60/1e5, NEd=0/1e5, b=60/100, Asv1=0/1e4, d1=0/100, Ash2=1/1e4, d2=0/100,
                               Ash2joint=0/1e4, d2joint=0/100, alpha2_025=0.095, alpha2_mu=0.104)
    mur.reslong()