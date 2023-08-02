from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appPoutreVoileBAEL import *


def resultat_long():
    repere = Element("repere").element.value
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    ag = float(Element("ag").element.value) / 100
    ad = float(Element("ad").element.value) / 100
    lo = float(Element("lo").element.value) / 100
    h = float(Element("h").element.value) / 100
    bo = float(Element("bo").element.value) / 100
    Pu = float(Element("Pu").element.value) / 100
    Pui = float(Element("Pui").element.value) / 100
    Vou = float(Element("Vou").element.value) / 100
    Mou = float(Element("Mou").element.value) / 100

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"

    situation = SituationProjet(situation)

    classeexposition = "XC3"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiint0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae,
                      fiint0)

    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)

    lt = ag / 2 + lo + ad / 2
    pv = PoutreVoileBAEL(beton, acier, lt, lo, h, bo, Pu, Pui, Vou, Mou)
    pv.resultat_long()


def minute():
    repere = Element("repere").element.value
    situation = Element("situation_projet").element.value
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    ag = float(Element("ag").element.value) / 100
    ad = float(Element("ad").element.value) / 100
    lo = float(Element("lo").element.value) / 100
    h = float(Element("h").element.value) / 100
    bo = float(Element("bo").element.value) / 100
    Pu = float(Element("Pu").element.value) / 100
    Pui = float(Element("Pui").element.value) / 100
    Vou = float(Element("Vou").element.value) / 100
    Mou = float(Element("Mou").element.value) / 100

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"

    situation = SituationProjet(situation)

    classeexposition = "XC3"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiint0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance, acc, act, age, classeciment, ae,
                      fiint0)

    diagramme = "Palier horizontal"
    diametre = 8
    acier = AcierArmature(situation, nuance, diagramme, diametre)

    lt = ag / 2 + lo + ad / 2
    pv = PoutreVoileBAEL(beton, acier, lt, lo, h, bo, Pu, Pui, Vou, Mou)
    print(f"## {repere}")
    print("")
    pv.minute()
