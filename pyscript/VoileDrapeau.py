from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appVoileDrapeau import *

def resultatLong():
    repere = Element("repere").element.value
    situation = Element("situation_projet").element.value
    classeexposition = Element("classeexposition").element.value
    classeeesistance = Element("classeresistance").element.value
    nuance = Element("nuance").element.value
    l = float(Element("l").element.value) / 100
    h = float(Element("h").element.value) / 100
    ep = float(Element("ep").element.value) / 100
    h = float(Element("h").element.value) / 100
    FEd = float(Element("FEd").element.value) / 100

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    
    situation = SituationProjet(situation)
    acc = 1
    act = 1 
    age = 28
    classeciment = "N"
    alpha_e = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeeesistance, acc, act, age, classeciment, alpha_e, fiinft0)
    
    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    
    vd1 = VoileDrapeau1(beton, acier, l, h, ep, FEd)
    print(f"Repère élément : {repere}")
    print("")
    vd1.resultatLong()