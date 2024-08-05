from library import db
from sqlalchemy.sql import func


class Book(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    title = db.Column(db.String(250),nullable = False)
    author = db.Column(db.String(250),nullable=False)
    average_rating = db.Column(db.Float,default = 0,nullable = True)
    isbn = db.Column(db.String(250),default = 0,nullable = False)
    language_code = db.Column(db.String(100),default = 0,nullable = True)
    num_pages = db.Column(db.Integer)
    publication_date = db.Column(db.Date)
    publisher = db.Column(db.String(250))
    stock  = db.Column(db.Integer,default = 1,nullable = False)
    created_date = db.Column(db.DateTime,default = func.now())
    updated_date = db.Column(db.DateTime,default = func.now(),onupdate = func.now())

    def dataReturn(self):
        return {
        'id': self.id,
        'title': self.title,
        'author': self.author,
        'averageRating': self.average_rating,
        'isbn': self.isbn,
        'numPages': self.num_pages,
        'stock':self.stock,
        'publicationDate': self.publication_date,
        'publisher': self.publisher

    }