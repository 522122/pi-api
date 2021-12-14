from db import db
from functions import now

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    title = db.Column(db.String)
    body = db.Column(db.String)
    mtime = db.Column(db.Integer)
    ctime = db.Column(db.Integer)
    removed = db.Column(db.Boolean)

    def __init__(self, user_id, title, body):
        self.user_id = user_id
        self.title = title
        self.body = body
        self.mtime = now()
        self.ctime = now()
        self.removed = False

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'mtime': self.mtime,
            'ctime': self.ctime,
            'removed': self.removed
        }