from library.models.memberModel import Member
from library.models.booksModel import Book
from library.models.issuedBooks import IssuedBooks
from datetime import datetime
from sqlalchemy import func

class DashboardService:
    def getMembersTotal():
        data={}
        data['memberCount'] = Member.query.count()
        data['bookCount'] =  Book.query.count()
        data['issuedBookCount'] = IssuedBooks.query.count()
        data['overDuebookCount'] = IssuedBooks.query.filter(IssuedBooks.return_date < func.current_date()).count()
        return data
