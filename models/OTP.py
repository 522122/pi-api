from db import db
import pyotp
from datetime import datetime

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    issuer = db.Column(db.String)
    name = db.Column(db.String)
    secret = db.Column(db.String)

    def __init__(self, user_id, issuer, name, secret):
        self.user_id = user_id
        self.issuer = issuer
        self.name = name
        self.secret = secret

    def serialize(self):
        totp = pyotp.TOTP(self.secret)
        remaining = totp.interval - datetime.now().timestamp() % totp.interval
        return {
            'id': self.id,
            'issuer': self.issuer,
            'name': self.name,
            'now': totp.now(),
            'remaining': int(remaining),
            'interval': totp.interval
        }