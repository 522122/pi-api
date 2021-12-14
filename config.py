from datetime import timedelta

JWT_SECRET_KEY = 'x'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/main.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET = 'x'
EXPIRES_DELTA = timedelta(minutes=15)