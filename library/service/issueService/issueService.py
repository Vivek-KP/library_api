from library import db
from library.models.issuedBooks import IssuedBooks
from sqlalchemy.orm import joinedload
from sqlalchemy import asc
from datetime import datetime

class IssueService:
    def issueBook(issueDetails):
        try:
            # check fee reaches 500 
            if (IssueService.checkAssignFee(issueDetails.member_id)>= 500):
                raise Exception('Fee is over or equals to 500')
            else:
                db.session.add(issueDetails)
                db.session.commit()
                return issueDetails.dataReturn()
        except Exception as e:
            db.session.rollback()
            raise e

    def getIssuedBookDetails(id):
        try:
            if id:
                issuedDetails = IssuedBooks.query.get(id)
                issuedData = IssueService.dataFormater(issuedDetails)
                return issuedData
            else:
                details = db.session.query(IssuedBooks).options(joinedload(IssuedBooks.book)).options(joinedload(IssuedBooks.member)).order_by(asc(IssuedBooks.return_date)).all()
                result=[]
                for data in details:
                    issuedData = IssueService.dataFormater(data)
                    result.append(issuedData)
                return result
        except Exception as e:
            raise e

    def dataFormater(data):
        current_date = datetime.now()
        issuedData = data.dataReturn()
        # setting the dates into required format
        issuedData['issuedDate'] = issuedData['issuedDate'].strftime("%d-%m-%Y")
        issuedData['returnDate'] = issuedData['returnDate'].strftime("%d-%m-%Y")

        # generating fee based on return date
        if(current_date>data.return_date):
            if(((current_date-data.return_date).days) * 5 < 500):
                issuedData['fee'] = ((current_date-data.return_date).days) * 5
            else:
                issuedData['fee'] = 500
        else:
            issuedData['fee'] = 0
        return issuedData
    

    def returnBook(id):
        try:
            issuedBook = IssuedBooks.query.get(id)
            if issuedBook:
                db.session.delete(issuedBook)
                db.session.commit()
            else:
                raise Exception ('Return Details not Found')
        except Exception as e:
            db.session.rollback()
            raise e



    def checkAssignFee(memberId):
        try:
            current_date = datetime.now()
            allBooksOwned = IssuedBooks.query.filter_by(member_id = memberId)
            totalFee = 0
            for bookDetails in allBooksOwned:
                if(current_date>bookDetails.return_date):
                    totalFee += ((current_date-bookDetails.return_date).days) * 5
                else:
                    totalFee += 0
            return totalFee
        except Exception as e:
            raise e