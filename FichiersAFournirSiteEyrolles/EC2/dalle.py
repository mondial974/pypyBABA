#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: dalle.py
"""
Module pour calculer les dalles en béton armé
"""
__version__ = '0.1'
import numpy as np
from math import pi, sin

def Mxx(x, y, nu, p, lx, ly):
    """ moment xx en (x,y) d'une dalle uniformément chargée
    entree x, y, lx, y [m] nu [] p [MN/m]
    sortie [MN.m/m]"""
    nip = np.arange(1, 50, 2)
    mip = np.arange(1, 50, 2)
    rho = lx / ly
    Mxx  = sum([sum([ 
        (m**2.0 + nu * n**2.0 * rho**2. ) / 
                (m * n * (m**2 + n**2.0  * rho**2.0)**2.0) 
                * sin( n * pi * y / ly) for n in nip]) 
                * sin( m * pi * x / lx) for m in mip])
    return Mxx * 16. / pi**4. * lx**2. * p

def Myy(x, y, nu, p, lx, ly):
    """ moment yy en (x,y) d'une dalle uniformément chargée
    entree x, y, lx, y [m] nu [] p [MN/m]
    sortie [MN.m/m]"""
    nip = np.arange(1, 50, 2)
    mip = np.arange(1, 50, 2)
    rho = lx / ly
    Myy  = sum([sum([ 
        (nu * m**2.0  + n**2.0 * rho**2.) / 
                (m * n * (m**2 + n**2. * rho**2.)**2.0) 
                * sin( n * pi * y / ly) for n in nip]) 
                * sin( m * pi * x / lx) for m in mip])
    return Myy * 16. / pi**4. * lx**2. * p 

def fmax(x, y, nu, D, p, lx, ly):
    """ fleche en (x,y) d'une dalle uniformément chargée
    entree x, y, lx, y [m] nu [] p [MN/m]
    sortie [m]"""
    nip = np.arange(1, 50, 2)
    mip = np.arange(1, 50, 2)
    rho = lx / ly
    fs2  = sum([sum([ 
                    1. / 
                (m * n * (m**2 + n**2. * rho**2.)**2.0) 
                * sin( n * pi * y / ly) for n in nip]) 
                * sin( m * pi * x / lx) for m in mip])
    return fs2 * 16. / pi**6. * lx**4. * p / D 

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    lx, ly = 4., 6. #m, lx < ly
    rho = 0.80
    lx = rho * ly
    p = 15e-3 #MN/m cahrage répartie en surface
    nu = 0.2
    h = 0.2 #m, epaisseur de la dalle
    E = 33000. #MPa, module du béton
    
    nip = np.arange(1, 50, 2)
    mip = np.arange(1, 50, 2)
    
    print("Calcul du moment fléchissant au milieu de la dalle")
    MxxC = sum([sum([ 
            (m**2.0 + nu * n**2.0 * rho**2.0) / 
                    (m * n * (m**2 + n**2.0 * rho**2.0)**2.0) 
                    * (-1)**((m + n - 2.) / 2.) for n in nip]) for m in mip])
    print("mu_x( rho = {:.3f}) = {:.4f}".format(rho, MxxC * 16. / pi**4))
    
    print("Calcul de la flèche au milieu de la dalle")
    D = E * h**3. / (12. * (1. - nu**2.) )
    fmaxC = sum([sum([ 
            1. / 
                    (m * n * (m**2 + n**2.0 * rho**2.0)**2.0) 
                    * (-1)**((m + n - 2.) / 2.) for n in nip]) for m in mip])
    print("f( rho = {:.3f}) = {:.4f}".format(rho, fmaxC * 16. / pi**6 * 12. * (1. - nu**2)))
    
