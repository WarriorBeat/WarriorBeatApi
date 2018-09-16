# warriorbeat/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DateField
from wtforms.validators import Email, DataRequired


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])


class AddFeedForm(FlaskForm):
    id = StringField('Email')
    title = StringField('Title')
    body = StringField('Body')
    author = StringField('Author')
    cover_img = FileField('Cover Image')
