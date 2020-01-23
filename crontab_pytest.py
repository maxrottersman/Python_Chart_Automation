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

pythonlog = open(str(ScriptPath)+"/log_crontab_pytest.txt", "a")
pythonlog.write(time.strftime("I was run from crontab"))