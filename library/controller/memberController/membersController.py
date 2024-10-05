from flask import Blueprint,request,jsonify
from library.models.memberModel import Member
from library.service.memberService.memberService import MemberService

members_bp = Blueprint('members', __name__)

class MemberController:

   
    @members_bp.route('/member', methods=['GET'])
    def getMembers():
        try:
            id = request.args.get('id')
            result = MemberService.getMember(id)
            return jsonify({'status':'SUCCESS','message': '','data':result})
        except ValueError as ve:
            return jsonify({'status': 'FAIL', 'message': str(ve)})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}), 500
        
        

    @members_bp.route('/member', methods=['POST'])
    def addMember():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'FAIL', 'message': 'Invalid or missing JSON data'})
            newMember = Member(
                name = data['name'],
                email = data['email']
            )
            result = MemberService.addMember(newMember)
            return jsonify({'status':'SUCCESS','message': 'New member added!','data':result})
        except ValueError as ve:
            return jsonify({'status': 'FAIL', 'message': str(ve)})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500




    @members_bp.route('/member', methods=['DELETE'])
    def deleteMember():
        try:
            id = request.args.get('id')
            MemberService.deleteMember(id)
            return jsonify({'status': 'SUCCESS', 'message': 'Deleted Successfully'})
        except ValueError as ve:
            return jsonify({'status': 'FAIL', 'message': str(ve)})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500





    @members_bp.route('/member', methods=['PUT'])
    def updateMember():
        try:
            data = request.get_json()
            if not data or 'id' not in data:
                return jsonify({'status':'FAIL','message':'Data not Found'})
            result = MemberService.updateMember(data)
            return jsonify({'status':'SUCCESS','message':'Member Updated Successfully','data':result})
        except Exception as e:
            return jsonify({'status':'FAIL','message':str(e)}),500
        