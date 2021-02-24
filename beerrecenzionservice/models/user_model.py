from mongoengine import Document, StringField, BooleanField


class User(Document):
    username = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    group = BooleanField()

    def __unicode__(self):
        return self.username