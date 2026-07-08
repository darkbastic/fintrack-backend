from flask import Blueprint
from app.appstats.controller import get_users_count

appstats_bp = Blueprint("appstats", __name__, url_prefix="/api/appstats")


@appstats_bp.route("", methods=["GET"])
def get_users_count_route():
    return get_users_count()
