from js import document as _DOC

from coresituationprojet import *
from corematbetonarme import *
from corematacierarmature import *
from coreDCpoutre import *

def resultat_long():
    classeresistance = Element("classe_resistance").element.value
    nuance = Element("nuance").element.value
    bw = float(Element("bw").element.value) / 100
    h = float(Element("h").element.value) / 100
    c = float(Element("c").element.value) / 100
    
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
    
    situation = SituationProjet("Durable")
    acier = AcierArmature(situation, nuance, diagramme="Palier horizontal", diametre=8)    
    beton = BetonArme(situation=situation, classeexposition="XC3", classeresistance=classeresistance,
                      acc=1, act=1, age=28, classeciment="N", ae=15, fiinft0=2)
    d = h - c
    Ac = bw * h
    fck = beton.fck()
    fcm = beton.fcm()
    fctm = beton.fctm()
    fyk = acier.fyk()
    Asmin1 = 0.26 * fctm / fyk * bw * d  
    Asmin2 = 0.0013 * bw * d
    Asmin = max(Asmin1, Asmin2)
    Asmax = 0.04 * Ac
        
    printentete()    
    print("Béton")
    printligne("Classe de résistance", "-", "-", f"{classeresistance}")
    printligne("Résitance car. compression", "fck", "MPa", f"{fck:.2f}")
    printligne("Résitance car. compression", "fcm", "MPa", f"{fcm:.2f}")
    printligne("Résitance car. compression", "fctm", "MPa", f"{fctm:.2f}")
    print("")
    printsep()
    print("Acier")
    printligne("Limite d'élasticité", "fyk", "MPa", f"{fyk:.2f}")
    print("")
    printsep()
    print("Sections minimale et maximale d'armatures")
    printligne("Asmin 1", "Asmin1", "cm2", f"{Asmin1*1e4:.2f}")
    printligne("Asmin 2", "Asmin2", "cm2", f"{Asmin2*1e4:.2f}")
    print("")
    printligne("Asmin", "Asmin", "cm2", f"{Asmin*1e4:.2f}")
    printligne("Asmax", "Asmax", "cm2", f"{Asmax*1e4:.2f}")
    printfintab()  