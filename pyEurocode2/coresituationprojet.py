# from rich.table import Table
# from rich.console import Console

class SituationProjet:

    def __init__(self, situation='Durable'):
        self.situation = situation

    def gc(self):
        if self.situation == 'Durable':
            return 1.5

        if self.situation == 'Accidentelle':
            return 1.2

    def gs(self):
        if self.situation == 'Durable':
            return 1.15

        if self.situation == 'Accidentelle':
            return 1.

    def resultatdetail(self):
        w = 40
        tableau = Table(title="PARAMETRE BETON ARME")
        tableau.add_column("Désignation", justify="left", width=w)
        tableau.add_column("Symbole", justify="left")
        tableau.add_column("Valeur", justify="right")
        tableau.add_column("unité", justify="left")
        tableau.add_row("Situation de projet", "-", f"{self.situation}", "-")
        tableau.add_row("Coefficient de sécurité sur le béton", "gc", f"{self.gc()}", "-")
        tableau.add_row("Coefficient de sécurité sur l'acier", "gs", f"{self.gs()}", "-")
        console = Console()
        console.print(tableau)