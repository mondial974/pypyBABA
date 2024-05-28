#-*- Encoding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: fissuration.py
"""
Module pour calculer l'ouverture de fissures
"""
__version__ = '0.1'
import EC2.constantes as CST
import EC2.materiaux as MAT
import EC2.FS_ELS as ELS

#################################
### calcul ouverture de fissures
#################################

def wkRect(MEd, As, Asp, bw, h, d, dp, fck, fyk, phi, a, phil, phit,
           cnom, aff = False, k = .6, k1 = .8, k2 = 0.5):
    """ ouverture de fissures conventionnelles
    entrée : MEd [MN.m] As, Asp [m²], bw, h, d dp, phi, a, phil, phit, cnom [m]
             fck, fyk [MPa]
    sortie : [m]
    """
    Es1 = CST.ES
    Ecm1 = MAT.Ecm(fck)
    fcteff1 = MAT.fctm(fck)    
    [alphaeCT, yqpCT, IqpCT, sigcCT, sigsCT, sigstCT] = \
        ELS.VerifContRect(MEd, As, Asp, bw, h, d, dp, fck, fyk, phi, k, aff)
    [alphaeLT, yqpLT, IqpLT, sigcLT, sigsLT, sigstLT] = \
        ELS.VerifContRect(MEd, As, Asp, bw, h, d, dp, fck, fyk, 0., k, aff)
    if (sigcLT < sigcCT):
        btype = True #
        kt  =  0.6
        yqp, sigs = yqpCT, sigsCT
    else:
        btype = False
        kt  =  0.4
        yqp, sigs  =  yqpLT, sigsLT
    hcef1 = min(2.5 * (h - d), (h - yqp) / 3., h / 2.) #attention valable en BA
    Acef = bw * hcef1
    rhopef = As / Acef
    alphae1 = Es1 / Ecm1
    DeltaEpscm1 = 0.6 * sigs / Es1
    DeltaEpscm2 = (sigs - kt * fcteff1 / rhopef * (1. + alphae1 * rhopef)) / Es1
    DeltaEpscm = max(DeltaEpscm1, DeltaEpscm2)
    c = cnom + phit
    if (c <= 25e-3): #annexe nationale !!!!
        k3 = 3.4
    else:
        k3 = 3.4 * (25e-3 / c)**(2. / 3.)
    k4 = 0.425
    srmax = k3 * c + k1 * k2 * k4 * phi /  rhopef
    if (a < 5. * (c + phil / 2.)):        
        k4 = 0.625
        srmax = k3 * c + k1 * k2 * k4 * phil / rhopef
    wk1 = DeltaEpscm * srmax
    if (aff):
        if (btype):
            print("Vérif à COURT TERME")
        else:
            print("Vérif à LONG TERME")
        print(" kt = {:.3f}".format(kt))    
        print(" yqp = {:.3f} m Sigs = {:.1} MPa".format(yqp, sigs))
        print(" hcef = {:.3f} m, Acef = {:.3f} m²".format(hcef1, Acef))
        print(" rhopef = {:.3f}".format(rhopef))
        print(" alphae = {:.3f}".format(alphae1))
        print(" -> Delta Eps = max({:.3f}, {:.3f}) = {:.3f}"
              .format(DeltaEpscm1, DeltaEpscm2, DeltaEpscm))
        print(" c = {:.3f} m".format(c))
        print(" k1 = {:.3f} k2 = {:.3f} k3 = {:.3f} k4 = {:.3f}"
              .format(k1, k2, k3, k4))
        print(" -> srmax = {:.3f} m".format(srmax))
        print(" wk = {:.2f} mm".format(wk1 * 1e3))
    return wk1

if __name__ == "__main__":
    print("Calcul ouverture de fissures")
    bw = 0.240 #m largeur de la section
    h = 0.650 #m hauteur de la section
    d = .600 #m position du centre de gravité des aciers tendus
    As = 1257e-6 #m² section aciers tendus
    dp = 0.067 #m position du centre de gravité des aciers comprimés
    Asp = 0e-6 #m² section aciers comprimés
    Mg = 0.155 #MN.m
    Mq = 0.0146
    fck = 30. #MPa,  résistance du béton en compression
    phi = 2. #coefficient de fluage initial
    
    fyk = 500.  #MPa résistance de l'acier
    psi2 = 0.3
    MEdqp = Mg + psi2 * Mq
    
    cnom = 30e-3 #m,  enrobage nominal
    phit = 8e-3 #diamètre armatures transversales
    phil = 20e-3 #diamètre armatures long
    a = 28e-3 #espacement entre axe entre les barres
    wmax = 0.3e-3#m ouverture de fissures
    wkRect(MEdqp, As, Asp, bw, h, d, dp, fck, fyk, phi, a, phil, phit, cnom, True)
    
