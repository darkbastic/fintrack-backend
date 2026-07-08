from app.appstats.repository import AppStatsRepository


class AppStatsService:

    @staticmethod
    def get_users_count():
        try:
            count = AppStatsRepository.get_users_count()
            return {
                "users_count": count
            }, 200
        except Exception as e:
            return {
                "message": "Error al obtener las estadísticas de la aplicación.",
                "error": str(e)
            }, 500
