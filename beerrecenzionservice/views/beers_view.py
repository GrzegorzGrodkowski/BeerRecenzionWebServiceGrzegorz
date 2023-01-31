import os
from datetime import datetime

from flask import (Blueprint, flash, g, redirect, render_template, request, sessions, url_for)
from flask_login import current_user
from flask_uploads import UploadSet, IMAGES

from werkzeug.exceptions import abort


from beerrecenzionservice.forms.beer_form import BeerForm
from beerrecenzionservice.forms.comment_form import CommentForm

from beerrecenzionservice.models.beer_model import Comment, Beer
from beerrecenzionservice.models.beercategory_model import BeerCategory

blueprint = Blueprint('beers', __name__, url_prefix='/beer')
photos = UploadSet('photos', IMAGES)


@blueprint.route('/<beer_id>', methods=('GET', 'POST'))
def beer(beer_id):
    form = CommentForm(request.form)
    selected_beer = None
    try:
        selected_beer = Beer.objects(id=beer_id).first()
    except:
        abort(404)

    if request.method == 'POST' and form.validate():
        if not current_user.is_authenticated:
            abort(401)

        user = current_user.user
        comment = Comment(content=form.content.data,
                          date=datetime.now().isoformat(' ', 'seconds'),
                          user=user)
        if selected_beer is not None:
            selected_beer.comments.append(comment)
            selected_beer.save()

        flash('Thanks for added comment')

    return render_template('beer.html', form=form, beer=selected_beer)


@blueprint.route('/search/<search_text>', methods=('GET', 'POST'))
def search_beers(search_text):
    beers = None
    try:
        beers = Beer.objects(name__icontains=search_text)
    except:
        abort(404)

    return render_template('category.html', beers=beers, category_name="Wyniki wyszukiwania: ", searching=True)


@blueprint.route('/add', methods=('GET', 'POST'))
def add_beer():
    form = BeerForm(request.form)
    categories = None
    try:
        categories = BeerCategory.objects()
    except:
        abort(404)

    form.category.choices = categories

    if request.method == 'POST' and form.validate():
        if not current_user.is_authenticated:
            abort(401)

        category_name = form.category.data
        category = BeerCategory.objects(name=category_name).first()
        user = current_user.user
        photo_file = request.files[form.photo.name]
        uploaded = None
        if len(photo_file.filename) > 0:
            storage = firebase.storage()
            filename, extension = os.path.splitext(photo_file.filename)
            uploaded = storage.child(f"images/{filename}-{datetime.timestamp(datetime.now())}{extension}").put(photo_file)

        beer = Beer(name=form.name.data,
                    category=category,
                    description=form.description.data,
                    user=user,
                    photo=uploaded)
        beer.save()
        flash('Thanks for added beer')
        return redirect(url_for('beers.beer', beer_id=beer.id))

    return render_template('add_beer.html', form=form)
