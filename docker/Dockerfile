FROM ubuntu:latest

# linux packages
RUN apt update && \
    apt install python3 python3-pip libopus0 -y
RUN apt install git -y

# get code
RUN mkdir -p /opt && \
    cd /opt && \
    git clone https://github.com/eng1neer-com/InterMumbleBot && \
    cd InterMumbleBot

# pip packages
RUN pip3 install -r /opt/InterMumbleBot/requirements.txt

# start the bot
COPY settings/run.sh /opt/InterMumbleBot/run.sh
RUN chmod +x /opt/InterMumbleBot/run.sh
ENTRYPOINT ["/bin/sh", "-c", "/opt/InterMumbleBot/run.sh"]


