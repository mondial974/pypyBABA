from numpy import cbrt
from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *


class PoutreVoileBAEL:

    def __init__(self, beton, acier, lt, lo, h, bo, Pu, Pui, Vou, Mou):
        self.beton = beton
        self.acier = acier
        self.lt = lt
        self.lo = lo
        self.h = h
        self.bo = bo
        self.Pu = Pu
        self.Pui = Pui
        self.Vou = Vou
        self.Mou = Mou


###############################################################################
# Définition des is
###############################################################################

    def isPoutreVoile(self):
        h = self.h
        l = self.l()
        if h >= l:
            return True
        else:
            return False


###############################################################################
# Portée de calcul et épaisseur mini de la poutre voile
###############################################################################

    def l(self):
        lt = self.lt
        lo = self.lo
        return min(lt, 1.15 * lo)

    def bMini(self):
        h = self.h
        l = self.l()
        Pu = self.Pu
        fc28 = self.beton.fck()
        if h > l:
            return max(0.14 * l * cbrt(Pu / (fc28 * h)), 3.75 * Pu / (fc28))
        else:
            return max(0.14 * l * cbrt(Pu / (fc28 * h)), 3.75 * Pu / (fc28) * l / h)


###############################################################################
# Contrainte tangente conventionnelle
###############################################################################

    def tou(self):
        h = self.h
        l = self.l()
        bo = self.bo
        Vou = self.Vou
        if h <= l:
            return (Vou / (bo * h))
        else:
            return (Vou / (bo * l))


###############################################################################
# Armatures tirant principal
###############################################################################

    def z(self):
        h = self.h
        l = self.l()
        if 0.5 <= h / l and h / l <= 1:
            return 0.2 * (l + 2 * h)
        else:
            return 0.6 * l

    def As_princ(self):
        Mou = self.Mou
        fyd = self.acier.fyd()
        z = self.z()
        return Mou / (z * fyd)

    def h_princ(self):
        l = self.l()
        h = self.h
        return min(0.15 * l, 0.15 * h)


###############################################################################
# Armatures horizontales secondaires
###############################################################################

# Réseau inférieur


    def rho_inf(self):
        tou = self.tou()
        fc28 = self.beton.fck()
        fyd = self.acier.fyd()
        return max(0.5 * (0.6 + 15 * tou / fc28) * tou / (fyd), 0.5 * tou / fyd)

    def As_inf(self):
        rho_inf = self.rho_inf()
        bo = self.bo
        return rho_inf * bo

    def h_inf(self):
        h = self.h
        l = self.l()
        if h <= l:
            return 0.40 * h
        else:
            return 0.40 * l

# Réseau supérieur
    def rho_sup(self):
        tou = self.tou()
        fyd = self.acier.fyd()
        return max(3 / 5 * self.rho_inf(), 0.3 * tou / fyd)

    def As_sup(self):
        rho_sup = self.rho_sup()
        bo = self.bo
        return rho_sup * bo

    def h_sup(self):
        h = self.h
        l = self.l()
        if h <= l:
            return 0.45 * h
        else:
            return 0.45 * l

# Armatures verticales
    def rho_v(self):
        tou = self.tou()
        fyk = self.acier.fyk()
        fyd = self.acier.fyd()
        return max(3 / 4 * tou / fyd,
                   0.8 / fyk)

    def As_v(self):
        rho_v = self.rho_v()
        bo = self.bo
        return rho_v * bo

    def As_v_inf(self):
        Pui = self.Pui
        fyd = self.acier.fyd()
        return Pui / fyd

    def As_v_total(self):
        As_v = self.As_v()
        As_v_inf = self.As_v_inf()
        return As_v + As_v_inf


###############################################################################
# Affichage des résultats  -6
###############################################################################

    def resultat_long(self):
        printentete()
        print("DONNEES D'ENTREE")
        printfintab()

        print("Béton")
        printligne("Classe de résistance", "-", "-", f"{self.beton.classeresistance}")
        printligne("Résistance caractéristique à la compression", "fck", "MPa", f"{self.beton.fck():.2f}")
        print("")
        printsep()
        print("Acier")
        printligne("Nuance", "-", "-", f"{self.acier.nuance}")
        printligne("Limite d'élasticité de l'acier", "fyk", "MPa", f"{self.acier.fyk():.2f}")
        printligne("Résistance de calcul à la traction", "fyd", "MPa", f"{self.acier.fyd():.2f}")
        print("")
        printsep()
        print("Chargement")
        printligne("Charge uniforme ELU", "Pu", "T/ml", f"{self.Pu*100:.2f}")
        printligne("Part de la charge reprise en partie", "Pui", "T/ml", f"{self.Pui*100:.2f}")
        printligne("inférieure", "", "", "")
        print("")
        printsep()
        print("Géométrie")
        printligne("Portée entre-axe", "lt", "cm", f"{self.lt*100:.2f}")
        printligne("Portée entre nu", "lo", "cm", f"{self.lo*100:.2f}")
        printligne("Portée de calcul", "l", "cm", f"{self.l()*100:.2f}")
        printligne("Hauteur de la poutre voile", "h", "cm", f"{self.h*100:.2f}")
        printligne("Epaisseur de la poutre voile", "bo", "cm", f"{self.bo*100:.2f}")
        printligne("Epaisseur mini", "bo mini", "cm", f"{self.bMini()*100:.2f}")
        print("")
        printfintab()
        print("RESULTATS")
        printfintab()
        printligne("Contraite tangente conventionnelle", "tou", "MPa", f"{self.tou():.2f}")
        print("")
        printsep()
        print("Armatures tirant")
        printligne("Bras de levier", "z", "cm", f"{self.z()*100:.2f}")
        printligne("Armatures de tirant", "As tirant", "cm2", f"{self.As_princ()*1e4:.2f}")
        printligne("Hauteur de répartion", "h tirant", "cm", f"{self.h_princ()*100:.2f}")
        printsep()
        print("")
        print("Armatures inférieures horizontales")
        printligne("Pourcentage d'armatures inférieures", "rho inf", "%", f"{self.rho_inf()*100:.4f}")
        printligne("Armatures inférieures horizontales", "As inf", "cm2", f"2 x {self.As_inf()/2*1e4:.2f}")
        printligne("Hauteur de répartition", "h As inf", "cm", f"{self.h_inf()*100:.2f}")
        print("")
        printsep()
        print("Armatures supérieures horizontales")
        printligne("Pourcentage d'armatures supérieures", "rho sup", "%", f"{self.rho_sup()*100:.4f}")
        printligne("Armatures supérieures horizontales", "As sup", "cm2", f"2 x {self.As_sup()/2*1e4:.2f}")
        printligne("Hauteur de répartition", "h sup", "cm", f"{self.h_sup()*100:.2f}")
        print("")
        printsep()
        print("Armatures verticales")
        printligne("Pourcentage d'armatures verticales", "rho vert", "%", f"{self.rho_v()*100:.4f}")
        printligne("Armatures verticales", "As vert", "cm2", f"2 x {self.As_v()/2*1e4:.2f}")
        printfintab()

    def minute(self):
        print(f"### Données d'entrée")
        print(f"- Situation {self.beton.situation.situation}")
        print(f"- Acier {self.acier.nuance}")
        print(f"- Béton {self.beton.classeresistance}")
        print(f"- Portée en nu = {self.lo*100:.2f} cm")
        print(f"- Portée entre axe = {self.lt*100:.2f} cm")
        print(f"- Hauteur = {self.h*100:.2f} cm")
        print(f"- Épaisseur = {self.bo*100:.2f} cm")
        print(f"- Pu total = {self.Pu*100:.2f} cm")
        print(f"- Pui = {self.Pui*100:.2f} cm")
        print(f"- Mu = {self.Mou*100:.2f} cm")
        print(f"- Vou = {self.Vou*100:.2f} cm")
        print(f"")
        print(f"### Résultats")
        print(f"- As tirant = {self.As_princ()*1e4:.2f} cm2, hauteur = {self.h_princ()*100:.2f} cm")
        print(f"- As inf = {self.As_inf()/2*1e4:.2f} cm2 / face, hauteur = {self.h_inf()*100:.2f} cm")
        print(f"- As sup = {self.As_sup()/2*1e4:.2f} cm2 / face, hauteur = {self.h_sup()*100:.2f} cm")
        print(f"- As vert = {self.As_v_total()/2*1e4:.2f} cm2 / ml / face")
        print("___")


###############################################################################
# Test
###############################################################################
if __name__ == "__main__":
    situation = "Durable"
    situation = SituationProjet(situation)

    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    alpha_e = 15
    fiint0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, alpha_e, fiint0)

    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)

    lo = 500 / 100
    lt = 520 / 100
    h = 300 / 100
    bo = 20 / 100
    Pu = 20 / 100
    Pui = 5 / 100
    Vou = 50 / 100
    Mou = 62.5 / 100
    pv = PoutreVoileBAEL(beton, acier, lt, lo, h, bo, Pu, Pui, Vou, Mou)
    pv.minute()