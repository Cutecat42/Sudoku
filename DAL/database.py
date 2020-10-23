from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from DAL.api import requesting
from models import db, data, connect_db, load_user, User, SavedGame, PersonalBest

def signup(name, username, password):

    name = name
    username = username
    password = password

    new_user = User(name=name,username=username,password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    data.user = new_user.id

    return new_user.id

def login(username,password):

    if is_username(username) == True:

        user = User.query.filter_by(username=username).first()

        if check_password_hash(user.password, password):
            login_user(user)
            data.user = user.id
            return True

    return False 

def is_username(username):

    user = User.query.filter_by(username=username).first()
    if user:
        return True

    return False

def get_user(user):

    return User.query.filter_by(id=user).first()

def get_games(request):

    level = requesting(request)[2]
    user = data.user

    return SavedGame.query.get((level,user))

def loading(level):

    usr = SavedGame.query.get((level,data.user))
    data.board = usr.unsolved
    data.solved = usr.solved
    data.level = usr.level
    data.clock = usr.time

    return usr

def saving(request):
    
    saved = get_games(request)

    board = requesting(request)[0]
    solved = requesting(request)[1]
    level = requesting(request)[2]
    clock = requesting(request)[3]

    user = data.user

    if saved != None:

        saved.time = clock
        saved.unsolved = board
        saved.solved = solved

        db.session.add(saved)
        db.session.commit()

        return saved

    else:

        new = SavedGame(level=level,unsolved=board,solved=solved,time=clock,user_id=user)
        db.session.add(new)
        db.session.commit()

        return saved

def any_saved():

    user = get_user(data.user)

    level = db.session.query(SavedGame).filter(SavedGame.user_id == user.id).all()
    level_list=[(i.level.lower(), i.level) for i in level]

    if not level_list:
        return False

    return level_list

def finishing(request):

    saved = get_games(request)

    board = requesting(request)[0]
    level = requesting(request)[2]
    clock = requesting(request)[3]

    user = data.user
    usr = PersonalBest.query.get((level,user))

    finished = User.query.filter_by(id=user).first()

    if user:
        finished.total_played += 1
        db.session.add(finished)
        db.session.commit()

        if saved.solved == str(board):
            db.session.delete(saved)
            db.session.commit()

        if usr != None:
            if usr.time > clock:
                PersonalBest.query.get((level,user)).time = clock
                PersonalBest.query.get((level,user)).level = level

                db.session.add(usr)
                db.session.commit()
        else:
                new = PersonalBest(level=level,time=clock,user_id=user)

                db.session.add(new)
                db.session.commit()

    return saved