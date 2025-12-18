from flask import Blueprint, request, jsonify
from app.services.user_services import 

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/add_user', methods=['POST'])
  
@user_bp.route('render_users', methods=['GET'])

@user_bp.route('/list_users', methods=['GET'])

@user_bp.route('/view_users', methods=['GET'])

@user_bp.route('/delete_user/<username>', methods =['DELETE'])