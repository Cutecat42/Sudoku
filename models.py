from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()


def connect_db(app):
    """Connect to database and start Flask-Login."""

    db.app = app
    db.init_app(app)
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    total_played = db.Column(db.Integer, nullable=False, default=0)

    games = db.relationship('SavedGame', backref='user')

class SavedGame(db.Model):

    __tablename__ = "saved_games"

    level = db.Column(db.Text, nullable=False, primary_key=True)
    unsolved = db.Column(db.String, nullable=False)
    solved = db.Column(db.String, nullable=False)
    time = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)

class PersonalBest(db.Model):

    __tablename__ = "personal_bests"

    level = db.Column(db.Text, nullable=False, primary_key=True)
    time = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)