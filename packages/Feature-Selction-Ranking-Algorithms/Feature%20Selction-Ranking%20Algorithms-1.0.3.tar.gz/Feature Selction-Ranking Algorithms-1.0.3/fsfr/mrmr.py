from skfeature.function.information_theoretical_based import LCSI
from discretiser import con_to_dis
import numpy as np

def mrmr(dm):
    
    df=dm.copy(deep=True)
    df=(con_to_dis(df)).copy(deep=True)
    df=np.array(df,dtype=int)
    X=df[:,:-1]
    y=df[:,-1]
    F,J_CMI,MIfy=LCSI.lcsi(X,y,gamma=0,function_name='MRMR',n_selected_features=(X.shape[1]))

    return F
