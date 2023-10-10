from fastapi import FastAPI
from fastapi import HTTPException
from config.cors import configure_cors
import uvicorn
from pydantic import BaseModel
from starlette import status
from database.dbconfig import get_database_connection
from models.user_model import UserRegistration


app = FastAPI()

# Configure CORS
configure_cors(app)

class Test(BaseModel):
    test: str

@app.get('/api/v1/test', status_code=status.HTTP_200_OK, response_model=Test)
async def get_test_response():

    response_string = {'test': 'Tämä on testi stringi bäkendistä!'}
    return response_string


@app.post("/register")
async def register_user(user_data: UserRegistration):
    connection = None  # Initialize the connection variable
    cursor = None  # Initialize the cursor variable

    try:
        # Get a database connection
        connection = get_database_connection()
        cursor = connection.cursor()

        # Insert user data into the database
        insert_query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_data.username, user_data.password, user_data.role))
        connection.commit()

        return {"message": "User registered successfully"}

    except Exception as error:
        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)
