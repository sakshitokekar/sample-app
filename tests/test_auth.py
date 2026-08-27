# Tests for auth service
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.auth_service import register_user, login_user, users_db

def setup_function():
    """Clear users_db before each test."""
    users_db.clear()

def test_register_user_success():
    result = register_user("alice", "alice@example.com", "password123")
    assert result["success"] == True
    assert result["user"]["username"] == "alice"

def test_register_duplicate_email():
    register_user("alice", "alice@example.com", "password123")
    result = register_user("alice2", "alice@example.com", "password456")
    assert result["success"] == False
    assert "Email already registered" in result["error"]

def test_register_short_password():
    result = register_user("bob", "bob@example.com", "123")
    assert result["success"] == False
    assert "Password must be at least" in result["error"]

def test_login_success():
    register_user("charlie", "charlie@example.com", "securepass")
    result = login_user("charlie@example.com", "securepass")
    assert result["success"] == True
    assert "token" in result

def test_login_wrong_password():
    register_user("dave", "dave@example.com", "correctpass")
    result = login_user("dave@example.com", "wrongpass")
    assert result["success"] == False

def test_login_nonexistent_user():
    result = login_user("nobody@example.com", "password")
    assert result["success"] == False
    assert "Invalid credentials" in result["error"]


import hashlib
from models.user import User

def test_login_plain_text_password_migration():
    # Manually add a user with a plain-text password, simulating a pre-migration user
    plain_password = "oldplainpass"
    user_email = "migrate@example.com"
    # Create a user object directly with a plain-text password for the test scenario
    user_with_plain_pass = User(username="migrator", email=user_email, password=plain_password)
    users_db[user_email] = user_with_plain_pass

    # Attempt to log in with the plain-text password
    login_result = login_user(user_email, plain_password)
    assert login_result["success"] == True
    assert "token" in login_result

    # Verify that the user's password in the database has now been hashed
    migrated_user = users_db.get(user_email)
    assert migrated_user is not None
    assert migrated_user.password != plain_password
    assert migrated_user.password == hashlib.sha256(plain_password.encode()).hexdigest()

    # Attempt to log in again with the *same* plain-text password (it should still work due to re-hashing for comparison)
    second_login_result = login_user(user_email, plain_password)
    assert second_login_result["success"] == True

    # Verify password remains hashed after second login attempt
    migrated_user_after_second_login = users_db.get(user_email)
    assert migrated_user_after_second_login.password == hashlib.sha256(plain_password.encode()).hexdigest()

def test_login_with_whitespace_email():
    register_user("eve", "eve@example.com", "password123")
    result = login_user("  eve@example.com ", "password123")
    assert result["success"] == True
    assert "token" in result

def test_register_with_whitespace_email():
    result = register_user("frank", " frank@example.com ", "password123")
    assert result["success"] == True
    login_result = login_user("frank@example.com", "password123")
    assert login_result["success"] == True