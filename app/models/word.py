import datetime

from sqlalchemy import ForeignKey

from app import db
from app.models import user


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(120))
    back = db.Column(db.String(120))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    due_date = db.Column(db.Date, default=datetime.datetime.utcnow)
    remembered_counter = db.Column(db.Integer(), default=0)
