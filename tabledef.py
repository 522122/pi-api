

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    public_id = Column(Integer, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    ctime = Column(Integer)
    admin = Column(Boolean)

    def __init__(self, username, password):
        self.public_id = str(uuid4())
        self.username = username
        self.password = password
        self.ctime = int(datetime.utcnow().timestamp())
        self.admin = False

class UserSchema(Schema):
    public_id = fields.Str()
    username = fields.Str()

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.public_id'))
    token = Column(String)
    ctime = Column(Integer)
    user = relationship('User')

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = str(uuid4())
        self.ctime = int(datetime.utcnow().timestamp())

class TokenSchema(Schema):
    token = fields.Str()

token_schema = TokenSchema()
tokenss_schema = TokenSchema(many=True)

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.public_id'))
    title = Column(String)
    text = Column(String)
    ctime = Column(Integer)
    mtime = Column(Integer)
    user = relationship('User')

    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.ctime = int(datetime.utcnow().timestamp())
        self.mtime = int(datetime.utcnow().timestamp())

class NoteSchema(Schema):
    title = fields.Str()
    text = fields.Str()
    ctime = fields.Date()
    mtime = fields.Date()

note_schema = NoteSchema()
notess_schema = NoteSchema(many=True)


Base.metadata.create_all(engine)