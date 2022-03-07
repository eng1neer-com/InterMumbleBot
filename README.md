# InterMumbleBot
Receive information about users on other server

Necessary packages:
pymumble

How to start:
- Install pymumble via pip (e.g. in venv)
- create settings.ini file based on settings_default.ini and set parameter inside it
- python3 InterMumbleBot.py

What will the bot do:
- It will connect to two servers and will monitor users on both
- If enabled: Will broadcast each user change to all channels
- If registered with server: Will create temporary channel indicating the user count of the other server
- Usernames of other server can be requested by a private message "!users"
