from db import db
from functions import now, hash
from uuid import uuid4

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    ctime = db.Column(db.Integer)
    admin = db.Column(db.Boolean)
    failed_logins = db.Column(db.Integer)

    def __init__(self, username, password):
        self.public_id = str(uuid4())
        self.username = username
        self.password = hash(password)
        self.ctime = now()
        self.admin = False
        self.failed_logins = 0

    def serialize(self):
        return {
            'public_id': self.public_id,
            'username': self.username,
            'ctime': self.ctime
        }