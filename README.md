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
- Install necessary linux packages:
```
apt update && apt get install python3 python3.8-venv libopus0 -y
```
- Clone this repo to your local folder
```
git clone https://github.com/eng1neer-com/InterMumbleBot
```
- Enter folder
```
cd InterMumbleBot
```
- Create virtual python environment
```
python3 -m venv venv
```
Enter virtual environment
```
source venv/bin/activate
```
- Install needed python packages
```
pip3 install -r requirements.txt
```
- Create local settings file and set parameter
```
cp settings_default.ini settings.ini
nano settings.ini
```
- Start bot
```
python3 src/InterMumbleBot.py
```

