from fastapi import HTTPException
import mysql.connector
from database.dbconfig import DB_CONFIG
from models.user_model import UserRegistration

def register_user(user_data: UserRegistration):
    try:
        # Create a database connection
        db_config = DB_CONFIG
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert user data into the database
        insert_query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_data.username, user_data.password, user_data.role))
        connection.commit()

        return {"message": "User registered successfully"}

    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
