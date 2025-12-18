from flask import Blueprint, request, jsonify
from app.services.user_services import view_users, get_user_by_id, create_user, delete_user

user_bp = Blueprint('user_routes', __name__, url_prefix="/user")

@user_bp.route('/', methods=['GET'])
def view_users():
    return jsonify({"message": "Listing all users"})
  
@user_bp.route("/<str:user>", methods=['GET'])
def get_user_by_id(user):
    return jsonify({"user": user}), 200

@user_bp.route("/create_user", methods=['POST'])
def create_user(): 
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        balance = data.get('balance')

        if not username:
            return jsonify({"error": "username required"}), 400
        if not password:
            return jsonify({"error": "password required"}), 400
        if not firstname:
            return jsonify({"error": "firstname required"}), 400
        if not lastname:
            return jsonify({"error": "lastname required"}), 400
        if not balance:
            return jsonify({"error": "balance required"}), 400
        
        result = create_user(username, password, firstname, lastname, balance)
        jsonify(result), 201
    except Exception as e:
        return jsonify ({"error": str(e)}),400

@user_bp.route('/delete_user/<username>', methods =['DELETE'])
def delete_user(username):
    try:
        result = delete_user(username)
        return jsonify(result), 200
    except Exception as e:
        return jsonify ({"error": str(e)}), 400