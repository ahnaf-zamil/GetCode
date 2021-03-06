from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from getcode import db
from getcode import app
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Model for user accounts."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         nullable=False,
                         unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    google_login = db.Column(db.Integer,
                             unique=False,
                             nullable=False)
    bio = db.Column(db.String(), primary_key=False,
                    unique=False, nullable=False)

    user_id=db.Column(db.String,primary_key=False,unique=True)

    def get_reset_token(self, expires_sec=1800):
        # defualt is 30min
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verifiy_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def serialize(self):
        return{
            "id": self.id,
            "username": self.username, 
            "email": self.email, 
            "bio": self.bio
        }


class Snippet(db.Model):
    __tablename__ = 'code_snippets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String(40),
                      unique=False,
                      nullable=False)
    code = db.Column(db.String, unique=False, nullable=False)
    created_date = db.Column(db.String, nullable=False, unique=False)
    likes = db.Column(db.Integer, primary_key=False,
                      nullable=False, unique=False)
    liked_users = db.Column(db.String, nullable=True, unique=False)
    comments = db.Column(db.String, nullable=True, unique=False)
    tags = db.Column(db.String, nullable=True, unique=False)
    visibility = db.Column(db.Integer, nullable=True)
    created_by_username = db.Column(db.String,
                                    nullable=False,
                                    unique=False)

    snippet_id=db.Column(db.String,primary_key=False,unique=True)

    @property
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "created_by_username": self.created_by_username,
            "created_date": self.created_date,
            "tags": self.tags,
            "visibility": self.visibility
        }


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    email_of_commenter = db.Column(db.String(40),
                                   unique=False,
                                   nullable=False)
    created_date = db.Column(db.String, nullable=False, unique=False)
    comment = db.Column(db.String, nullable=False, unique=False)
    post_name = db.Column(db.String, nullable=False, unique=False)


db.init_app(app)
