from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def serialize_list(collection):
    return list(map(lambda item: item.serialize(), collection))
