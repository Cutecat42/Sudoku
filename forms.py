from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField , validators

class ChooseLevel(FlaskForm):

    level = SelectField('Choose a level', choices=[('e', 'Easy'), ('m', 'Medium'), ('h', 'Hard')])


class Level(FlaskForm):

    level = SelectField('Choose a saved Game', coerce=str)

class SignUp(FlaskForm):
    
    name = StringField("Enter your name:", [validators.required()])
    username = StringField("Enter your username:", [validators.required()])
    password = PasswordField("Enter your password:", [validators.required()])

class Login(FlaskForm):

    username = StringField("Enter your username:", [validators.required()])
    password = PasswordField("Enter your password:", [validators.required()])