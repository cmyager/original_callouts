#!/bin/bash
cd /home/callouts/original_callouts/callouts
# source /home/callouts/spirit/.new/bin/activate
source /home/callouts/original_callouts/callouts/.venv/bin/activate
export PYTHONDONTWRITEBYTECODE=1
python -B callouts.py