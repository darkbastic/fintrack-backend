from flask import Blueprint, jsonify, g
from app.user.controller import register, login, get_profile, update_profile, update_password
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
    return get_profile()

@user_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile_route():
    return update_profile()

@user_bp.route("/password", methods=["PUT"])
@login_required
def update_password_route():
    return update_password()