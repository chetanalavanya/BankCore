import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """Create and return a MySQL database connection."""

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "bankcore")
        )

        return connection

    except Error as e:
        print(f"Database connection error: {e}")
        return None