# app.py
import streamlit as st
from model import SharedAssistant, OpenAIBot, MessageItem
import uuid
import time
import json
import os

# -------------------------------
# File Paths
# -------------------------------
CHAT_DATA_FILE = "chat_data.json"

# -------------------------------
# Load & Save Chat Metadata
# -------------------------------
def load_chat_data(api_key):
    if not os.path.exists(CHAT_DATA_FILE):
        return {}
    try:
        with open(CHAT_DATA_FILE, "r") as f:
            raw = json.load(f)
        chats = {}
        for chat_id, data in raw.items():
            thread_id = data.get("thread_id")
            bot = OpenAIBot(
                name=data["name"],
                api_key=api_key,
                thread_id=thread_id
            ) if thread_id else None
            chats[chat_id] = {
                "name": data["name"],
                "thread_id": thread_id,
                "bot": bot
            }
        return chats
    except Exception as e:
        st.error(f"Error loading chat  {e}")
        return {}

def save_chat_data(chats):
    data = {
        cid: {
            "name": c["name"],
            "thread_id": c["thread_id"]
        }
        for cid, c in chats.items() if c.get("thread_id")
    }
    with open(CHAT_DATA_FILE, "w") as f:
        json.dump(data, f)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="📘 Math Tutor", page_icon="📘", layout="wide")
st.title("📘 Math Tutor")
st.write("Ask math questions. I'll help you solve them step by step.")

# -------------------------------
# Session State Initialization
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "assistant_initialized" not in st.session_state:
    st.session_state.assistant_initialized = False
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

def new_chat():
    """Create a new chat. Auto-recreates assistant if missing."""
    if not st.session_state.api_key:
        st.error("API key not set.")
        return

    # Heal assistant if missing
    if not SharedAssistant.is_assistant_valid():
        st.info("🛠️ Assistant missing. Recreating...")
        success = SharedAssistant.initialize(
            api_key=st.session_state.api_key,
            name="Math Tutor",
            instructions="You are a personal math tutor. Explain step by step.",
            model="gpt-3.5-turbo-1106"
        )
        if not success:
            st.error("❌ Failed to initialize assistant. Check your API key.")
            return
        st.session_state.assistant_initialized = True

    # Create new chat
    chat_id = str(uuid.uuid4())
    bot = OpenAIBot(
        name=f"Chat {len(st.session_state.chats) + 1}",
        api_key=st.session_state.api_key
    )
    st.session_state.chats[chat_id] = {
        "name": bot.name,
        "thread_id": bot.thread_id,
        "bot": bot
    }
    st.session_state.current_chat_id = chat_id
    save_chat_data(st.session_state.chats)
    st.rerun()

# -------------------------------
# Sidebar: API Key with Button
# -------------------------------
st.sidebar.header("🔑 API Settings")
api_key_input = st.sidebar.text_input(
    "Enter OpenAI API Key",
    type="password",
    value=st.session_state.api_key,
    placeholder="sk-..."
)

if st.sidebar.button("✅ Set API Key"):
    if not api_key_input.strip():
        st.sidebar.error("API key cannot be empty.")
    else:
        st.session_state.api_key = api_key_input.strip()
        st.session_state.assistant_initialized = False
        st.session_state.chats = {}
        if "current_chat_id" in st.session_state:
            del st.session_state.current_chat_id
        st.rerun()

# Validate API key
if not st.session_state.api_key:
    st.info("🔑 Please enter your OpenAI API key and click **'Set API Key'**.")
    st.stop()

if not SharedAssistant.validate_api_key(st.session_state.api_key):
    st.error("❌ Invalid API key. Please re-enter.")
    st.session_state.api_key = ""
    st.stop()

# -------------------------------
# Auto-Initialize or Heal Assistant
# -------------------------------
if not st.session_state.assistant_initialized or not SharedAssistant.is_assistant_valid():
    with st.spinner("🧠 Setting up your math tutor..."):
        success = SharedAssistant.initialize(
            api_key=st.session_state.api_key,
            name="Math Tutor",
            instructions="You are a personal math tutor. Explain step by step.",
            model="gpt-3.5-turbo-1106"
        )
        if success:
            st.session_state.assistant_initialized = True
            st.session_state.chats = load_chat_data(st.session_state.api_key)
            if not st.session_state.chats:
                new_chat()
            st.rerun()
        else:
            st.error("❌ Failed to initialize assistant. Check your API key and connection.")
            st.stop()

# Show status
if st.session_state.assistant_initialized:
    st.sidebar.success("✅ Tutor Ready")
else:
    st.sidebar.warning("⚙️ Initializing...")

# -------------------------------
# Chat Management
# -------------------------------
if st.session_state.assistant_initialized:
    st.sidebar.header("🧮 Chats")

    chat_names = {
        cid: data["name"]
        for cid, data in st.session_state.chats.items()
        if "name" in data
    }

    if not chat_names:
        new_chat()
        st.rerun()

    selected = st.sidebar.selectbox(
        "Select Chat",
        options=list(chat_names.keys()),
        format_func=lambda cid: chat_names[cid],
        index=list(chat_names.keys()).index(st.session_state.current_chat_id)
        if st.session_state.current_chat_id in chat_names else 0,
        key="chat_select"
    )

    if selected != st.session_state.current_chat_id:
        st.session_state.current_chat_id = selected
        st.rerun()

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("➕ New"):
            new_chat()
            st.rerun()
    with col2:
        if len(st.session_state.chats) > 1:
            if st.button("❌ Delete"):
                chat = st.session_state.chats[st.session_state.current_chat_id]
                if chat.get("bot"):
                    chat["bot"].delete_thread()
                del st.session_state.chats[st.session_state.current_chat_id]
                if st.session_state.current_chat_id == selected:
                    remaining = list(st.session_state.chats.keys())
                    st.session_state.current_chat_id = remaining[0] if remaining else None
                save_chat_data(st.session_state.chats)
                st.rerun()

    current = st.session_state.chats[st.session_state.current_chat_id]
    rename = st.sidebar.text_input("Rename Chat", value=current["name"])
    if st.sidebar.button("✅ Save"):
        current["name"] = rename
        st.session_state.chats[st.session_state.current_chat_id]["name"] = rename
        save_chat_data(st.session_state.chats)
        st.rerun()

# -------------------------------
# Load Current Bot and Messages
# -------------------------------
if not st.session_state.chats:
    st.stop()

if st.session_state.current_chat_id not in st.session_state.chats:
    new_chat()
    st.rerun()

bot = st.session_state.chats[st.session_state.current_chat_id]["bot"]

with st.spinner("📥 Loading chat history..."):
    try:
        messages = bot.getMessages()
    except Exception as e:
        st.error("Failed to load messages.")
        messages = []
        print(f"Error: {e}")

# -------------------------------
# Display Messages with Colors
# -------------------------------
for msg in messages:
    if msg.role == "user":
        with st.chat_message("user"):
            st.markdown(
                f'<div style="background-color: #e6f2ff; padding: 10px; border-radius: 10px; margin-bottom: 5px;">'
                f'<strong>You:</strong> {msg.content}</div>',
                unsafe_allow_html=True
            )
    else:
        with st.chat_message("assistant"):
            st.markdown(
                f'<div style="background-color: #fff9e6; padding: 10px; border-radius: 10px; margin-bottom: 5px;">'
                f'<strong>Math Tutor:</strong> {msg.content}</div>',
                unsafe_allow_html=True
            )

# -------------------------------
# Handle New Input
# -------------------------------
if prompt := st.chat_input("Ask a math question..."):
    with st.chat_message("user"):
        st.markdown(
            f'<div style="background-color: #e6f2ff; padding: 10px; border-radius: 10px; margin-bottom: 5px;">'
            f'<strong>You:</strong> {prompt}</div>',
            unsafe_allow_html=True
        )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            for chunk in bot.stream_response(prompt):
                full_response += chunk
                placeholder.markdown(
                    f'<div style="background-color: #fff9e6; padding: 10px; border-radius: 10px; margin-bottom: 5px;">'
                    f'<strong>Math Tutor:</strong> {full_response}▌</div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.02)
            placeholder.markdown(
                f'<div style="background-color: #fff9e6; padding: 10px; border-radius: 10px; margin-bottom: 5px;">'
                f'<strong>Math Tutor:</strong> {full_response}</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            placeholder.markdown(
                f'<div style="background-color: #ffe6e6; padding: 10px; border-radius: 10px;">'
                f'<strong>Math Tutor:</strong> Sorry, I encountered an error: {str(e)}</div>',
                unsafe_allow_html=True
            )
            print(f"Error in chat: {e}")