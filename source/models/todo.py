from mongoengine import *
from mongoengine import signals
from datetime import datetime

class Todo(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    done = BooleanField(required=False, default=False)
    user = ObjectIdField()
    created_at = DateTimeField(required=False, default=datetime.now())
    updated_at = DateTimeField(required=False, default=datetime.now())

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """
        Executes before save the user
        """
        document.updated_at = datetime.now()

signals.pre_save.connect(Todo.pre_save, sender=Todo)