from .filters import filter_to
from .formulas import sumup

# Filters : allow to select (selectors)
contract = lambda df: filter_to.column(df, column="契約調整電力")
reduction = lambda df: filter_to.columns(df, column="^調整電力量*", regex=True)

# Formula SPECIFIC TO DEMAND RESPONSE
# A formula can be a metric (in this case, no pipeline)
def success(contract, adjust):
    '''
    Calculates the success rate of the customers.
    '''
    accomp = adjust/contract    
    return accomp


# GENERAL OPERATION
def average(df):
    # Type: Operation
    return df.groupby(df.index).mean()


import pandas as pd
data= pd.DataFrame()
AverageSuccess = data.pipe(success).pipe(average)
