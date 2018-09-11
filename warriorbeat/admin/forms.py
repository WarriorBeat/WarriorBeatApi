# warriorbeat/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import Email, DataRequired


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])


class AddFeedForm(FlaskForm):
    id = StringField('Email')
    name = StringField('Name')
    photo = FileField('Cover Image')
    
