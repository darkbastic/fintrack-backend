from flask import Blueprint, jsonify, g
from app.user.controller import register, login
from app.middleware.auth_middleware import login_required


user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.post("/register")
def register_route():
    return register()

@user_bp.route("/login", methods=["POST"])
def login_route():
    return login()

@user_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    return jsonify({
        "user_id": g.user_id
    })