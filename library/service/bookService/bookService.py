from library.models.booksModel import Book
from library import db
from datetime import datetime
from library.service.issueService.issueService import IssueService
import requests,math
import json



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
            raise Exception('Something Went Wrong'+ str(e))


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
        

    def importBook(data):
        try:
            print(data)
            url = 'https://frappe.io/api/method/frappe-library'
            params = {'page':1}
            if(data['title']):
                params['title'] = data['title']
            if(data['author']):
                 params['author'] = data['author']
            if(data['publisher']):
                 params['publisher'] = data['publisher']
            importedBooks = 0
            print(params)
            pageNumber = math.ceil(int(data['bookCount'])/20)
            for i in range(1,pageNumber+1):
                params['page'] = i
                response = requests.get(url,params=params).json()
                responseData = response['message']
                for book in responseData:
                    if(importedBooks== int(data['bookCount'])):
                        break
                    else:
                        newBook = Book(
                                title= book['title'],
                                author =  book['authors'],
                                average_rating =  float(book['average_rating']),
                                isbn =  book['isbn'],
                                stock = 1,
                                publication_date =  datetime.strptime(book['publication_date'], '%m/%d/%Y').date(),
                                publisher = book['publisher']
                        )
                        importedBooks+=1
                        db.session.add(newBook)
                        db.session.commit()
                if(importedBooks==data['bookCount']):
                        break
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception('Something Went Wrong'+str(e))
    
        



