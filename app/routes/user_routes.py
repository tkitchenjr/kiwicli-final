from flask import Blueprint, request, jsonify
from app.services.user_services import add_user, render_users, list_users, view_users, delete_user

user_routes = Blueprint('user_routes', __name__)

@user_bp.route('/add_user', methods=['POST'])
  
@user_bp.route('render_users', methods=['GET'])

@user_bp.route('/list_users', methods=['GET'])

@user_bp.route('/view_users', methods=['GET'])

@user_bp.route('/delete_user/<username>', methods =['DELETE'])