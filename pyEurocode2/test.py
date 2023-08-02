class Poutre:
    
    def __init__(self, b, h):
        self.b = b
        self.h = h
        
    def aire(self):
        b = self.b
        h = self.h
        return b * h
    
    def perimetre(self):
        b = self.b
        h = self.h
        return 2 * (b + h)
        
        
######################
# TEST
######################

if __name__ == "__main__":
    poutre = Poutre(20, 50)
    print("largeur =", poutre.b)
    print("hauteur =", poutre.h)
    print("aire =", f"{poutre.aire()}")
    print("perimetre =", f"{poutre.perimetre()}")