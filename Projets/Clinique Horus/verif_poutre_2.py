# from pyEurocode5.pyEC5_app_assemblage_bois_metal_boulon import *
from pyEurocode5.pyEC5matbois import *
from pyEurocode2.utilsprint import *
from math import radians, sin, cos, sqrt, pi
# import RDM.rdm_section as rdm 

# BOIS
def f_h_0_k(d, rhok):
    return 0.082 * (1. - 0.01 * d) * rhok
    
def f_h_alpha_k(fh0k, alpha, k90):
    alpha = radians(alpha)
    return fh0k / (k90 * (sin(alpha))**2. + (cos(alpha))**2.)
    
def k_90(nature_bois, d):
    dict_k90 = {'résineux' : 1.35 + 0.015 * d,
                'LVL' : 1.30 + 0.015 * d,
                'feuillus' : 0.90 + 0.015 * d}
    return dict_k90[nature_bois]


# PLAQUE METALLIQUE
def type_plaque(epaisseur, d):
    if epaisseur <= 0.5 * d:
        return 'plaque mince'
    if epaisseur > 1.1 * d:
        return 'plaque épaisse'
    else:
        return 'plaque intermédiaire'

# BOULONS
def diametre(reference_boulon):
    df = pd.read_excel(r"pyEurocode3/EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
    return df.at['d', reference_boulon]

def dint_rondelle(reference_boulon):
    df = pd.read_excel(r"D:\pypyBABA\pyEurocode3\EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
    return df.at['dint', reference_boulon]    

def dext_rondelle(reference_boulon):
    df = pd.read_excel(r"D:\pypyBABA\pyEurocode3\EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
    return df.at['dext', reference_boulon]  


def f_ub(classe_resistance_boulon):
    df = pd.read_excel(r"D:\pypyBABA\pyEurocode3\EC3_bdd_classe_boulon.xlsx", index_col="Symbole")
    return df.at['f_ub', classe_resistance_boulon]

def F_ax_Rk(fc90k, dint, dext):
    return 3 * fc90k * pi * (dext**2 - dint**2) / 4

def M_y_Rk(f_ub, d):
    return 0.3 * f_ub * d**2.6

def F_v_Rk_a(fhk, t1, d):
        return 0.4 * fhk * t1 * d
        
def F_v_Rk_b(MyRk, fhk, d, FaxRk):
    F = 1.15 * sqrt(2. * MyRk * fhk * d)
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
def F_v_Rk_c(fhk, t1, d):
    return fhk * t1 * d
            
def F_v_Rk_d(fhk, t1, d, MyRk, FaxRk):
    F = fhk * t1 * d * (sqrt(2. + 4. * MyRk / (fhk * d * t1**2)) - 1) 
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
def F_v_Rk_e(MyRk, fhk, d, FaxRk):
    F = 2.3 * sqrt(MyRk * fhk * d)  + FaxRk / 4.
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
def F_v_Rk_f(fh1k, t1, d):
    return fh1k * t1 * d
    
def F_v_Rk_g(fh1k, t1, d, MyRk, FaxRk):
    F = fh1k * t1 * d * (sqrt(2. + 4. * MyRk / (fh1k * d * t1**2)) - 1)
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
def F_v_Rk_h(MyRk, fh1k, d, FaxRk):
    F= 2.3 * sqrt(MyRk * fh1k * d)
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
def F_v_Rk_j(fh2k, t2, d):
    return 0.5 * fh2k * t2 * d
        
def F_v_Rk_k(MyRk, fh2k, d, FaxRk):
    F = 1.15 * sqrt(2. * MyRk * fh2k * d) + FaxRk / 4.
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
      
def F_v_Rk_l(fh2k, t2, d):
    return 0.5 * fh2k * t2 * d
    
def F_v_Rk_m(MyRk, fh2k, d, FaxRk):
    F =  2.3 * sqrt(MyRk * fh2k * d)  + FaxRk / 4.
    effet_corde = min(F/4., FaxRk/4)
    return F + effet_corde
    
def F_v_Rk_simple_cisaillement(fhk, t1, d, MyRk, FaxRk, typeplaque, epaisseurplaque):
    FvRk_mince =  min(F_v_Rk_a(fhk, t1, d),
                      F_v_Rk_b(MyRk, fhk, d, FaxRk))
    FvRk_epaisse = min(F_v_Rk_c(fhk, t1, d),
                       F_v_Rk_d(fhk, t1, d, MyRk, FaxRk),
                       F_v_Rk_e(MyRk, fhk, d, FaxRk))
    if typeplaque == 'plaque mince':
        return FvRk_mince
    if typeplaque == 'plaque épaisse':
        return FvRk_epaisse
    if typeplaque == 'plaque intermédiaire':
        x = epaisseurplaque
        xa = 0.5 * d
        xb = 1.1 * d
        ya = FvRk_mince
        yb = FvRk_epaisse
        return interpolation(xa, xb, ya, yb, x)

def F_v_Rk_interne(fh1k, t1, d, MyRk, FaxRk):
    return min(F_v_Rk_f(fh1k, t1, d),
               F_v_Rk_g(fh1k, t1, d, MyRk, FaxRk),
               F_v_Rk_h(MyRk, fh1k, d, FaxRk))

def F_v_Rk_double_cisaillement(fh2k, t2, d, MyRk, FaxRk, typeplaque, epaisseurplaque):
    FvRk_mince =  min(F_v_Rk_j(fh2k, t2, d),
                      F_v_Rk_k(MyRk, fh2k, d, FaxRk))
    FvRk_epaisse = min(F_v_Rk_l(fh2k, t2, d),
                       F_v_Rk_m(MyRk, fh2k, d, FaxRk))
    if typeplaque == 'plaque mince':
        return FvRk_mince
    if typeplaque == 'plaque épaisse':
        return FvRk_epaisse
    if typeplaque == 'plaque intermédiaire':
        x = epaisseurplaque
        xa = 0.5 * d
        xb = 1.1 * d
        ya = FvRk_mince
        yb = FvRk_epaisse
        return interpolation(xa, xb, ya, yb, x)

def F_v_Rk(typeplaque, epaisseurplaque, d, t1, t2, fhk, fh1k, fh2k, MyRk, FaxRk, typeassemblage):
    if typeassemblage == 'simple cisaillement':
        return F_v_Rk_simple_cisaillement(fhk, t1, d, MyRk, FaxRk, typeplaque, epaisseurplaque)
    if typeassemblage == 'interne':
        return F_v_Rk_interne(fh1k, t1, d, MyRk, FaxRk)
    if typeassemblage == 'double cisaillement':
        return F_v_Rk_double_cisaillement(fh2k, t2, d, MyRk, FaxRk, typeplaque, epaisseurplaque)





if __name__ == "__main__":
    
    # POUTRE 2 - VERIFICATION ATTACHE
       
    ###################################################
    # DONNEES D'ENTRÉES
    ###################################################
    
    AFFAIRE = 'CLINIQUE HORUS'
    ATTACHE = 'ATTACHE A'
    
    # COEFFICIENT
    gamma_M = 1.25  # lamelle colle
    k_mod = 0.55 # classe de service 1 + action de long terme
    
    # POUTRE
    largeur_poutre = 160.   # mm
    hauteur_poutre = 600.   # mm
    
    # BOIS 1
    t1 = largeur_poutre / 2.
    classe_resistance_bois_1 =  'GL28h'
    nature_bois_1 = 'résineux'
    bois_1 = Bois(nature_bois=nature_bois_1, classe_resistance_bois=classe_resistance_bois_1)
    
    # BOIS 2
    t2 = largeur_poutre / 2.
    classe_resistance_bois_2 =  'GL28h'
    nature_bois_2 = 'résineux'
    bois_2 = Bois(nature_bois=nature_bois_2, classe_resistance_bois=classe_resistance_bois_2)
        
    # PLAQUE METALLIQUE
    epaisseur_plaque = 8. # mm
        
    # BOULONS
    reference_boulon = 'M20'
    classe_resistance_boulon = '6.8'  
      
    # ASSEMBLAGE
    type_assemblage = 'interne'
    
    # EFFORT
    FvEd = 8200 # N
    alpha = 90. # deg
    
    
    ###################################################
    # CALCULS INTERMEDIAIRES
    ###################################################
    d = diametre(reference_boulon)
    
    # BOIS 1
    rhok1 = bois_1.rho_k()
    k901 = k_90(nature_bois_1, d)
    fh0k = f_h_0_k(d, rhok1)
    fh0k1 = f_h_0_k(d, rhok1)
    fhk = f_h_alpha_k(fh0k, alpha, k901)
    fh1k = f_h_alpha_k(fh0k1, alpha, k901)
    fc90k1 = bois_1.f_c_90_k()
    
    # BOIS 2
    rhok2 = bois_2.rho_k()
    k902 = k_90(nature_bois_2, d)
    fh0k2 = f_h_0_k(d, rhok2)
    fh2k = f_h_alpha_k(fh0k2, alpha, k902)
    fc90k2 = bois_2.f_c_90_k()
    
    # BOULONS
    fub = f_ub(classe_resistance_boulon)
    MyRk = M_y_Rk(fub, d)
    df = pd.read_excel(r"pyEurocode3\EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
    dint_rondelle = df.at['dint', reference_boulon]
    dext_rondelle = df.at['dext', reference_boulon]
    FaxRk = F_ax_Rk(fc90k1, dint_rondelle, dext_rondelle)
    FaxRk_4 = FaxRk / 4.
    
    
    # PLAQUE METALLIQUE
    typeplaque = type_plaque(epaisseur_plaque, d)
    
    # ASSEMBLAGE
    FvRk = F_v_Rk(typeplaque, epaisseur_plaque, d, t1, t2, fhk, fh1k, fh2k, MyRk, FaxRk, type_assemblage)
    FvRd = k_mod * FvRk / gamma_M
 
    
     
    ###################################################
    # RÉSULTATS
    ###################################################  
    f = open(r'Projets\Clinique Horus\ndc_attache_A.txt', 'w', encoding='utf-8')
    
    printfile(f'AFFAIRE : {AFFAIRE}', f)
    printfile(f'ATTACHE : {ATTACHE}', f)
    printfile('', f)
    printentetefile(f)
    
    printfile("DONNÉES D'ENTRÉE", f)
    printfile('', f)
    printlignefile("Section poutre", "largeur", "mm", f"{largeur_poutre:.0f}", f)
    printlignefile("", "hauteur", "mm", f"{hauteur_poutre:.0f}", f)
    printlignefile("Classe de résistance", "-", "-", f"{classe_resistance_bois_1}", f)
    printlignefile("Masse volumique caractéristique", "-", "kg/m3", f"{rhok1}", f)
    printlignefile("Résistance car. à la compression transversale", "fc90k", "MPa", f"{fc90k1}", f)
    
    printfile('', f)
    printlignefile("Référence boulon", "-", "-", f"{reference_boulon}", f)
    printlignefile("Diamètre", "d", "mm", f"{d:.0f}", f)
    printlignefile("Classe de résistance", "", "", f"{classe_resistance_boulon}", f)   
    printlignefile("Résistance ultime à la traction", "f_ub", "MPa", f"{fub:.0f}", f)
    printlignefile("Diamètre intérieur rondelle", "dint", "mm", f"{dint_rondelle:.0f}", f)
    printlignefile("Diamètre extérieur rondelle", "dext", "mm", f"{dext_rondelle:.0f}", f)

    printfile('', f)
    printlignefile("Épaisseur plaque", "-", "mm", f"{epaisseur_plaque:.0f}", f)
    printlignefile("type de plaque", "-", "mm", f"{typeplaque}", f)
    
    printfile('', f)
    printlignefile("Assemblage", "-", "-", f"{type_assemblage}", f)
    printlignefile("", "t1", "mm", f"{t1:.0f}", f)
    printlignefile("Angle effort par rappor au fil du bois", "alpha", "deg", f"{alpha}", f)
    
    printfile('', f)
    printlignefile("Effort sollicitant", "FvEd", "N", f"{FvEd:.0f}", f)
    
    
    printfile('', f)
    printsepfile(f)
    printfile("RÉSULTzzzATS", f)
    printlignefile("Portance locale caractéristique du bois", "fh1k", "MPa", f"{fh1k:.2f}", f)
    printlignefile("Moment d'écoulement plastique", "MyRk", "N.mm", f"{MyRk:.0f}", f)
    printlignefile("Capacité d'arrachement axial du boulon", "FaxRk", "N", f"{FaxRk:.0f}", f)
    printlignefile("Capacité résistance caractéristique", "FvRk", "N", f"{FvRk:.0f}", f)
    printlignefile("", "kmod", "-", f"{k_mod}", f)
    printlignefile("", "gamma_M", "-", f"{gamma_M}", f)
    printlignefile("Capacité résistance de calcul", "FvRd", "N", f"{FvRd:.0f}", f)
    
    printsepfile(f)
    f = open(r'Projets\Clinique Horus\ndc_attache_A.md', 'w', encoding='utf-8')
    txt = f"""
# Objet
Vérification de l'attache A

# Données d'entrée
## Poutre en bois lamellé collé
Section de la poutre : {largeur_poutre:.0f} x {hauteur_poutre:.0f} mm  
Classe de résistance du bois : {classe_resistance_bois_1}  
Masse volumique caractéristique : {rhok1:.0f} kg/m3  
Résistance caractéristique à la compression transversale : $\\rho$ = {fc90k1} MPa  


### Titre 3
    """
    f.write(txt)



    
    
    
    
    
    
    
    
    
    
    # print('a', file=f)
    # Création des objets
    


    # printentete()
    # print("Bois")
    # printligne("Classe de résistance", "-", "-", f"{profile_1.classe_resistance_bois}")
    # printsep()   
    # print("Organe")
    # printligne("Type d'organe", "-", "-", f"{organe.organe}")
    # printligne("Diamètre", "-", "-", f"{organe.reference_diametre}")
    # printligne("", "d", "mm", f"{organe.diametre()}")
    # printligne("Classe de résistance", "-", "", f"{organe.classe_resistance_organe}")
    # printligne("", "f_yb", "MPa", f"{organe.f_yb()}")
    # printligne("", "f_ub", "MPa", f"{organe.f_ub()}")
    # printsep()
    # print("Plaque")
    # printligne("Type de plaque", "-", "-", f"{plaque.type_plaque()}")
    # printsep()
    # print("Assemblage")
    # printligne("Type d'assemblage", "-", "-", f"{assemblage.mode_cisaillement}")
    # printligne("Type d'assemblage", "M_y_Rk", "N.mm", f"{assemblage.M_y_Rk():.2f}")
    
        
