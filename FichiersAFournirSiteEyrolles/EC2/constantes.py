#-*- coding: Utf-8 -*-
#### IMPORTANT : 07 / 11 / 2021
#### L'auteur n'est pas tenu responsable de l'utilisation faite de ce programme
#### --------------------------------------------------------------------------
# Nom de fichier: constantes.py
"""
 Module des constantes 
"""
__version__ = '0.1'

SITUATIONS = {'TRANSITOIRE' : [1.5, 1.15, 1.15], 
              'DURABLE' : [1.5, 1.15, 1.15], 
              'ACCIDENTELLE' : [1.2, 1., 1.],
              'SISMIQUE': [1.3, 1., 1.]}
##marche pas problème d'espace de nommage
def modif_situation(situation):
    global GAMMAC, GAMMAS, GAMMAP, SITUATION
    if (situation.upper() in SITUATIONS):
        GAMMAC, GAMMAS, GAMMAP = SITUATIONS[situation.upper()]   #coefficient de sécurité sur le béton 
        print("Sitation initiale : {:s}".format(SITUATION))
        print("Situation finale : {:s} avec GAMMAC = {:.1f} GAMMAS = {:.1f} GAMMAP = {:.1f}"
              .format(situation.upper(), GAMMAC, GAMMAS, GAMMAP))
        SITUATION = situation.upper()
    else: #valeur par défaut, situation de projet DURABLE
        print(u"Attention, situation uniquement en TRANSITOIRE, DURABLE, " + 
              "ACCIDENTELLE, SISMIQUE, pas en {:s}".format(situation))
        print(u"Valeurs des constantes non modifiées")
       
SITUATION = "DURABLE"
GAMMAC, GAMMAS, GAMMAP = SITUATIONS["DURABLE"] 
CMAX = 90.      #MPa, compression limite pour le béton
#GAMMAC = 1.5   #coefficient de sécurité sur le béton 
ALPHAC = 1.	 #coefficient effet à long terme en compression
ALPHACT = 1.	 #coefficient effet à long terme en traction
GAMMACE = 1.2 #coefficient pour les instabilités 
TYPECIMENTEC2 = ["N", "R", "S"] #type de ciment autorisé
SEC2 =  {"S":.38, "N":.25, "R":.2} #clé pour le coefficient s (évolution temporelle)
ALPHAEC2 = {"S":-1, "N":0, "R":-1} #clé pour le coefficient alpha (fluage)
ALPHADSEC2 = {"S": [3, 0.13], "N": [4, .12], "R": [6, .11]} #clé pour le coefficient alphads (retrait)
#acier
#GAMMAS = 1.15  #coefficient de sécurité sur l'acier
RHOS = 7850. #kg/m3, masse volumique de l'acier
ES = 200000. #MPa module d'élasticité de l'acier
#numérique
ZERO = 1e-9 #utile pour les comparaisons

#cisaillement
KTABLENERV = {"lisse" : 1, "rugeuse" : 0.5}
#flèche
KFLECH = {1: 1., 2:1.3, 3:1.5, 4:1.2, 5:.4}
##durabilité
CMIN = 10e-3 #m, enrobage minimal 4.4.1.2(2)P
NB = 3.0 #[], nombre de barres maximales dans le paquet 8.9.1(2)
PHINMAX = 55e-3 #m, diamètre maximal du paquet 8.9.1(2)
EHMIN = 20e-3 #m, espacement horizontal minimal  8.2(2)
K1PHI = 1  #[], pour espacement horizontal minimal 8.2(2)
K2DG = 5e-3 #m, pour espacement horizontal minimal 8.2(2)
PHIIPHIJ = 1.7 #, rapport de diamètre maxi 8.9.1(1)
DCDEV = 10e-3 #m, tolérance d'exécution 4.4.1.2(2)P
CMINDG = 5e-3 #mm, majoration pour diamètre de granulats
DGDIFF = 32e-3 #mm, seuil pour la majoration
CMINDURBA1 = {
#######"          S1  S2  S3  S4  S5  S6   
           'X0' : [10, 10, 10, 10, 15, 20],
           'XC1': [10, 10, 10, 15, 15, 25],
           'XC2': [10, 10, 10, 15, 15, 25],
           'XC3': [10, 15, 20, 25, 30, 35],
           'XC4': [15, 20, 25, 30, 35, 40],           
           'XD1': [20, 25, 30, 35, 40, 45],     
           'XS1': [20, 25, 30, 35, 40, 45],           
           'XA1': [20, 25, 30, 35, 40, 45],           
           'XD2': [25, 30, 35, 40, 45, 50],
           'XS2': [25, 30, 35, 40, 45, 50],           
           'XA2': [25, 30, 35, 40, 45, 50],           
           'XD3': [30, 35, 40, 45, 50, 55],
           'XS3': [30, 35, 40, 45, 50, 55],
           'XA3': [30, 35, 40, 45, 50, 55]}#a justifier en fonction agent
CMINDURBA2 = {'XF1pf'  : CMINDURBA1['XC4'],#XF1 peu fréquent
              'XF2f'   : CMINDURBA1['XD1'],#XF2 fréquent
              'XF2fexp': CMINDURBA1['XD3'],#XF2 fréquent exposé
              'XF3pf'  : CMINDURBA1['XC4'],#XF3 peu fréquent
              'XF3pfee': CMINDURBA1['XC4'],#XF3 avec entraineur air peu fréquent
              'XF4f'   : CMINDURBA1['XD2'],#XF4 fréquent
              'XF4fexp': CMINDURBA1['XD3'],#XF4 fréquent exposé
              'XF4tf'  : CMINDURBA1['XD3']}#XF4 très fréquent 
KXM = {'XM1': 5,  #prise en compte de l'attrition
       'XM2': 10,
       'XM3': 15}
ENRCOMP = {'X0': -1, 'XC1': -1, 'XC2': -1, 'XC3': -1, 'XC4': -1,
           'XD1': -1, 'XS1': -1, 'XA1': -1,
           'XD2': -1, 'XS2': -1, 'XA2': -1,
           'XD3': -1, 'XS3': -1, 'XA3': -1}
DUREE100 = {'X0': 2, 'XC1': 2, 'XC2': 2, 'XC3': 2, 'XC4': 2,
           'XD1': 2, 'XS1': 2, 'XA1': 2,
           'XD2': 2, 'XS2': 2, 'XA2': 2,
           'XD3': 2, 'XS3': 2, 'XA3': 2}
DUREE25 = {'X0': -1, 'XC1': -1, 'XC2': -1, 'XC3': -1, 'XC4': -1,
           'XD1': -1, 'XS1': -1, 'XA1': -1,
           'XD2': -1, 'XS2': -1, 'XA2': -1,
           'XD3': -1, 'XS3': -1, 'XA3': -1}
NATURELIANT = {'X0': 0, 'XC1': -1, 'XC2': -1, 'XC3': -1, 'XC4': -1,
           'XD1': 0, 'XS1': 0, 'XA1': 0,
           'XD2': 0, 'XS2': 0, 'XA2': 0,
           'XD3': 0, 'XS3': 0, 'XA3': 0}
CLASSRESIST = {'X0': [[30, -1], [50, -2]],
               'XC1': [[30, -1], [50, -2]],
               'XC2': [[30, -1], [55, -2]],
               'XC3': [[30, -1], [55, -2]],
               'XC4': [[35, -1], [60, -2]],
               'XD1': [[40, -1], [60, -2]],
               'XS1': [[40, -1], [60, -2]], 
               'XA1': [[40, -1], [60, -2]],
               'XD2': [[40, -1], [60, -2]],
               'XS2': [[40, -1], [60, -2]], 
               'XA2': [[40, -1], [60, -2]],
               'XD3': [[45, -1], [75, -2]],
               'XS3': [[45, -1], [75, -2]],
               'XA3': [[45, -1], [75, -2]]}
CLASSESTRUCTMIN, CLASSESTRUCTMAX = 1, 6
CLASSESTRUCTDEF = 4 #classe structurale par défaut en batiment
DUREEMAJ = 100.
DUREEMIN = 25.
FCKEC2 = [12., 16., 20., 25., 30., 35., 40., 45., 50., 55., 60., 70., 80., 90.]
FCKMINIDUR = {'X0': 12., 'XC1': 20., 'XC2': 25., 'XC3': 30., 'XC4': 30.,
           'XD1': 30., 'XS1': 30., 'XA1': 30., 'XF1': 30.,
           'XD2': 30., 'XS2': 35., 'XA2': 30., 'XF2': 25.,
           'XD3': 35., 'XS3': 35., 'XA3': 35., 'XF3': 30.}