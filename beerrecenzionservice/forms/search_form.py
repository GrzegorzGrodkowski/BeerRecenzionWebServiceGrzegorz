from wtforms import Form, StringField, validators


class SearchForm(Form):
    search_text = StringField('Podaj frazę', [
        validators.DataRequired()
    ])