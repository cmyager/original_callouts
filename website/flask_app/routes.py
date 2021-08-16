from quart import render_template, request, redirect, url_for, flash, g
from quart_discord import DiscordOAuth2Session, requires_authorization, exceptions
import os
from flask_app import app
from flask_app.forms import EventForm
from discord.ext import ipc

discord = DiscordOAuth2Session(app)
ipc_client = ipc.Client(secret_key="iDunno")

########################################################################################################################
@app.before_request
async def check_discrd_ipc():
    try:
        await ipc_client.request("ping")
    except:
        await ipc_client.init_sock()

########################################################################################################################
@app.route("/")
async def index():
    return await render("index.html")

########################################################################################################################
@app.route("/event", methods=['GET', 'POST'])
@requires_authorization
async def event():
    if not hasattr(g, 'guilds'):
        g.guilds = await ipc_client.request("get_guilds_ipc", user_id=(await discord.fetch_user()).id)

    form = EventForm(guilds=g.guilds)

    if form.validate_on_submit():
        create_event_response = await process_event(form.data)
        if create_event_response["status"] is True:
            await flash('Your event has been created!', 'success')
            await ipc_client.request("reload_events_ipc")
        else:
            await flash(f'There was an error creating your event: {create_event_response["status"]}', 'danger')
        return redirect(url_for('event'))

    return await render("event.html", guilds=g.guilds, form=form)

########################################################################################################################
async def process_event(data):
    EVENT = {}
    EVENT["author_id"] = (await discord.fetch_user()).id
    EVENT["event_title"] = data["title"]
    EVENT["start_time"] = f"{data['start_date'].strftime('%Y-%m-%d')} {data['start_time'].strftime('%I:%M %p')}"
    EVENT["guild_id"] = g.guilds[0]["id"]
    EVENT["description"] = data["description"]
    EVENT["max_members"] = data["max_members"]
    EVENT["rsvp"] = [g.guilds[0]["users"][i]["id"] for i in g.guilds[0]["users"].keys() if i in data["members"]]

    return await ipc_client.request("create_event_ipc", event=EVENT)

########################################################################################################################
## Base functions
########################################################################################################################

########################################################################################################################
@app.errorhandler(exceptions.Unauthorized)
async def unauthorized_error_handler(error):
    return redirect(url_for(".index"))

########################################################################################################################
async def render(page, **kwargs):
    return await render_template(page, discord=discord, **kwargs)

########################################################################################################################
@app.route("/login/")
async def login():
    return await discord.create_session(scope=["identify"])

########################################################################################################################
@app.route("/callback/")
async def callback():
    try:
        data = await discord.callback()
        user = await discord.fetch_user()
        if await ipc_client.request("user_in_guild_ipc", user_id=user.id) is not True:
            raise Exception()
        await flash("Authentication Successful", "success")
        redirect_to = data.get("redirect", "/event")
    except:
        await flash('Authentication Failed. Are you in the clan?', 'danger')
        redirect_to = url_for(".index")
    finally:
        return redirect(redirect_to)

########################################################################################################################
@app.route("/secret/")
@requires_authorization
async def secret():
    return os.urandom(16)

########################################################################################################################
@app.route("/logout/")
@requires_authorization
async def logout():
    discord.revoke()
    g.pop("guilds", None)
    await flash('Logged out!', 'success')
    return redirect(url_for(".index"))
