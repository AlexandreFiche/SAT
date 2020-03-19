import numpy as np
# Alexandre FICHE 2020 

def test_consistance(C,S):
    consistant = True
    Ccur = []
    # Parcours de chaque clause
    for clause in C:
        clause_valide = False
        present = False
        copy = clause.copy()
        # Pour chaque litteral
        for litteral in clause:
            valeur = True
            # Pour chaque elem de S
            for elem in S: 
                # Si on a une correspondance, l'elem est dans S
                if elem[0] == abs(litteral):
                    v = elem[0] * elem[1]
                    valeur =  v == litteral
                    present = present or valeur
                    # Si ce n'est pas la bonne valeur alors on le retire de la clause
                    if not valeur:
                        if litteral in copy:
                            copy.remove(litteral)
                        else:
                            print("doublon!")
                            print("litteral: ",litteral)
                            print("S:",S)
                            print("clause:",clause,copy)
                            return [],False
                    # Sinon c'est la bonne valeur, donc la clause est valide et on la supprime
                    else:
                        break
            clause_valide = clause_valide or valeur
            if present:
                break
        # Si la clause est valide et qu'aucun des litteraux est dans S avec la bonne valeur
        # alors on l'ajoute, les litteraux avec la mauvaise valeur sont supprimees
        if clause_valide and len(copy) != 0 and not present:
            Ccur.append(copy)   
        consistant = consistant and clause_valide
        if not consistant:
            break
    return consistant, Ccur

# Renvoie True si elem est dans S
def elem_in_first_tuple(S,elem):
    if len(S) == 0:
        return False
    present = False
    for e in S:
        if e[0] == elem:
            present = True
            break
    return present

# Ancienne version pour choisir les variables
# mises dans le backtrack pour pouvoir compter 
def choix_variable(S,P,C,taille):
    a = clause_unitaire(P)
    if a != []:
        return a
    b = litteraux_purs(P,taille)
    if b != []:
        return b
    #c =  heuristique_max(P,taille)
    #if c != []:
     #   return c
    d = heuristique_plus_courte(P)
    if d != []:
        return d
    
    return choix_simple(S,taille)

# Renvoie la variabble dans la premiere clause unitaire trouvee
def clause_unitaire(P):
    for c in P:
        if len(c) == 1:
            return [abs(c[0]),int(abs(c[0])/c[0]),0]
    return []

# Renvoie le premier litteraux purs trouvee
def litteraux_purs(P,taille):
    varplus  = [0] * taille
    varmoins  = [0] * taille
    for c in P: 
        for l in c:
            if l == abs(l):
                varplus[abs(l)-1] += 1
            else: 
                varmoins[abs(l)-1] += 1
    for i in range(taille):
        if varplus[i] > 0 and varmoins[i] == 0:
            return [i+1,1,-1]
        if varmoins[i] > 0 and varplus[i] == 0:
            return [i+1,-1,1]
    return []

# Heuristique qui renvoie le litteral present dans le plus de clause avec la meme valeur
def heuristique_max(P,taille):
    varplus  = [0] * taille
    varmoins  = [0] * taille
    for c in P: 
        for l in c:
            if l == abs(l):
                varplus[abs(l)-1] += 1
            else: 
                varmoins[abs(l)-1] += 1
    maxplus = 0 
    maxmoins = 0
    iplus = 0
    imoins = 0
    for i in range(taille):
        if varplus[i] > maxplus:
            maxplus = varplus[i]
            iplus = i 
        if varmoins[i] > maxmoins:
            maxmoins = varmoins[i]
            imoins = i 
    if maxplus > maxmoins:
        print("+")
        return [iplus+1,1,-1]
    else:
        print("-")
        return [imoins+1,-1,1]
    return []

# Renvoie le litteral present dans la clause la plus courte
def heuristique_plus_courte(P):
    if(len(P) == 0):
        return []
    taille_min = len(P[0])
    indice = 0
    for i in range(len(P)):
        if len(P[i]) < taille_min:
            taille_min = len(P[i])
            indice = i
    return [abs(P[indice][0]),abs(P[indice][0])/P[indice][0],-abs(P[indice][0])/P[indice][0]]
    
# renvoie la premiere valeur qui n'est pas dans S
def choix_simple(S,taille):
    i = 1
    while i <= taille and elem_in_first_tuple(S,i):
        i += 1
    return [i,1,-1]

def backtrack(C,taille):
    n = taille
    fini = False
    S = []
    i = 0
    nb_bt = 0
    nb_pur = 0
    nb_unitaire = 0
    nb_pc = 0
    while not fini:
        consistant,P = test_consistance(C,S)
        if consistant:
            if len(S) == n:
                fini = True
            else:
                elem = clause_unitaire(P)
                if elem != []:
                    nb_unitaire += 1
                if elem == []:
                    elem = litteraux_purs(P,taille)
                    if elem != []:
                        nb_pur += 1
                if elem == []:
                    elem = heuristique_plus_courte(P)
                    if elem != []:
                        nb_pc += 1
                if elem == []:
                    elem = choix_variable(S,P,C,taille)          
                S.append(elem)
        else:
            elem = S.pop()
            while len(S) > 0 and elem[2] == 0:
                elem = S.pop()
                nb_bt += 1 
            if elem[2] != 0:
                S.append((elem[0],elem[2],0))
            else:
                fini = True 
        i += 1
    print("TOTAL OPERATION:\nNombre de backtrack: ",nb_bt,"\nNombre de choix à partir de clauses:\n\t- Pur: ",nb_pur,"\n\t- Unitaires: ",nb_unitaire,"\n\t- Plus courte: ",nb_pc)
    return S

