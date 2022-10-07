
from zetta_app import db
from datetime import datetime
from zetta_app import login_manager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(username):
    return(User.query.get(int(username)))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(20),unique=False, nullable=False)
    designation = db.Column(db.String(60),unique=False, nullable=False)
    # location = db.Column(db.String(120), unique=False, nullable=False)
    contact = db.Column(db.String(20), unique=False,nullable=False)
    gmail = db.Column(db.String(60), unique=False,nullable=False)
    password = db.Column(db.String(60),unique=False, nullable=False)
    date_created = db.Column(db.DateTime,unique=False, nullable=False, default=datetime.utcnow())
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class zetta_dbform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Float, nullable=False)

    blood_pressure = db.Column(db.Integer, nullable=False)
    insulin = db.Column(db.Float, nullable=False)
    cardio = db.Column(db.Float, nullable=False)
    liver = db.Column(db.Float, nullable=False)

    smoking = db.Column(db.Integer, nullable=False)
    date_filled = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    def __repr__(self):
        return f"Post('{self.patient_name}', '{self.date_filled}')"