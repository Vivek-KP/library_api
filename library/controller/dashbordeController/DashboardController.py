from flask import Blueprint,jsonify
from library.service.dashboardService.DashboardService import DashboardService

dashboard_bp = Blueprint('dashboard',__name__)

class DashboardController:

    @dashboard_bp.route('/dashboard',methods=['GET'])
    def getAllDataForDashboard():
        try:
            result = DashboardService.getMembersTotal()
            return jsonify({'status':'SUCCESS','message': 'Dashboard Data','data':result})
        except Exception as e:
            return jsonify({'status': 'FAIL', 'message': str(e)}),500