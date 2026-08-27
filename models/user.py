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

    # WHO: Agent 2 (Dev Agent)
    # WHAT: Corrected indentation of check_password method.
    # WHY: The method was incorrectly nested inside hash_password, making it unreachable and causing login failures (SDLC-4).
    # WHEN: 2026-08-27T15:22:59.534467
    # WHERE: models/user.py User.check_password
    def check_password(self, password: str) -> bool:
        # WHO: Agent 2 (Dev Agent)
        # WHAT: Compares the hashed input password with the stored hashed password.
        # WHY: To correctly authenticate users whose passwords are already stored as hashes (part of the original SDLC-4 fix).
        # WHEN: 2026-08-27T00:54:33.930591
        # WHERE: models/user.py User.check_password
        if self.password == self.hash_password(password):
            return True

        # WHO: Agent 2 (Dev Agent)
        # WHAT: Added a fallback to check if the stored password is a plain-text version of the input password for migration.
        # WHY: To resolve login failures for users registered prior to the password hashing deployment (SDLC-4 regression).
        #      Upon successful login with a plain-text password, it is re-hashed and stored for future use.
        # WHEN: 2026-08-27T15:21:02.827859
        # WHERE: models/user.py User.check_password
        if self.password == password:
            self.password = self.hash_password(password)
            print(f"INFO: Password for user '{self.email}' migrated to hash.") # For monitoring/debugging during migration
            return True
        
        return False
