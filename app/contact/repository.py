from app.database.connection import get_connection


class ContactRepository:

    @staticmethod
    def create(full_name, email, subject, message):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            sql = """
                INSERT INTO contacts (full_name, email, subject, message)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """

            cursor.execute(
                sql,
                (full_name, email, subject, message)
            )

            contact_id = cursor.fetchone()[0]

            connection.commit()

            return contact_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()
