from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

# Username max length is 25
# Migrate with ' flask db migrate -m "users table" '
# TODO: Can the property 'is_anonymous'/anonymous user support by Flask-Login
#  be used as an attack vector?
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index=True,
                                                unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Print for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)

# Gets string id from flask-login  
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))