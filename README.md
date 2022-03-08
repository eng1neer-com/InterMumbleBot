[![Build+Testing](https://github.com/eng1neer-com/InterMumbleBot/actions/workflows/python-app.yml/badge.svg)](https://github.com/eng1neer-com/InterMumbleBot/actions/workflows/python-app.yml)

# InterMumbleBot
Receive information about users on other server

Necessary packages:
pymumble

How to start:
- Clone this repo to your local folder ("git clone https://repo.url")
- Enter folder
- Create virtual python environment ("python -m venv")
- Enter virtual environment ("source venv/bin/activate")
- Install pymumble in virtual environment ("pip3 install pymumble")
- create settings.ini file based on settings_default.ini and set parameter inside it
- Start bot ("python3 src/InterMumbleBot.py")

What will the bot do:
- It will connect to two servers and will monitor users on both
- If enabled: Will broadcast each user change to all channels
- If registered with server: Will create temporary channel indicating the user count of the other server
- Usernames of other server can be requested by a private message "!users"
