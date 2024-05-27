from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appDalle4AppuisArticules import *
from appPorteeUtilePoutreDalle import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    
    G = float(Element("G").element.value) / 1e5
    Q = float(Element("Q").element.value) / 1e5
    AC = float(Element("AC").element.value) / 1e5
    
    lnx = float(Element("lnx").element.value) / 100
    agx = float(Element("agx").element.value) / 100
    adx = float(Element("adx").element.value) / 100
    typeAppuisx = Element("typeAppuisx").element.value
    
    lny = float(Element("lny").element.value) / 100
    agy = float(Element("agy").element.value) / 100
    ady = float(Element("ady").element.value) / 100
    typeAppuisy = Element("typeAppuisy").element.value
    
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
       
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    classeexposition = "XC3"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    alpha_e = 15
    fiinft0 = 2
    # nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    
    axeAppareil = 0
    traveex = Travee(typeAppuisx, lnx, agx, adx, h, axeAppareil)
    traveey = Travee(typeAppuisy, lny, agy, ady, h, axeAppareil)
    leffx = traveex.leff()
    leffy = traveey.leff()
    
    situation = SituationProjet(situation)
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, alpha_e, fiinft0)
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, leffx, leffy, h, c)
    dalle.resultat_long()


def resultat_court():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    G = float(Element("G").element.value) / 1e5
    Q = float(Element("Q").element.value) / 1e5
    AC = float(Element("AC").element.value) / 1e5
    
    lnx = float(Element("lnx").element.value) / 100
    agx = float(Element("agx").element.value) / 100
    adx = float(Element("adx").element.value) / 100
    typeAppuisx = Element("typeAppuisx").element.value
    
    lny = float(Element("lny").element.value) / 100
    agy = float(Element("agy").element.value) / 100
    ady = float(Element("ady").element.value) / 100
    typeAppuisy = Element("typeAppuisy").element.value
    
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
       
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    classeexposition = "XC3"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    alpha_e = 15
    fiinft0 = 2
    # nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    
    axeAppareil = 0
    traveex = Travee(typeAppuisx, lnx, agx, adx, h, axeAppareil)
    traveey = Travee(typeAppuisy, lny, agy, ady, h, axeAppareil)
    leffx = traveex.leff()
    leffy = traveey.leff()
    
    situation = SituationProjet(situation)
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, alpha_e, fiinft0)
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, leffx, leffy, h, c)
    dalle.resultat_court()

# def minute():
#         situation = Element("situation_projet").element.value
#     classeresistance = Element("classe_resistance").element.value
#     nuance = Element("nuance").element.value
    
#     G = float(Element("G").element.value) / 1e5
#     Q = float(Element("Q").element.value) / 1e5
#     AC = float(Element("AC").element.value) / 1e5
    
#     lnx = float(Element("lnx").element.value) / 100
#     agx = float(Element("agx").element.value) / 100
#     adx = float(Element("adx").element.value) / 100
#     typeAppuisx = Element("typeAppuisx").element.value
    
#     lny = float(Element("lny").element.value) / 100
#     agy = float(Element("agy").element.value) / 100
#     ady = float(Element("ady").element.value) / 100
#     typeAppuisy = Element("typeAppuisy").element.value
    
#     h = float(Element("h").element.value) / 100
#     c = float(Element("c").element.value) / 100
       
#     ter = _DOC.getElementById("resultat")
#     ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
#     classeexposition = "XC3"
#     acc = 1
#     act = 1
#     age = 28
#     classeciment = "N"
#     alpha_e = 15
#     fiinft0 = 2
#     # nuance = "S500A"
#     diagramme = "Palier horizontal"
#     diametre = 8
    
#     axeAppareil = 0
#     traveex = Travee(typeAppuisx, lnx, agx, adx, h, axeAppareil)
#     traveey = Travee(typeAppuisy, lny, agy, ady, h, axeAppareil)
#     leffx = traveex.leff()
#     leffy = traveey.leff()
    
#     situation = SituationProjet(situation)
#     beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, alpha_e, fiinft0)
#     acier = AcierArmature(situation, nuance, diagramme, diametre)
#     dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, leffx, leffy, h, c)
#     dalle.minute()