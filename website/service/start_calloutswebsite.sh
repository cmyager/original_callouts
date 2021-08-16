#!/bin/bash
cd /home/callouts/website
source /home/callouts/website/.env/bin/activate
export PYTHONDONTWRITEBYTECODE=1
export OAUTHLIB_INSECURE_TRANSPORT=1
.env/bin/hypercorn -w 3 flask_app:app