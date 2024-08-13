from library.models.booksModel import Book
from library import db
from datetime import datetime



class BookService :
    def addBook(newBook):
        try:
            db.session.add(newBook)
            db.session.commit()
            return newBook.dataReturn()
        except Exception as e:
            db.session.rollback()
            raise e


    def updateBook(self,data):
        try:
            book = self.getBook(data['id'])
            book.title= data['title']
            book.author =  data['author']
            book.average_rating =  float(data['averageRating'])
            book.isbn =  data['isbn']
            book.num_pages = int(data['numPages'])
            book.stock = int(data['stock'])
            book.publicationDate =   datetime.strptime(data['publicationDate'], '%d/%m/%Y').date()
            book.publisher = data['publisher']
            db.session.commit()
            return book.dataReturn()
        except Exception as e:
            raise e

    def deleteBook(id):
        try:
            if not id:
                raise Exception ('Member_id not found')
            book = BookService.getMember(id)
            if not book:
                raise Exception ('Book not found')
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    def getBook(id):
        try:
            if id:
                book = Book.query.get(id)
                if not book:
                    raise ValueError ('Book not found')
                else:
                    result = book.dataReturn()
                    result['publicationDate'] =  result['publicationDate'].strftime("%Y-%m-%d")
            else:
                books = Book.query.all()
                result = []
                for book in books:
                    bookdata = book.dataReturn()
                    bookdata['publicationDate'] =  bookdata['publicationDate'].strftime("%d-%m-%Y")
                    result.append(bookdata)

            return result
        except Exception as e:
            raise e
        


