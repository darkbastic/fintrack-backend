from functools import wraps
from flask import request, jsonify, g
from app.common.jwt_service import JwtService

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Token no proporcionado."
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "message": "Token inválido."
            }), 401

        token = auth_header.split(" ")[1]

        payload = JwtService.verify_token(token)

        if payload is None:
            return jsonify({
                "message": "Token inválido o expirado."
            }), 401

        g.user_id = payload["user_id"]

        return f(*args, **kwargs)

    return decorated