from app.appstats.service import AppStatsService


def get_users_count():
    return AppStatsService.get_users_count()
