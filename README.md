[![Python application](https://github.com/eng1neer-com/InterMumbleBot/actions/workflows/python-app.yml/badge.svg)](https://github.com/eng1neer-com/InterMumbleBot/actions/workflows/python-app.yml)

# InterMumbleBot
Receive information about users on other mumble/murmur server

## Necessary python packages:
pymumble

## Necessary linux libraries
libopus0

## What will the bot do:
- It will connect to two servers and will monitor users on both
- If enabled: Will broadcast each user change to all channels
- If registered with server: Will create temporary channel indicating the user count of the other server
- Usernames of other server can be requested by a private message "!users"

## How to start:
Install necessary linux packages:
```
apt update && apt get install python3 python3.8-venv libopus0 -y
```
Clone this repo to your local folder
```
git clone https://github.com/eng1neer-com/InterMumbleBot
```
Enter folder
```
cd InterMumbleBot
```
Create virtual python environment
```
python3 -m venv venv
```
Enter virtual environment
```
source venv/bin/activate
```
Install needed python packages
```
pip3 install -r requirements.txt
```
Leave virtual environment
```
deactivate
```
Create certificate and key for bot
```
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out $
```
Create local settings file and set parameter
```
cp settings_default.ini settings.ini
nano settings.ini
```
Example settings.ini:
```
[bot-settings]
bot-client-name = My-Inter-Mumble-Bot
hostname_server1 = my.hostname1.com
hostname_server2 = my.hostname2.com
port1 = 60001
port2 = 60002
pw1 =
pw2 =
certificate = cert.pem
private_key = key.pem
public_reply = True
broadcast_changes = True
```
Start bot
```
python3 src/InterMumbleBot.py
```

