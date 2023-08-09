
class Travee:
   
   
    def __init__(self, typeAppuis, ln, t1, t2, h, axeAppareil):
        self.typeAppuis = typeAppuis
        self.ln = ln
        self.t1 = t1
        self.t2 = t2
        self.h = h
        self.axeAppareil = axeAppareil
       
    def a1(self):
        h = self.h
        t1 = self.t1
        typeAppuis = self.typeAppuis
        axeAppareil = self.axeAppareil
        dict_a = {"Isostatique" : min(h/2, t1/2), "Continu" : min(h/2, t1/2), "Encastrement" : min(h/2, t1/2),
                  "Appareil d'appuis" : axeAppareil, "Console" : min(h/2, t1/2)}
        return dict_a[typeAppuis] 
    
    def a2(self):
        h = self.h
        t2 = self.t2
        typeAppuis = self.typeAppuis
        axeAppareil = self.axeAppareil
        dict_a = {"Isostatique" : min(h/2, t2/2), "Continu" : min(h/2, t2/2), "Encastrement" : min(h/2, t2/2),
                  "Appareil d'appuis" : axeAppareil, "Console" : min(h/2, t2/2)}
        return dict_a[typeAppuis] 
    
    def leff(self):
        ln = self.ln
        a1 = self.a1()
        a2 = self.a2()
        return ln + a1 + a2

if __name__ == "__main__":
    
    typeAppuis = "Appareil d'appuis"
    lnx = 400 / 100
    agx = 20 / 100
    adx = 40 / 100
    h = 22 / 100
    axeAppareil = 15 / 100
        
    traveex = Travee(typeAppuis, lnx, adx, agx, h, axeAppareil)
    
    print(f"a1 = {traveex.a1() * 100} cm")
    print(f"a2 = {traveex.a2() * 100} cm")
    print(f"leff = {traveex.leff() * 100:.2f} cm")