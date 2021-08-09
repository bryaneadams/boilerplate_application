from .model import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    DateTimeField,
    IntegerField,
    FloatField,
    SelectField,
    PasswordField,
    BooleanField,
    SelectMultipleField,
    validators
)

from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

import mgrs

class BoilerplateForm(FlaskForm):

    statement = TextAreaField("Enter Text")
    submit = SubmitField("Submit Form")
