from app.database.connection import get_connection


class AppStatsRepository:

    @staticmethod
    def get_users_count():
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = "SELECT COUNT(*) FROM users;"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            connection.close()
