from dataclasses import dataclass
from math import sqrt
from pyEurocode2.utilsmath import interpolation
import pandas as pd

@dataclass
class Bois:
    nature_bois : str
    classe_resistance_bois : str
    
    
    def f_m_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_m_k', self.classe_resistance_bois]
    
    def f_t_0_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_t_0_k', self.classe_resistance_bois]
    
    def f_t_90_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_t_90_k', self.classe_resistance_bois]
    
    def f_c_0_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_c_0_k', self.classe_resistance_bois]
    
    def f_c_90_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_c_90_k', self.classe_resistance_bois]
    
    def f_v_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_v_k', self.classe_resistance_bois]
    
    def f_r_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['f_r_k', self.classe_resistance_bois]
    
    def E_0_mean(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['E_0_mean', self.classe_resistance_bois]
    
    def E_0_05(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['E_0_05', self.classe_resistance_bois]
    
    def E_90_mean(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['E_90_mean', self.classe_resistance_bois]
    
    def E_90_05(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['E_90_05', self.classe_resistance_bois]
    
    def G_mean(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['G_mean', self.classe_resistance_bois]
    
    def G_05(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['G_05', self.classe_resistance_bois]
    
    def G_r_mean(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['G_r_mean', self.classe_resistance_bois]
    
    def G_r_05(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['G_r_05', self.classe_resistance_bois]
    
    def rho_k(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['rho_k', self.classe_resistance_bois]
    
    def rho_mean(self):
        df = pd.read_excel(r"D:\pypyBABA\pyEurocode5\pyEC5_bdd_caracteristique_bois.xlsx", sheet_name='Feuil1', index_col="Symbole")
        return df.at['rho_mean', self.claclasse_resistance_boissse_bois]    