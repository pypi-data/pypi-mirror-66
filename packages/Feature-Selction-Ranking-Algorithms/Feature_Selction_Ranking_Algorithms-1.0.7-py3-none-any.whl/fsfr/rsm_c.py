import numpy as np
from reldep import relevance,dependency
from discretiser import con_to_dis

def rsm(dm):
    
    df=dm.copy(deep=True)
    df=(con_to_dis(df)).copy(deep=True)
    df=np.array(df,dtype=int)
    B=np.zeros((df.shape[1]-1),dtype=int)
    S=np.zeros((df.shape[1]-1),dtype=int)
    for i in range(1,len(B)):
        B[i]=i

    relevance_features=relevance(df)
    k=0
    S[k]=np.argmax(relevance_features)
    B=np.delete(B,np.argmax(relevance_features)).copy()
    k=k+1

    while(len(B)):
        
        f=np.zeros(len(B),dtype=float)
        for i in range(0,len(B)):
            b=np.zeros(k,dtype=float)
            l=0
            for j in range(0,k):
                if(relevance_features[B[i]]>relevance_features[S[j]]):
                    l=l+1
                b[j]=b[j]+dependency(df[:,[B[i],S[j],-1]])-dependency(df[:,[S[j],-1]])
            f[i]=((l+1)/(k-l+1))*((max(b)+1)/(min(b)+1))
        S[k]=B[np.argmax(f)]
        B=np.delete(B,np.argmax(f)).copy()
        k=k+1

    return S
