from js import document as _DOC

from coresituationprojet import *
from corematbetonarme import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classe_exposition = Element("classe_exposition").element.value
    classe_resistance = Element("classe_resistance").element.value
    classe_ciment = Element("classe_ciment").element.value
    acc = float(Element("acc").element.value)
    act = float(Element("act").element.value)
    alpha_e = float(Element("alpha_e").element.value)
    fiinft0 = float(Element("fiinft0").element.value)
    age = float(Element("age").element.value)
    
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    situation = SituationProjet(situation)
    beton = BetonArme(situation, classeexposition=classe_exposition, classeresistance=classe_resistance,
                      acc=acc, act=act, age=age, classeciment=classe_ciment, alpha_e=alpha_e, fiinft0=fiinft0)
    #beton.resultatdetail()
    beton.__repr__()

def resultat_court():
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"