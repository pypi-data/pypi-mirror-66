import pandas as pd
from modules.customers_info import mierukagamenxls as kanrishito
from modules.database import database


def get_timeslot_mean(customer, start, end, pulse_rate):
    '''Get yearly mean for the given timeslot'''
    weekly_cons = get_weekly_cons(customer, pulse_rate)
    timeslot = weekly_cons[start:end]
    return timeslot.cons.mean()

###################################################
bullshit_loader = kanrishito.get_cgroup_infos("ネガワット事業", ['ビルID', 'ユーザー名', 'パルスレート'])
timeslot_yearly_mean(bullshit_loader)

def timeslot_yearly_mean(dataframe):
    '''Returns the average of the weekday DR happened on '''

    # setup the df
    ids = data.index.values.tolist()
    results = pd.DataFrame(columns=["name","2019-04-10", "2019-09-09", "2019-09-10"], index=ids)


    # Calculate mean for each customer, for each day
    for idx in customers_info:
        
        print(customer, end= "      \r")
        results.loc[customer.ビルID, "name"] = customer.ユーザー名
        
        for dr_day in dr:
            if database.table_exists(customer.ビルID, conn):
                avg = get_timeslot_mean(customer.ビルID, dr_day["start"], dr_day["end"], customer.パルスレート)
                results.loc[customer.ビルID, dr_day["day"]] = avg
    return results



conn = database.sqlite_connect('./negawatt.db')

# Get DR dates and start/end times
dr = []
dr.append(dict({"day" : "2019-04-10", "start" : "Wednesday 16:00", "end": "Wednesday 19:00"}))
dr.append(dict({"day" : "2019-09-09", "start" : "Monday 16:00", "end": "Monday 19:00"}))
dr.append(dict({"day" : "2019-09-10", "start" : "Tuesday 16:00", "end": "Tuesday 19:00"}))

results = get_dr_WoD_avg()
# Clean the DF from non encodable chars
results.name = results.name.str.replace("\u3231", "") # （株）creates a bug
results.to_csv("year_avgs.csv", encoding="shift-jis") # Change to cp932 ?

