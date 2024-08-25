from flask import Blueprint,jsonify,request
from library.models.issuedBooks import IssuedBooks
from library.service.issueService.issueService import IssueService
from datetime import datetime

issueBook_bp = Blueprint('issueBook',__name__)

class IssueController:

    @issueBook_bp.route('/issue',methods=['POST'])
    def issueBook():
        try:
            data = request.get_json()
            issuedDetails = IssuedBooks(
                book_id = data['bookId'],
                member_id = data['memberId'],
                issued_date = datetime.strptime(data['dateOfIssue'], '%d-%m-%Y').date(),
                return_date = datetime.strptime(data['returnDate'], '%d-%m-%Y').date()

            )
            result = IssueService.issueBook(issuedDetails)
            return jsonify({'status':'SUCCESS','message': 'Book Issued','data':result})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}) , 500
        

    @issueBook_bp.route('/issue',methods=['GET'])
    def getIssuedBookDetails():
        try:
            id = request.args.get('id')
            result = IssueService.getIssuedBookDetails(id)
            return jsonify({'status':'SUCCESS','message': 'Issued Books','data':result})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500
    
    @issueBook_bp.route('/issue',methods=['DELETE'])
    def returnBook():
        try:
            id = request.args.get('id')
            result = IssueService.returnBook(id)
            return jsonify({'status':'SUCCESS','message': 'New member added!','data':result})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500
            

