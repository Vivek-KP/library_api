from library import db
from library.models.issuedBooks import IssuedBooks
from library.service.memberService.memberService import MemberService

class IssueService:
    def issueBook(issueDetails):
        try:
            db.session.add(issueDetails)
            db.session.commit()
            return issueDetails.dataReturn()
        except Exception as e:
            db.session.rollback()
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



    def assignFee(feeDetaills):
        try:
            member = MemberService.getMember(feeDetaills['memberId'])
            if member and (member.fee+feeDetaills['fee'])<500:
                member.fee = feeDetaills['fee']
                db.session.commit()
        except Exception as e:
            raise e