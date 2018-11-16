#!/usr/bin/env python3
from app import create_app, db
from app.models import User

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        db.create_all()
        if User.query.filter_by(username='admin').first() is None:
            User.create_user('Luke', 'mugapedia@gmail.com', 'admin', 'admin', True)
    app.run()
