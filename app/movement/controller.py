from flask import request, g
from app.movement.service import MovementService


def get_movements():
    return MovementService.get_movements(g.user_id)


def create_movement():
    data = request.get_json()
    return MovementService.create_movement(g.user_id, data)


def update_movement(movement_id):
    data = request.get_json()
    return MovementService.update_movement(g.user_id, movement_id, data)


def delete_movement(movement_id):
    return MovementService.delete_movement(g.user_id, movement_id)
