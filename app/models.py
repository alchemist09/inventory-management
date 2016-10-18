from werkzeug.security import generate_password_hash, check_password_hash
from . import db, lm
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    email = db.Column(db.String(20), index=True, unique=True)
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
        user = User(name=name, email=email, username=username, is_admin=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User({0}, {1})>'.format(self.name, self.username)


@lm.user_loader
def load_user(id):
    """Given *id*, return the associated User object.

    :param unicode id: id of user to retrieve
    """
    return User.query.get(int(id))
