from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    email_confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.name}>'
