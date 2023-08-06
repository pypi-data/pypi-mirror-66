from sklearn.feature_selection import mutual_info_classif
import numpy as np

def mutual_information(X,y,fclass=0):
    
    if(fclass):
        return mutual_info_classif(X,y,discrete_features=True)
    
    ff_mutual_info=np.zeros([X.shape[1],X.shape[1]],dtype=float)
    
    for i in range(0,X.shape[1]):
        ff_mutual_info[i,:]=(mutual_info_classif(X,X[:,i],discrete_features=True)).copy()

    for i in range(0,X.shape[1]):
        for j in range(0,i):
            ff_mutual_info[i,j]=0
    
    return ff_mutual_info
