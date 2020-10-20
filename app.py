from flask import Flask, request, redirect, render_template, session, flash
from flask_login import login_user, current_user, logout_user
from models import db, connect_db, load_user, User, SavedGame, PersonalBest
from forms import ChooseLevel, Level, Login, SignUp
from werkzeug.security import generate_password_hash, check_password_hash
import requests, json, os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecret7f75ht6ghdmcbc739')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Sudoku'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.route('/')
def index():
    """Shows homepage"""

    user = session.get('logged_in_user', None)

    return render_template('/index.html',user=user)

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up_user():
    """Shows form to sign-up user if not logged in and then redirects to /"""

    user = session.get('logged_in_user', None)

    if user:

        return redirect('/')

    form = SignUp()

    if form.validate_on_submit():

        name = form.name.data
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists.')
            return redirect('/sign_up')

        new_user = User(name=name,username=username,password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        session['logged_in_user'] = new_user.id

        return redirect('/')
        
    else:
        return render_template('/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Shows form to login user if not logged in and then redirects to /"""

    user = session.get('logged_in_user', None)

    if user:

        return redirect('/')

    form = Login()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user: 
            if check_password_hash(user.password, password):
                login_user(user)
                session['logged_in_user'] = user.id
                return redirect('/')

        flash('Please check your login details and try again.')
        return redirect('/login')


    else:
        return render_template('/login.html', form=form)

@app.route('/logout')
def logout():
    """If not logged out, logs user out"""

    user = session.get('logged_in_user', None)

    if not user:

        return redirect('/login')

    logout_user()
    session.pop('logged_in_user')

    return redirect('/')

@app.route('/profile')
def show_profile():
    """Shows profile if logged in"""

    user = session.get('logged_in_user', None)

    if not user:
    
        return redirect('/login')

    usr = User.query.filter_by(id=user).first()

    return render_template('/profile.html',usr=usr)


@app.route('/choose_level', methods=["GET", "POST"])
def game():
    """Shows form to play game and then redirects to /play_game"""

    form = ChooseLevel()

    if form.validate_on_submit():
        clock = session.get('clock', None)
        if clock:
            session.pop('clock')

        if form.level.data == "e":
            r = requests.get('https://sudoku.com/api/getLevel/easy').json()
            session['board'] = board=r['desc'][0]
            session['solved']= board=r['desc'][1]
            session['level'] = "Easy"
            return redirect('/play_game')
        if form.level.data  == "m":
            r = requests.get('https://sudoku.com/api/getLevel/medium').json()
            session['board'] = board=r['desc'][0]
            session['solved']= board=r['desc'][1]
            session['level'] = "Medium"
            return redirect('/play_game')
        if form.level.data == "h":
            r = requests.get('https://sudoku.com/api/getLevel/hard').json()
            session['board'] = board=r['desc'][0]
            session['solved']= board=r['desc'][1]
            session['level'] = "Hard"
            return redirect('/play_game')

    else:
        return render_template('/level.html', form=form)

@app.route('/play_game')
def play_game():
    """Loads selected game from either the api or saved game data"""

    user = session.get('logged_in_user', None)
    board = session.get('board', None)
    solved = session.get('solved', None)
    level = session.get('level', None)
    clock = session.get('clock', None)
    c = clock

    if clock == None:
        c = "00:00:00"
    if len(c) == 5:
        if clock == "00:00":
            c = "00:00:00"
        else:
            c = "00:" + clock
    clock_cut1 = slice(0,2)
    clock_cut2 = slice(3,5)
    clock_cut3 = slice(6,8)
    clock1 = c[clock_cut1]
    clock2 = c[clock_cut2]
    clock3 = c[clock_cut3]

    return render_template('/sudoku.html', board=board, level=level, c=clock, clock1=clock1, 
                            clock2=clock2, clock3=clock3, user=user, solved=solved)

@app.route('/save_game', methods=["POST"])
def get_javascript_data():
    """Gets clock/board/solved/level from javascript to save a game if logged in"""
    x = json.loads(request.data)

    board = x['board']
    solved = x['solved']
    level = x['level']
    clock = x['clock']

    print(board,solved,level,clock)

    user = session.get('logged_in_user', None)

    usr = SavedGame.query.get((level,user))

    if usr != None:
        SavedGame.query.get((level,user)).time = clock
        SavedGame.query.get((level,user)).unsolved = board
        SavedGame.query.get((level,user)).solved = solved

        db.session.add(usr)
        db.session.commit()
    else:
        new = SavedGame(level=level,unsolved=board,solved=solved,time=clock,user_id=user)
        db.session.add(new)
        db.session.commit()

    return x

@app.route('/finish_game', methods=["POST"])
def finish_game():
  
    x = json.loads(request.data)

    board = x['board']
    solved = x['solved']
    level = x['level']
    clock = x['clock']

    user = session.get('logged_in_user', None)

    usr = PersonalBest.query.get((level,user))

    saved = SavedGame.query.get((level,user))
    finished = User.query.filter_by(id=user).first()
    print(finished.name)

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

    return x

@app.route('/load', methods=['GET', 'POST'])
def load_game():
    """Shows form to load game if logged in and then redirects to /play_game"""
 
    user = session.get('logged_in_user', None)

    if not user:

        return redirect('/login')

    usr = User.query.get(user)
    level = db.session.query(SavedGame).filter(SavedGame.user_id == user).all()
    level_list=[(i.level.lower(), i.level) for i in level]

    if not level_list:
        return redirect('/choose_level')

    form = Level()
    form.level.choices = level_list

    if form.validate_on_submit():
        
        usr = SavedGame.query.get((form.level.data.title(),user))
        session['board'] = usr.unsolved
        session['solved']= usr.solved
        session['level'] = usr.level
        session['clock'] = usr.time

        return redirect('/play_game')

    else:
        return render_template('/load.html',form=form)
