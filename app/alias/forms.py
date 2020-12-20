# app/api/forms.py

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from ..models import Alias


class NewAliasForm(FlaskForm):
    """
    Form to generate a new Alias
    """
    name = StringField('Name', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired(), Email()])
    destination = StringField('Destination', validators=[DataRequired(), Email()])
    submit = SubmitField('Add new Alias')

    def validate_source(self, field):
        domain = str(current_app.config['DOMAIN']).lower()
        if domain not in str(field.data).lower():
            raise ValidationError(f'Invalid source email. Use Keemail domain: {domain}')

        if Alias.query.filter_by(source=field.data).first():
            raise ValidationError('Source email is already in use.')

    def validate_destination(self, field):
        domain = str(current_app.config['DOMAIN']).lower()
        field_data = str(field.data).lower()
        if domain in field_data:
            raise ValidationError('Can not set destination to Keemail')
        if str(self.source.data).lower() == field_data:
            raise ValidationError('Can not set source = destination')