from app.database.connection import get_connection


class CategoryRepository:

    @staticmethod
    def find_all(user_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                SELECT id, name, type, is_default, user_id
                FROM categories
                WHERE is_default = TRUE OR user_id = %s
                ORDER BY type ASC, name ASC;
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_id(category_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                SELECT id, name, type, is_default, user_id
                FROM categories
                WHERE id = %s;
            """
            cursor.execute(sql, (category_id,))
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_name_and_type(name, category_type, user_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                SELECT id, name, type, is_default, user_id
                FROM categories
                WHERE LOWER(name) = LOWER(%s)
                  AND type = %s
                  AND (is_default = TRUE OR user_id = %s);
            """
            cursor.execute(sql, (name, category_type, user_id))
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create(name, category_type, is_default, user_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                INSERT INTO categories (name, type, is_default, user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                sql,
                (name, category_type, is_default, user_id)
            )

            category_id = cursor.fetchone()[0]

            connection.commit()

            return category_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update(category_id, name, category_type):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                UPDATE categories
                SET name = %s, type = %s
                WHERE id = %s;
            """
            cursor.execute(sql, (name, category_type, category_id))
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def delete(category_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                DELETE FROM categories
                WHERE id = %s;
            """
            cursor.execute(sql, (category_id,))
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()
