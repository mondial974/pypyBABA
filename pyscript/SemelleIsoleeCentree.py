from js import document as _DOC

from coresituationprojet import *
from corematacierarmature import *
from corematbetonarme import *
from appSemelleIsoleeCentree import *

situation = Element("situation_projet").element.value
situation = SituationProjet(situation="Durable")
    
classe_resistance = Element("classe_resistance").element.value
classe_exposition = Element("classe_exposition").element.value
classe_ciment = Element("classe_ciment").element.value
alpha_cc = Element("alpha_cc").element.value
alpha_ct = Element("alpha_ct").element.value
alpha_e = Element("alpha_e").element.value
fi_infini_t0 = Element("fi_infini_t0").element.value
age = Element("age").element.value
beton = BetonArme(situation, classe_exposition, classe_resistance, alpha_cc, alpha_ct, age, classe_ciment, alpha_e, fi_infini_t0, h=0, maitrise_fissuration=False)
    
nuance = Element("nuance").element.value
acier = AcierArmature(situation, nuance, diagramme="Palier incliné", diametre=8)
   
SsolELU = float(Element("SsolELU").element.value)
SsolELS = float(Element("SsolELS").element.value)
Nu = float(Element("Nu").element.value)
Nser = float(Element("Nser").element.value)
    
Hpot = float(Element("Hpot").element.value)
Bpot = float(Element("Bpot").element.value)
Asem = float(Element("Asem").element.value)
Bsem = float(Element("Bsem").element.value)
Hsem = float(Element("Hsem").element.value)
enr = float(Element("enr").element.value)
AsAsem = float(Element("AsAsem").element.value)
AsBsem = float(Element("AsBsem").element.value)

si = SemelleIsolee(beton, acier, Nu, Nser, SsolELS, SsolELU, Bpot, Hpot, Asem, Bsem, Hsem, enr, AsAsem, AsBsem)

ter = _DOC.getElementById("resultat")
ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
         

def resultat_long():
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    si.resultat_long()

def resultat_court():
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    si.resultat_court()