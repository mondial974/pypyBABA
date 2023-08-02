from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appVerificationContrainteELS import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    Mser = float(Element("Mser").element.value) / 100
    bw = float(Element("bw").element.value) / 100
    beff = float(Element("beff").element.value) / 100
    h = float(Element("h").element.value) / 100
    hf = float(Element("hf").element.value) / 100
    c1 = float(Element("c1").element.value) / 100
    c2 = float(Element("c2").element.value) / 100
    As1 = float(Element("As1").element.value) / 1e4
    As2 = float(Element("As2").element.value) / 1e4
           
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    classeexposition = "XC3"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    nuance = "S500A"
    diagramme = "Palier horizontal"
    diametre = 8
    
    situation = SituationProjet(situation)
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    acier = AcierArmature(situation, nuance, diagramme, diametre)
    vc = VerifContrainteELSSectionRectangulaire(beton, acier, Mser, bw, beff, h, hf, c1, c2, As1, As2)
    vc.resultat_long()
    