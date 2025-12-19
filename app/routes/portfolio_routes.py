from flask import Blueprint, request, jsonify
from app.services.portfolio_services import view_all_portfolios, get_portfolio_by_id, create_portfolio, delete_portfolio, add_new_security, harvest_investment


portfolio_bp = Blueprint('portfolio_routes', __name__, url_prefix="/portfolios")

@portfolio_bp.route('/', methods=['GET'])
def view_portfolios_route():
    try:
        result = view_all_portfolios()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@portfolio_bp.route("/<int:portfolio_id>", methods=['GET'])
def get_portfolio_by_id_route(portfolio_id):
    try:
        result = get_portfolio_by_id(portfolio_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@portfolio_bp.route("/create", methods=['POST'])
def create_portfolio_route(): 
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        owner = data.get('owner')

        if not name:
            return jsonify({"error": "name required"}), 400
        if not description:
            return jsonify({"error": "description required"}), 400
        if not owner:
            return jsonify({"error": "owner required"}), 400
        
        result = create_portfolio(name, description, owner)
        return jsonify(result), 201
    except Exception as e:
        return jsonify ({"error": str(e)}),400
    
@portfolio_bp.route('/delete/<int:portfolio_id>', methods =['DELETE'])
def delete_portfolio_route(portfolio_id):
    try:
        result = delete_portfolio(portfolio_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify ({"error": str(e)}), 400
    
@portfolio_bp.route('/add_security', methods=['POST'])
def add_new_security_route():
    try:
        data = request.get_json()
        portfolio_id = data.get('portfolio_id')
        ticker = data.get('ticker')
        quantity = data.get('quantity')

        if not portfolio_id:
            return jsonify({"error": "portfolio_id required"}), 400
        if not ticker:
            return jsonify({"error": "ticker required"}), 400
        if quantity is None:
            return jsonify({"error": "quantity required"}), 400
        
        result = add_new_security(portfolio_id, ticker, quantity)
        return jsonify(result), 200
    except Exception as e:
        return jsonify ({"error": str(e)}),400