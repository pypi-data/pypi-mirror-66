import pandas as pd

def feature_selection(df,fs,ftf):

    features=0
    if(fs is 'gpso'):                   #GPSO Feature Selection methods series
        if(ftf is 'ftf_1'):
            from gpso_a import gpso
            features=gpso(df,1)

        elif(ftf is 'ftf_2'):
            from gpso_bc import gpso
            featues=gpso(df,2)

        elif(ftf is 'ftf_3'):
            from gpso_bc import gpso
            features=gpso(df,3)

    elif(fs is 'ga'):                   #Genetic Algorithm series

        if(ftf is 'ftf_1'):
            from ga_a import ga
            features=ga(df,1)

        elif(ftf is 'ftf_2'):
            from ga_bc import ga
            features=ga(df,2)

        elif(ftf is 'ftf_3'):
            from ga_bc import ga
            features=ga(df,3)

    return features


def feature_ranking(df,fr):

    if(fr is 'rsm_1'):
        from rsm_a import rsm
        features=rsm(df)
    elif(fr is 'rsm_2'):
        from rsm_b import rsm
        features=rsm(df)
    elif(fr is 'rsm_3'):
        from rsm_c import rsm
        features=rsm(df)
    elif(fr is 'mifsnd'):
        from mifsnd import mifsnd
        features=mifsnd(df)
    elif(fr is 'mrmr'):
        from mrmr import mrmr
        features=mrmr(df)

    return features


def fsfr(dataset,fs='',fr='',ftf=''):

    df=dataset.copy(deep=True)
    #Checking whether the passed variable df is a pandas dataframe or not
    if (isinstance(df,pd.DataFrame)==False):
        print('Error! Pass the dataset as a pandas dataframe')
        quit()

    #if fs='' and fr='', then it's an error
    #if fs='fsmethod#' and fr='', then perform only feature selection by fsmethod#
    #if fs='' and fr='frmethod#', then perform only feature ranking by frmethod#
    #if fs='fsmethod#' and fr='frmethod#', then first perform feature selection followed by feature ranking of the selected features by frmethod#
    
    if(fs is '' and fr is ''):
        print('Error! Specify atleast one feature selection or ranking method')
        quit()

    #Feature Selection Methods
    fsmethods=['gpso','ga']
    #Feature Ranking Methods
    frmethods=['rsm_1','rsm_2','rsm_3','mifsnd','mrmr']

    #Checking whether the mentioned feature selection method is available or not
    if(fs not in fsmethods and fs is not ''):
        print(fs,'feature selection method not available')
        quit()
    
    #Checking whether the mentioned feature ranking  method is available or not
    if(fr not in frmethods and fr is not ''):
        print(fr,'feature ranking method not available')
        quit()
    
    #Checking whether the type of fitness function is mentioned or not in case feature selection method is selected
    if(fs is not '' and ftf is ''):
        print('Error! Mention the type of fitness funtion to be used')
        quit()

    fitness_function=['ftf_1','ftf_2','ftf_3']
    #Check if the fitness function mentioned is compatible or not
    if(ftf not in fitness_function):
        print('Error! The fitness funtion mentioned is not available')
        quit()
    
    #Feature Selection Phase
    features=feature_selection(df,fs,ftf)           
    #Return the features and the acuuracy obtained if the feature ranking is not specified
    if(fr is ''):
        return features
    
    #Feature Ranking Phase
    if(fs is not ''):
        df=df.iloc[:,features]
    features=feature_ranking(df,fr)

    return features
