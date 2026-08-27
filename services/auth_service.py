# Authentication business logic
# CHANGELOG
# - WHO: Agent 2 (Dev Agent)
#   WHAT: Added changelog and email normalization to register_user and login_user.
#   WHY: To ensure consistent, case-insensitive email handling across the application, fixing login issues (SDLC-3).
#   WHEN: 2026-08-27T04:36:27.863317
#   WHERE: services/auth_service.py register_user, login_user
from models.user import User
from config import Config

# In-memory user store (simulating a database)
users_db: dict[str, User] = {}

def register_user(username: str, email: str, password: str) -> dict:
    """Register a new user."""
    # WHO: Agent 2 (Dev Agent)
    # WHAT: Normalized email to lowercase.
    # WHY: To ensure consistent, case-insensitive email handling, preventing login issues (SDLC-3).
    # WHEN: 2026-08-27T04:36:27.863317
    # WHERE: services/auth_service.py register_user
    email = email.lower()  
    
    # Check if user already exists
    for user in users_db.values():
        if user.email == email:
            return {"success": False, "error": "Email already registered"}
        if user.username == username:
            return {"success": False, "error": "Username already taken"}

    # Validate password length
    if len(password) < Config.MIN_PASSWORD_LENGTH:
        return {"success": False, "error": f"Password must be at least {Config.MIN_PASSWORD_LENGTH} characters"}

    # Create and store user
    # WHO: Agent 2 (Dev Agent)
    # WHAT: Removed the 'BUG' comment as the User constructor now handles password hashing.
    # WHY: The underlying User model now handles password hashing, resolving the plain text storage issue mentioned (SDLC-4).
    # WHEN: 2026-08-27T00:54:33.930591
    # WHERE: services/auth_service.py register_user
    new_user = User(username=username, email=email, password=password)
    users_db[new_user.id] = new_user

    return {"success": True, "user": new_user.to_dict()}

def login_user(email: str, password: str) -> dict:
    """Authenticate a user by email and password."""
    # WHO: Agent 2 (Dev Agent)
    # WHAT: Normalized email to lowercase.
    # WHY: To ensure consistent, case-insensitive email lookup, fixing login issues (SDLC-3).
    # WHEN: 2026-08-27T04:36:27.863317
    # WHERE: services/auth_service.py login_user
    email = email.lower()  
    
    # Find user by email
    user = None
    for u in users_db.values():
        if u.email == email:
            user = u
            break

    if not user:
        return {"success": False, "error": "Invalid credentials"}

    # Check if account is active
    if not user.is_active:
        return {"success": False, "error": "Account is deactivated"}

    # WHO: Agent 2 (Dev Agent)
    # WHAT: Removed the 'BUG' comment regarding plain text password comparison.
    # WHY: The User.check_password method has been updated to correctly compare hashed passwords, resolving the described bug (SDLC-4).
    # WHEN: 2026-08-27T00:54:33.930591
    # WHERE: services/auth_service.py login_user
    if not user.check_password(password):
        return {"success": False, "error": "Invalid credentials"}

    return {
        "success": True,
        "user": user.to_dict(),
        "token": f"mock-jwt-token-{user.id}"  # Simplified token for demo
    }

def get_user_by_id(user_id: str) -> dict:
    """Fetch a user by their ID."""
    user = users_db.get(user_id)
    if not user:
        return {"success": False, "error": "User not found"}
    return {"success": True, "user": user.to_dict()}
