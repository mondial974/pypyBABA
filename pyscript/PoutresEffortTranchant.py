from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appEffortTranchant import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    bw = float(Element("bw").element.value) / 100
    h = float(Element("h").element.value) / 100
    c1 = float(Element("c1").element.value) / 100
    VEdmax = float(Element("VEdmax").element.value) / 100
    VEdred = float(Element("VEdred").element.value) / 100
    NEd = float(Element("NEd").element.value) / 100
    Asl = float(Element("Asl").element.value) / 1e4
    Asw = float(Element("Asw").element.value) / 1e4
    s = float(Element("s").element.value) / 100
    alpha = float(Element("alpha").element.value)
    teta = float(Element("teta").element.value)
           
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    situation = SituationProjet(situation)
    
    classeexposition = "XC3"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    b = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae, fiinft0)
    
    diagramme = "Palier horizontal"
    diametre = 8
    a = AcierArmature(situation, nuance, diagramme, diametre)
    
    
    redistribution = "Poutre"
    ef = EffortTranchant(b, a, redistribution, VEdmax, VEdred, NEd, bw, h, c1, Asl,  Asw, s, alpha, teta)
    
    ef.resultat_long()