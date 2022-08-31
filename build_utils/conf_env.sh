#!/bin/bash
ENV_PY=$1
ENV_NAME=py$(echo "$ENV_PY" | sed "s/\.//")
sudo apt update --fix-missing
sudo apt upgrade
sudo apt install -y build-essential libssl-dev libffi-dev python$ENV_PY-dev python$ENV_PY-distutils
sudo apt install -y python-pip
python3 -m pip install virtualenv
virtualenv $ENV_NAME --python=python$ENV_PY
source $ENV_NAME/bin/activate
pip install build wheel pytest