import numpy as np
from itertools import chain
from mutual_information import mutual_information
from dominion import dominion
from discretiser import con_to_dis

def mifsnd(dm):
    
    df=dm.copy(deep=True)
    df=(con_to_dis(df)).copy(deep=True)
    df=np.array(df,dtype=int)
    
    B=np.zeros((df.shape[1]-1),dtype=int)
    S=np.zeros((df.shape[1]-1),dtype=int)
    for i in range(1,len(B)):
        B[i]=i

    fcmi=mutual_information(df[:,:-1],df[:,-1],1)
    ffmi=mutual_information(df[:,:-1],df[:,-1])
    k=0
    S[k]=np.argmax(fcmi)
    B=np.delete(B,np.argmax(fcmi)).copy()
    k=k+1
    
    while(len(B)):

        affmi=np.zeros(len(B),dtype=float)
        fcmii=np.zeros(len(B),dtype=float)
        for i in range(0,len(B)):
            b=0
            for j in range(0,k):
                b=b+ffmi[B[i],S[j]]
            affmi[i]=b/k
            fcmii[i]=fcmi[B[i]]
        
        f=dominion(fcmii,affmi)
        S[k]=B[f]
        B=np.delete(B,f).copy()
        k=k+1

    return S	
