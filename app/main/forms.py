from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, DateField
from wtforms.validators import Required, Length


class LoginForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 20)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class UserCreationForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 20)])
    email = StringField('Email', validators=[Required(), Length(1, 40)])
    username = StringField('Username', validators=[Required(), Length(1, 20)])
    password = PasswordField('Password', validators=[
                             Required(), Length(1, 20)])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Submit')


class AssetCreationForm(Form):
    name = StringField('Item Name', validators=[Required(), Length(3, 40)])
    description = TextField('description')
    serial_no = StringField('Serial  Number', validators=[
                            Required(), Length(3, 40)])
    andela_code = StringField('Andela Code', validators=[
                              Required(), Length(3, 64)])
    bought = DateField('Date Bought', validators=[Required()])
    cost = StringField('Cost(Ksh)', validators=[Required()])
    submit = SubmitField('Submit')
