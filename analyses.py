# -*- coding: utf-8 -*-
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

def analyse_profil_temp(list_Bi,prm):
    X = [0,prm.L]       #Position selon l'axe des z (rayon)
    Y = [0,prm.R]       #Position selon l'axe des r
    z = np.linspace(0, prm.L, prm.nz)
    x,y = position(X, Y, prm)
    

    for Bi_i in list_Bi:
        prm.setBi(Bi_i)
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        c_R = c_reshaped[0,:].transpose()
        c_0 = c_reshaped[-1,:].transpose()
        # label_0 = "Profil r=0 "+str(prm.Bi)
        # label_R = "Profil r="+str(prm.R)+" Bi="+str(prm.Bi)
        label_0 = "Profil r=0 "
        label_R = "Profil r="+str(prm.R)
        plt.plot(x[0,:],c_R,label=label_R)  
        plt.plot(x[-1,:],c_0,label=label_0)  
        if prm.Bi<200:
            T = ref_analytique(z,prm)
            plt.plot(z, T, '--r', label="Profil analytique")
        plt.legend()
        plt.title("Profil de température Bi: "+str(prm.Bi))
        plt.ylabel("Température (K)")
        plt.xlabel("Position z (m)")
        plt.savefig("ComparaisonProfilTemperature_Bi"+str(prm.Bi)+".png", dpi=400)
        plt.show()

def analyse_erreur(list_Bi,prm):
    
    
    X = [0,prm.L]       #Position selon l'axe des z (rayon)
    Y = [0,prm.R]       #Position selon l'axe des r
    z = np.linspace(0, prm.L, prm.nz)
    x,y = position(X, Y, prm)    
    q_contour_isole = []
    q_analytique=[]
    r = np.linspace(prm.R, 0, prm.nr)

    for Bi_i in list_Bi:
        bout = True
        D=2
        prm.setBi(Bi_i)
        prm.setCL("isole")
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        T= c_reshaped
        q_contour_isole.append(inte_fluxContour(T,z,r,bout,D,prm))
        D=1
        bout = False
        T = ref_analytique(z,prm)
        q_analytique.append(inte_fluxContour(T, z,r,bout,D, prm))


    erreur=[]
    for i in range(len(list_Bi)):
        erreur.append(abs(q_analytique[i]-q_contour_isole[i])/q_analytique[i]*100)
    plt.title("Erreur entre analytique et isole flux contour")    
    plt.plot(list_Bi,erreur,label="erreur")  
    plt.ylabel("Pourcentage (%)")
    plt.xlabel("Bi")
    plt.legend()
    plt.semilogx()
#    plt.semilogy()
    plt.savefig("q_erreur_fluxContour.png", dpi=400)
    plt.show()