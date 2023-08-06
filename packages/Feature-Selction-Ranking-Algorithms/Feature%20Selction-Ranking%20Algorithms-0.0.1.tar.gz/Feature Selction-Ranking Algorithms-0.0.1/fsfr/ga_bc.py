import pandas as pd
import numpy as np
from pinitialise import population_initialisation
from preprocessing import preprocessing
from cmr import crossover_mutate_replace
from svc import svm_fitness

def ga(dm,ftf):
    
    df=dm.copy(deep=True)
    X=df.iloc[:,:-1]
    X=np.array(X,dtype=float)
    X_=preprocessing(X)
    X=X_.copy()
    y=df.iloc[:,len(df.columns)-1]
    y=np.array(y,dtype=int)

    population_size=40
    population=population_initialisation(len(df.columns)-1,population_size=40,no_population_slots=4)
    fitness=np.zeros(population_size,dtype=float)
    best_fitness=-999999
    best_particle=np.zeros((len(df.columns)-1),dtype=int)

    k=0

    while(k!=100):

        for i in range(0,population_size):
            fitness[i]=svm_fitness(X,y,population[i],ftf)

        if(str(best_fitness)!=str(max(fitness))):
            f=[max(fitness),best_fitness]
            if(f.index(max(f))==0):
                best_particles_i=np.array((*np.where(fitness==max(fitness))),dtype=int)
                best_p=[sum(population[i]) for i in best_particles_i]
                best_p=best_p.index(min(best_p))
                best_particle=population[best_particles_i[best_p]].copy()
                best_fitness=max(fitness)

        elif(str(best_fitness)==str(max(fitness))):
            best_particles_i=np.array((*np.where(fitness==max(fitness))),dtype=int)
            best_p=[sum(population[i]) for i in best_particles_i]
            if(sum(best_particle)>min(best_p)):
                best_p=best_p.index(min(best_p))
                best_particle=population[best_particles_i[best_p]].copy()
                best_fitness=max(fitness)

        population=(crossover_mutate_replace(population,fitness,prob_crossover=0.9,prob_mutate=0.1)).copy()
        k=k+1

    global_best=best_particle.copy()
    features_best=list(*(np.where(global_best==1)))

    return features_best
