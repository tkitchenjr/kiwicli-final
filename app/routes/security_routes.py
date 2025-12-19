from flask import Blueprint, request, jsonify
from app.services.security_services import view_all_securities


security_bp = Blueprint('security_routes', __name__, url_prefix="/securities")

@security_bp.route('/', methods=['GET'])
def view_all_securities_route():
    try:
        result = view_all_securities()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400