#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

# Initialize the DB class
my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

try:
    # Add a user
    user = my_db.add_user(email, hashed_password)
    print(f"User ID: {user.id}")

    # Update the user's password
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except (InvalidRequestError, NoResultFound, ValueError) as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

