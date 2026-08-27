# User model
import hashlib
import uuid
from datetime import datetime

# CHANGELOG
# - WHO: Agent 2 (Dev Agent)
#   WHAT: Added changelog and email normalization to User.__init__.
#   WHY: To ensure consistent, case-insensitive email handling across the application, fixing login issues (SDLC-3).
#   WHEN: 2026-08-27T04:36:27.863317
#   WHERE: models/user.py User.__init__
class User:
    def __init__(self, username: str, email: str, password: str, user_id: str = None):
        self.id = user_id or str(uuid.uuid4())
        self.username = username
        # WHO: Agent 2 (Dev Agent)
        # WHAT: Normalized email to lowercase.
        # WHY: To ensure consistent, case-insensitive email handling at the model level, preventing login issues (SDLC-3).
        # WHEN: 2026-08-27T04:36:27.863317
        # WHERE: models/user.py User.__init__
        self.email = email.lower()  
        # WHO: Agent 2 (Dev Agent)
        # WHAT: Hashed the password before storing.
        # WHY: To prevent storing passwords in plain text, addressing SDLC-4.
        # WHEN: 2026-08-27T00:54:33.930591
        # WHERE: models/user.py User.__init__
        self.password = self.hash_password(password)  
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
        # WHO: Agent 2 (Dev Agent)
        # WHAT: Modified to compare the hashed input password with the stored hashed password.
        # WHY: To correctly authenticate users when passwords are stored as hashes, addressing SDLC-4.
        # WHEN: 2026-08-27T00:54:33.930591
        # WHERE: models/user.py User.check_password
        return self.password == self.hash_password(password)
