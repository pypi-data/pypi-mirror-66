from .filters import filter_to
    
def failures_count(data):
    '''
    Parameters: data, the dataframe to process
    Returns: occurences of negative values
    Returns:
        1. [Filter] for negative values (returns boolean mask)
        2. [Count] the occurences of negative values
     Note:
        失敗：調整力 <= 0  
    '''
    #.pipe: has to expect series, df or groupby as objects
    
    countNonNull = lambda df : df.count(axis="columns")
    
    (data
    .pipe(filter_to.negatives, arg1="調整電力量*", arg2=True)
    .pipe(countNonNull, arg1="columns")
    )    
    
    #fails = (data, column=, regex=True)    
    #failures_count = fails.count(axis="columns")

    return data

data = pd.DataFrame()
failures(data)
