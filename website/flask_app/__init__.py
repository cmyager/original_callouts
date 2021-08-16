import quart.flask_patch
from quart import Quart
import json

app = Quart(__name__)

with open('config.json') as config_file:
  config = json.load(config_file)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config["DISCORD_CLIENT_ID"] = config.get('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = config.get('DISCORD_CLIENT_SECRET')
app.config["DISCORD_BOT_TOKEN"] = config.get('DISCORD_BOT_TOKEN')
app.config["DISCORD_REDIRECT_URI"] = config.get('DISCORD_REDIRECT_URI')

from flask_app import routes
