from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
from ..models import User
from . import main
from .forms import LoginForm


@main.route('/', methods=['GET', 'POST'])
def index():
    """
        For GET requests, display the login form. 
        For POSTS, login the current user by processing the form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.index', **request.args))
        login_user(user, form.remember_me.data)
        flash("Login Successful")
        return redirect(request.args.get('next') or url_for('main.dashboard'))
    return render_template('index.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# @main.route('/')
# def index():
#     return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@main.route('/create_user')
@login_required
def create_user():
    user = UserCreationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('username already taken')
            return redirect(url_for('main.index', **request.args))
        login_user(user, form.remember_me.data)
        flash("Login Successful")
        return redirect(request.args.get('next') or url_for('main.dashboard'))
    return render_template('index.html', form=form)
