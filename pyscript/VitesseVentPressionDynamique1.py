from js import document as _DOC

from pyec14vent import *

def resultat_long():
    regionclimatique = Element("region_vent").element.value
    categorieterrain = Element("categorie_terrain").element.value
    cdir = float(Element("cdir").element.value)
    cseason = float(Element("cseason").element.value)
    co = float(Element("co").element.value)
    casorographique = Element("cas_orographique").element.value
    h = float(Element("h").element.value)
    ze = float(Element("ze").element.value)
        
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    
    pression = PressionVent(regionclimatique=regionclimatique, categorieterrain=categorieterrain, cdir=cdir, cseason=cseason, co=co, casorographique=casorographique, ze=ze, h=h)
    pression.resultat_long()

def resultat_court():
    regionclimatique = Element("region_vent").element.value
    categorieterrain = Element("categorie_terrain").element.value
    cdir = float(Element("cdir").element.value)
    cseason = float(Element("cseason").element.value)
    co = float(Element("co").element.value)
    casorographique = Element("cas_orographique").element.value
    h = float(Element("h").element.value)
    ze = float(Element("ze").element.value)
        
    ter = _DOC.getElementById("resultat")
    ter.innerHTML = "<py-terminal id='terminal'></py-terminal>"
        
    
    pression = PressionVent(regionclimatique=regionclimatique, categorieterrain=categorieterrain, cdir=cdir, cseason=cseason, co=co, casorographique=casorographique, ze=ze, h=h)
    pression.resultat_court()