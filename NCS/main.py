from NCS_model_final import *

import time

mode = "NCS" #Pour passer au NCS, sélectionner mode = "NCS"

start=time.time()

if mode == "MAXSAT" :
        from MAXSAT import *
        i2v, x , y = MAXSATModel(data, single_peak = False)
        results =exec_maxsat(maxsat_file, i2v)
        solution, frontieres = traduction_maxsat(results, x,y)
else :
        i2v,x,y = NCSModel(data)
        results =exec_gophersat(dimacs_file, i2v)
        solution, frontieres  = traduction_NCS(results, x,y)
end=time.time()


print("Le modèle", mode, "est satisfiable: "+str(results[0]))
print("Les clauses sont les suivantes: "+str(results[1]))
print("La solution est décrite de la manière suivante: ")
#for value in results[2]:
#        print(f"{value}\t{results[2][value]}")
#Nouvelle version plus détaillée
print("les parametres du modele sont :", params)
print("frontières évaluées ")
print(frontieres)
print("il y a", len(solution['coalitions']) , "Coalitions suffisantes, qui sont :")
print(solution["coalitions"],)

if mode == "MAXSAT" :
        print("Pourcentage d'instances classifiées :", len(solution["classified"])/nb_instances*100)
elapsed=end-start
print(f'Temps d\'exécution : {elapsed:.4}s')
