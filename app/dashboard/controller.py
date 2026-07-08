from flask import g
from app.dashboard.service import DashboardService


def get_dashboard():
    return DashboardService.get_dashboard(g.user_id)
