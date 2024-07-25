from rich.table import Table
from rich.console import Console
from pyEurocode2.coreconstante import *

class SituationProjet:

    def __init__(self, situation='Durable'):
        self.situation = situation

    def gamma_c(self):
        situation = self.situation
        return DICT_GAMMA_C[situation]

    def gamma_s(self):
        situation = self.situation
        return DICT_GAMMA_S[situation]

    def resultatdetail(self):
        w = 40
        tableau = Table(title="PARAMETRE BETON ARME")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="left")
        tableau.add_column("Valeur", justify="right")
        tableau.add_column("unité", justify="left")
        tableau.add_row("Situation de projet", "-", f"{self.situation}", "-")
        tableau.add_row("Coefficient de sécurité sur le béton", "gamma_c", f"{self.gamma_c()}", "-")
        tableau.add_row("Coefficient de sécurité sur l'acier", "gamma_s", f"{self.gamma_s()}", "-")
        console = Console()
        console.print(tableau)