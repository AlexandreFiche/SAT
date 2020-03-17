import numpy as np

def test_consistance(C,S):
    #print("S:",S)
    consistant = True
    Ccur = []
    for clause in C:
        clause_valide = False
        present = False
        copy = clause.copy()
        for litteral in clause:
            valeur = True
            for elem in S: 
                if elem[0] == abs(litteral):
                    v = elem[0] * elem[1]
                    valeur =  v == litteral
                    present = present or valeur
                    if not valeur:
                        if litteral in copy:
                            #print("supprime: ",litteral)
                            copy.remove(litteral)
                        else:
                            print("doublon!")
                            print("litteral: ",litteral)
                            print("S:",S)
                            print("clause:",clause,copy)
                            return [],False
                    else:
                        present = True
            
            clause_valide = clause_valide or valeur
        #print(clause,clause_valide)
        if clause_valide and len(copy) != 0 and not present:
            Ccur.append(copy)   
        consistant = consistant and clause_valide
        if not consistant:
            break
    return consistant, Ccur

def elem_in_first_tuple(S,elem):
    if len(S) == 0:
        return False
    present = False
    for e in S:
        if e[0] == elem:
            present = True
            break
    return present


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

def clause_unitaire(P):
    for c in P:
        if len(c) == 1:
        #print("unitaire!")
            return [abs(c[0]),int(abs(c[0])/c[0]),0]
    return []

def litteraux_purs(P,taille):
    varplus  = [0] * taille
    varmoins  = [0] * taille
    for c in P: 
        for l in c:
            if l == abs(l):
                varplus[abs(l)-1] += 1
            else: 
                varmoins[abs(l)-1] += 1
    #and not elem_in_first_tuple(S,l)
    for i in range(taille):
        if varplus[i] > 0 and varmoins[i] == 0:
            return [i+1,1,-1]
        if varmoins[i] > 0 and varplus[i] == 0:
            return [i+1,-1,1]

    return []

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
        """
        if elem_in_first_tuple(S,iplus+1):
            print("probleme hmax",iplus+1,maxplus)
            print("S: ",S)
            print("P: ",P) """  
        return [iplus+1,1,-1]
    else:
        print("-")

        return [imoins+1,-1,1]
    return []

def heuristique_max2(P,taille):
    var  = [0] * taille
    for c in P: 
        for l in c:
            if l == abs(l):
                var[abs(l)-1] += 1
            else: 
                var[abs(l)-1] -= 1
    maxi = 0 
    indice = 0
    for i in range(taille):
        if var[i] > maxi:
            maxi = var[i]
            indice = i 


    return [indice+1,1,-1]


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
    #print("--BACKTRACK--")
    while not fini:
        consistant,P = test_consistance(C,S)
        if consistant:
            #print("----CONSISTANCE: OK")
            if len(S) == n:
                fini = True
            else:
                #print("------CHOIX VARIABLE")
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
                        
                #print("------AJOUT DE: ",elem)
                S.append(elem)
        else:
            #print("----CONSISTANCE: NOT OK")
            elem = S.pop()

            while len(S) > 0 and elem[2] == 0:
                elem = S.pop()
                nb_bt += 1
            
            if elem[2] != 0:
                S.append((elem[0],elem[2],0))
            else:
                fini = True 
        i += 1
        #print("---FIN BOUCLE S:",S)
    #print("--FIN BACKTRACK: TAILLE S: ",len(S)," S = ",S)
    #print(test_consistance(C,S))
    print("TOTAL OPERATION:\nNombre de backtrack: ",nb_bt,"\nNombre de choix à partir de clauses:\n\t- Pur: ",nb_pur,"\n\t- Unitaires: ",nb_unitaire,"\n\t- Plus courte: ",nb_pc)
    #print(S)
    return S

