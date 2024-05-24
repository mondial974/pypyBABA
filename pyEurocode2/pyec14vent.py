from math import log, log10

class PressionVent():
    
    def __init__(self, regionclimatique, categorieterrain, cdir, cseason, co, casorographique, ze, h):
        self.regionclimatique = regionclimatique
        self.categorieterrain = categorieterrain
        self.cdir = cdir
        self.cseason = cseason
        self.co = co
        self.casorographique = casorographique
        self.ze = ze
        self.h = h
    
    def vb0(self):
        dict_vb0 = {'1': 22, '2': 24, '3': 26, '4': 28, 'Guadeloupe': 36,
                  'Guyanne': 17, 'Martinique': 32, 'Mayotte': 30,
                  'Réunion': 34}
        return dict_vb0[self.regionclimatique]
    
    def vb(self):
        return self.cdir * self.cseason * self.vb0()
    
    def R(self):
        return max(23 * self.h**1.2, 300)
    
    def z0(self):
        dict_categorieterrain = {'0': 0.005, 'II': 0.05, 'IIIa': 0.20, 'IIIb': 0.5, 'IV': 1}
        return dict_categorieterrain[self.categorieterrain]
    
    def zmin(self):
        dict_categorieterrain = {'0': 1, 'II': 2, 'IIIa': 5, 'IIIb': 9, 'IV': 15}
        return dict_categorieterrain[self.categorieterrain]
    
    def zmax(self):
        return 200
    
    def z0II(self):
        dict_categorieterrain = {'0': 0.005, 'II': 0.05, 'IIIa': 0.20, 'IIIb': 0.5, 'IV': 1}
        return dict_categorieterrain['II']
        
    def kr(self):
        return 0.19 * (self.z0() / self.z0II())**0.07
    
    def cr(self):
        if self.zmin() < self.ze and self.ze < self.zmax():
            return self.kr() * log(self.ze / self.z0())
        else:
            return self.kr() * log(self.zmin() / self.z0())
    
    def vm(self):
        return self.cr() * self.co * self.vb()
    
    def kl(self):
        kl = 1 - 2e-4 * (log10(self.z0()) + 3)**6
        if self.casorographique == "Cas 1":
            return self.co * kl
        else:
            return kl
    
    def Iv(self):
        if self.zmin() < self.ze and self.ze < self.zmax():
            return self.kl() / (self.co * log(self.ze / self.z0()))
        else:
            return self.kl() / (self.co * log(self.zmin() / self.z0()))
    
    def rhoair(self):
        return 1.225
    
    def qp(self):
        return (1 + 7 * self.Iv()) * 0.5 * self.rhoair() * self.vm()**2 / 10
    
    def qb(self):
        return 0.5 * self.rhoair() * self.vb()**2 / 10
    
    def ce(self):
        return self.qp() / self.qb()        
        
    
    def resultat_long(self):
        def printligne(designation, symbole, unite, valeur):
            print(f'{designation:45} {symbole:<10} {valeur:>10} {"   "} {unite:<10}')
        
        def printsep():
            print("-"*77)
        
        def printentete():
            print("="*77)
            print(f'{"DESIGNATION":45} {"SYMBOLE":<10} {"VALEUR":^10} {" "} {"UNITE":^10}')
            print("="*77)
        
        printentete()  
        print("Construction")
        printligne("  Hauteur de la construction"         , "h"           , "m"       , f'{self.h}')
        printligne("  Hauteur de référence"               , "ze"           , "m"       , f'{self.ze}')
        print("")
        print("Vitesse de vent")
        printligne("  Region climatique"                     , "-"           , "-"       , f'{self.regionclimatique}')
        printligne("  Vitesse de base de vent"            , "vb0"         , "m/s"     , f'{self.vb0():.0f}')
        printligne("  Coefficient de direction"           , "cdir"        , "-"       , f'{self.cdir:.2f}')
        printligne("  Coefficient de saison"              , "cseason"     , "-"       , f'{self.cseason:.2f}')
        printligne("  Vitesse de référence de vent"       , "vb"          , "m/s"     , f'{self.vb():.2f}')
        printligne("  Vitesse moyenne de vent"            , "vm"          , "m/s"     , f'{self.vm():.2f}')
        print("")
        print("Catégorie de terrain")
        printligne("  atégorie de terrain"               , "-"           , "-"       , f'{self.categorieterrain}')
        printligne("  Distance au vent"                   , "R"           , "m"       , f'{self.R():.0f}')
        printligne("  -"                                  , "z0"          , "m"       , f'{self.z0():.3f}')
        printligne("  -"                                  , "zmin"        , "m"       , f'{self.zmin()}')
        printligne("  -"                                  , "zmax"        , "m"       , f'{self.zmax()}')
        printligne("  -"                                  , "z0II"        , "m"       , f'{self.z0II():.3f}')
        printligne("  Facteur de terrain"                 , "kr"          , "-"       , f'{self.kr():.3f}')
        printligne("  Coefficient de rugosité"            , "cr(z)"       , "-"       , f'{self.cr():.3f}')
        print("")
        print("Orographie")
        printligne("  Cas orographique"                   , "-"           , "-"       , f'{self.casorographique}')
        printligne("  Coefficient orographique"           , "co"          , "-"       , f'{self.co:.2f}')
        print("")
        print("Turbulence du vent")
        printligne("  Coefficient de turbulence"          , "kl"          , "-"       , f'{self.kl():.2f}')
        printligne("  Intensité de turbulence"            , "Iv"          , "-"       , f'{self.Iv():.3f}')
        print("")
        print("Pression dynamique de pointe")
        printligne("  Masse volumique de l'air"           , "rho_air"         , "kg/m3"   , f'{self.rhoair():.3f}')
        printligne("  Pression dynamique de pointe"       , "qp"          , "daN/m2"  , f'{self.qp():.0f}')
        printligne("  Pression dynamique de référence"    , "qb"          , "daN/m2"  , f'{self.qb():.0f}')
        printligne("  Cefficient d'exposition"            , "ce"          , "-"       , f'{self.ce():.3f}')
        printsep()
    
    def resultat_court(self):
        def printligne(designation, symbole, unite, valeur):
            print(f'{designation:45} {symbole:<10} {valeur:>10} {"   "} {unite:<10}')
        
        def printsep():
            print("-"*77)
        
        def printentete():
            print("="*77)
            print(f'{"DESIGNATION":45} {"SYMBOLE":<10} {"VALEUR":^10} {" "} {"UNITE":^10}')
            print("="*77)
        
        printentete()  
        print("Construction")
        printligne("Hauteur de la construction"         , "h"           , "m"       , f'{self.h}')
        printligne("Hauteur de référence"               , "ze"           , "m"       , f'{self.ze}')
        print("")
        print("Vitesse de vent")
        printligne("Region de vent"                     , "-"           , "-"       , f'{self.regionclimatique}')
        printligne("Coefficient de direction"           , "cdir"        , "-"       , f'{self.cdir:.2f}')
        printligne("Coefficient de saison"              , "cseason"     , "-"       , f'{self.cseason:.2f}')
        print("")
        print("Catégorie de terrain")
        printligne("Catégorie de terrain"               , "-"           , "-"       , f'{self.categorieterrain}')
        print("")
        print("Orographie")
        printligne("Cas orographique"                   , "-"           , "-"       , f'{self.casorographique}')
        printligne("Coefficient orographique"           , "co"          , "-"       , f'{self.co:.2f}')
        print("")
        print("Pression dynamique de pointe")
        printligne("Pression dynamique de pointe"       , "qp"          , "daN/m2"  , f'{self.qp():.0f}')
        printligne("Pression dynamique de référence"    , "qb"          , "daN/m2"  , f'{self.qb():.0f}')
        printsep()
        
if __name__ == '__main__':
    pression = PressionVent(regionclimatique="Réunion", categorieterrain="II", cdir=1, cseason=1, co=1, casorographique="Cas 1", ze=12, h=12)
    pression.__repr__()