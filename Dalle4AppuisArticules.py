from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appDalle4AppuisArticules import *

def resultat_long():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    G = float(Element("G").element.value) / 1e5
    Q = float(Element("Q").element.value) / 1e5
    AC = float(Element("AC").element.value) / 1e5
    lx = float(Element("lx").element.value) / 100
    ly = float(Element("ly").element.value) / 100
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
       
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
    dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, lx, ly, h, c)
    dalle.resultat_long()

def resultat_court():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    G = float(Element("G").element.value) / 1e5
    Q = float(Element("Q").element.value) / 1e5
    AC = float(Element("AC").element.value) / 1e5
    lx = float(Element("lx").element.value) / 100
    ly = float(Element("ly").element.value) / 100
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
       
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
    dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, lx, ly, h, c)
    dalle.resultat_court()

def minute():
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    G = float(Element("G").element.value) / 1e5
    Q = float(Element("Q").element.value) / 1e5
    AC = float(Element("AC").element.value) / 1e5
    lx = float(Element("lx").element.value) / 100
    ly = float(Element("ly").element.value) / 100
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
       
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
    dalle = Dalle4AppuisArticules(situation, beton, acier, G, Q, AC, lx, ly, h, c)
    dalle.minute()    