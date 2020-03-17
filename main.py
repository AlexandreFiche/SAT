import sat as st
import cProfile
import re
import os
import sys
import time

def lire_fichier_sat(nom):
    with open(nom, "r") as fichier:
        lignes = fichier.readlines()
        C = []

        for l in lignes:
            if l[0] != "c" and l[0] != "p" and l[0] != "%" and l[0] != "0":
                clause = l[:-2].split(' ')
                while '' in clause:
                    clause.remove('')
                clause_int = [int(i) for i in clause]
                if clause_int != []:
                    C += [clause_int]
            if l[0] == "p":
                param = l.split(' ')
                taille = int(param[2])
        #print(C)
    return C,taille

def lire_fichier_graphe(nom):
    with open(nom, "r") as fichier:
        lignes = fichier.readlines()
        C = []
        couleur = 3

        for l in lignes:
            if l[0] != "c" and l[0] != "p" and l[0] != "%" and l[0] != "0":
                #print(l)
                clause = l[1:].split(' ')
                while '' in clause:
                    clause.remove('')
                clause_int = [int(i) for i in clause]
                if len(clause_int) == 2:
                    clause_arc = cree_arc(clause_int,couleur)
                    #print("arc: ",clause_int[0]," ",clause_int[1],": ",clause_arc)
                    C += clause_arc
            if l[0] == "p":
                param = l.split(' ')
                taille = int(param[2])
                #print("p:",param)
                C = cree_coloration(taille,couleur)
        #print(C)
    return C,taille,couleur 

def ecrire_fichier_graphe(S,couleur):
    with open("coloration_res.txt","w") as fichier:
        for elem in S:
            if elem[1] == 1:
                print("Solution du sommet ",(elem[0]-1)//couleur+ + 1,": ",elem[0] % (couleur) + 1, elem[0])
                fichier.write( str((elem[0]-1)//couleur+ + 1) + " " + str(elem[0] % (couleur) + 1) + "\n")

def ecrire_fichier_sat(S):
    with open("sat_res.txt","w") as fichier:
        for elem in S:
            if elem[1] == 1:
                print("Solution de la variable ",elem[0],elem[1])
                fichier.write(str(elem[0]) + " " + str(elem[1]) + "\n")
   
def cree_coloration(nb_sommets, couleur):
    C = []
    for s in range(nb_sommets):
        #print(s)
        clause_s = []
        for c in range(couleur):
            #On attribut a chaque couleur un nombre
            clause_s += [c+s*couleur+1]
        C += [clause_s]
        for c1 in range(couleur):
            for c2 in range(couleur):
                if c1 != c2:
                    C += [[-(c1+s*couleur+1),-(c2+s*couleur+1)]]
        #print(C)  
        #print("\n\n")
    return C

def cree_arc(arc, couleur):
    C = []
    (a,b) = arc 
    for c in range(couleur):
        C += [[-((a-1)*couleur+ c + 1), -((b-1)*couleur + c + 1)]]
    return C
def main(argv):
    
    print("Solveur SAT d'Alexandre FICHE\n")
    if len(argv) == 0:
        print("Aucun fichier en entree, choisissez en un dans la selection:\n")
        path = "./Data"
        i = 0
        liste_fichier = []
        for _,_,f in os.walk(path):
            for e in f:
                liste_fichier.append(e)
                print("\t",i,":",e)
                i += 1
        #fichier = "./Data/test.col"
        choix = int(input())
        while choix > len(liste_fichier) and choix < 0:
            choix = int(input())
        fichier = "./Data/" + liste_fichier[choix]

    else:
        fichier = argv[0]
    print("Solveur SAT ",end="")
    s = fichier.split('.')
    if s[-1] == "col":
        C,nb_som,nb_coul = lire_fichier_graphe(fichier)
        taille = nb_som * nb_coul
        print("sur une coloration de graphe")
    else:
        #"./Data/uf50-01.cnf
        C,taille = lire_fichier_sat(fichier)
        print("classique")

    print("Nb de variable total: ",taille)

    #C = [[1, 2, 3, 4], [-1, 2, -3, -4],[-2,-5],[2,3,5]]
    #S = [[1,1,-1],[2,-1,1]]
    #print(st.test_consistance(C,S))
    S = st.backtrack(C,taille)
    #cProfile.run("S = st6.backtrack(C,taille)")
    print("Le modele est: ", len(S) != 0)
    print(S)
    print("taille de :",len(S))

    if s[-1] == "col":
        ecrire_fichier_graphe(S,nb_coul)
    else :
        ecrire_fichier_sat(S)

if __name__ == "__main__":
    main(sys.argv[1:])