from base64 import b64encode

from flask import Flask, url_for
import flask_fs as fs
import flask_admin as admin
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import rules
from flask_bootstrap import Bootstrap
from flask_login import current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import redirect

from . import db
from beerrecenzionservice.views import main_view, categories_view, beers_view, userauth_view
from .login_manager import login_manager

from .models.user_model import User
from .models.beer_model import Beer, Comment
from .models.beercategory_model import BeerCategory

import os.path as op

class CategoryBeerView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user.group

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))



class BeerView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user.group

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))

    form_subdocuments = {
        'comments': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the end of the form
                    'form_rules': ('content', 'date', 'user', rules.HTML('<hr>')),
                    }
                }
            },
    }

class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user.group

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('auth.login'))


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    fs.init_app(app)
    app.config.from_object('config')

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    db.initialize_db(app)

    login_manager.init_app(app)
    app.register_blueprint(userauth_view.blueprint)
    app.register_blueprint(categories_view.blueprint)
    app.register_blueprint(beers_view.blueprint)
    app.register_blueprint(main_view.blueprint)

    configure_uploads(app, beers_view.photos)

    admin_panel = Admin(app)

    admin_panel.add_view(MyModelView(User))
    admin_panel.add_view(CategoryBeerView(BeerCategory))
    admin_panel.add_view(BeerView(Beer))

    Bootstrap(app)
    return app
