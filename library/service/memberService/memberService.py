from library.models.memberModel import Member
from flask import jsonify
from library import db
from library.models.memberModel import Member
from library.service.issueService.issueService import IssueService



class MemberService :
    def addMember(newMember):
        try:
            db.session.add(newMember)
            db.session.commit()
            return newMember.dataReturn()
        except Exception as e:
            db.session.rollback()
            raise e


    def updateMember(data):
        try:
            member = Member.query.get(data['id'])
            member.name = data['name']
            member.email = data['email']
            member.fee = data['fee']
            db.session.commit()
            return member.dataReturn()
        except Exception as e:
            raise e

    def deleteMember(id):
        try:
            if not id:
                raise Exception ('Member_id not found')
            member =  Member.query.get(id)
            if not member:
                raise Exception ('Member not found')
            db.session.delete(member)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    def getMember(id):
        try:
            if id:
                member = Member.query.get(id)
                if not member:
                    raise ValueError ('Member not found')
                else:
                    result = member.dataReturn()
                    result['joined'] =  result['joined'].strftime("%Y-%m-%d")
                    result['fee'] = IssueService.checkAssignFee(member.id) if IssueService.checkAssignFee(member.id) < 500 else 500
            else:
                members = Member.query.all()
                result = []
                for member in members:
                    memberData = member.dataReturn()
                    memberData['joined'] =  memberData['joined'].strftime("%d-%m-%Y")
                    memberData['fee'] = IssueService.checkAssignFee(member.id) if IssueService.checkAssignFee(member.id) < 500 else 500

                    result.append(memberData)
            return result
        except Exception as e:
            raise e
