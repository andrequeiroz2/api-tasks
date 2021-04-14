from tasks.database import db


class Tasks(db.Document):
    email = db.EmailField(required=True, unique=True)
    tasks = db.ListField()