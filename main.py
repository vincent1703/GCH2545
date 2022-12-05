# -*- coding: utf-8 -*-

# =============================================================================
# Importations de librairies et modules
# =============================================================================

try:
    from functions.Parametres import *
    from functions.analyses import *
    from functions.test_integration import *
except:
    pass

import numpy as np

# =============================================================================
# Definition des parametres pour les analyses
# =============================================================================

L =     0.2         # [m] Longueur
k =     10          # [W/m*K] Conductivité thermique
T_inf = 0 + 273.15  # [K] Température de l'air ambiant
T_w =   100 + 273.15# [K] Température de base
R =     0.2         # [m] Rayon 
h =     1           # [W/m^2*K] Coefficient de convection
Bi =    1           # [-] Nombre de Biot 
"""                 ***UTILISER ARGUMENT LISTES POUR ANALYSES, prm.Bi seulement
                    pour initialisation **"""
nr =    20          # [-] Nombre de points pour discrétisation en r
                    # "prendre plus que 20 n'est pas necessaire selon erreur 
                    # avec analytique"
nz =    20          # [-] Nombre de points pour discrétisation en z
                    # "prendre plus que 20 n'est pas necessaire selon erreur 
                    # avec analytique"
CL =    "isole"     # Condition limite ("isole" ou "convection")
    
prm = Parametres(L, k, T_inf, T_w, R, h, nr, nz,CL)


# =============================================================================
# Liste des nombres de Biot à utiliser pour les analyses :
#     - list_Bi_discr : Pour analyses de profil, d'erreur et bonus
#     - list_Bi_cont : Pour analyses selon le nombre de Biot (davantage de Bi)
# =============================================================================

list_Bi_discr = np.array([0.05,0.1, 1, 10, 20, 100])  
list_Bi_cont=np.linspace(0.01,100,100) 
list_noeuds = np.array([5,6,7,8,9,10, 15, 20, 25, 30,35,40,50,60,70,80,90,100])  

# =============================================================================
# Appel des fonctions d'analyses(description plus détaillées dans les fonctions
#                                d'analyse)
# =============================================================================

analyse_profil_temp(list_Bi_discr,prm)

analyse_flux(list_Bi_cont,prm)   


analyse_erreur(list_Bi_discr,prm)

analyse_ordre_erreur(0.05,list_noeuds,prm)

analyse_bonus(list_Bi_discr,prm)


# =============================================================================
# Appel de la fonction du test d'intégration
# =============================================================================

test_integration()


