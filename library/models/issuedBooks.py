from library import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint


class IssuedBooks(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'),nullable = False)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'),nullable=False)
    created_date = db.Column(db.DateTime,default = func.now())
    updated_date = db.Column(db.DateTime,default = func.now(),onupdate = func.now())
    issued_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    
    book = db.relationship('Book', backref=db.backref('issued_books', lazy=True))
    member = db.relationship('Member', backref=db.backref('issued_members', lazy=True))

    __table_args__ = (
         UniqueConstraint('book_id', 'member_id', name='uq_book_member'),
    )

    def dataReturn(self):
        return {
        'id': self.id,
        'issuedDate': self.issued_date,
        'returnDate' : self.return_date,
        'book':self.book.dataReturn(),
        'member': self.member.dataReturn(),
        'fee':0

    }