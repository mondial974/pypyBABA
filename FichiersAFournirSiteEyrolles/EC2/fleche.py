#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: fleches.py
"""
Module pour calculer les fleches 
"""
__version__ = '0.1'
import EC2.constantes as CST
import EC2.FS_ELS as FS

def lsurdmax(bw, d, dp, h, As, Asp, typeStruct, fck, MEdqp, phi, fyk, 
             aff = False, corr = 1):
    """ rapport L / d max de dispense du calcul de flèche
    entrée bw, d, dp, h, [m], As, Asp [m²], typeStruct, phi [], MEdqp [MN.m], fck, fyk [MPa]
    sortie []
    typeStruct = 
    1 : poutre sur appuis simples, dalle sur appuis simples portant
        dans 1 ou 2 direction
    2 : travée de rive d'une poutre continue, d'une dalle continue
        portant dans 1 direction ou d'une dalle continue le long
        d'un grand côté et portant dans 2 directions
    3 : travée intermédiaire d'une poutre ou d'une dalle portant 
        dans 1 ou 2 directions
    4 : dalle sans nervures sur poteaux (plancher dalle) pour la portée 
        la plus longue
    5 : console"""
    if (typeStruct in CST.KFLECH.keys()): #classes initiales
        K = CST.KFLECH[typeStruct] 
    else:
        s = ""
        for cle in CST.KFLECH.keys():
            s += cle + " "
        print("Clés utilisables : {0:s}".format(s))
        raise ValueError("Cle absente pour K = {0:s}".format(typeStruct))
    rho, rhop = As / (bw * d), Asp / (bw * d)
    rho0 = fck**0.5 * 1e-3
    if (rho <= rho0):
        ldmax1 = K * (11 + 1.5 * fck**.5 * rho0 / rho 
                      + 3.2 * fck**0.5 * (rho0 / rho - 1)**1.5)
    else:
        ldmax1 = K * (11 + 1.5 * fck**.5 * rho0 / (rho - rhop)
                      + 1.  / 12. * fck**0.5 * (rhop / rho0)**0.5)
    [alfc, yc, Ic, sigc, sigs, sigst] = \
                    FS.VerifContRect(MEdqp, As, Asp, bw, h, d, dp,
                                  fck, fyk, phi, 0.6)
    ldmax2 = ldmax1 * 310 / sigst * corr
    if (aff):
        print("Calcul de L/d max")
        print( "rho = {:.3f} % rho' = {:.3f} %, rho0 = {:.3f} %"
              .format(rho * 1e2, rhop * 1e2, rho0 * 1e2))
        print(" K = {:.2}".format(K))
        print(" sigma_s = {:.2f} MPa".format(sigst))
        print(" correction corr = {:.2f}".format(corr))
        print(" sans correction sigma_s, ni corr : L/d max = {:.3f}".format(ldmax1)) 
        print("L/d max = {:.3f}".format(ldmax2))
    return ldmax2

if __name__ == "__main__":
    import EC2.dispositionsconstructives as DC
    bw, h = 0.2, 0.4
    d, dp = 0.35, 0.05
    fck, fyk = 25., 500
    phi = 2
    MEdqp = .05
    As, Asp = DC.HA(4, 10), 0.
    typeStruct = 1
    lsurdmax(bw, d, dp, h, As, Asp, typeStruct, fck, MEdqp, phi, fyk, True)
