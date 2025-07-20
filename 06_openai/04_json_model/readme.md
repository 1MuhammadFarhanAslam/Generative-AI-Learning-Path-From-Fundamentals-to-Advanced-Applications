# JSON mode

- https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses

We use **structured outputs** when working with the OpenAI API in application development for the **same reasons we use structured data in general software design** — to make responses predictable, machine-readable, and easier to integrate into downstream systems.


### What are Structured Outputs?

Instead of just getting a block of text from the model (natural language), **structured outputs** give you responses in **JSON or schema-conforming formats** that your code can directly parse and use.

OpenAI supports structured outputs via:

* **Function calling** (`tool_calls`)
* **JSON mode** (`response_format="json"`)
* **Tool use with OpenAPI schemas** (like in assistants API)


### Why Use Structured Outputs?

Here are the main reasons developers use structured outputs:

#### 1. **Reliable Data for Automation**

When the model replies with JSON, you can **directly parse and use** that data in your app.

🔧 Example:

```json
{
  "product": "iPhone 15",
  "price": 1099,
  "availability": "In stock"
}
```

Instead of parsing unstructured text like:

> “The iPhone 15 is available now for \$1,099.”


#### 2. **Avoid Error-Prone Text Parsing**

Natural language responses are ambiguous. Parsing raw text for values, status, or flags is fragile.

With structured output, your backend logic doesn't need to "guess" or use regex — it just reads fields.


#### 3. **Build More Reliable Features**

Features like:

* **Chatbots that fill forms**
* **AI agents that control apps or call APIs**
* **E-commerce bots that return structured product info**
* **Trading bots interpreting AI sentiment**

…all benefit from **predictable fields** and formats.


#### 4. **Schema Validation**

You can define schemas (like OpenAPI or Pydantic) so the AI is **guided** to generate output in a valid format — and you can reject/retry if validation fails.


#### 5. **Tool Use Integration**

With **function calling**, you define tools the model can call with specific parameters. The response gives you the **function name + arguments** in structured form — which your app can execute directly.


### Use Cases in Real Apps

| App Type     | Why Use Structured Output                  |
| ------------ | ------------------------------------------ |
| Chatbot      | Extract intent and slots cleanly           |
| E-commerce   | Return product info in JSON                |
| Trading bot  | Return structured risk calculation         |
| AI assistant | Trigger tools/functions with arguments     |
| Form filler  | Auto-fill forms with structured user input |

---

### Example in Python (OpenAI SDK)

```python
response = client.chat.completions.create(
  model="gpt-4",
  messages=[{"role": "user", "content": "Summarize this article."}],
  response_format="json"
)

data = response.choices[0].message.content
summary = json.loads(data)["summary"]
```

---

### Summary

> Use **structured outputs** when you want your app to **reliably extract and use information** from the OpenAI model, **without parsing messy text**.

It's a best practice when building **production-grade AI apps**.