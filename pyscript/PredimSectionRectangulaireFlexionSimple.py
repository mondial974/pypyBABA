from js import document as _DOC

from coresituationprojet import *
from corematbetonarme import *
from appPredimSectionRectangulaireFlexionSimple import *


def resultat_long():
    Mu = float(Element("Mu").element.value) / 100
    mu_lu = float(Element("mu_lu").element.value)
    k = float(Element("k").element.value)

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"

# -------------------------------------------------------------------
    situation = "Durable"
    situation = SituationProjet(situation)

    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance,
                      acc, act, age, classeciment, ae, fiinft0)

    predim = PredimSectionRectangulaireFlexionSimple(
        situation, beton, Mu, mu_lu, k)
    predim.resultat_long()


###############################################################################
def resultat_court():
    Mu = float(Element("Mu").element.value) / 100
    mu_lu = float(Element("mu_lu").element.value)
    k = float(Element("k").element.value)

    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"

# ------------------------------------------------------------------------------
    situation = "Durable"
    situation = SituationProjet(situation)

    classeexposition = "XC3"
    classeresistance = "C25/30"
    acc = 1
    act = 1
    age = 28
    classeciment = "N"
    ae = 15
    fiinft0 = 2
    beton = BetonArme(situation, classeexposition, classeresistance,
                      acc, act, age, classeciment, ae, fiinft0)

    predim = PredimSectionRectangulaireFlexionSimple(
        situation, beton, Mu, mu_lu, k)
    predim.resultat_court()
