from flask import request
from app.contact.service import ContactService


def create_contact():
    data = request.get_json()
    return ContactService.create_contact(data)
