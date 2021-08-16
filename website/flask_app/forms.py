from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.fields.html5 import DateField, IntegerField, TimeField
from wtforms.validators import DataRequired, Optional, NumberRange, ValidationError
from datetime import datetime, timedelta
import pytz

########################################################################################################################
CENTRAL_TIMEZONE = pytz.timezone('US/Central')

########################################################################################################################
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description (Optional)', validators=[Optional()])
    max_members = IntegerField("Max Attendees (Optional)", validators=[Optional(), NumberRange(min=1, max=6)])
    start_date = DateField('Event Date', validators=[DataRequired()])
    start_time = TimeField("Event Time in US/Central", validators=[DataRequired()])

    members = SelectMultipleField("Invite Members (Optional)",
                                  validators=[Optional()])
    submit = SubmitField('Create Event')

    ####################################################################################################################
    def validate_members(self, data):
        choices = data.data
        bad_choices = [i for i in choices if i not in data.users.keys()]
        valid = True
        if len(bad_choices) != 0:
            valid = "Invalid Invitee"
        elif self.data['max_members'] is not None and len(choices) > self.data['max_members']:
            valid = "Too Many Invitees"
        if valid is not True:
            raise ValidationError(valid)
    
    ####################################################################################################################
    def validate_start_date(self, data):
        if data.data < datetime.now(CENTRAL_TIMEZONE).date():
            raise ValidationError("Date cannot be in the past")

    ####################################################################################################################
    # def validate_start_time(self, data):
    # if data.data < (datetime.now(CENTRAL_TIMEZONE) - timedelta(minutes=1)).time():
    # raise ValidationError("Time cannot be in the past")

    ####################################################################################################################
    def get_current_date_cst(self):
        return datetime.now(CENTRAL_TIMEZONE).strftime("%m/%d/%y")

    ####################################################################################################################
    def get_current_time_cst(self):
        return datetime.now(CENTRAL_TIMEZONE).strftime("%I:%M %p")
    
    ####################################################################################################################
    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

        # Populate Members
        self.members.users = kwargs['guilds'][0]['users']
        user_keys = list(self.members.users.keys())
        user_keys.sort()
        self.members.choices = [(user, user) for user in user_keys]
