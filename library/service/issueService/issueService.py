from library import db
from library.models.issuedBooks import IssuedBooks
from library.models.booksModel import Book
from sqlalchemy.orm import joinedload
from sqlalchemy import asc,and_
from datetime import datetime

class IssueService:
    def issueBook(issueDetails):
        try:
            # check the book already assigned to the member
            if(IssueService.checkBookAlreadyAssignedtotheMember(issueDetails.book_id,issueDetails.member_id)):
                raise ValueError('Book already assigned to that member')
                
            # check fee reaches 500 
            if (IssueService.checkAssignFee(issueDetails.member_id)>= 500):
                raise ValueError('Fee is over or equals to 500')
            IssueService.updateStock(issueDetails.book_id,'ISSUE')
            db.session.add(issueDetails)
            db.session.commit()
            return issueDetails.dataReturn()
        except ValueError as ve:
            db.session.rollback()
            raise ve
        except Exception as e:
            db.session.rollback()
            raise Exception('Something Went Wrong'+str(e))

    def getIssuedBookDetails(id):
        try:
            if id:
                issuedDetails = IssuedBooks.query.get(id)
                issuedData = IssueService.dataFormater(issuedDetails)
                return issuedData
            else:
                details = IssuedBooks.query.options(joinedload(IssuedBooks.book)).options(joinedload(IssuedBooks.member)).order_by(asc(IssuedBooks.return_date)).all()
                result=[]
                for data in details:
                    issuedData = IssueService.dataFormater(data)
                    result.append(issuedData)
                return result
        except Exception as e:
           raise Exception('Something Went Wrong' + str(e))

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
                IssueService.updateStock(issuedBook.book_id,'RETURN')
                db.session.delete(issuedBook)
                db.session.commit()
            else:
                raise ValueError ('Return Details not Found')
        except ValueError as ve:
            raise ve
        except Exception as e:
            db.session.rollback()
            raise Exception('Something Went Wrong' + str(e))



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
            raise Exception('Something Went Wrong')
    
    # these to two function is to check book or memeber is present in the issued details before delete
    def checkMemberhasIssuedDetails(memberId):
        try:
            member = IssuedBooks.query.filter_by(member_id = memberId).first()
            if member:
                return True
            else:
                return False
        except Exception as e:
            raise  Exception('Something Went Wrong')
        
    def checkBookhasIssuedDetails(bookId):
        try:
            book = IssuedBooks.query.filter_by(book_id = bookId).first()
            if book:
                return True
            else:
                return False
        except Exception as e:
            raise Exception('Something Went Wrong')
        
        

    def checkBookAlreadyAssignedtotheMember(bookId,memberId):
        try:
            details = IssuedBooks.query.filter(and_(IssuedBooks.book_id == bookId,IssuedBooks.member_id == memberId)).first()
            if details:
                return True
            else:
                return False
        except Exception as e:
            raise Exception('Something Went Wrong' + str(e))


    def updateStock(bookId,type):
        try:
            book = Book.query.filter_by(id = bookId).first()
            if book and book.stock>0 and type == 'ISSUE':
                book.stock -= 1
                db.session.commit()
            elif book and type == 'RETURN':
                book.stock += 1
                db.session.commit()
        except Exception as e:
            raise Exception('Something went wrong'+str(e))