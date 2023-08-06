import pandas as pd
import numpy as np

def columntypes(ctype):

    ctypes=np.zeros(len(ctype),dtype=int)
    for i in range(0,len(ctype)):
        if('float' in str(ctype[i])):
            ctypes[i]=1
        elif('object' in str(ctype[i])):
            ctypes[i]=2
        elif('int' in str(ctype[i])):
            ctypes[i]=0
    return ctypes

def con_to_dis(df):
    
    ctype=columntypes(df.dtypes)
    for i in range(0,(len(ctype)-1)):
        if(ctype[i]==1):
            uniq,counts=np.unique(df.iloc[:,i],return_counts=True)
            b=len(uniq)
            df.iloc[:,i]=pd.cut(df.iloc[:,i],bins=b,labels=False)

    return df
