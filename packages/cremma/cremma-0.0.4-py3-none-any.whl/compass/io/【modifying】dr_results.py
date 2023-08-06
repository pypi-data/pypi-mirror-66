import pandas as pd
from .modules import database 

def from_3sheets_excel(fpath="./2019結果.xlsx"):
    '''Read from the excel summary file '''
    results = pd.read_excel(fpath, sheet_name=events, index_col=1, dtype={"電気契約番号": "string"})    
    return results

def from_sqlite(table, fpath="../../database/negawatt_infos.db"):
    conn = database.sqlite_connect(fpath)
    results = database.sqlite_read("SELECT * FROM '%s'" % table, conn)
    return results

def from_pandas(table, fpath="../../database/negawatt_infos.db"):
    conn = database.sqlite_connect(fpath)
    results = pd.read_sql("SELECT * FROM '%s'" % table, conn)
    results.index = results[results.columns[0]]
    return results
