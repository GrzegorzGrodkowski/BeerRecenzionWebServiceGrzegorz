from mongoengine import Document, StringField


class BeerCategory(Document):
    name = StringField(required=True)

    def __unicode__(self):
        return self.name