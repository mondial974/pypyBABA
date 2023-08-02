from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from appSemelleFilanteChargeCentree import *

def resultat_long():
    situation = Element("situation_projet").element.value
    nuance = Element("nuance").element.value
    Nu = float(Element("Nu").element.value)
    Nser = float(Element("Nser").element.value)
    SsolELU = float(Element("SsolELU").element.value)
    SsolELS = float(Element("SsolELS").element.value)
    Bmur = float(Element("Bmur").element.value)
    Bsem = float(Element("Bsem").element.value)
    Hsem = float(Element("Hsem").element.value)
    c1 = float(Element("c1").element.value)
    As1 = float(Element("As1").element.value)

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    situation = SituationProjet(situation="Durable")
    acier = AcierArmature(situation, nuance, diagramme="Palier incliné", diametre=8)
    sf = SemelleFilante(acier, Nu/100, Nser/100, SsolELS/1000, SsolELU/1000, Bmur/100, c1/100, Bsem/100, Hsem/100, As1/1e4) 
    sf.resultat_long()

def resultat_court():
    situation = Element("situation_projet").element.value
    nuance = Element("nuance").element.value
    Nu = float(Element("Nu").element.value)
    Nser = float(Element("Nser").element.value)
    SsolELU = float(Element("SsolELU").element.value)
    SsolELS = float(Element("SsolELS").element.value)
    Bmur = float(Element("Bmur").element.value)
    Bsem = float(Element("Bsem").element.value)
    Hsem = float(Element("Hsem").element.value)
    c1 = float(Element("c1").element.value)
    As1 = float(Element("As1").element.value)

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    situation = SituationProjet(situation="Durable")
    acier = AcierArmature(situation, nuance, diagramme="Palier incliné", diametre=8)
    sf = SemelleFilante(acier, Nu/100, Nser/100, SsolELS/1000, SsolELU/1000, Bmur/100, c1/100, Bsem/100, Hsem/100, As1/1e4) 
    sf.resultat_court()