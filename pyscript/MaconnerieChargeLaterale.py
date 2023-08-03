from js import document as _DOC

from pyec6maconnerie import *

def resultat_long():
    situation = Element("situation_projet").element.value
    groupe = Element("groupe").element.value
    t = float(Element("t").element.value)
    fb = float(Element("fb").element.value)
    fk1 = float(Element("fk1").element.value)
    fk2 = float(Element("fk2").element.value)
    fxk1 = float(Element("fxk1").element.value)
    fxk2 = float(Element("fxk2").element.value)
    gamma_M = float(Element("gamma_M").element.value)
    nuance = Element("nuance").element.value
    l = float(Element("l").element.value)
    h = float(Element("h").element.value)
    alpha2_025 = float(Element("alpha2_025").element.value)
    alpha2_mu = float(Element("alpha2_mu").element.value)
    liaison = Element("liaison").element.value
    WEd = float(Element("WEd").element.value)
    NEd = float(Element("NEd").element.value)
    b = float(Element("b").element.value)
    Asv1 = float(Element("Asv1").element.value)
    d1 = float(Element("d1").element.value)
    Ash2 = float(Element("Ash2").element.value)
    d2 = float(Element("d2").element.value)
    Ash2joint = float(Element("Ash2joint").element.value)
    d2joint = float(Element("d2joint").element.value)   
    
        
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    
    situation = SituationProjet(situation=situation)
    acier = AcierArmature(situation, nuance, diagramme="Palier incliné", diametre=8)
    bloc = BlocMaconnerie(groupe=groupe, t=t/100, fb=fb, fk1=fk1, fk2=fk2, fxk1=fxk1, fxk2=fxk2, fvk0=0, gamma_M=gamma_M)
    #bloc.reslong()       
    mur = MurChargementLateral(situation=situation, bloc=bloc, acier=acier, h=h/100, l=l/100,
                               liaison=liaison, WEd=WEd*1e-5, NEd=NEd*1e-5, b=b/100, Asv1=Asv1/1e4, d1=d1/100,
                               Ash2=Ash2/1e4, d2=d2/100, Ash2joint=Ash2joint/1e4, d2joint=d2joint/100, alpha2_025=alpha2_025, alpha2_mu=alpha2_mu)
    mur.reslong()

def resultat_court():
   
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"    