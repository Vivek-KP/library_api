from library import db
from library.models.issuedBooks import IssuedBooks
from library.service.memberService.memberService import MemberService
from sqlalchemy.orm import joinedload
from sqlalchemy import asc
from datetime import datetime

class IssueService:
    def issueBook(issueDetails):
        try:
            # check fee reaches 500 
            if IssueService.checkAssignFee(issueDetails):
                raise Exception('Fee is over or equals to 500')
            else:
                db.session.add(issueDetails)
                db.session.commit()
                return issueDetails.dataReturn()
        except Exception as e:
            db.session.rollback()
            raise e

    def getIssuedBookDetails():
        try:
            current_date = datetime.now()
            details = db.session.query(IssuedBooks).options(joinedload(IssuedBooks.book)).options(joinedload(IssuedBooks.member)).order_by(asc(IssuedBooks.return_date)).all()
            result=[]
            for data in details:
                issuedData = data.dataReturn()
                # setting the dates into required format
                issuedData['issuedDate'] = issuedData['issuedDate'].strftime("%d-%m-%Y")
                issuedData['returnDate'] = issuedData['returnDate'].strftime("%d-%m-%Y")

                # generating fee based on return date
                if(current_date>data.return_date):
                    issuedData['fee'] = ((current_date-data.return_date).days) * 5
                else:
                    issuedData['fee'] = 0
                result.append(issuedData)
            return result
        except Exception as e:
            raise e


    def returnBook(returnDetails):
        try:
            issuedBook = IssuedBooks.query.filter_by(member_id = returnDetails['memberId'] ,book_id=returnDetails['bookId'] )
            if issuedBook:
                db.session.delete(issuedBook)
                db.session.commit()
            else:
                raise Exception ('Return Details not Found')
        except Exception as e:
            db.session.rollback()
            raise e



    def checkAssignFee(member):
        try:
            current_date = datetime.now()
            allBooksOwned = IssuedBooks.query.filter_by(member_id = member.member_id)
            totalFee = 0
            for bookDetails in allBooksOwned:
                if(current_date>bookDetails.return_date):
                    totalFee += ((current_date-bookDetails.return_date).days) * 5
                else:
                    totalFee += 0
            if(totalFee>=500):
                return True
            else:
                return False
        except Exception as e:
            raise e