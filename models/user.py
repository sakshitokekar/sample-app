# User model
import hashlib
import uuid
from datetime import datetime

class User:
    def __init__(self, username: str, email: str, password: str, user_id: str = None):
        self.id = user_id or str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password  # BUG: storing plain text password, should be hashed
        self.created_at = datetime.utcnow()
        self.is_active = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        # BUG: comparing plain text to plain text, not using hash
        return self.password == password
