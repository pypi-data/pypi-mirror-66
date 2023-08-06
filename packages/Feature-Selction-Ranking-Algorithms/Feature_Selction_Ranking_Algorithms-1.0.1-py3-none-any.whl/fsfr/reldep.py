import numpy as np
import pandas as pd

def dependency(df):
   
    dt=pd.DataFrame(df)
    features=list([i for i in range(0,(df.shape[1]-1))])
    dupr=dt.groupby(features).apply(lambda x: list(x.index)).tolist()
    dupr.sort()
    rrows=[]
    for i in dupr:
        if(len(i)==1):
            rrows.append(i)
        elif(len(i)>1):
            uniq,counts=np.unique(df[i,-1],return_counts=True)
            if(len(uniq)==1):
                rrows.append(i)
    
    rrows=np.array([j for k in rrows for j in k],dtype=int)
    dependency_features=len(rrows)/len(df)
    
    return dependency_features

def relevance(df):
    
    relevance_features=np.zeros((df.shape[1]-1),dtype=float)
    for i in range(0,len(relevance_features)):
        relevance_features[i]=dependency(df[:,[i,-1]])

    return relevance_features
