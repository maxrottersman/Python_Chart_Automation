#import requests
#import json

from sqlite_utils import Database
import sqlite3

#pip install -U coindesk

from coindesk.client import CoindeskAPIClient

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