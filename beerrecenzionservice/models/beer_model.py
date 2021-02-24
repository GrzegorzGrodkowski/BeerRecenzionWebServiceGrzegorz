from mongoengine import EmbeddedDocument, StringField, DateTimeField, ReferenceField, Document, ListField, \
    EmbeddedDocumentField, URLField

from beerrecenzionservice.models.beercategory_model import BeerCategory
from beerrecenzionservice.models.user_model import User


class Comment(EmbeddedDocument):
    content = StringField(required=True)
    date = DateTimeField(required=True)
    user = ReferenceField(User)

    def __unicode__(self):
        return self.content


class Beer(Document):
    name = StringField(required=True)
    category = ReferenceField(BeerCategory)
    description = StringField(required=False)
    comments = ListField(EmbeddedDocumentField(Comment), default=[])
    photo = URLField()
    user = ReferenceField(User)

    def __unicode__(self):
        return self.name