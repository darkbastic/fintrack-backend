from app.database.connection import get_connection


class MovementRepository:

    @staticmethod
    def find_all(user_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT m.id, m.description, m.amount, m.movement_date, m.category_id, c.name, c.type
                FROM movements m
                JOIN categories c ON m.category_id = c.id
                WHERE m.user_id = %s
                ORDER BY m.movement_date DESC, m.id DESC;
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_id(movement_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                SELECT id, description, amount, movement_date, category_id, user_id
                FROM movements
                WHERE id = %s;
            """
            cursor.execute(sql, (movement_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create(description, amount, movement_date, category_id, user_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO movements (description, amount, movement_date, category_id, user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """
            cursor.execute(sql, (description, amount, movement_date, category_id, user_id))
            movement_id = cursor.fetchone()[0]
            connection.commit()
            return movement_id
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update(movement_id, description, amount, movement_date, category_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                UPDATE movements
                SET description = %s, amount = %s, movement_date = %s, category_id = %s
                WHERE id = %s;
            """
            cursor.execute(sql, (description, amount, movement_date, category_id, movement_id))
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(movement_id):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            sql = """
                DELETE FROM movements
                WHERE id = %s;
            """
            cursor.execute(sql, (movement_id,))
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
