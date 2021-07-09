from datetime import datetime
from user_login_system import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as jws


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_of_registration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        jws_obj = jws(app.config['SECRET_KEY'], expires_sec)
        return jws_obj.dumps({'user_id': self.id}).decode('UTF-8')

    @staticmethod
    def verify_reset_token(token):
        jws_obj = jws(app.config['SECRET_KEY'])
        try:
            user_id = jws_obj.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'Username: {self.username} email: {self.email} is_verified: {self.is_verified} ' \
               f'reviewed: {self.reviewed}'
