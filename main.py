from flask import Flask, jsonify, request, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from flask_cors import CORS
from datetime import timedelta

# custom imports
import config
from db import db, serialize_list
from functions import message, hash, now, required_params
from models.User import User
from models.Note import Note
from models.OTP import OTP

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
jwt = JWTManager(app)
db.init_app(app)

###################################### REQUESTS 
@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/initdb')
def init_db():
    try:
        db.create_all()
        return message('Tables created')
    except:
        return message('Error creating tables'), 500

###################################### REGISTER ######################################
@app.route('/register', methods=['POST'])
def register():
    if not required_params(['username', 'password'], request.form):
    #if 'username' not in request.form or 'password' not in request.form:
        return message('Invalid form data'), 400

    username = request.form['username']
    password = request.form['password']

    if len(username) < 3 or len(password) < 6:
        return message('Username or password too short'), 400

    user = User(request.form['username'], request.form['password'])
    try:
        db.session.add(user)
        db.session.commit()
        return message('User created'), 201
    except Exception as e:
        print('Error creating user', e)
        return message('Username already taken'), 500

###################################### LOGIN ######################################
@app.route('/login', methods=['POST'])
def login():
    if not required_params(['username', 'password'], request.form):
    #if 'username' not in request.form or 'password' not in request.form:
        return message('Invalid form data'), 400

    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return message('Wrong username or password'), 401

    if user.password != hash(password):
        user.failed_logins += 1
        return message('Wrong username or password'), 401


    user.failed_logins = 0
        
    return (message('Login successful', {
        **user.serialize(),
        'access': create_access_token(identity=user.public_id, expires_delta=config.EXPIRES_DELTA),
        'refresh': create_refresh_token(identity=user.serialize())
    }))

###################################### REFRESH ######################################
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    return message('Refresh token accepted', {
        **user,
        'access': create_access_token(identity=user['public_id'], expires_delta=config.EXPIRES_DELTA)
    })

###################################### NOTES ######################################
@app.route('/notes', methods=['GET', 'POST'])
@jwt_required
def notes():
    user_public_id = get_jwt_identity()

    if request.method == 'GET':
        notes = Note.query.filter_by(user_id=user_public_id, removed=False).all()
        return message('All notes', serialize_list(notes))

    elif request.method == 'POST':
        if not required_params(['title', 'body'], request.form):
        #if 'title' not in request.form or 'body' not in request.form:
            return message('Body and title are required'), 400

        try:
            note = Note(user_public_id, request.form['title'], request.form['body'])
            db.session.add(note)
            db.session.commit()
            return message('Note created', note.serialize()), 201
        except Exception as e:
            print('Error creating note', e)
            return message('Error creating note'), 500

###################################### NOTE ######################################
@app.route('/note/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def note(id):
    user_public_id = get_jwt_identity()

    if request.method == 'GET':
        note = Note.query.filter_by(id=id, user_id=user_public_id).first()
        return message('Success', note.serialize()) if note else (message('Not found'), 404)
    
    elif request.method == 'DELETE':
        note = Note.query.filter_by(id=id, user_id=user_public_id).first()
        if not note:
            return message('Not found'), 404

        try:
            db.session.delete(note)
            db.session.commit()
            return message('Success')
        except Exception as e:
            print('Error removing note', e)
            return message('Error removing note'), 500

    elif request.method == 'PUT':
        if not required_params(['title', 'body'], request.form):
        #if 'title' not in request.form or 'body' not in request.form:
            return message('Body and title are required'), 400

        note = Note.query.filter_by(id=id, user_id=user_public_id).first()
        
        if not note:
            return message('Not found'), 404

        note.body = request.form['body']
        note.title = request.form['title']
        note.mtime = now()
        db.session.commit()
        return message('Note modified', note.serialize())

###################################### OTP ######################################
@app.route('/otp', methods=['GET', 'PUT'])
@app.route('/otp/<id>', methods=['GET', 'DELETE'])
@jwt_required
def otp(id=None):
    user_public_id = get_jwt_identity()

    if request.method == 'GET':
        if not id:
            otps = OTP.query.filter_by(user_id=user_public_id).all()
            return message('All OTPs', serialize_list(otps))
        else:
            otp = OTP.query.filter_by(id=id, user_id=user_public_id).first()
            return message('OTP', otp.serialize())

    elif request.method == 'PUT':
        if not required_params(['secret', 'name', 'issuer'], request.form):
            return message('Secret and name are required'), 400

        try:
            otp = OTP(user_public_id, request.form['issuer'], request.form['name'], request.form['secret'])
            # will fail if invalid content ...
            otp.serialize()
            db.session.add(otp)
            db.session.commit()
            return message('OTP created', otp.serialize()), 201
        except Exception as e:
            print('Error creating OTP', e)
            return message('Error creating OTP'), 500

    elif request.method == 'DELETE':
        if not id:
            return message('Invalid ID'), 400

        otp = OTP.query.filter_by(id=id, user_id=user_public_id).first()
        if not otp:
            return message('Not found'), 404

        try:
            db.session.delete(otp)
            db.session.commit()
            return message('Success')
        except Exception as e:
            print('Error removing OTP', e)
            return message('Error removing OTP'), 500




if "__main__" == __name__:
    app.run(debug=True)


#####

# def now():
#     return int(datetime.utcnow().timestamp() * 1000)

# def hash(string):
#     return hashlib.sha256(f"{string}{SECRET}".encode()).hexdigest()

# def auth_required():
#     args = auth_parser.parse_args()
#     try:
#         return decode_token(args['x-auth-token'])['public_id']
#     except:
#         abort(401)


# def create_token(user):
#     token_data = {
#        'public_id': user.public_id,
#        'exp': now() + (60 * 10) * 1000
#     }
#     return jwt.encode(token_data, KEY, algorithm='HS256').decode()


# def decode_token(token):
#     return jwt.decode(token, KEY, algorithm='HS256')

# def create_refresh_token(user):
#     try:
#         token = Token(user.id)
#         db_session.add(token)
#         db_session.commit()
#         return token
#     except:
#         abort(500)

# def get_refresh_token(user):
#     token = db_session.query(Token).filter(Token.user_id == user.id).first()
#     return token if token else create_refresh_token(user)

# def get_auth_user_public_id():
#     args = auth_parser.parse_args()

# def get_user(username, password):
#     user = db_session.query(User).filter(User.username==username, User.password==hash(password)).first()
#     return user if user else abort(401)

# def create_user(user):
#     try:
#         db_session.add(user)
#         db_session.commit()
#     except:
#         abort(500)

# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()

# class Login(Resource):
#     login_parser = reqparse.RequestParser()
#     login_parser.add_argument('username', type=str, help='Username required', required=True)
#     login_parser.add_argument('password', type=str, help='Password required', required=True)
    
#     def post(self):
#         args = self.login_parser.parse_args()
#         user = get_user(args['username'], args['password'])
#         refresh_token = get_refresh_token(user)
#         token = create_token(user)
#         print(token)
#         print(decode_token(token))
#         return {
#             'refresh_token': refresh_token.token,
#             'token': token
#         }

# class Register(Resource):
#     register_parser = reqparse.RequestParser()
#     register_parser.add_argument('username', type=str, help='Username required', required=True)
#     register_parser.add_argument('password', type=str, help='Password required', required=True)

#     def post(self):
#         args = self.register_parser.parse_args()
#         user = User(args['username'], hash(args['password']))
#         create_user(user)
#         return user_schema.dump(user), 201

# class Notes(Resource):

#     def select_one(self, user_id, note_id):
#         note = db_session.query(Note).filter(Note.user_id==user_id, Note.id==note_id).first()
#         return note if note else abort(404)

#     def select_all(self, user_id):
#         return db_session.query(Note).filter(Note.user_id==user_id).all()

#     def get(self, note_id=None):
#         user_public_id = auth_required()
#         return self.select_one(user_public_id, note_id) if note_id else self.select_all(user_public_id)

# class Test(Resource):
#     def get(self):
#         public_id = auth_required()
#         print(public_id)
#         users = db_session.query(User).all()
#         return users_schema.dump(users)

# api.add_resource(Test, "/rest/test")
# api.add_resource(Register, "/rest/register")
# api.add_resource(Login, "/rest/login")
# api.add_resource(Notes, "/rest/notes", "/rest/notes/<note_id>")
