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