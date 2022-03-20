"""Database models."""
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db


class User(db.Model):
    __tablename__ = 'belinsky_db'
    # User info
    user_id = db.Column(db.Integer())
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    created_at = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())

    # User data
    known_phrases = db.Column(db.ARRAY(db.String()), default=[])

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
