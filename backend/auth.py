import os
import json
import bcrypt
import jwt
import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Load secret from environment or use default
SECRET_KEY = os.getenv("JWT_SECRET", "your_super_secret_key")
ALGORITHM = "HS256"
USERS_FILE = "users.json"

# OAuth2 scheme for protected routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --------------------------
# Utility: Load users file
# --------------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# --------------------------
# Utility: Save users file
# --------------------------
def save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# --------------------------
# Password Hashing + Check
# --------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# --------------------------
# Token Creation
# --------------------------
def create_token(username: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token if isinstance(token, str) else token.decode("utf-8")

# --------------------------
# Token Verification
# --------------------------
def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --------------------------
# Register New User
# --------------------------
def register_user(username: str, password: str):
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[username] = hash_password(password)
    save_users(users)

# --------------------------
# Authenticate User
# --------------------------
def authenticate_user(username: str, password: str):
    users = load_users()
    if username not in users or not verify_password(password, users[username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_token(username)
