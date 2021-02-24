from wtforms import Form, StringField, validators, PasswordField, BooleanField


class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
    remember_me = BooleanField('Remember me')