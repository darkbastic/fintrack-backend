from flask import Blueprint
from app.movement.controller import get_movements, create_movement, update_movement, delete_movement
from app.middleware.auth_middleware import login_required

movement_bp = Blueprint("movements", __name__, url_prefix="/api/movements")


@movement_bp.route("", methods=["GET"])
@login_required
def get_movements_route():
    return get_movements()


@movement_bp.route("", methods=["POST"])
@login_required
def create_movement_route():
    return create_movement()


@movement_bp.route("/<int:movement_id>", methods=["PUT"])
@login_required
def update_movement_route(movement_id):
    return update_movement(movement_id)


@movement_bp.route("/<int:movement_id>", methods=["DELETE"])
@login_required
def delete_movement_route(movement_id):
    return delete_movement(movement_id)
