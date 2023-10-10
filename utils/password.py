from passlib.context import CryptContext

# Create an instance of the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the user's password
hashed_password = pwd_context.hash("user_password")

# Store the hashed password in the database
# Insert username, hashed_password, and role into the users table
