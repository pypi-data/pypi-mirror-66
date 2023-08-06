import pandas as pd

def get_weekly_cons(customer, pulse_rate):    
    '''Returns the average of the weekday DR happened on '''
    data = pd.read_sql("SELECT DISTINCT * FROM '%s'" % str(customer), conn, index_col="DateTime", parse_dates=True)
    data.index = pd.to_datetime(data.index)
    data["cons"] = data["PulseCount"].diff().dropna().shift(-1) *pulse_rate
    weekly_cons = data.groupby(df.index.strftime('%A %H:%M')).mean()
    return weekly_cons