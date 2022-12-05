# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

try:
    from functions.Parametres import *
    from functions.profil import *
except:
    pass
from functions.inte_fluxBase import inte_fluxBase
from functions.inte_fluxContour import inte_fluxContour
from functions.analytique import ref_analytique



def analyse_profil_temp(list_Bi,prm):
    """
    Fonction générant des graphiques de la température selon la position 
    dans l'ailette et effectuant une comparaison avec 

    Parameters
    ----------
    list_Bi : Numpy array
        Liste discrète des nombres de Biot à analyser.
    prm : Objet class parametres()
                     L : [m] Longueur
                     k : [W/m*K] Conductivité thermique
                     T_inf : [K] Température de l'air ambiant
                     T_w : [K] Température de base
                     R : [m] Rayon 
                     h :[W/m^2*K] Coefficient de convection
                     Bi : [Bi] Nombre de Biot
                     nr : Nombre de noeuds (direction radiale, r=0 à r=R)
                     nz : Nombre de noeuds (direction axiale, de z=0 à z=L)
                     CL : Condition limite ("isole" ou "convection")

    Returns
    -------
    None.

    """
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
        plt.savefig("renders/profils/ComparaisonProfilTemperature_Bi"+str(prm.Bi)+".png", dpi=400)
        plt.show()

def analyse_erreur(list_Bi,prm):
    """
    Fonction analysant l'erreur entre la solution analytique et la solution par
    MDF pour différents nombres de Biot
    
    Entrées : 
        
    list_Bi : Numpy array
        Liste discrète des nombres de Biot à analyser.
    prm : Objet class parametres()
                     L : [m] Longueur
                     k : [W/m*K] Conductivité thermique
                     T_inf : [K] Température de l'air ambiant
                     T_w : [K] Température de base
                     R : [m] Rayon 
                     h :[W/m^2*K] Coefficient de convection
                     Bi : [Bi] Nombre de Biot
                     nr : Nombre de noeuds (direction radiale, r=0 à r=R)
                     nz : Nombre de noeuds (direction axiale, de z=0 à z=L)
                     CL : Condition limite ("isole" ou "convection")

    """
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
    label_title = "erreur pour nr="+str(prm.nr)+" nz="+str(prm.nz)
    plt.plot(list_Bi,erreur,label=label_title)  
    plt.ylabel("Pourcentage (%)")
    plt.xlabel("Bi")
    plt.legend()
    plt.semilogx()
#    plt.semilogy()
    plt.savefig("renders/flux/q_erreur_fluxContour.png", dpi=400)
    plt.show()

def analyse_ordre_erreur(Bi,list_noeuds,prm):
    """
    Fonction analysant l'erreur entre la solution analytique et la solution par
    MDF pour différents nombres de Biot
    
    Entrées : 
        
    list_Bi : Numpy array
        Liste discrète des nombres de Biot à analyser.
    prm : Objet class parametres()
                     L : [m] Longueur
                     k : [W/m*K] Conductivité thermique
                     T_inf : [K] Température de l'air ambiant
                     T_w : [K] Température de base
                     R : [m] Rayon 
                     h :[W/m^2*K] Coefficient de convection
                     Bi : [Bi] Nombre de Biot
                     nr : Nombre de noeuds (direction radiale, r=0 à r=R)
                     nz : Nombre de noeuds (direction axiale, de z=0 à z=L)
                     CL : Condition limite ("isole" ou "convection")

    """
    X = [0,prm.L]       #Position selon l'axe des z (rayon)
    Y = [0,prm.R]       #Position selon l'axe des r
    z = np.linspace(0, prm.L, prm.nz)
    x,y = position(X, Y, prm)    
    q_contour_isole = []
    q_analytique=[]
    r = np.linspace(prm.R, 0, prm.nr)
    for noeuds in list_noeuds:
        prm.nr = noeuds
        prm.nz =noeuds
        r = np.linspace(prm.R, 0, prm.nr)
        z = np.linspace(0, prm.L, prm.nz)
        x,y = position(X, Y, prm)
        bout = True
        D=2
        prm.setBi(Bi)
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
    for i in range(len(list_noeuds)):
        erreur.append(abs(q_analytique[i]-q_contour_isole[i])/q_analytique[i]*100)
    plt.title("Erreur entre analytique et isole flux contour")   
    label_title = "erreur pour Bi="+str(prm.Bi)
    plt.plot((list_noeuds),(erreur),label=label_title)  
    plt.ylabel("Pourcentage (%)")
    plt.xlabel("Nombre noeuds")
    plt.legend()
    plt.semilogx()
    plt.semilogy()
    plt.savefig("renders/flux/q_erreur_ordre.png", dpi=400)
    plt.show()    
    print(linregress(np.log(list_noeuds), np.log(erreur)))
    
def analyse_flux(list_Bi,prm):
    """
    Fonction analysant le flux de chaleur à travers la base et à travers le 
    contour de l'ailette (avec ou sans les extrémités). Génère 2 graphiques
    
    Entrées : 
    list_Bi : Numpy array
        Liste discrète des nombres de Biot à analyser.
    prm : Objet class parametres()
                     L : [m] Longueur
                     k : [W/m*K] Conductivité thermique
                     T_inf : [K] Température de l'air ambiant
                     T_w : [K] Température de base
                     R : [m] Rayon 
                     h :[W/m^2*K] Coefficient de convection
                     Bi : [Bi] Nombre de Biot
                     nr : Nombre de noeuds (direction radiale, r=0 à r=R)
                     nz : Nombre de noeuds (direction axiale, de z=0 à z=L)
                     CL : Condition limite ("isole" ou "convection")

    """
    
    # Initialisation des paramètres et vecteurs pour l'analyse
    
    X = [0,prm.L]       #Position selon l'axe des z (rayon)
    Y = [0,prm.R]       #Position selon l'axe des r
    r = np.linspace(prm.R, 0, prm.nr)
    z = np.linspace(0, prm.L, prm.nz)
    q_base_isole = []
    q_base_convection = []
    q_contour_isole = []
    q_contour_convection_bout = []
    q_contour_convection_sansbout = []
    
# =============================================================================
# 1ere analyse : Flux par la base
# =============================================================================
    
    for i in range(len(list_Bi)):
        prm.setBi(list_Bi[i])
        prm.setCL("isole")
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        T = c_reshaped
        q_base_isole.append(inte_fluxBase(T,r,prm))
        prm.setCL("convection")
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        T = c_reshaped
        q_base_convection.append(inte_fluxBase(T,r,prm))
        bout = True
        D=2
        
        prm.setBi(list_Bi[i])
        prm.setCL("isole")
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        T= c_reshaped
        q_contour_isole.append(inte_fluxContour(T,z,r,bout,D,prm))
        prm.setCL("convection")
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        T = c_reshaped
        q_contour_convection_bout.append(inte_fluxContour(T,z,r,bout,D,prm))
        bout = False
        q_contour_convection_sansbout.append(inte_fluxContour(T,z,r,bout,D,prm))
        
    plt.title("Q en fonction du nombre de Bi")    
    plt.plot(list_Bi,q_base_isole,label="cond isole - flux base")  
    plt.plot(list_Bi,q_base_convection,label="cond convection - flux base")  
    plt.plot(list_Bi,q_contour_isole,label="cond isole - flux contour")  
    plt.plot(list_Bi,q_contour_convection_sansbout,label="cond convection - flux contour") 
    plt.plot(list_Bi,q_contour_convection_bout,'--', color="orange",label="cond convection + bout - flux contour") 
    plt.ylabel("q (W)")
    plt.xlabel("Bi") 
    plt.legend()
    plt.savefig("renders/flux/q_flux_base.png", dpi=400)
    plt.show()

# =============================================================================
# 2e analyse: flux par le contour (avec et sans prise en compte de la 
#                                  convection au bout)
# =============================================================================

    q_contour_isole = []
    q_contour_convection_bout = []
    q_contour_convection_sansbout = []
    q_analytique=[]
    r = np.linspace(prm.R, 0, prm.nr)
    z = np.linspace(0, prm.L, prm.nz)
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
        prm.setCL("convection")
        A,b = mdf_assemblage(X,Y,prm)
        c = np.linalg.solve(A,b) 
        c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
        T = c_reshaped
        q_contour_convection_bout.append(inte_fluxContour(T,z,r,bout,D,prm))
        bout = False
        q_contour_convection_sansbout.append(inte_fluxContour(T,z,r,bout,D,prm))
        D=1
        bout = False
        T = ref_analytique(z,prm)
        q_analytique.append(inte_fluxContour(T, z,r,bout,D, prm))

    plt.title("Q en fonction du nombre de Bi et flux contour")    
    plt.plot(list_Bi,q_contour_isole,label="cond isole")  
    plt.plot(list_Bi,q_contour_convection_bout,'--', color="orange",label="cond convection + bout")  
    plt.plot(list_Bi,q_contour_convection_sansbout,label="cond convection")  
    plt.plot(list_Bi,q_analytique,'--r',label="analytique")  
    plt.ylabel("q (W)")
    plt.xlabel("Bi")
    plt.legend()
    plt.savefig("renders/flux/q_flux_contour.png", dpi=400)
    plt.show()
    
    
    
def analyse_bonus(list_Bi, prm):
    """
    Fonction générant une analyse de la température dans l'ailette, à la fois
    dans la direction radiale et axiale (carte 2D des températures)
    Génère des graphiques pour chaque nombre de Biot et pour chaque C.L. 
    
    Entrées : 
    list_Bi : Numpy array
        Liste discrète des nombres de Biot à analyser.
    prm : Objet class parametres()
                     L : [m] Longueur
                     k : [W/m*K] Conductivité thermique
                     T_inf : [K] Température de l'air ambiant
                     T_w : [K] Température de base
                     R : [m] Rayon 
                     h :[W/m^2*K] Coefficient de convection
                     Bi : [Bi] Nombre de Biot
                     nr : Nombre de noeuds (direction radiale, r=0 à r=R)
                     nz : Nombre de noeuds (direction axiale, de z=0 à z=L)
                     CL : Condition limite ("isole" ou "convection")

    """
    
    X = [0,prm.L]       #Position selon l'axe des z (rayon)
    Y = [0,prm.R]       #Position selon l'axe des r
    x,y = position(X, Y, prm)    
    min_val = 273
    max_val = 373
    
    condition_limite = ["isole","convection"]
    for Bi_i in list_Bi:
        for cl in condition_limite:
            prm.setBi(Bi_i)
            prm.setCL(cl)
            A,b = mdf_assemblage(X,Y,prm)
            c = np.linalg.solve(A,b)
            c_reshaped = c.reshape(prm.nz,prm.nr).transpose()
            fig,ax = plt.subplots(nrows=1,ncols=1)
            fig1 = ax.pcolormesh(x,y, c_reshaped, vmin=min_val, vmax=max_val)
            plt.colorbar(fig1, ax=ax)
            ax.set_title("Profil Temperature (K) Bi="+str(prm.Bi)+" CL="+str(prm.CL))
            ax.set_xlabel("Position z")
            ax.set_ylabel("Position r")
            plt.savefig("renders/profils_2D/Profil2D_Bi"+str(prm.Bi)+"_"+str(prm.CL)+".png", dpi=400)
            plt.show()
        