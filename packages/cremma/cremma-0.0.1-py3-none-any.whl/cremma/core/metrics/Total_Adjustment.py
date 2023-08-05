from .filters import filter_to

def Total_Adjustment(df):
    ''' Returns total adjusted power'''
    adjust = filter_to.column(df, column="^調整電力量", regex=True)
    total_per_id = adjust.groupby(df.index).sum()
    total = total_per_id.sum(axis="columns")

    print("Total Adjustment \n\n", total, "\n\n\n\n")
    return total