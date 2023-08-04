from js import document as _DOC

from coresituationprojet import *
from corematbetonarme import *
from appCorbeaux import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classe_exposition = Element("classe_exposition").element.value
    classe_resistance = Element("classe_resistance").element.value
    classe_ciment = Element("classe_ciment").element.value
    acc = float(Element("acc").element.value)
    act = float(Element("act").element.value)
    ae = float(Element("ae").element.value)
    fiinft0 = float(Element("fiinft0").element.value)
    age = float(Element("age").element.value)
    nuance = Element("nuance").element.value
    FEd = float(Element("FEd").element.value)
    HEd = float(Element("HEd").element.value)
    ac = float(Element("ac").element.value)
    aH = float(Element("aH").element.value)
    bw = float(Element("bw").element.value)
    h = float(Element("h").element.value)
    cnom = float(Element("cnom").element.value)
    t = float(Element("t").element.value)
    bp = float(Element("bp").element.value)
      
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    situation = SituationProjet(situation=situation)
    beton = BetonArme(situation, classeexposition=classe_exposition, classeresistance=classe_resistance, acc=acc, act=act, age=age, classeciment=classe_ciment, ae=ae, fiinft0=fiinft0)
    acier = AcierArmature(situation, nuance, diagramme="Palier incliné", diametre=8)
    corbeau = Corbeau(beton, acier, FEd=FEd/100, HEd=HEd/100, ac=ac/100, aH=aH/100, bw=bw/100, h=h/100, cnom=cnom/100, t=t/100, bp=bp/100)
    corbeau.resultat_long()

def resultat_court():
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"