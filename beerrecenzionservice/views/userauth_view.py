from flask import (Blueprint, flash, g, redirect, render_template, request, sessions, url_for)

from flask_login import login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

from beerrecenzionservice.forms.registration_form import RegistrationForm
from beerrecenzionservice.forms.login_form import LoginForm
from beerrecenzionservice.models.user_model import User
from beerrecenzionservice.wrappers import UserWrapper

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        username_exists = User.objects(username=form.username.data).first()

        if not username_exists:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(f'{form.username.data}:{form.password.data}'))
            user.save()
            flash('Thanks for registering')
            return redirect(url_for('auth.login'))
        else:
            form.username.errors.append("Użytkownik o takiej nazwie już istnieje.")
    return render_template('auth/register.html', form=form)


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.objects(username=form.username.data).first()
        if user and check_password_hash(user.password, f'{form.username.data}:{form.password.data}'):
            login_user(UserWrapper(user))
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            form.username.errors.append("Niepoprawne dane logowania.")

    return render_template('auth/login.html', form=form)

@blueprint.route('/logout', methods=('GET',))
def logout():
    logout_user()
    return redirect('login')