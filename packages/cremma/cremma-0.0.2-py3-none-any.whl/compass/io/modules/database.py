from sqlalchemy import create_engine #Python2を推奨
import sqlite3
import pandas as pd
from sqlite3 import Error
 
 
 
def sqlite_connect(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    return conn

def sqlite_read(query, conn):
    """ Read from a SQLite database """
    cur = conn.cursor()
    cur.execute(query) 
    result = cur.fetchall()
    return result

def mysql_connect(db, user_id=None, pw=None):
    '''Connect to the given database '''
    conn_string = ""
    if user_id != None:
        conn_string = "mysql+pymysql://" + user_id + ":" + pw + "@localhost/" + db
    else:
        conn_string = "mysql+pymysql://localhost/" + db
    
    engine = create_engine(conn_string)
    db_connection = engine.connect()
    return db_connection

def read_df(sqlStatement, table, db_connection):
    '''SQL select statement '''
    df = pd.read_sql(sqlStatement, con=db_connection)
    db_connection.close()
    return df

def insert_df(df,table, db_connection):
    '''Insert dataframe in the table '''
    msg = df.to_sql(name=table,con=db_connection,if_exists='append') 

def read(sqlStatement, table, db_connection):
    '''SQL select statement '''
    item = get(sqlStatement, con=db_connection)
    db_connection.close()
    return item

def table_exists(table, conn):
    ''' Checks that a table exists. Returns a Boolean.'''
    check = "SELECT name FROM sqlite_master WHERE type='table' AND name='%d';" % table
    result = sqlite_read(check, conn)
    return len(result) > 0

def delete(conn, table, column, value):
    query = "DELETE FROM '{0}' WHERE {1} LIKE '{2}%'".format(table, column, value)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

def drop_table(conn, table):
    query = "DROP TABLE '{0}'".format(table)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
