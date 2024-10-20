from library.models.booksModel import Book
from library import db
from datetime import datetime
from library.service.issueService.issueService import IssueService
import requests


class BookService :
    def addBook(newBook):
        try:
            db.session.add(newBook)
            db.session.commit()
            return newBook.dataReturn()
        except Exception as e:
            db.session.rollback()
            raise Exception('Something Went Wrong')


    def updateBook(data):
        try:
            book = Book.query.get(data['id'])
            book.title= data['title']
            book.author =  data['author']
            book.average_rating =  float(data['averageRating'])
            book.isbn =  data['isbn']
            book.stock = int(data['stock'])
            book.publicationDate =   datetime.strptime(data['publicationDate'], '%d-%m-%Y').date()
            book.publisher = data['publisher']
            db.session.commit()
            return book.dataReturn()
        except Exception as e:
            raise Exception('Something Went Wrong')

    def deleteBook(id):
        try:
            if not id:
                raise ValueError ('Book_id not found')
            book = Book.query.get(id)
            if not book:
                raise ValueError ('Book not found')
            if IssueService.checkBookhasIssuedDetails(id):
                raise ValueError ('Please return all this book from  assigned members')
                
            db.session.delete(book)
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            raise ve
        except Exception as e:
            db.session.rollback()
            raise Exception('Something Went Wrong')


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
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception('Something Went Wrong')
        

    def importBook():
        url = 'https://frappe.io/api/method/frappe-library'
        response = requests.get(url).json()
        print(response)
        



