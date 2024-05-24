from utilsprint import *

class DCPoutreRectangulaire:
    
    def __init__(self, beton, acier, bw, h, c):
        self.beton = beton
        self.acier = acier
        self.bw = bw
        self.h = h
        self.c = c
        
    def Ac(self):
        return self.bw * self.h
    
    def d(self):
        return self.h - self.c
    
    def Asmin1(self):
        fctm = self.beton.fctm()
        fyk = self.acier.fyk()
        bw = self.bw
        d = self.d()
        return 0.26 * fctm / fyk * bw * d  
    
    def Asmin2(self):
        bw = self.bw
        d = self.d()
        return 0.0013 * bw * d
    
    def Asmin(self):
        Asmin1 = self.Asmin1()
        Asmin2 = self.Asmin2()
        return max(Asmin1, Asmin2)
        
    def Asmax(self):
        return 0.04 * self.Ac()
    
    def resultat_long(self):
        print("Béton")
        printligne("Classe de résistance", "-", "-", f"{self.beton.classeresistance}")
        printligne("Résitance car. compression", "fck", "MPa", f"{self.beton.fck():.2f}")
        printligne("Résitance car. compression", "fcm", "MPa", f"{self.beton.fcm():.2f}")
        printligne("Résitance car. traction", "fctm", "MPa", f"{self.beton.fctm():.2f}")
        print("")
        printsep()
        print("Acier")
        printligne("Limite d'élasticité", "fyk", "MPa", f"{self.acier.fyk():.2f}")
        print("")
        printsep()
        print("Sections minimale et maximale d'armatures")
        printligne("Asmin 1", "Asmin1", "cm2", f"{self.Asmin1()*1e4:.2f}")
        printligne("Asmin 2", "Asmin2", "cm2", f"{self.Asmin2()*1e4:.2f}")
        print("")
        printligne("Asmin", "Asmin", "cm2", f"{self.Asmin()*1e4:.2f}")
        printligne("Asmax", "Asmax", "cm2", f"{self.Asmax()*1e4:.2f}")
        printfintab() 