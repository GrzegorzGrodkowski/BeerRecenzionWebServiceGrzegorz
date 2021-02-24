from bson import ObjectId
from flask import (Blueprint, flash, g, redirect, render_template, request, sessions, url_for, Response, jsonify)

from flask_login import login_user, logout_user, current_user
from flask_uploads import UploadSet, IMAGES
from werkzeug.exceptions import abort

from beerrecenzionservice.models.beer_model import Beer
from beerrecenzionservice.forms.search_form import SearchForm

blueprint = Blueprint('main', __name__, url_prefix='/')

@blueprint.route('', methods=('GET', 'POST'))
def index():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('beers.search_beers', search_text=form.search_text.data))
    beers = Beer.objects[:5].order_by('-comments.date')
    return render_template('index.html', beers=beers, form=form)


@blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        strin = f"Photo saved. {photos.url(filename)}"
        return jsonify(saved=strin)
    return render_template('upload.html')