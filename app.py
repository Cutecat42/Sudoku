import json, os

from flask import Flask, request, redirect, render_template, session, flash, Markup
from flask_login import current_user, logout_user
from forms import ChooseLevel, Level, Login, SignUp

from DAL.api import get_level, set_clock
from DAL.database import signup, login, is_username, get_user, edit_user, get_games, loading, saving, any_saved, finishing, ending, best_times, global_best
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

        if is_username(form.username.data) == True:
            flash(Markup('Username already exists. Go to <a href="/login" class="alert-link">login</a> page.'))
            return redirect('/sign_up')

        signup(form.name.data,form.username.data,form.password.data)
        session['logged_in_user'] = data.user
        data.board = None
        return redirect('/')
        
    else:
        return render_template('/signup.html', form=form,user=user)


@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Shows form to login user if not logged in and then redirects to /"""

    user = session.get('logged_in_user', None)

    if user:
        return redirect('/')

    form = Login()

    if form.validate_on_submit():

        if login(form.username.data,form.password.data) == True:
            session['logged_in_user'] = data.user
            data.board = None
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
    data.user = None
    data.board = None
    session.pop('logged_in_user')

    return redirect('/')

@app.route('/profile')
def show_profile():
    """Shows profile if logged in"""

    user = session.get('logged_in_user', None)

    if not user:
        return redirect('/')

    usr = get_user(user)
    best_time = best_times(user)

    return render_template('/profile.html',usr=usr,best_times=best_time,user=user)

@app.route('/edit', methods=["GET", "POST"])
def edit_user_page():
    """Shows form to edit user if logged in, edits if password is authenticated, 
    and then redirects back to user profile"""

    user = session.get('logged_in_user', None)

    if not user:
        return redirect('/')

    form = SignUp()

    if form.validate_on_submit():
        print(form.username.data)
        print(get_user(user).username)

        if form.username.data != get_user(user).username:
            
            if is_username(form.username.data) == True:
                print("hi")
                flash('Username already exists.')
                return redirect('/edit')
        if login(get_user(user).username,form.password.data) == False:
            flash('Incorrect Password.')
            logout_user()
            data.user = None
            session.pop('logged_in_user')
            return redirect('/login')

        edit_user(form.name.data,get_user(user).username,form.username.data)
        # session['logged_in_user'] = data.user
        return redirect('/profile')
        
    else:
        return render_template('/signup.html', form=form,user=user)

@app.route('/global_leaderboards')
def leader_boards():
    """Show the best times and games completed for all users"""

    user = session.get('logged_in_user', None)

    users = global_best()[0]
    easy = global_best()[1]
    medium = global_best()[2]
    hard = global_best()[3]

    return render_template('global.html', users=users,easy=easy,medium=medium,hard=hard,user=user)


@app.route('/choose_level', methods=["GET", "POST"])
def game():
    """Shows form to play game and then redirects to /play_game"""

    user = session.get('logged_in_user', None)

    form = ChooseLevel()

    if user:
        if any_saved(user) == False:
            no_saved = False
        else:
            no_saved = True
    else:
        no_saved = False

    if form.validate_on_submit():
                  
        get_level(form.level.data)
        return redirect('/play_game')

    else:
        return render_template('/level.html', form=form,user=user,no_saved=no_saved)

@app.route('/play_game')
def play_game():
    """Loads selected game from either the api or saved game data"""

    user = session.get('logged_in_user', None)

    if data.board == None:
        return redirect('/choose_level')

    set_clock(data.clock)

    return render_template('/sudoku.html', board=data.board, level=data.level, c=data.clock, clock1=data.clock1, 
                            clock2=data.clock2, clock3=data.clock3, user=user, solved=data.solved)

@app.route('/save_game', methods=["POST"])
def get_javascript_data():
    """Gets clock/board/solved/level from javascript to save a game if logged in"""
    
    request_data = json.loads(request.data)

    user = session.get('logged_in_user', None)

    saving(request_data,user)

    return request_data

@app.route('/finish_game', methods=["POST"])
def finish_game():

    user = session.get('logged_in_user', None)
  
    request_data = json.loads(request.data)

    finishing(request_data,user)

    return request_data

@app.route('/end_game', methods=["POST"])
def end_game():
    """End current game if too many mistakes have been made and delete if saved"""

    user = session.get('logged_in_user', None)

    flash('You made too many mistakes - Better luck next time!')

    request_data = json.loads(request.data)
    ending(request_data,user)

    return request_data

@app.route('/load', methods=['GET', 'POST'])
def load_game():
    """Shows form to load game if logged in and then redirects to /play_game"""

    user = session.get('logged_in_user', None)
 
    if not user:
        return redirect('/login')

    if any_saved(user) == False:
        return redirect('/choose_level')

    form = Level()
    form.level.choices = any_saved(user)

    if form.validate_on_submit():

        loading(form.level.data.title(),user)

        return redirect('/play_game')

    else:
        return render_template('/load.html',form=form,user=user)
