from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *

def resultat_long():
    situationprojet = Element("situation_projet").element.value
    nuance = (Element("nuance").element.value)
    diagramme = (Element("diagramme").element.value)
    diametre = float(Element("diametre").element.value)
     
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    
    situation = SituationProjet(situation=situationprojet)
    acier = AcierArmature(situation=situation, nuance=nuance, diagramme=diagramme, diametre=diametre)
    acier.resultat_long()