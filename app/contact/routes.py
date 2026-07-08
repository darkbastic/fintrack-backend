from flask import Blueprint
from app.contact.controller import create_contact


contact_bp = Blueprint("contacts", __name__, url_prefix="/api/contacts")


@contact_bp.route("", methods=["POST"])
def create_contact_route():
    return create_contact()
