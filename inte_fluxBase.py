# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:12:07 2022

@author: Étienne
"""
import numpy as np

def inte_fluxBase(T,z,prm):
    """Fonction qui intègre la convection sur la surface de l'ailette.

    Entrées:
        - T : Vecteur comprenant les températures  en Kelvin sur la longueur de l'ailette
                pour une combinaison géométrique donnée
        - z : Vecteur comprenant les points sur la longueur en mètre
        - prm : Objet class parametres()
            - k : Conductivité thermique
            - T_a : Température ambiante
            - T_w : Température du mur
            - h : Coefficient de convection
            - N : Nombre de points utilisés pour la méthode

    Sortie:
        - Valeur numérique de l'intégrale résultante (perte en W)
    """


    # Fonction à écrire
    I=0
    for i in range(1,len(T)):
        f_i = np.pi*prm.D*(T[i]-prm.T_a)*prm.h
        f_i_1 = np.pi*prm.D*(T[i-1]-prm.T_a)*prm.h
        I += (z[i]-z[i-1])*(f_i+f_i_1)/2
    q = 2*np.pi*prm.R*I
    return q# à compléter