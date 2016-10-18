from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 20)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class UserCreationForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 20)])
    email = StringField('Email', validators=[Required(), Length(1, 20)])
    username = StringField('Username', validators=[Required(), Length(1, 20)])
    password = StringField('Password', validators=[Required(), Length(1, 20)])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Submit')
