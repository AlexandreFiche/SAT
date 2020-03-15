import sat as st
import cProfile
import re

def lire_fichier_sat(nom):
    fichier = open(nom, "r")
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
    fichier = open(nom, "r")
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
#Data/jnh1.cnf" 5 min
C,taille = st.lire_fichier_sat("./Data/uuf125-01.cnf")
#C = [[1, 2, 3, 4], [-1, 2, -3, -4],[-2,-5],[2,3,5]]
#S = [[1,1,-1],[2,-1,1]]
#print(st.test_consistance(C,S))
print("prout")
#taille = 5

#print(C)

S = st.backtrack(C,taille)
#cProfile.run("S = st.backtrack(C,taille)")
print("Le modele est: ", len(S) != 0)
print(S)
print("taille de :",len(S))

#S = [(51, 1, 0), (0, 1, 0)]
#print("test",2 in S[:][0])
#print([e[0] for e in S)

#print(choix_variable(S,52))