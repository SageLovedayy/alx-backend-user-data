#!/usr/bin/env python3

import unittest
from app import app  # Import the Flask app from the app module
from flask.testing import FlaskClient


class TestUserFlow(unittest.TestCase):
    def setUp(self):
        self.client: FlaskClient = app.test_client()
        self.client.testing = True

    def test_update_password_success(self):
        # Step 1: Register a user
        response = self.client.post('/users', data={
            'email': 'testuser@ex.com',
            'password': 'oldpassword123'
        })
        self.assertEqual(response.status_code, 200)

        # Step 2: Log in to create a session
        response = self.client.post('/sessions', data={
            'email': 'testuser@ex.com',
            'password': 'oldpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('session_id', response.cookies)

        # Step 3: Request reset token
        response = self.client.post('/reset_password', data={
            'email': 'testuser@ex.com'
        })
        self.assertEqual(response.status_code, 200)
        token = response.json['reset_token']

        # Step 4: Update the password
        response = self.client.put('/reset_password', data={
            'email': 'testuser@ex.com',
            'reset_token': token,
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'email': 'testuser@ex.com',
            'message': 'Password updated'
            })

    def test_update_password_invalid_token(self):
        # Register a user
        response = self.client.post('/users', data={
            'email': 'testuser@ex.com',
            'password': 'oldpassword123'
        })
        self.assertEqual(response.status_code, 200)

        # Attempt to update the password with an invalid token
        response = self.client.put('/reset_password', data={
            'email': 'testuser@ex.com',
            'reset_token': 'invalid_token',
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
