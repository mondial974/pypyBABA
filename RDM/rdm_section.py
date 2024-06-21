from dataclasses import dataclass

@dataclass
class SectionRectangulaire:
    largeur : float
    hauteur : float
    
    def aire(self):
        return self.largeur * self.hauteur
    
    def perimetre(self):
        return 2 * (self.largeur + self.hauteur)
    
    def Ixx(self):
        """Inertie axe fort"""
        return self.largeur * pow(self.hauteur, 3.) / 12.
    
    def Iyy(self):
        """Inertie axe faible"""
        return self.hauteur * pow(self.largeur, 3.) / 12.