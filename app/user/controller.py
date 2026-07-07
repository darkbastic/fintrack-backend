from flask import request, g
from app.user.service import UserService

def register():
    data = request.get_json()
    return UserService.register(data)

def login():
    data = request.get_json()
    return UserService.login(data)

def get_profile():
    return UserService.get_profile(g.user_id)

def update_profile():
    data = request.get_json()
    return UserService.update_profile(g.user_id, data)

def update_password():
    data = request.get_json()
    return UserService.update_password(g.user_id, data)