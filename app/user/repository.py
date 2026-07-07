from app.database.connection import get_connection


class UserRepository:

    @staticmethod
    def find_by_email(email):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                SELECT id, name, lastname, email, password
                FROM users
                WHERE email = %s;
            """
            cursor.execute(sql, (email,))
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def create(name, lastname, email, password):
           connection = get_connection()
    
           try:
               cursor = connection.cursor()
    
               sql = """
                   INSERT INTO users (name, lastname, email, password)
                   VALUES (%s, %s, %s, %s)
                   RETURNING id;
               """
    
               cursor.execute(
                   sql,
                   (name, lastname, email, password)
               )
    
               user_id = cursor.fetchone()[0]
    
               connection.commit()
    
               return user_id
    
           except Exception:
               connection.rollback()
               raise
    
           finally:
               cursor.close()
               connection.close()

    @staticmethod
    def find_by_id(user_id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                SELECT id, name, lastname, email, password
                FROM users
                WHERE id = %s;
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_profile(user_id, name, lastname):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                UPDATE users
                SET name = %s, lastname = %s
                WHERE id = %s;
            """
            cursor.execute(sql, (name, lastname, user_id))
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_password(user_id, hashed_password):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                UPDATE users
                SET password = %s
                WHERE id = %s;
            """
            cursor.execute(sql, (hashed_password, user_id))
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()