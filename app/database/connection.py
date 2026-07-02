import psycopg2
from app.config import Config

def get_connection():
    return psycopg2.connect(
        host=str(Config.DB_HOST),
        port=int(Config.DB_PORT),
        database=str(Config.DB_NAME),
        user=str(Config.DB_USER),
        password=str(Config.DB_PASSWORD)
    )