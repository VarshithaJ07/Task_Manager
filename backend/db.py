import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="varsha",   
            database="task_manager"
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None