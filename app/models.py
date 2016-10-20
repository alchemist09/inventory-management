from werkzeug.security import generate_password_hash, check_password_hash
from . import db, lm
from flask_login import UserMixin
from datetime import date


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    email = db.Column(db.String(40), index=True, unique=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_user(name, email, username, password, is_admin=False):
        """
            Create a user entry into the database
        """
        user = User(name=name, email=email, username=username, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


    def __repr__(self):
        return '<User({0}, {1})>'.format(self.name, self.username)

    @staticmethod
    def find_all():
        users = User.query.all()[1:]
        return users


class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(30), index=True)
    description = db.Column(db.String(250), index=True)
    serial_no = db.Column(db.String(150), index=True, unique=True)
    andela_code = db.Column(db.String(150), index=True)
    bought = db.Column(db.DateTime)
    cost = db.Column(db.Integer)
    assigned = db.Column(db.Boolean, default=False)
    date_assigned = db.Column(db.String(30))
    reclaim_date = db.Column(db.String(30))
    date_reclaimed = db.Column(db.String(30))


    def __repr__(self):
        return '<Asset({0}, {1})>'.format(self.name, self.serial_no)

    @staticmethod
    def create_asset(name, description, serial_no, andela_code, bought, cost):
        """
            Create new asset record in assets table
        """
        asset = Asset(name=name, description=description, serial_no=serial_no, andela_code=andela_code, bought=bought, cost=cost)
        db.session.add(asset)
        db.session.commit()

    @staticmethod
    def find_all():
        """
            Find all assets
        """
        assets = Asset.query.all()
        return assets


    @staticmethod
    def find_unassigned_items():
        """
            Find all items that have not been assigned
            to any user
        """
        assets = Asset.query.filter_by(assigned=False).all()
        return assets
        

    @staticmethod
    def assign_item(user_id, item_id, start_date, end_date):
        asset = Asset.query.filter_by(id=item_id).first()
        asset.assigned = True
        asset.date_assigned = start_date
        asset.end_date = end_date
        asset.user_id = user_id
        db.session.add(asset)
        db.session.commit()


@lm.user_loader
def load_user(id):
    """Given *id*, return the associated User object.

    :param unicode id: id of user to retrieve
    """
    return User.query.get(int(id))
