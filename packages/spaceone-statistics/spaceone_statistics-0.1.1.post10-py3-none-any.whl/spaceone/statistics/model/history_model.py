from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class History(MongoModel):
    topic = StringField(max_length=255)
    values = DictField()
    domain_id = StringField(max_length=255)
    created_at = DateTimeField(required=True)

    meta = {
        'updatable_fields': [],
        'exact_fields': [
            'domain_id'
        ],
        'ordering': [
            '-created_at'
        ],
        'indexes': [
            'topic',
            'domain_id',
            'created_at'
        ]
    }
