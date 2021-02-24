from wtforms import Form, StringField, validators, DateTimeField
from wtforms.widgets import TextArea


class CommentForm(Form):
    content = StringField('Treść', [
        validators.DataRequired()
    ], widget=TextArea())
    date = DateTimeField('Date')
