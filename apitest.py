import requests
import json
import pprint

from sqlite_utils import Database
import sqlite3

import datetime as dt
import time
import cryptocompare
from sqlite3 import Error

# To work with files on any OS
from pathlib import Path

# assume script in root of our project
ScriptPath = Path.cwd()
# assume our database in folder /sqlite_db
dbPath = ScriptPath / 'db'
# get system neutral (win/unix) path and convert to string
dbPathandFile = dbPath / 'db_cryptocompare.sqlite'
db_uri = r'sqlite:///' + str(dbPathandFile)

# create connection to DB at top
global conn
# In Linux need to create the 'db' folder first
# Python Sqlite won't create automatically like Windows
conn = sqlite3.connect(str(dbPathandFile))

# cryptocompare.get_coin_list(format=False)
def get_coin_value_byMinute(coin):

    res = cryptocompare.get_historical_price_minute(coin, curr='USD',limit=1)

    TimeYYYYMMDDHHMM = dt.datetime.utcfromtimestamp(res['Data'][1]['time']).strftime("%Y %m %d H%H M%M")

    record = ([coin,
            res['Data'][1]['open'], 
            res['Data'][1]['close'], 
            TimeYYYYMMDDHHMM, 
            res['Data'][1]['volumeto']])

    # Pretty print return dictionary if we want
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(res)
    print(record)
    #print(record[3])
    return record

def create_connection(db_file):
  #db_uri = "sqlite:///db.sqlite"
    #conn = sqlite3.connect(db_file) #created at top

    # create table
    createTable = ('CREATE TABLE IF NOT EXISTS Value_ByMinute_BTC (' 
                    'id INTEGER NOT NULL,' 
                    'symbol TEXT,' 
                    'close REAL,' 
                    'open REAL,' 
                    'time TEXT,' 
                    'volumeto REAL,'   
                    'PRIMARY KEY (id));')

    cur = conn.cursor()
    cur.execute(createTable)
 
    return cur

def insert_into_table(cur, record):
    cur.execute('INSERT INTO Value_ByMinute_BTC (symbol, open,close,time,volumeto) VALUES (?,?,?,?,?)', (record))
    conn.commit()      
    #cur.execute('INSERT INTO Value_ByMinute_BTC(symbol,open,close,time,volumeto) VALUES (?,?,?,?,?)', (record))   
    #print(record)
    # cur.execute('INSERT INTO Value_ByMinute_BTC (symbol, open,close,time,volumeto) VALUES (?,?,?,?,?)', (
    #         't',
    #         0,
    #         0,
    #         'time',
    #         0)
    #         )

    # cur.execute('INSERT INTO Value_ByMinute_BTC (symbol, open,close,time,volumeto) VALUES (?,?,?,?,?)', (
    #         record[0],
    #         record[1],
    #         record[2],
    #         str(record[3]),
    #         record[4])
    #         )
    # conn.commit()
     

    # If we had many rows .executemany, or something like
    #for r in record:
    #    cur.execute('INSERT INTO Value_ByMinute_BTC (?,?,?,?,?)', r)


if __name__ == '__main__':
    #pythonlog = open(str(ScriptPath)+"/pylog.txt", "a")
    #pythonlog.write(time.strftime("%m/%d/%Y"))

    record = get_coin_value_byMinute('BTC')
    cur = create_connection(dbPathandFile)
    insert_into_table(cur, record)
    conn.close()
    #main()

#pretty_json = json.loads(res)
#print (json.dumps(pretty_json, indent=2))

#print(res)

#api_client = CoindeskAPIClient.start('currentprice')
#response = api_client.get()

#mydict = json.loads(response.text)

#db = Database(sqlite3.connect("sqlite/apidata.db"))
#coindesk = db["coindesk"]
#coindesk.insert(mydict)


#pretty_json = json.loads(response.text)
#print (json.dumps(pretty_json, indent=2))

#print(db.table_names())

#print(response.text)

# dogs.insert({
#     "name": "Cleo",
#     "twitter": "cleopaws",
#     "age": 3,
#     "is_good_dog": True,
# })


# look at later: https://min-api.cryptocompare.com/