import mysql.connector

def create_connection():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jitesh@93",
            database="cybercafe_management"
        )

        if con.is_connected():
            return con

    except mysql.connector.Error as err:
        print("Database connection failed:", err)

    return None
