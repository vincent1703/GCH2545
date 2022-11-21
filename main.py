# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:34:32 2022

@author: Étienne
"""
import numpy as np
import matplotlib.pyplot as plt

try:
    from Parametres import *
    from profil import *
except:
    pass
from inte_fluxBase import inte_fluxBase
from inte_fluxContour import inte_fluxContour
from analytique import ref_analytique

L = 10       # [m] Longueur
k = 5       # [W/m*K] Conductivité thermique
T_inf = 20+273.15     # [K] Température de l'air ambiant
T_w = 50+273.15     # [K] Température de base
R = 1       # [m] Rayon 
h = 1      # [W/m^2*K] Coefficient de convection
Bi = 1
nr = 100       # [-] Nombre de points en z
nz = 100
CL = "isole"
    
prm = Parametres(L, k, T_inf, T_w, R, h, nr, nz,CL)


# Paramètres
X = [0,prm.R]       #Position selon l'axe des r (rayon)
Y = [0,prm.L]       #Position selon l'axe des z
x,y = position(X, Y, prm)

#Conditons limites frontières à z=L

#Condion d'isolation

#Condition de convection

#1ere analyse
z = np.linspace(0, prm.L, prm.nz*prm.nr)
T = ref_analytique(z,prm)
plt.plot(z, T, '--r', label="Profil analytique")
plt.legend()
plt.title("Profil de température")
plt.ylabel("Température (K)")
plt.xlabel("Position (m)")
plt.savefig("ProfilTemperature.png", dpi=400)
plt.show()

list_Bi = [0.1, 1, 10, 20, 100]

for Bi_i in list_Bi:
    prm.setBi(Bi_i)
    A,b = mdf_assemblage(X,Y,prm)
    c = np.linalg.solve(A,b) 
    c_reshaped = c.reshape(prm.nr,prm.nz).transpose()
    c_R = c_reshaped[-1,:].transpose()
    c_0 = c_reshaped[0,:].transpose()
    label_0 = "Profil r=0 Bi= "+str(prm.Bi)
    label_R = "Profil r=R Bi= "+str(prm.Bi)
    plt.plot(x[-1,:],c_R,label_R)  
    plt.plot(x[0,:],c_0,label_0)  