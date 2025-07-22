from model import BotModel
import streamlit as st
from dotenv import load_dotenv
import uuid
from state_utils import save_user_session_state, load_user_session_state, get_user_session_path
from model import (
    create_new_chat,
    list_chat_ids_for_user,
    list_chats_for_user,
    get_chat_by_id,
    save_chat_by_id,
    rename_chat_title,
    delete_chat_by_id
)

import openai

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Multi-User Chatbot", layout="wide")
st.title("Multi-User Chatbot powered by OpenAI LLM developed by Muhammad Farhan Aslam")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# --- API KEY ---
api_key = st.sidebar.text_input("🔑 Enter your OpenAI API key", type="password")
if not api_key:
    st.warning("Please enter your API key to start chatting.")
    st.stop()

openai.api_key = api_key

# --- USER ID ---
user_id = st.sidebar.text_input("🧑 Your User ID", value="default_user")

# --- CHAT HISTORY HANDLING ---
if "chat_ids" not in st.session_state:
    st.session_state.chat_ids = list_chat_ids_for_user(user_id)

if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = (
        st.session_state.chat_ids[0] if st.session_state.chat_ids else None
    )

# --- SIDEBAR: CHAT LIST ---
st.sidebar.markdown("## 💬 Your Chats")
chat_list = list_chats_for_user(user_id)

for chat in chat_list:
    if st.sidebar.button(chat['title'], key=chat['id']):
        st.session_state.selected_chat_id = chat['id']

# --- SIDEBAR: NEW CHAT ---
if st.sidebar.button("➕ New Chat"):
    new_id = create_new_chat(user_id)
    st.session_state.chat_ids.insert(0, new_id)
    st.session_state.selected_chat_id = new_id
    st.rerun()

# --- MAIN CHAT AREA ---
selected_chat = get_chat_by_id(user_id, st.session_state.selected_chat_id)
if not selected_chat:
    st.info("Start by creating a new chat from the sidebar.")
    st.stop()

st.markdown(f"### 📝 {selected_chat['title']}")

# --- Display chat messages ---
for msg in selected_chat["messages"]:
    with st.chat_message(msg["role"], avatar=USER_AVATAR if msg["role"] == "user" else BOT_AVATAR):
        st.markdown(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Your message")
if user_input:
    # Add user message
    selected_chat["messages"].append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_input)

    # Streaming assistant reply
    try:
        response = ""
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            stream = openai.chat.completions.create(
                model="gpt-4",
                messages=selected_chat["messages"],
                stream=True
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                response += delta
                message_placeholder.markdown(response + "▌")
            message_placeholder.markdown(response)
    except Exception as e:
        response = f"❌ Error: {str(e)}"
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            st.markdown(response)

    # Save assistant message
    selected_chat["messages"].append({"role": "assistant", "content": response})
    save_chat_by_id(user_id, st.session_state.selected_chat_id, selected_chat)

# --- Delete Chat ---
if st.sidebar.button("🗑️ Delete Chat"):
    if st.session_state.selected_chat_id:
        delete_chat_by_id(user_id, st.session_state.selected_chat_id)
        st.session_state.chat_ids = list_chat_ids_for_user(user_id)
        st.session_state.selected_chat_id = (
            st.session_state.chat_ids[0] if st.session_state.chat_ids else None
        )
        st.rerun()

# --- Rename Chat Title ---
new_title = st.sidebar.text_input("✏️ Rename Chat", value=selected_chat['title'])
if new_title and new_title != selected_chat['title']:
    rename_chat_title(user_id, st.session_state.selected_chat_id, new_title)
    st.rerun()
