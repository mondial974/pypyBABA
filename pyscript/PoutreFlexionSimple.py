from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appFlexionSimpleSectionRectangulaire import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    classeexposition = Element("classe_exposition").element.value
    nuance = Element("nuance").element.value
    Mu = float(Element("Mu").element.value) / 100
    Mser = float(Element("Mser").element.value) / 100
    bw = float(Element("bw").element.value) / 100
    bd = float(Element("bd").element.value) / 100
    bg = float(Element("bg").element.value) / 100
    h = float(Element("h").element.value) / 100
    hf = float(Element("hf").element.value) / 100
    c1 = float(Element("c1").element.value) / 100
    c2 = float(Element("c2").element.value) / 100
    As2imposee = float(Element("As2imposee").element.value) / 1e4
       
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    diagramme = "Palier horizontal"
    diametre = 8
    
    situation = SituationProjet(situation)
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    fsrect = FlexionSimpleSectionRectangulaire(beton, acier, bw, h, c1, c2, Mu, Mser, As2imposee)
    fsrect.resultat_long()