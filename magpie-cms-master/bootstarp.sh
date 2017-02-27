#!/bin/bash
# 08.11.2014
# Creates the minimal environment needed to start the local installation
# procedure.
# Should only be run on localhost for setting up your local dev environment.
# Assumes an Ubuntu/Debian environment.
set -e
sudo apt-get update
sudo apt-get install python-dev
sudo apt-get install build-essential

# Ensure our system's global pip install is up to date.
wget http://peak.telecommunity.com/dist/ez_setup.py -O /tmp/ez_setup.py
sudo python2.7 /tmp/ez_setup.py -U setuptools
sudo easy_install -U pip
sudo pip2.7 install --upgrade setuptools
sudo pip2.7 install --upgrade distribute
sudo pip2.7 install --upgrade virtualenv

# Create the stub Python virtual environment.
virtualenv -p /usr/bin/python2.7 --no-site-packages .env

#Install all required package for project from pip-requirement.txt
.env/bin/pip install -r pip-requirements.txt

echo "Bootstrap complete!"

