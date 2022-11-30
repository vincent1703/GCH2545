# -*- coding: utf-8 -*-


# Fonction de test servant à tester la fonction d'intgration trapezoidale
# Comparaison avec l'integration d'un polynome de degre 3 analytiquement avec 
# erreur sous le seuil prescrit. Aucune entree ou sortie

import numpy as np
from functions.inte_trapz import inte_trapz

# Bornes d'integration
xi = -2
xf = 49

#nb points :
npts = int(1e6)

seuil=1e-5

x=np.linspace(xi,xf,npts)

# Fonction test : 
y=x**2+3.7*x**3-3*x+7

# Integration numerique
I_num = inte_trapz(x, y)
def I_anal_ref(x):
    return x**3/3+3.7*x**4/4-3*x**2/2+7*x

if np.abs(I_num-(I_anal_ref(xf)-I_anal_ref(xi)))<seuil:
    print("TEST REUSSI")
else:
    print("ECHEC")
    



