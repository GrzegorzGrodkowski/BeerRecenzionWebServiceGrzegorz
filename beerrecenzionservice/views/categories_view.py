from flask import Blueprint, render_template
from werkzeug.exceptions import abort

from beerrecenzionservice.models.beer_model import Beer
from beerrecenzionservice.models.beercategory_model import BeerCategory

blueprint = Blueprint('categories', __name__, url_prefix='/categories')

@blueprint.route('/', methods=('GET', 'POST'))
def categories():
    categories = BeerCategory.objects()
    return render_template('categories.html', categories=categories)


@blueprint.route('/<category_id>', methods=('GET', 'POST'))
def beers(category_id):
    beers = None
    try:
        category = BeerCategory.objects(id=category_id).first()
        beers = Beer.objects(category=category)
    except:
        abort(404)

    return render_template('category.html', beers=beers, category_name=category.name)
