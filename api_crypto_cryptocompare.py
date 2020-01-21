import requests
import json
import pprint

from sqlite_utils import Database
import sqlite3

import datetime
import time
import cryptocompare

# api key see privatekeys.txt

# cryptocompare.get_coin_list(format=False)
coin = ['BTC']

res = cryptocompare.get_historical_price_minute(coin[0], curr='USD',limit=1)

dl = [coin[0],res['Data'][1]['open'], res['Data'][1]['close'], res['Data'][1]['time'], res['Data'][1]['volumeto']]

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(res)

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