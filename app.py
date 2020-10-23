import json, os

from flask import Flask, request, redirect, render_template, session, flash
from flask_login import current_user, logout_user
from forms import ChooseLevel, Level, Login, SignUp

from DAL.api import get_level, set_clock
from DAL.database import signup, login, is_username, get_user, get_games, loading, saving, any_saved, finishing
from models import db, data, connect_db, load_user, DataStore, User, SavedGame, PersonalBest


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecret7f75ht6ghdmcbc739')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///Sudoku')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.route('/')
def index():
    """Shows homepage"""

    return render_template('/index.html',user=data.user)

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up_user():
    """Shows form to sign-up user if not logged in and then redirects to /"""

    if data.user:
        return redirect('/')

    form = SignUp()

    if form.validate_on_submit():

        if is_username(form.username.data) == True:
            flash('Username already exists.')
            return redirect('/sign_up')

        signup(form.name.data,form.username.data,form.password.data)
        return redirect('/')
        
    else:
        return render_template('/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Shows form to login user if not logged in and then redirects to /"""

    if data.user:
        return redirect('/')

    form = Login()

    if form.validate_on_submit():

        if login(form.username.data,form.password.data) == True:
            return redirect('/')

        flash('Please check your login details and try again.')
        return redirect('/login')

    else:
        return render_template('/login.html', form=form)

@app.route('/logout')
def logout():
    """If not logged out, logs user out"""

    if not data.user:
        return redirect('/login')

    logout_user()
    data.user = None

    return redirect('/')

@app.route('/profile')
def show_profile():
    """Shows profile if logged in"""

    if not data.user:
        return redirect('/')

    usr = get_user(data.user)

    return render_template('/profile.html',usr=usr)


@app.route('/choose_level', methods=["GET", "POST"])
def game():
    """Shows form to play game and then redirects to /play_game"""

    form = ChooseLevel()

    if form.validate_on_submit():
            
        get_level(form.level.data)
        return redirect('/play_game')

    else:
        return render_template('/level.html', form=form)

@app.route('/play_game')
def play_game():
    """Loads selected game from either the api or saved game data"""

    if data.board == None:
        return redirect('/choose_level')

    set_clock(data.clock)

    return render_template('/sudoku.html', board=data.board, level=data.level, c=data.clock, clock1=data.clock1, 
                            clock2=data.clock2, clock3=data.clock3, user=data.user, solved=data.solved)

@app.route('/save_game', methods=["POST"])
def get_javascript_data():
    """Gets clock/board/solved/level from javascript to save a game if logged in"""
    
    request_data = json.loads(request.data)

    saving(request_data)

    return request_data

@app.route('/finish_game', methods=["POST"])
def finish_game():
  
    request_data = json.loads(request.data)

    finishing(request_data)

    return request_data

@app.route('/load', methods=['GET', 'POST'])
def load_game():
    """Shows form to load game if logged in and then redirects to /play_game"""
 
    if not data.user:
        return redirect('/login')

    if any_saved() == False:
        return redirect('/choose_level')

    form = Level()
    form.level.choices = any_saved()

    if form.validate_on_submit():

        loading(form.level.data.title())

        return redirect('/play_game')

    else:
        return render_template('/load.html',form=form)
