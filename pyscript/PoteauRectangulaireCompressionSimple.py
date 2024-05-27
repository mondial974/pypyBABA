from js import document as _DOC

from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from appPoteauRectangulaireCompressionSimple import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classe_resistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    b = float(Element("b").element.value)
    h = float(Element("h").element.value)
    c = float(Element("c").element.value)
    l = float(Element("l").element.value)
    kf = float(Element("kf").element.value)
    NEd = float(Element("NEd").element.value)
    Asl = float(Element("Asl").element.value)
      
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    situation = SituationProjet("Durable")
    beton = BetonArme(situation, classeexposition="XC3", classeresistance=classe_resistance, acc=1, act=1, age=28, classeciment="N", alpha_e=15, fiinft0=2)
    acier = AcierArmature(situation, nuance=nuance, diagramme="Palier incliné", diametre=8)
    poteau = PoteauRectCompressionSimple(beton, acier, b/100, h/100, c/100, l/100, kf, NEd/100, Asl/1e4)
    poteau.resultat_long()

def resultat_court():
    situation = Element("situation_projet").element.value
    classe_resistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    b = float(Element("b").element.value)
    h = float(Element("h").element.value)
    c = float(Element("c").element.value)
    l = float(Element("l").element.value)
    kf = float(Element("kf").element.value)
    NEd = float(Element("NEd").element.value)
    Asl = float(Element("Asl").element.value)
    
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    
    situation = SituationProjet("Durable")
    beton = BetonArme(situation, classeexposition="XC3", classeresistance=classe_resistance, acc=1, act=1, age=28, classeciment="N", alpha_e=15, fiinft0=2)
    acier = AcierArmature(situation, nuance=nuance, diagramme="Palier incliné", diametre=8)
    poteau = PoteauRectCompressionSimple(beton, acier, b/100, h/100, c/100, l/100, kf, NEd/100, Asl/1e4)
    poteau.resultat_court()