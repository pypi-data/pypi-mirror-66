import numpy as np

def dominion(fcmii,affmi):

    domination=np.zeros(len(affmi),dtype=float)
    dominated=np.zeros(len(affmi),dtype=float)
    domination_dominated=np.zeros(len(affmi),dtype=float)

    for i in range(0,len(fcmii)):
        for j in range(0,len(fcmii)):
            if(fcmii[i]>fcmii[j]):
                domination[i]=domination[i]+1
            if(affmi[i]>affmi[j]):
                dominated[i]=dominated[i]+1
        domination_dominated[i]=domination[i]-dominated[j]
    
    brr=list(*(np.where(domination_dominated==max(domination_dominated))))
    
    if(len(brr)>1):
        maxo=domination[brr].copy()
        l=list(*(np.where(maxo==max(maxo))))
        return brr[l[0]]
        
    elif(len(brr)==1):

        return brr[0]
