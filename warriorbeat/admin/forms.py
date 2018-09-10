# warriorbeat/admin/forms.py

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Email, DataRequired

class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    
class AddFeedForm(Form):
    id = StringField('Email')
    name = StringField('Name')