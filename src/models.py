from datetime import datetime

from . import db, jwt


@jwt.user_loader_callback_loader
def load_user(identity):
    try:
        return User.query.get(identity)
    except Exception:
        return None


class User(db.Model):
    __tablename__ = 'JWT_USERS_PY'.lower()

    id = db.Column(
        db.Integer, db.Sequence(f'{__tablename__}_id_seq'), primary_key=True)

    username = db.Column(
        db.String(), index=True, unique=True, nullable=False)

    def __str__(self):
        return '({}, {})'.format(self.id, self.username)
