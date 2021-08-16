import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true" # !! Only in development environment.

from flask_app import *

if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)
