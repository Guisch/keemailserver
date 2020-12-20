# app/api/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GenerateApiKeyForm(FlaskForm):
    """
    Form to generate a new API Key
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Generate')
