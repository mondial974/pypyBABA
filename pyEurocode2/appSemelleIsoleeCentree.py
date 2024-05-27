# non utilisable en l'état

#from colorama import Fore, Style
from rich.table import Table
from rich.console import Console
from coreDCdalle import *
from utilsprint import *
from corematacierarmature import *
from corematbetonarme import *
from coresituationprojet import *

class SemelleIsolee():
    
    def __init__(self, beton, acier, Nu, Nser, SsolELS, SsolELU, Bpot, Hpot, Asem, Bsem, Hsem, enr, AsAsem, AsBsem) -> None:
        self.beton = beton
        self.acier = acier
        self.Nu = Nu
        self.Nser = Nser
        self.SsolELS = SsolELS
        self.SsolELU = SsolELU
        self.Bpot = Bpot
        self.Hpot = Hpot
        self.Asem = Asem
        self.Bsem = Bsem
        self.Hsem = Hsem
        self.enr = enr
        self.AsAsem = AsAsem
        self.AsBsem = AsBsem
    
    def dimAsem(self):
        if self.Bsem == 0:
            A = self.Hpot
            B = self.Bpot
            
            while (B * 100 % 5) != 0 or (B * 100 % 2) != 0:
                B += 0.01
                
            while (A * 100 % 5) != 0 or (A * 100 % 2) != 0:
                A += 0.01
                
            SELS = self.Nser / (A * B)
            SELU = self.Nu / (A * B)
         
            while SELS > self.SsolELS or SELU > self.SsolELU:
                A += 0.05
                B += 0.05
                SELS = self.Nser / (A * B)
                SELU = self.Nu / (A * B)
        else:
            A = self.Asem
            B = self.Bsem
            SELS = self.Nser / (A * B)
            SELU = self.Nu / (A * B)
        
        return A
    
    
    def dimBsem(self):
        if self.Bsem == 0:
            A = self.Hpot
            B = self.Bpot
            
            while (B * 100 % 5) != 0 or (B * 100 % 2) != 0:
                B += 0.01
                
            while (A * 100 % 5) != 0 or (A * 100 % 2) != 0:
                A += 0.01
                
            SELS = self.Nser / (A * B)
            SELU = self.Nu / (A * B)
         
            while SELS > self.SsolELS or SELU > self.SsolELU:
                A += 0.05
                B += 0.05
                SELS = self.Nser / (A * B)
                SELU = self.Nu / (A * B)
        else:
            A = self.Asem
            B = self.Bsem
            SELS = self.Nser / (A * B)
            SELU = self.Nu / (A * B)
            
        return B
    
    def dimHsem(self):
        if self.Hsem == 0:
            H = 0.20
            while (H - self.enr) < min((self.dimBsem()-self.Bpot)/4, (self.dimAsem() - self.Hpot)/4):
                H += 0.05
        else:
            H = self.Hsem        
        return H
    
    def dimDsem(self):
        return self.dimHsem() - self.enr
    
    def SELS(self):
        return self.Nser / (self.dimAsem()*self.dimBsem())
    
    def SELU(self):
        return self.Nu / (self.dimAsem()*self.dimBsem())
    
    def dimAsAsem(self):
        As1 = self.Nu  / 8 * (self.dimAsem() - self.Hpot) / self.dimDsem() / self.acier.fyd()
        dalle = DC_Dalle(self.beton, self.acier, self.Hsem, self.enr, As1) 
        As2 = dalle.Asx_min_dalle()
        return max(As1, As2)
    
    def dimAsBsem(self):
        As1 = self.Nu  / 8 * (self.dimBsem() - self.Bpot) / self.dimDsem() / self.acier.fyd()
        dalle = DC_Dalle(self.beton, self.acier, self.Hsem, self.enr, As1) 
        As2 = dalle.Asx_min_dalle()
        return max(As1, As2)
    
    def smax_slabs_princ(self):
        situation = "Durable"
        situation = SituationProjet(situation)
        classe_exposition = self.beton.classe_exposition
        classe_resistance = self.beton.classe_resistance
        alpha_cc = self.beton.alpha_cc
        alpha_ct = self.beton.alpha_ct
        age = self.beton.age
        classe_ciment = self.beton.classe_ciment
        alpha_e = self.beton.alpha_e
        fi_infini_t0 = self.beton.fi_infini_t0
        beton = BetonArme(situation, classe_exposition, classe_resistance, alpha_cc, alpha_ct, age, classe_ciment, alpha_e, fi_infini_t0, h=0, maitrise_fissuration=True)
        acier = self.acier
        h = self.dimHsem()
        enr = self.enr
        As = self.dimAsAsem()
        dcdalle = DC_Dalle(beton, acier, h , enr , As)
        return dcdalle.smax_slabs_princ()
    
    def dimAs_second(self):
        return 20 / 100 * self.dimAs_princ()
    
    def smax_slabs_second(self):
        situation = "Durable"
        situation = SituationProjet(situation)
        classe_exposition = self.beton.classe_exposition
        classe_resistance = self.beton.classe_resistance
        alpha_cc = self.beton.alpha_cc
        alpha_ct = self.beton.alpha_ct
        age = self.beton.age
        classe_ciment = self.beton.classe_ciment
        alpha_e = self.beton.alpha_e
        fi_infini_t0 = self.beton.fi_infini_t0
        beton = BetonArme(situation, classe_exposition, classe_resistance, alpha_cc, alpha_ct, age, classe_ciment, alpha_e, fi_infini_t0, h=0, maitrise_fissuration=True)
        acier = self.acier
        h = self.dimHsem()
        enr = self.enr
        As = self.dimAsAsem()
        dcdalle = DC_Dalle(beton, acier, h , enr , As)
        return dcdalle.smax_slabs_second()
    
    
    def resultat_court(self):
        print("RESULTATS NON FINALISES")
        print(f"SI {self.dimAsem()*100:.0f} x {self.dimBsem()*100:.0f} x {self.dimHsem()*100:.0f} ht")
        print('')
        print(f"AsAsem = {self.dimAsAsem()*1e4:.2f} cm2/l")
        print(f"Esp max smax1 = {self.smax_slabs_princ()*100:.0f} cm")
        print('')
        print(f"AsBsem = {self.dimAsBsem()*1e4:.2f} cm2")
        print(f"Esp max smax2 = {self.smax_slabs_second()*100:.0f} cm")
        print('')

        if self.SELS() <= self.SsolELS:
            print("SresELS < SadmELS ==> VERIFIE")
        else:
            print("SresELS > SadmELS ==> NON VERIFIE")
        
        if self.SELU() <= self.SsolELU:
            print("SresELU < SadmELU ==> VERIFIE")
        else:
            print("SresELU > SadmELU ==> NON VERIFIE")

        print('')
        if self.dimDsem() > (self.dimBsem() - self.Bpot) / 4:
            print("POINCONNEMENT VERIFIE")
        else:
            print("POINCONNEMENT NON VERIFIE")
        
        if self.AsAsem != 0:
            if self.AsAsem < self.dimAsAsem() :
                print(f'AsAsem réel ({self.AsAsem*1e4:.2f} cm2/ml) < AsAsem calculée ({self.AsAsem()*1e4:.2f} cm2/ml) => NON VERIFIE')
            else:
                print(f'AsAsem réel ({self.AsAsem*1e4:.2f} cm2/ml) > AsAsem calculée ({self.AsAsem()*1e4:.2f} cm2/ml) => VERIFIE')
        
        if self.AsBsem != 0:
            if self.AsBsem < self.dimAsAsem() :
                print(f'AsBsem réel ({self.AsBsem*1e4:.2f} cm2/ml) < AsBsem calculée ({self.AsBsem()*1e4:.2f} cm2/ml) => NON VERIFIE')
            else:
                print(f'AsBsem réel ({self.AsBsem*1e4:.2f} cm2/ml) > AsBsem calculée ({self.AsBsem()*1e4:.2f} cm2/ml) => VERIFIE')
    
    def resultat_long(self):
        self.resultat_court()
        printentete()  
        print('Géométrie')
        printligne("Largeur du mur", "Bmur", "cm", f'{self.Bmur*100:.2f}')
        
        printligne("Largeur semelle", "Bsem", "cm", f'{self.dimBsem()*100:.2f}')
        printligne("Hauteur semelle", "Hsem", "cm", f'{self.dimHsem()*100:.2f}')
        printligne("Hauteur utile semelle", "Dsem", "cm", f'{self.dimDsem()*100:.2f}')
        printligne("Enrobage semelle", "c1", "cm", f'{self.c1*100:.2f}')
        print('')
        printsep()
        print('Descente de charge')  
        printligne("Effort vertical ELU", "Nu", "T/ml", f'{self.Nu*100:.2f}')
        printligne("Effort vertical ELS", "Nser", "T/ml", f'{self.Nser*100:.2f}')
        print('')
        printsep()
        print('Contrainte de sol')  
        printligne("Contrainte admissible ELU", "SadmELU", "MPa", f'{self.SsolELU:.2f}')
        printligne("Contrainte admissible ELS", "SadmELS", "MPa", f'{self.SsolELS:.2f}')
        printligne("Contrainte résiduelle ELU", "SresELU", "MPa", f'{self.SELU():.2f}')
        printligne("Contrainte résiduelle ELS", "SresELS", "MPa", f'{self.SELS():.2f}')
        print('')
        printsep()
        print('Armatures')  
        printligne("Résistance car. à la traction", "fyk", "MPa", f'{self.acier.fyk():.2f}')
        printligne("Résistance de calcul à la traction", "fyd", "MPa", f'{self.acier.fyd():.2f}')
        printligne("Armatures transversales", "As1", "cm2/ml", f'{self.dimAs_princ()*1e4:.2f}')
        printligne("Espacement max", "smax1", "cm", f'{self.smax_slabs_princ()*100:.2f}')
        printligne("Armatures longitudinales", "As2", "cm2", f'{self.dimAs_second()*1e4:.2f}')
        printligne("Espacement max", "smax2", "cm", f'{self.smax_slabs_second()*100:.2f}')
        printsep()
        print('')
        



         
if __name__ == "__main__":
    fyk = 500
    Nu = 30 / 100
    Nser = 26 / 100
    SsolELS = 260 / 1000
    SsolELU = 300 / 1000
    Bmur = 20 / 100
    c1 = 6 / 100
    Bsem = 0 / 100
    Hsem = 0 / 100
    As1 = 0 / 1e4
    situation = SituationProjet(situation='Durable')
    
    nuance = "S500B"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    sf = SemelleIsolee(beton, acier, Nu, Nser, SsolELS, SsolELU, Bpot, Hpot, Asem, Bsem, Hsem, enr, AsAsem, AsBsem) 
    sf.resultat_long()