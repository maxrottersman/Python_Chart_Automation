# Python_Chart_Automation

# Python Chart Automation
### Automate Updates on Cloud Server and serve chart

(Note to git-forgetful self) I setup this repo to work with my Visual Code repos on my PCs with:

- Create new repo on Github.com (add readme and .gitignore)
- Create folder matching repo name on PC, like python_chart_automation
- Open that empty folder in Visual Code (VC)
- Open Terminal | New Terminal in VC
- Through browser/Github, copy Clone with HTTPS string
- In terminal, write command:
	git clone https://github.com/maxrottersman/python_chart_automation.git .
	(NOTE: Dot . at end very important or it will create sub-folder with same name as repo)
- In .gitignore add:
```.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.code-workspace
venv/*
.venv/*
```
- Make first commit in VC (branch-circles icon), name, click on checkmark above
- click on circular arrow bottom left to push to github, then check github
- PHASE 2: Setting up Python. In terminal, create your virtual python env: python -m venv .venv
- create new file like test.py, which will get VC to look for Python.
- VC may ask to download python, instead, pick .venv/etc.. by clicking on pick interpreter bottom left.  It will ask to install pylint.  Install
- In terminal you should see something like: (.venv) C:\Files2020_Dev\ByProject\python_chart_automation>, the (.venv) telling you VC is using Python from your virtual environment. 
- Create requirements.txt file for later when I want to create same python environment on cloud server (or anywhere else)

### Setting up Google Linux Cloud server (prob similar for any cloud linux)
- Create instance on GC, check allow HTTP and HTTPs access
- click on SSH button so GC create SSH key between server and terminal you can access through Google's cloud console
- sudo apt-get update
- sudo apt-get pip3
- sudo apt install python3 python3-dev python3-venv
- sudo apt-get install nginx (for domain name if used later)
- sudo apt-get install lynx (test web server locally)

- mkdir ~/python_chart_automation
- cd python_chart_automation
- python3 -m venv venv
- source venv/bin/activate

- pip install --upgrade pip
- pip install wheel
- pip install gunicorn flask
- sudo ufw allow 5000

## Test server and firewall
- nano testflask.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```
nano wsgi.py
```
from testflask import app

if __name__ == "__main__":
    app.run()
gunicorn --bind 0.0.0.0:5000 wsgi:app
```
Could not reach on Internet, but "lynx localhost:5000" worked from 2nd terminal, so problem must be Google firewall.  
Fix (though probably too broad, improve later)  Create Google Cloud FW rule Ingress, Allow, All Instances in the network, 0.0.0.0/0, Protocols and ports "Allow All"

## Automation
In Google VM Terminal, clicking on gear, top right, provides "upload" file option.  Other methods see: [transfer files](https://cloud.google.com/compute/docs/instances/transfer-files)

In Ubuntu
~/ is home folder
ls -a (will show .ssh and other folders like that)
For commmand line checking of sqlite database get:
Ctrl+Shift+V to copy from Windows into terminal
```
    sudo apt-get install sqlite3 libsqlite3-dev
```
.open db/db_cryptocompare.sqlite
.tables
Select * from Value_ByMinute_BTC; 
WARNING! Must have that ending ; or it won't return anything!

## crontab

crontab -e
grep CRON /var/log/syslog

Was getting an MTA error in cron job so: sudo apt-get install postfix. However, decided I didn't want emails so set MAILTO="" in crontab instead

PERMISSIONS (try if things don't work)
```chmod u+x apitest.py
sudo service cron stop
sudo service cron start
sudo chmod 775 db
sudo chmod 664 db/db_cryptocompare.sqlite
```


The following was not picking up the scripts true folder,
but the one before.  Hours of pain until I figured it out.
A virtual env issue my guess
from pathlib import Path
ScriptPath = Path.cwd()
Instead:
```ScriptPath = Path(__file__).parent```

## SQLite3
```
.open db_cryptocompare.sqlite
Select * from Value_ByMinute_BTC; (DO NOT FORGET SEMI-COLON ; )
 ```


MISC

- We want an SSH key which will allow our server to pull our code from github.  In practical terms, SSH keys are how we can have computers login to each other without going through a login/password process. [ssh info](https://www.ssh.com/ssh/keygen)
