from library import db
from sqlalchemy.sql import func


class IssuedBooks(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'),nullable = False)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'),nullable=False)
    created_date = db.Column(db.DateTime,default = func.now())
    updated_date = db.Column(db.DateTime,default = func.now(),onupdate = func.now())
    issued_date = db.Column(db.DateTime)

    book = db.relationship('Book', backref=db.backref('issued_books', lazy=True))
    member = db.relationship('Member', backref=db.backref('issued_books', lazy=True))

    def dataReturn(self):
        return {
        'id': self.id,
        'book_id': self.book_id,
        'member_id': self.member_id,
        'created_date': self.created_date,
        'issuedDate': self.issued_date

    }