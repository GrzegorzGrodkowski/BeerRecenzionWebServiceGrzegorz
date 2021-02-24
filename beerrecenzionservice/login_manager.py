from flask_login import LoginManager
from beerrecenzionservice.models.user_model import User
from beerrecenzionservice.wrappers import UserWrapper

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserWrapper(User.objects(id=user_id).first())
