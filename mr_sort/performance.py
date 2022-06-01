from mr_sort.model import *
from mr_sort.generate import *
import time
from sklearn.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt

taille_data_test=500
taille_total=nb_instances+taille_data_test
nb_instances_list=[500,1000,1500,2000,3000]
nb_matieres_list=[4,5,6,7]

def prediction(data_test,frontiers,weights,lmbda,nb_matieres):
    res=[]
    notes = [i[:-1] for i in data_test]
    for r in range(len(notes)):
        accepted=0
        for j in range(nb_classes - 1):
                somme = 0
                for k in range(nb_matieres):
                    if notes[r][k] >= frontiers[k][j]:
                        somme += weights[k]
                if somme >= lmbda:
                    accepted += 1

        res.append(accepted)
    return res

def perf_nb_inst():
    f1_total=[]
    accuracy_total=[]
    computing_time=[]
    for nb_instances in nb_instances_list:
        print('Traitement de: '+str(nb_instances))
        f1_temp=0
        accuracy_temp=0
        time_temp=0
        for nb_test in range(3):
            taille_total=nb_instances+taille_data_test
            start=time.time()
            data,parameters = generate_data(nb_matieres,nb_classes,taille_total)
            result = MRSortmodel(data[:taille_total-taille_data_test], nb_matieres, nb_classes)
            end=time.time()
            data_test=data[taille_total-taille_data_test:]
            list_class_test=[i[nb_matieres] for i in data_test]
            list_class_prediction=prediction(data_test,result[3],result[0],result[1],nb_matieres)
            f1_temp+=f1_score(list_class_test, list_class_prediction,average='macro')/3
            accuracy_temp+=accuracy_score(list_class_test, list_class_prediction)/3
            time_temp+=(end-start)/3
        f1_total.append(f1_temp)
        accuracy_total.append(accuracy_temp)
        computing_time.append(time_temp)

    return f1_total,accuracy_total,computing_time


'''f1_scores,accuracy_scores,computing_time=perf_nb_inst()

plot1 = plt.figure(1)
plt.plot(nb_instances_list,f1_scores, label='F1_score')
plt.plot(nb_instances_list,accuracy_scores, label='accuracy_score')
plt.title("variation du F1_score et de l'accuracy_score avec classes = 3 selon le nb instances")
plt.xlabel("nb_instances")
plt.ylabel("score")
plt.legend()

plot2 = plt.figure(2)
plt.plot(nb_instances_list,computing_time, label='time')
plt.title("variation du temps de run avec classes=3 selon le nb instances")
plt.xlabel("nb_instances")
plt.ylabel("time")
plt.legend()

plt.show()'''


def perf_nb_matiere():
    f1_total=[]
    accuracy_total=[]
    computing_time=[]
    for nb_mati in nb_matieres_list:
        print('Traitement de: '+str(nb_mati))
        print("Taille de l'instance: "+str(nb_instances))
        f1_temp=0
        accuracy_temp=0
        time_temp=0
        for nb_test in range(3):
            taille_total=nb_instances+taille_data_test
            start=time.time()
            data,parameters = generate_data(nb_mati,nb_classes,taille_total)
            result = MRSortmodel(data[:taille_total-taille_data_test], nb_mati, nb_classes)
            end=time.time()
            data_test=data[taille_total-taille_data_test:]
            list_class_test=[i[nb_mati] for i in data_test]
            list_class_prediction=prediction(data_test,result[3],result[0],result[1],nb_mati)
            f1_temp+=f1_score(list_class_test, list_class_prediction,average='macro')/3
            accuracy_temp+=accuracy_score(list_class_test, list_class_prediction)/3
            time_temp+=(end-start)/3
        f1_total.append(f1_temp)
        accuracy_total.append(accuracy_temp)
        computing_time.append(time_temp)

    return f1_total,accuracy_total,computing_time


'''f1_scores,accuracy_scores,computing_time=perf_nb_matiere()

plot3 = plt.figure(3)
plt.plot(nb_matieres_list,f1_scores, label='F1_score')
plt.plot(nb_matieres_list,accuracy_scores, label='accuracy_score')
plt.title("variation du F1_score et de l'accuracy_score avec nb_instances=1000 selon le nb matieres")
plt.xlabel("nb_matieres")
plt.ylabel("score")
plt.legend()
plt.show()


plot4 = plt.figure(4)
plt.plot(nb_matieres_list,computing_time, label='time')
plt.title("variation du temps de run avec nb_instances=1000 selon le nb matieres")
plt.xlabel("nb_matieres")
plt.ylabel("time")
plt.legend()
plt.show()'''
