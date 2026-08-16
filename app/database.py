import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "todo_user"),
        password=os.getenv("MYSQL_PASSWORD", "todo_password"),
        database=os.getenv("MYSQL_DATABASE", "todo_db")
    )
