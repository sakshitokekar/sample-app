# Auth routes
from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user, get_user_by_id

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    result = register_user(
        username=data["username"],
        email=data["email"],
        password=data["password"]
    )

    if not result["success"]:
        return jsonify({"error": result["error"]}), 400

    return jsonify(result["user"]), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login with email and password."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    result = login_user(email=data["email"], password=data["password"])

    if not result["success"]:
        return jsonify({"error": result["error"]}), 401

    return jsonify({
        "token": result["token"],
        "user": result["user"]
    }), 200

@auth_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user details by ID."""
    result = get_user_by_id(user_id)
    if not result["success"]:
        return jsonify({"error": result["error"]}), 404
    return jsonify(result["user"]), 200
