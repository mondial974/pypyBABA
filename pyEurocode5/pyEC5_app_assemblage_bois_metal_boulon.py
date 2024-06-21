import pandas as pd
from math import radians, sin, cos, sqrt, pi
from pyEurocode2.utilsmath import  interpolation


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
def diametre_boulon(reference_boulon):
    df = pd.read_excel(r"D:\pypyBABA\pyEurocode3\EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
    return df.at['d', reference_boulon]

def dint_rondelle(reference_boulon):
    df = pd.read_excel(r"D:\pypyBABA\pyEurocode3\EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
    return df.at['dint', reference_boulon]    

def dext_rondelle(reference_boulon):
    df = pd.read_excel(r"D:\pypyBABA\pyEurocode3\EC3_bdd_diametre_boulon.xlsx", index_col="Symbole")
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


# ESPACEMENTS ET DISTANCE MINIMALE POUR LES BOULONS

def a1_boulon(alpha, d):
    alpha = radians(alpha)
    return (4 + abs(cos(alpha))) * d

def a2_boulon(d):
    return 4 * d

def a3t_boulon(d):
    return max(7*d, 80)

def a3c_boulon(alpha, d):
    if alpha < 90:
        return 0
    if 90. <= alpha and alpha < 150.:
        alpha = radians(alpha)
        return (1 + 6 * sin(alpha)) * d
    if 150. <= alpha and alpha < 210.:
        alpha = radians(alpha)
        return 4 * d
    if 210. <= alpha and alpha < 270.:
        alpha = radians(alpha)
        return (1 + 6 * sin(alpha)) * d

def a4t_boulon(alpha, d):
    alpha = radians(alpha)
    return max((2 + 2 * sin(alpha)) * d, 3 * d)

def a4c_boulon(d):
    return 3 *d