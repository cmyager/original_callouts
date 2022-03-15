#!/bin/bash
# call from sub directories "../setup.sh"
python3.8 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
