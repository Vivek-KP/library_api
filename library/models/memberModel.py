from sqlalchemy.sql import func
from library import db


class Member(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    fee = db.Column(db.Integer,default = 0)
    created_date = db.Column(db.DateTime,default = func.now())
    updated_date = db.Column(db.DateTime,default = func.now(),onupdate = func.now())

    def dataReturn(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'fee': self.fee,
        'joined':self.created_date

    }