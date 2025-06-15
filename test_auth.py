# To run: python -m unittest test_auth.py

import os
import unittest
import tempfile
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

import backend.auth as auth

class TestAuthModule(unittest.TestCase):
    def setUp(self):
        # Setup a temporary users file
        self.temp_users_file = tempfile.NamedTemporaryFile(delete=False)
        self.original_users_file = auth.USERS_FILE
        auth.USERS_FILE = self.temp_users_file.name

        # Setup a dummy user
        self.username = "testuser"
        self.password = "securepassword"
        self.hashed_password = auth.hash_password(self.password)

        # Save dummy user manually
        with open(auth.USERS_FILE, "w") as f:
            json.dump({self.username: self.hashed_password}, f)

    def tearDown(self):
        # Clean up temporary file
        os.unlink(auth.USERS_FILE)
        auth.USERS_FILE = self.original_users_file

    def test_hash_and_verify_password(self):
        hashed = auth.hash_password("mypassword")
        self.assertTrue(auth.verify_password("mypassword", hashed))
        self.assertFalse(auth.verify_password("wrong", hashed))

    def test_register_user(self):
        new_user = "newuser"
        new_pass = "newpass"
        auth.register_user(new_user, new_pass)
        users = auth.load_users()
        self.assertIn(new_user, users)
        self.assertTrue(auth.verify_password(new_pass, users[new_user]))

    def test_register_user_already_exists(self):
        with self.assertRaises(Exception):
            auth.register_user(self.username, "newpass")

    def test_authenticate_user_success(self):
        token = auth.authenticate_user(self.username, self.password)
        self.assertIsInstance(token, str)

    def test_authenticate_user_fail(self):
        with self.assertRaises(Exception):
            auth.authenticate_user("wronguser", "wrongpass")

    def test_create_and_verify_token(self):
        token = auth.create_token(self.username)
        decoded_user = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])["sub"]
        self.assertEqual(decoded_user, self.username)


if __name__ == "__main__":
    unittest.main()
