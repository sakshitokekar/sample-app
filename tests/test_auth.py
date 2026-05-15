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
