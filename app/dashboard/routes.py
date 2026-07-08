from flask import Blueprint
from app.dashboard.controller import get_dashboard
from app.middleware.auth_middleware import login_required


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.route("", methods=["GET"])
@login_required
def get_dashboard_route():
    return get_dashboard()
