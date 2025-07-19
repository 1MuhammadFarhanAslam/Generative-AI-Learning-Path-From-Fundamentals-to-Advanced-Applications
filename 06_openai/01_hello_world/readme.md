## 🚀 OpenAI Hello World in Python

A simple starter to interact with OpenAI's GPT models using the Python SDK, safely using `.env` for API keys and configuration.

### 📦 Project Structure

```
openai-hello-world/
│
├── .env              ← Your secrets (not committed)
├── .env.template     ← Safe-to-share template (no secrets)
├── openai_hello_world.py   ← Main script
├── requirements.txt  ← Dependencies
└── README.md         ← This guide
```

### 🔐 Step 1: Get Your OpenAI API Key

1. Go to: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Click **"Create secret key"**
3. Copy your key (starts with `sk-...`) – you’ll only see it once.


### 📝 Step 2: Create Your `.env` File

Create a file named `.env` in your project root (windows):

```bash
echo.>.env
```

Add your API key like this:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Important**: Never share or commit this file.


### 📄 Optional: Create `.env.template`

Share this file with collaborators instead of `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

> This ensures no secrets are leaked, while maintaining config structure.

---

### 🔧 Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
openai>
python-dotenv
```

---

### 🧠 Step 4: Write Your Python Script

**openai\_hello\_world.py**

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Get API key securely
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client (v1.0+)
client = OpenAI(api_key=api_key)

# Send a simple message
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, world!"}
    ],
)

# Print assistant's reply
print("GPT says:", response.choices[0].message.content)
```

---

### 🚀 Step 5: Run Your App

```bash
python openai_hello_world.py
```

You should see a friendly AI response like:

```
GPT says: Hello! How can I assist you today?
```


### 🛡️ Best Practices for Env Management

| Environment    | File                    | Purpose                      |
| -------------- | ----------------------- | ---------------------------- |
| Production     | `.env`                  | Real API keys, not committed |
| Template       | `.env.template`         | Shared with team, no secrets |
| Backup         | `.env.bak`              | Manual or auto backups       |
| Other Profiles | `.env.dev`, `.env.prod` | Multiple setups for dev/prod |

You can load a specific file like this:

```python
load_dotenv(dotenv_path=".env.prod")
```


### 🧪 Bonus: Print Environment Safely

```python
# Debug environment (safe)
print("🔐 OpenAI Key Loaded:", bool(api_key))  # True or False
```

Never print your API key directly.


### 🧼 .gitignore (Add this!)

```
.env
.env.*
!*.template
```
---
