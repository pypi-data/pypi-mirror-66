import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

def svmm(X,y):
    
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
    clf=svm.SVC(kernel='linear').fit(X_train,y_train)
    scores=cross_val_score(clf,X,y,cv=10)
    
    return np.mean(scores)


def svm_fitness(X,y,l,ftf):
    
    if(sum(l)==0):
        if(ftf==1):
            return 999999
        if(ftf==2 or ftf==3):
            return -999999

    features=list(*(np.where(l==1)))
    X=X[:,features]
    accuracy=svmm(X,y)
    if(ftf==1):
        fitness=(0.75*(100/accuracy))+(0.25*(sum(l)))
    elif(ftf==2):
        fitness=0.75*accuracy+0.25*(1/sum(l))
    elif(ftf==3):
        fitness=accuracy*(1-sum(l)/len(l))
    
    return fitness
