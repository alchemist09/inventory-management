from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User, Asset
from . import main
from .forms import LoginForm, UserCreationForm, AssetCreationForm
from functools import wraps


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
            flash("Invalid login credentials")
            return redirect(url_for('main.index', **request.args))
        login_user(user, form.remember_me.data)
        flash("Login Successful")
        return redirect(request.args.get('next') or url_for('main.dashboard'))
    return render_template('index.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('main.index'))


# @main.route('/')
# def index():
#     return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


def check_is_super_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.username != 'admin':
            flash("You don't have the required privileges to access that page")
            return redirect(url_for('main.dashboard'))
        return func(*args, **kwargs)

    return decorated_function


def check_is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("You don't have the required privileges to access that page")
            return redirect(url_for('main.dashboard'))
        return func(*args, **kwargs)

    return decorated_function


@main.route('/create_admin', methods=['GET', 'POST'])
@login_required
@check_is_super_admin
def create_admin():
    form = UserCreationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('username already taken')
            return redirect(url_for('main.create_admin', **request.args))
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        is_admin = form.is_admin.data
        User.create_user(name, email, username, password, is_admin)
        flash("User created")
        return redirect(request.args.get('next') or url_for('main.dashboard'))
    return render_template('create_admin.html', form=form)


@main.route('/create_user', methods=['GET', 'POST'])
@login_required
@check_is_admin
def create_user():
    form = UserCreationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('username already taken')
            return redirect(url_for('main.create_user', **request.args))
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        is_admin = form.is_admin.data
        User.create_user(name, email, username, password, is_admin)
        flash("User created")
        return redirect(request.args.get('next') or url_for('main.dashboard'))
    return render_template('create_user.html', form=form)


@main.errorhandler(404)
def page_not_found(e):
    return render_template('templates/404.html')


@main.route('/users')
def users():
    users = User.find_all()
    return render_template('users.html', users=users)


@main.route('/create_asset', methods=['GET', 'POST'])
@login_required
@check_is_admin
def create_asset():
    form = AssetCreationForm()
    if form.validate_on_submit():
        asset = Asset.query.filter_by(serial_no=form.serial_no.data).first()
        if asset is not None:
            flash('an asset with a similar serial number already exists')
            return redirect(url_for('main.create_asset', **request.args))
        name = form.name.data
        description = form.description.data
        serial_no = form.serial_no.data
        andela_code = form.andela_code.data
        bought = form.bought.data
        cost = form.cost.data
        Asset.create_asset(name, description, serial_no,
                           andela_code, bought, cost)
        flash("Asset created")
        return redirect(request.args.get('next') or url_for('main.assets'))
    return render_template('create_asset.html', form=form)


@main.route('/assets')
def assets():
    assets = Asset.find_all()
    return render_template('assets.html', assets=assets)
