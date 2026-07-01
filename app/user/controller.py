from flask import request
from app.user.service import UserService

def register():
    data = request.get_json()
    return UserService.register(data)

def login():
    data = request.get_json()
    return UserService.login(data)