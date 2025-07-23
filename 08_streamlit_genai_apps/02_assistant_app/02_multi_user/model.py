# model.py
import openai
import os

# File to persist assistant ID
ASSISTANT_ID_FILE = "assistant_id.txt"


class MessageItem:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class SharedAssistant:
    assistant_id = None
    client = None

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate the API key."""
        try:
            SharedAssistant.client = openai.OpenAI(api_key=api_key)
            SharedAssistant.client.models.list()
            return True
        except Exception as e:
            print(f"API key validation failed: {e}")
            return False

    @staticmethod
    def initialize(api_key: str, name: str, instructions: str, model: str) -> bool:
        """
        Automatically initialize or load the assistant.
        Ensures exactly ONE assistant exists.
        """
        if SharedAssistant.client is None:
            SharedAssistant.client = openai.OpenAI(api_key=api_key)

        # Step 1: Try to load existing assistant ID
        if os.path.exists(ASSISTANT_ID_FILE):
            with open(ASSISTANT_ID_FILE, "r") as f:
                SharedAssistant.assistant_id = f.read().strip()

            # Step 2: Verify it exists on OpenAI
            try:
                assistant = SharedAssistant.client.beta.assistants.retrieve(SharedAssistant.assistant_id)
                # Valid → use it
                return True
            except Exception:
                print("Stored assistant ID not found. Will create a new one.")
                SharedAssistant.assistant_id = None

        # Step 3: Create new assistant
        try:
            assistant = SharedAssistant.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model
            )
            SharedAssistant.assistant_id = assistant.id

            # Save ID for future runs
            with open(ASSISTANT_ID_FILE, "w") as f:
                f.write(assistant.id)

            print(f"Assistant created with ID: {assistant.id}")
            return True
        except Exception as e:
            print(f"Failed to create assistant: {e}")
            return False

    @staticmethod
    def get_assistant_id():
        return SharedAssistant.assistant_id


class OpenAIBot:
    def __init__(self, name: str, api_key: str, thread_id: str = None):
        self.name = name
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)

        if thread_id:
            self.thread_id = thread_id
        else:
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id

    def getMessages(self) -> list:
        """Fetch messages from OpenAI."""
        try:
            response = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            messages = []
            for msg in reversed(response.data):
                for content_block in msg.content:
                    if content_block.type == "text":
                        messages.append(MessageItem(
                            role=msg.role,
                            content=content_block.text.value
                        ))
            return messages
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []

    def stream_response(self, prompt: str):
        """Stream response from assistant."""
        try:
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=prompt
            )

            with self.client.beta.threads.runs.stream(
                thread_id=self.thread_id,
                assistant_id=SharedAssistant.get_assistant_id(),
            ) as stream:
                for event in stream:
                    if hasattr(event, 'event') and event.event == "thread.message.delta":
                        for content in event.data.delta.content:
                            if content.type == "text" and content.text.value:
                                yield content.text.value
        except Exception as e:
            yield f"Sorry, I encountered an error: {str(e)}"

    def delete_thread(self):
        """Delete thread."""
        try:
            self.client.beta.threads.delete(self.thread_id)
        except Exception as e:
            print(f"Error deleting thread: {e}")