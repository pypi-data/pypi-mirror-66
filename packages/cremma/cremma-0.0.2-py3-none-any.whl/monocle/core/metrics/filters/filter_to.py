import numpy as np

def negatives(data, column, regex=False):
    '''
    DEPRECATED - REPLACED by filter + formula
    Returns total count of negative values 
    '''
    bool_mask = ""
    if regex :
        bool_mask = data.filter(regex=(column))<0
    else :
        bool_mask = data.filter(column)<0
    fails = bool_mask.replace(False,np.NaN)
    
    return fails

def column(df, column, regex=False):
    '''
    Returns dataframe with only the selected column(s) 
    '''
    if regex :
        df = df.filter(regex=(column))
    else :
        df = df[column]
    
    return df
