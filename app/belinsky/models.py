"""Belinsky Database models."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db


# pylint: disable=no-member
class User(UserMixin, db.Model):
    """Belinsky User model."""
    __tablename__ = 'belinsky_db'
    # User info
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
