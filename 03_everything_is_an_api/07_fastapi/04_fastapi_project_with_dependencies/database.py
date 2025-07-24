# database.py
import os
import asyncpg
from typing import List, Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# Import our Pydantic models
from model import User, ChatSession, ChatMessage

# --- Configuration ---
# IMPORTANT: Replace with your actual Neon Database URL.
# In a production app, use environment variables: os.getenv("NEON_DATABASE_URL")
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
# Example: DATABASE_URL = "postgresql://your_user:your_password@ep-long-glade-12345.us-east-2.aws.neon.tech/your_db_name?sslmode=require"

# Global connection pool
pool = None

async def connect_db():
    """
    Establishes a connection pool to the Neon PostgreSQL database.
    This pool will manage connections efficiently.
    """
    global pool
    if pool is None:
        try:
            pool = await asyncpg.create_pool(CONNECTION_STRING)
            print("Successfully connected to Neon database!")
            await create_tables() # Ensure tables exist when connected
        except Exception as e:
            print(f"Failed to connect to Neon database: {e}")
            raise

async def close_db():
    """
    Closes the database connection pool.
    """
    global pool
    if pool:
        await pool.close()
        pool = None
        print("Neon database connection closed.")

async def get_db_connection():
    """
    Provides a connection from the pool.
    This function will be used as a FastAPI dependency.
    """
    if pool is None:
        await connect_db() # Ensure connection is established if not already

    async with pool.acquire() as connection:
        yield connection

async def create_tables():
    """
    Creates necessary tables in the database if they don't already exist.
    """
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
                role VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        ''')
    print("Database tables checked/created successfully.")

# --- User Operations ---

async def get_user_by_email(conn: asyncpg.Connection, email: str) -> Optional[User]:
    """Retrieves a user by their email address."""
    row = await conn.fetchrow("SELECT id, email, password_hash, created_at FROM users WHERE email = $1", email)
    if row:
        return User(id=row['id'], email=row['email'], password=row['password_hash'], created_at=row['created_at'])
    return None

async def create_new_user(conn: asyncpg.Connection, email: str, password_hash: str) -> User:
    """Creates a new user in the database."""
    row = await conn.fetchrow(
        "INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email, created_at",
        email, password_hash
    )
    return User(id=row['id'], email=row['email'], password=password_hash, created_at=row['created_at']) # password_hash is passed back as 'password' for consistency

# --- Chat Session Operations ---

async def create_chat_session(conn: asyncpg.Connection, user_id: int, title: str) -> ChatSession:
    """Creates a new chat session for a user."""
    row = await conn.fetchrow(
        "INSERT INTO chat_sessions (user_id, title) VALUES ($1, $2) RETURNING id, user_id, title, created_at, updated_at",
        user_id, title
    )
    return ChatSession(
        id=row['id'],
        user_id=row['user_id'],
        title=row['title'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    )

async def get_chat_session_by_id(conn: asyncpg.Connection, session_id: int, user_id: int) -> Optional[ChatSession]:
    """Retrieves a chat session by ID, ensuring it belongs to the given user."""
    row = await conn.fetchrow(
        "SELECT id, user_id, title, created_at, updated_at FROM chat_sessions WHERE id = $1 AND user_id = $2",
        session_id, user_id
    )
    if row:
        return ChatSession(
            id=row['id'],
            user_id=row['user_id'],
            title=row['title'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    return None

async def get_user_chat_sessions(conn: asyncpg.Connection, user_id: int) -> List[ChatSession]:
    """Retrieves all chat sessions for a given user."""
    rows = await conn.fetch(
        "SELECT id, user_id, title, created_at, updated_at FROM chat_sessions WHERE user_id = $1 ORDER BY updated_at DESC",
        user_id
    )
    return [ChatSession(
        id=row['id'],
        user_id=row['user_id'],
        title=row['title'],
        created_at=row['created_at'],
        updated_at=row['updated_at']
    ) for row in rows]

async def update_chat_session_timestamp(conn: asyncpg.Connection, session_id: int):
    """Updates the 'updated_at' timestamp of a chat session."""
    await conn.execute("UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = $1", session_id)

# --- Chat Message Operations ---

async def add_chat_message(conn: asyncpg.Connection, session_id: int, role: str, content: str) -> ChatMessage:
    """Adds a new message to a chat session."""
    row = await conn.fetchrow(
        "INSERT INTO chat_messages (session_id, role, content) VALUES ($1, $2, $3) RETURNING id, session_id, role, content, timestamp",
        session_id, role, content
    )
    return ChatMessage(
        id=row['id'],
        session_id=row['session_id'],
        role=row['role'],
        content=row['content'],
        timestamp=row['timestamp']
    )

async def get_chat_messages_for_session(conn: asyncpg.Connection, session_id: int) -> List[ChatMessage]:
    """Retrieves all messages for a given chat session, ordered by timestamp."""
    rows = await conn.fetch(
        "SELECT id, session_id, role, content, timestamp FROM chat_messages WHERE session_id = $1 ORDER BY timestamp ASC",
        session_id
    )
    return [ChatMessage(
        id=row['id'],
        session_id=row['session_id'],
        role=row['role'],
        content=row['content'],
        timestamp=row['timestamp']
    ) for row in rows]

