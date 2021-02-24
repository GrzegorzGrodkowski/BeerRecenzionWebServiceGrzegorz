from flask_wtf.file import FileRequired
from wtforms import Form, StringField, validators, SelectField, FileField
from wtforms.widgets import TextArea


class BeerForm(Form):
    name = StringField('Nazwa', [
        validators.DataRequired()
    ])
    category = SelectField('Rodzaj')
    description = StringField('Opis', [
        validators.DataRequired()
    ], widget=TextArea())
    photo = FileField('Zdjęcie')