import numpy as np
import math as mt
import gc
from random import *

def crossover(population,fitness_index):

    for i in range(0,len(fitness_index),2):
    
        a=population[fitness_index[i]].copy()
        b=population[fitness_index[i+1]].copy()
        c=np.append(a[len(a)*2//3:],[*b[len(b)//3:len(b)*2//3],*a[:len(a)//3]])
        d=np.append(b[len(b)*2//3:],[*a[len(a)//3:len(a)*2//3],*b[:len(b)//3]])
        population[fitness_index[i]]=c.copy()
        population[fitness_index[i+1]]=d.copy()
        gc.collect()

    return population

def mutate(population_i,prob_mutate):
  
    positions=[]
    a=population_i.copy()
    a_c=np.zeros(len(a),dtype=int)
    while((sum(a_c)==0)):
        a_c=a.copy()
        for i in range(0,prob_mutate):
            r=randint(0,(len(a)-1))
            while(r in positions):
                r=randint(0,(len(a)-1))
            positions.append(r)
            if(a_c[r]==1):
                a_c[r]=0
            else:
                a_c[r]=1
    a=a_c.copy()

    return a
    
def crossover_mutate_replace(population,fitness,prob_crossover=0.9,prob_mutate=0.1):
    
    prob_crossover=mt.ceil(len(population)*0.9)
    prob_mutate=mt.ceil(len(population[0])*0.1)
    fitness_index=np.argsort(fitness)
    fitness_index=(fitness_index[:prob_crossover]).copy()

    cross_population=crossover(population,fitness_index)
    population=cross_population.copy()
    
    for i in fitness_index:
        population[i]=(mutate(population[i],prob_mutate)).copy()
    
    return population
