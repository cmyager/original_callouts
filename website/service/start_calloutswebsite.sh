#!/bin/bash
cd /home/callouts/original_callouts/website
source /home/callouts/original_callouts/website/.env/bin/activate
export PYTHONDONTWRITEBYTECODE=1
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_RUN_PORT=5000
.env/bin/hypercorn -w 3 flask_app:app