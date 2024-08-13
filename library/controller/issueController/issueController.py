from flask import Blueprint,jsonify,request
from library.models.issuedBooks import IssuedBooks
from library.service.issueService.issueService import IssueService

issueBook_bp = Blueprint('issueBook',__name__)

class IssueController:

    @issueBook_bp.route('/issue',Methods=['POST'])
    def issueBook():
        try:
            data = request.get_json()
            issuedDetails = IssuedBooks(
                book_id = data['bookId'],
                member_id = data['memberId'],
                issued_date = data['issuedDate']
            )
            result = IssueService.issueBook(issuedDetails)
            return jsonify({'status':'SUCCESS','message': 'New member added!','data':result})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)})
        
    def returnBook():
        try:
            data = request.get_json()
            result = IssueService.returnBook(data)
            return jsonify({'status':'SUCCESS','message': 'New member added!','data':result})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)})
            

