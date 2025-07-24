# main.py
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List
from datetime import datetime, timedelta

# Import security utilities and configurations from our new auth.py module
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    openai_client
)

# Import our models and database functions
from model import User, UserCreate, UserLogin, UserResponse, Token, ChatSession, ChatMessage, ChatCompletionRequest, ChatCompletionResponse
from database import connect_db, close_db, get_db_connection, create_new_user, get_user_by_email, \
                     create_chat_session, get_chat_session_by_id, get_user_chat_sessions, \
                     add_chat_message, get_chat_messages_for_session, update_chat_session_timestamp

import asyncpg # For type hinting the connection

# FastAPI application instance
app = FastAPI(
    title="AI Chat API (OpenAI & Neon)",
    description="An API for AI chat completions powered by OpenAI, with user authentication and chat history stored in Neon DB.",
    version="1.0.0",
)

# --- Lifespan Events (Database Connection Management) ---
@app.on_event("startup")
async def startup_event():
    """Connect to the database when the application starts."""
    print("Application startup: Connecting to database...")
    await connect_db()
    print("Application startup: Database connection established.")

@app.on_event("shutdown")
async def shutdown_event():
    """Close the database connection when the application shuts down."""
    print("Application shutdown: Closing database connection...")
    await close_db()
    print("Application shutdown: Database connection closed.")

# OAuth2PasswordBearer for JWT token extraction from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme), conn: asyncpg.Connection = Depends(get_db_connection)):
    """
    Dependency to get the current authenticated user from the JWT token.
    It also fetches the user from the database to ensure they exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(f"Attempting to validate token: {token[:20]}...") # Print first 20 chars of token

    # Use the new decode_access_token function
    payload = decode_access_token(token)
    if payload is None:
        print("Error: Token decoding failed (invalid token or JWTError).")
        raise credentials_exception

    print(f"JWT Payload decoded: {payload}")

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        print("Error: 'sub' (user_id) not found in JWT payload.")
        raise credentials_exception
    
    # Ensure user_id is an integer, as our DB uses int primary keys
    if not isinstance(user_id, int):
        try:
            user_id = int(user_id)
        except ValueError:
            print(f"Error: user_id '{user_id}' from token is not a valid integer.")
            raise credentials_exception

    # Fetch user from DB to ensure they still exist and are active
    user_in_db = await conn.fetchrow("SELECT id, email, created_at FROM users WHERE id = $1", user_id)
    if user_in_db is None:
        print(f"Error: User with ID {user_id} not found in database.")
        raise credentials_exception
    
    print(f"User {user_in_db['email']} (ID: {user_in_db['id']}) successfully authenticated.")
    return UserResponse(id=user_in_db['id'], email=user_in_db['email'], created_at=user_in_db['created_at'])

# --- API Endpoints ---

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Chat API! Go to /docs for API documentation."}

# User Signup
@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Registers a new user."""
    existing_user = await get_user_by_email(conn, user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = await create_new_user(conn, user_data.email, hashed_password)
    print(f"New user signed up: {new_user.email} with ID {new_user.id}")
    return UserResponse(id=new_user.id, email=new_user.email, created_at=new_user.created_at)

# User Login (generates JWT token)
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), conn: asyncpg.Connection = Depends(get_db_connection)):
    """Authenticates a user and returns an access token."""
    user = await get_user_by_email(conn, form_data.username) # OAuth2PasswordRequestForm uses 'username' for email
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, # 'sub' is standard for subject (user ID)
        expires_delta=access_token_expires
    )
    print(f"User {user.email} logged in. Token generated.")
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Test Endpoint
@app.get("/protected-test", response_model=UserResponse)
async def protected_route(current_user: UserResponse = Depends(get_current_user)):
    """A test endpoint that requires authentication."""
    return current_user # Returns the authenticated user's details

# --- Chat Endpoints ---

@app.post("/chat/complete", response_model=ChatCompletionResponse)
async def chat_completion(
    request: ChatCompletionRequest,
    current_user: UserResponse = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """
    Sends a message to the AI for completion and saves the conversation.
    If session_id is not provided, a new chat session is created.
    """
    user_id = current_user.id
    session_id = request.session_id
    chat_title = "New Chat Session" # Default title for new sessions

    # 1. Get or Create Chat Session
    if session_id:
        session = await get_chat_session_by_id(conn, session_id, user_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found or does not belong to user")
        print(f"Continuing chat in session ID: {session_id} for user {user_id}")
    else:
        # Create a new session
        session = await create_chat_session(conn, user_id, chat_title)
        session_id = session.id
        print(f"New chat session created: {session_id} for user {user_id}")


    # 2. Add user message to DB
    user_message_db = await add_chat_message(conn, session_id, "user", request.message)
    print(f"User message added to session {session_id}: {request.message}")

    # 3. Get previous messages for context (optional, but good for coherent chat)
    messages_for_openai = []
    history_messages = await get_chat_messages_for_session(conn, session_id)
    for msg in history_messages:
        messages_for_openai.append({"role": msg.role, "content": msg.content})

    # Add current user message to context for OpenAI
    # This ensures the current user's message is always the last in the context for OpenAI
    # (The loop above already adds all, including the just-added user_message_db)
    # If the history_messages already includes the latest user message (which it should),
    # this line might be redundant or needs careful handling to avoid duplicates.
    # For simplicity and correctness, ensure history_messages includes the current user message,
    # or add it here if it's not fetched as part of history.
    # Given add_chat_message is called *before* get_chat_messages_for_session, it should be included.
    # So, the line below is technically redundant if history_messages is complete.
    # messages_for_openai.append({"role": "user", "content": request.message})
    print(f"Messages sent to OpenAI (including history): {messages_for_openai}")

    # 4. Call OpenAI API for completion
    try:
        # Use gpt-3.5-turbo as requested
        openai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_for_openai,
            temperature=0.7, # Adjust creativity
            max_tokens=150 # Limit response length
        )
        ai_content = openai_response.choices[0].message.content.strip()
        print(f"OpenAI response received: {ai_content}")
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get AI completion: {e}")

    # 5. Add AI response to DB
    ai_message_db = await add_chat_message(conn, session_id, "assistant", ai_content)
    print(f"AI message added to session {session_id}: {ai_content}")

    # 6. Update session timestamp
    await update_chat_session_timestamp(conn, session_id)
    print(f"Session {session_id} timestamp updated.")

    return ChatCompletionResponse(
        session_id=session_id,
        message_id=ai_message_db.id,
        role=ai_message_db.role,
        content=ai_message_db.content,
        timestamp=ai_message_db.timestamp
    )

@app.get("/chat/sessions", response_model=List[ChatSession])
async def get_chat_sessions(
    current_user: UserResponse = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Retrieves all chat sessions for the authenticated user."""
    sessions = await get_user_chat_sessions(conn, current_user.id)
    print(f"Retrieved {len(sessions)} sessions for user {current_user.id}")
    return sessions

@app.get("/chat/sessions/{session_id}/messages", response_model=List[ChatMessage])
async def get_session_messages(
    session_id: int,
    current_user: UserResponse = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Retrieves all messages for a specific chat session, ensuring it belongs to the user."""
    # First, verify the session belongs to the user
    session = await get_chat_session_by_id(conn, session_id, current_user.id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found or does not belong to user")

    messages = await get_chat_messages_for_session(conn, session_id)
    print(f"Retrieved {len(messages)} messages for session {session_id} (user {current_user.id})")
    return messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)