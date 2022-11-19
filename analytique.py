# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:57:54 2022

@author: Étienne
"""
import numpy as np

def ref_analytique(z,prm):
    """
    

    Parameters
    ----------
    z : Vecteur
        Vecteur comprenant les points sur la longueur en mètre
    prm : Objet class Parametres()
        - L : Longueur
        - D : Diamètre
        - k : Conductivité thermique
        - T_inf : Température ambiante
        - T_w : Température de la base
        - h : Coefficient de convection
        - N : Nombre de points utilisés pour la méthode

    Returns
    -------
    T : Vecteur
        Vecteur comprenant la température sur la longueur en mètre.

    """
    m = np.sqrt(2*prm.h/(prm.k*prm.R))
    T = (prm.T_w-prm.T_inf)*(np.cosh(m*(prm.L-z))/np.cosh(m*prm.L))+prm.T_inf
    return T