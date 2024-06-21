from js import document as _DOC

from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from coreDCpoutre import *

def resultat_long():
    classe_resistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    bw = float(Element("bw").element.value) / 100
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
    
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    
    situation = SituationProjet("Durable")
    acier = AcierArmature(situation, nuance, diagramme="Palier horizontal", diametre=8)    
    beton = BetonArme(situation=situation, classe_exposition="XC3", classe_resistance=classe_resistance,
                      alpha_cc=1, alpha_ct=1, age=28, classe_ciment="N", alpha_e=15, fi_infini_t0=2)
    poutre = DCPoutreRectangulaire(beton, acier, bw, h, c)
    # fck = beton.fck()
    # fcm = beton.fcm()
    # fctm = beton.fctm()
    # fyk = acier.fyk()
    # Asmin1 = poutre.Asmin1()
    # Asmin2 = poutre.Asmin2()
    # Asmin = poutre.Asmin()
    # Asmax = poutre.Asmax()
    poutre.resultat_long()