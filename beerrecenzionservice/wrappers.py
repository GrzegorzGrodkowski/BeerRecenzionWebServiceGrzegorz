from flask_login import UserMixin


class UserWrapper(UserMixin):
    user = None

    def __init__(self, user):
        self.user = user

    def get_id(self):
        return str(self.user.id)
