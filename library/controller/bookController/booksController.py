from flask import Blueprint,request,jsonify
from library.models.booksModel import Book
from library.service.bookService.bookService import BookService
from datetime import datetime

books_bp = Blueprint('books', __name__)

class MemberController:

   
    @books_bp.route('/book', methods=['GET'])
    def getBooks():
        try:
            id = request.args.get('id')
            result = BookService.getBook(id)
            return jsonify({'status':'SUCCESS','message': '','data':result})
        except ValueError as ve:
            return jsonify({'status': 'FAIL', 'message': str(ve)})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}), 500
        
        

    @books_bp.route('/book', methods=['POST'])
    def addBook():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'FAIL', 'message': 'Invalid or missing JSON data'})
            newBook = Book(
                title= data['title'],
                author =  data['author'],
                average_rating =  float(data['averageRating']),
                isbn =  data['isbn'],
                stock = int(data['stock']),
                publication_date =  datetime.strptime(data['publicationDate'], '%d-%m-%Y').date(),
                publisher = data['publisher']
            )
            result = BookService.addBook(newBook)
            return jsonify({'status':'SUCCESS','message': 'New book added!','data':result})
        except ValueError as ve:
            return jsonify({'status': 'FAIL', 'message': str(ve)})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500




    @books_bp.route('/book', methods=['DELETE'])
    def deleteBook():
        try:
            id = request.args.get('id')
            BookService.deleteBook(id)
            return jsonify({'status': 'SUCCESS', 'message': 'Deleted Successfully'})
        except ValueError as ve:
            return jsonify({'status': 'FAIL', 'message': str(ve)})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500





    @books_bp.route('/book', methods=['PUT'])
    def updateBook():
        try:
            data = request.get_json()
            if not data or 'id' not in data:
                return jsonify({'status':'FAIL','message':'Data not Found'})
            result = BookService.updateBook(data)
            return jsonify({'status':'SUCCESS','message':'Book Updated Successfully','data':result})
        except Exception as e:
            return jsonify({'status':'FAIL','message':str(e)}),500
        