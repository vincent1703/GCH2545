# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:12:07 2022

@author: Étienne
"""
import numpy as np

def inte_fluxBase(T,z,r,prm):
    """Fonction qui intègre la convection sur la surface de l'ailette.

    Entrées:
        - T : Matrice comprenant les températures  en Kelvin sur la longueur et le rayon de l'ailette
                pour une combinaison géométrique donnée
        - r : Vecteur comprenant les points sur le rayon en mètre
        - z : Vecteur comprenant les points sur la longueur en mètre
        - prm : Objet class parametres()
            - k : Conductivité thermique
            - T_inf : Température ambiante
            - T_w : Température du mur
            - h : Coefficient de convection
            - N : Nombre de points utilisés pour la méthode

    Sortie:
        - Valeur numérique de l'intégrale résultante (perte en W)
    """
    "T[r,z]"
    # Fonction à écrire
    I=0
    for i in range(1,len(r)):
        for j in range(1,len(z)):
            f_i_1 = T[i-1,j+1]-T[i-1,j-1]
            f_i = T[i,j+1]-T[i,j-1]
            I += (r[i]-r[i-1])/(z[j]-z[j-1])*r[i]*(f_i_1+f_i)/2
    q = np.pi*prm.k*I
    return q# à compléter