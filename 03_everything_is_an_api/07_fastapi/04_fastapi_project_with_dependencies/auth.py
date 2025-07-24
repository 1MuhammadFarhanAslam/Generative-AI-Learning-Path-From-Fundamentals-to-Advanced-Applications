# Password hashing
from passlib.context import CryptContext
from typing import Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

# --- Security Utilities ---

# --- Configuration ---
# IMPORTANT: Replace with your actual OpenAI API Key.
# In a production app, use environment variables: os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# JWT Configuration
# IMPORTANT: Generate a strong secret key and store it securely (e.g., environment variable)
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# laod .env
_ = load_dotenv(find_dotenv())

# OpenAI client
openai_client : OpenAI = OpenAI(api_key=OPENAI_API_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Convert the 'sub' (user ID) to a string before encoding
    # This is the crucial change!
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodes a JWT access token. Returns payload if valid, None otherwise."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None