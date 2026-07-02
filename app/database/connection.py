import psycopg2
from app.config import Config

def get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=int(Config.DB_PORT or 5432),
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )