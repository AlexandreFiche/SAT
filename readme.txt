Pour utiliser le solveur:
python main.py [nom_fichier]

si nom_fichier: .cnf ou .col a resoudre
sinon une liste d'instance et de coloration sera liste depuis le dossier Data
possibilite d'en rajouter, le programme liste tout les fichiers present dans data.
Merci de ne mettre que des fichiers .cnf ou .col dedans 

Suivant si c'est une instance SAT ou une coloration le fichier sorti ne sera pas le même:
- instance SAT: liste de chaque variable de la solution avec sa valeur
- coloration: liste de chaque sommet avec sa couleur

J'utilise l'heuristique qui prends les clauses les plus courtes

Alexandre FICHE