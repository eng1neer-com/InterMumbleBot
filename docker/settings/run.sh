#!/bin/bash

err=0

cp /data/settings.ini /opt/InterMumbleBot/settings.ini
if [ $? -ne 0 ];
then
	echo "WARNING: settings.ini file was not found. Creating one based on the settings_default.ini file..."
	cp /opt/InterMumbleBot/settings_default.ini /data/settings.ini && \
	cp /data/settings.ini /opt/InterMumbleBot/settings.ini
	if [ $? -ne 0 ];
	then
		echo "fatal error"
		err=1
	fi
fi

cp /data/key.pem /opt/InterMumbleBot/key.pem && \
cp /data/cert.pem /opt/InterMumbleBot/cert.pem

if [ $? -ne 0 ];
then
	echo "WARNING: No cert/key files found. Creating new key/cert pair..."
	rm -f key.pem
	rm -f cert.pem
	cd /data
	openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem -subj "/C=xx/ST=xx/L=xx/O=xx/OU=xx/CN=intermumblebot" && \
	cp /data/key.pem /opt/InterMumbleBot/key.pem && \
	cp /data/cert.pem /opt/InterMumbleBot/cert.pem
	if [ $? -ne 0 ];
	then
		echo "fatal error"
		err=1
	fi
fi

if [ $err -ne 1 ];
then
	python3 /opt/InterMumbleBot/src/InterMumbleBot.py
else
	echo "Bot was not started due to setup errors"
fi


