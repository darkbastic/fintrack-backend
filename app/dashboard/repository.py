from app.database.connection import get_connection


class DashboardRepository:

    @staticmethod
    def get_summary(user_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT 
                    COALESCE(SUM(CASE WHEN c.type = 'income' THEN m.amount ELSE 0 END), 0) AS income,
                    COALESCE(SUM(CASE WHEN c.type = 'expense' THEN m.amount ELSE 0 END), 0) AS expense,
                    COUNT(m.id) AS movements
                FROM movements m
                JOIN categories c ON m.category_id = c.id
                WHERE m.user_id = %s;
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_last_movements(user_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT m.id, m.description, m.amount, m.movement_date, c.name, c.type
                FROM movements m
                JOIN categories c ON m.category_id = c.id
                WHERE m.user_id = %s
                ORDER BY m.movement_date DESC, m.id DESC
                LIMIT 5;
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_expenses_by_category(user_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT c.name, SUM(m.amount) AS total
                FROM movements m
                JOIN categories c ON m.category_id = c.id
                WHERE m.user_id = %s AND c.type = 'expense'
                GROUP BY c.name
                ORDER BY total DESC;
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_monthly_balance(user_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT 
                    COALESCE(SUM(CASE WHEN c.type = 'income' THEN m.amount ELSE 0 END), 0) AS income,
                    COALESCE(SUM(CASE WHEN c.type = 'expense' THEN m.amount ELSE 0 END), 0) AS expense
                FROM movements m
                JOIN categories c ON m.category_id = c.id
                WHERE m.user_id = %s 
                  AND DATE_TRUNC('month', m.movement_date) = DATE_TRUNC('month', CURRENT_DATE);
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()
