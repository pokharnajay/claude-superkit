---
name: manage-chats
description: Create and manage text-based chat conversations in Vapi using assistants, squads, or workflows. Use when building chat interfaces, testing assistants via text, or integrating with OpenAI-compatible chat endpoints.
---

# Manage Chats Skill

This skill covers creating, retrieving, listing, and deleting text-based chat conversations in Vapi. The Chats API enables AI-powered text conversations without voice processing -- ideal for websites, mobile apps, messaging platforms, and automated workflows.

> **See also:** `create-assistant` (building assistants for chat), `create-workflow` (workflows usable via chat), `create-squad` (squads usable via chat)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- An existing assistant, squad, or workflow to chat with

---

## Quick Start

### Send a Chat Message via cURL

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id",
    "input": "Hi, I need help with my account"
  }'
```

### Send a Chat Message via Python

```python
import requests

url = "https://api.vapi.ai/chat"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "assistantId": "your-assistant-id",
    "input": "Hi, I need help with my account",
}

response = requests.post(url, headers=headers, json=payload)
chat = response.json()
print(f"Chat ID: {chat['id']}")
print(f"Assistant says: {chat['output'][0]['content']}")
```

### Send a Chat Message via TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/chat", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    assistantId: "your-assistant-id",
    input: "Hi, I need help with my account",
  }),
});

const chat = await response.json();
console.log(`Chat ID: ${chat.id}`);
console.log(`Assistant says: ${chat.output[0].content}`);
```

---

## CRUD Operations

### Create a Chat

Start a new chat conversation with an assistant:

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id",
    "input": "What are your business hours?"
  }'
```

**With assistant overrides (dynamic variables):**

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id",
    "input": "I need help with my account",
    "assistantOverrides": {
      "variableValues": {
        "companyName": "TechFlow Solutions",
        "serviceType": "software",
        "customerTier": "Premium"
      }
    }
  }'
```

**With inline assistant configuration (no pre-built assistant needed):**

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant": {
      "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful customer support agent."
          }
        ]
      }
    },
    "input": "How do I reset my password?"
  }'
```

**Python:**

```python
import requests

response = requests.post(
    "https://api.vapi.ai/chat",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "assistantId": "your-assistant-id",
        "input": "What are your business hours?",
    },
)
chat = response.json()
print(f"Chat ID: {chat['id']}, Reply: {chat['output'][0]['content']}")
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/chat", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    assistantId: "your-assistant-id",
    input: "What are your business hours?",
  }),
});
const chat = await response.json();
console.log(`Chat ID: ${chat.id}, Reply: ${chat.output[0].content}`);
```

### List All Chats

```bash
curl https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination and filtering:**

```bash
curl "https://api.vapi.ai/chat?page=1&limit=20&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

response = requests.get(
    "https://api.vapi.ai/chat",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 20, "sortOrder": "desc"},
)
chats = response.json()
for c in chats:
    print(f"{c['id']} — {c.get('name', 'unnamed')} — {c['createdAt']}")
```

**TypeScript:**

```typescript
const params = new URLSearchParams({ page: "1", limit: "20", sortOrder: "desc" });
const response = await fetch(`https://api.vapi.ai/chat?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const chats = await response.json();
chats.forEach((c: any) => console.log(`${c.id} — ${c.name ?? "unnamed"} — ${c.createdAt}`));
```

### Get a Specific Chat

```bash
curl https://api.vapi.ai/chat/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/chat/{chat_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
chat = response.json()
print(f"Messages: {len(chat['messages'])}, Output: {chat['output'][0]['content']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/chat/${chatId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const chat = await response.json();
console.log(`Messages: ${chat.messages.length}, Output: ${chat.output[0].content}`);
```

### Delete a Chat

```bash
curl -X DELETE https://api.vapi.ai/chat/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/chat/{chat_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted = response.json()
print(f"Deleted chat: {deleted['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/chat/${chatId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deleted = await response.json();
console.log(`Deleted chat: ${deleted.id}`);
```

---

## OpenAI-Compatible Endpoint

The `/chat/openai` endpoint provides an OpenAI-compatible chat completions interface. This lets you use Vapi assistants as a drop-in replacement for OpenAI's API in existing code.

The `model` field maps to a Vapi assistant, squad, or workflow ID.

```bash
curl -X POST https://api.vapi.ai/chat/openai \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-assistant-id",
    "messages": [
      {"role": "user", "content": "What is the weather today?"}
    ]
  }'
```

**With streaming:**

```bash
curl -X POST https://api.vapi.ai/chat/openai \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-assistant-id",
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
  }'
```

**Python (using the OpenAI SDK):**

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-vapi-api-key",
    base_url="https://api.vapi.ai/chat",
)

response = client.chat.completions.create(
    model="your-assistant-id",
    messages=[{"role": "user", "content": "What is the weather today?"}],
)
print(response.choices[0].message.content)
```

**TypeScript (using the OpenAI SDK):**

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "your-vapi-api-key",
  baseURL: "https://api.vapi.ai/chat",
});

const response = await client.chat.completions.create({
  model: "your-assistant-id",
  messages: [{ role: "user", content: "What is the weather today?" }],
});
console.log(response.choices[0].message.content);
```

---

## Common Patterns

### Multi-Turn Conversation with previousChatId

Chain messages together for context-aware conversations:

```python
import requests

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# First message
response = requests.post(
    "https://api.vapi.ai/chat",
    headers=headers,
    json={
        "assistantId": "your-assistant-id",
        "input": "I need help with billing",
    },
)
chat = response.json()
last_chat_id = chat["id"]
print(f"Assistant: {chat['output'][0]['content']}")

# Follow-up message (maintains context)
response = requests.post(
    "https://api.vapi.ai/chat",
    headers=headers,
    json={
        "assistantId": "your-assistant-id",
        "previousChatId": last_chat_id,
        "input": "I was charged twice for my subscription",
    },
)
chat = response.json()
last_chat_id = chat["id"]
print(f"Assistant: {chat['output'][0]['content']}")
```

### Session-Based Conversations

Use sessions for long-running, complex conversations:

```python
import requests

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# 1. Create a session
session_resp = requests.post(
    "https://api.vapi.ai/session",
    headers=headers,
    json={"assistantId": "your-assistant-id"},
)
session = session_resp.json()
session_id = session["id"]

# 2. Send messages using the session ID (no need for assistantId or previousChatId)
response = requests.post(
    "https://api.vapi.ai/chat",
    headers=headers,
    json={
        "sessionId": session_id,
        "input": "Hello, I need technical support",
    },
)
chat = response.json()
print(f"Assistant: {chat['output'][0]['content']}")

# 3. Continue the conversation in the same session
response = requests.post(
    "https://api.vapi.ai/chat",
    headers=headers,
    json={
        "sessionId": session_id,
        "input": "My app crashes on startup",
    },
)
chat = response.json()
print(f"Assistant: {chat['output'][0]['content']}")
```

> **Note:** Never use both `previousChatId` and `sessionId` in the same request. Sessions expire after 24 hours by default.

### List Recent Chats with Date Filtering

```bash
# Chats created in the last 24 hours
curl "https://api.vapi.ai/chat?createdAtGt=2026-03-09T00:00:00Z&sortOrder=desc&limit=50" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Use a Squad or Workflow for Chat

Instead of a single assistant, route chats through a squad or workflow:

```bash
# Chat with a squad
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "squadId": "your-squad-id",
    "input": "I need help with a complex issue"
  }'

# Chat with a workflow
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workflowId": "your-workflow-id",
    "input": "Start the onboarding process"
  }'
```

---

## Chat Object Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique chat identifier |
| `orgId` | string | Organization ID |
| `assistantId` | string | Assistant that processed the chat |
| `sessionId` | string | Session identifier (if using sessions) |
| `name` | string | Optional display name for the chat |
| `messages` | array | Array of user input messages (`{role, content}`) |
| `output` | array | Array of assistant response messages (`{role, content}`) |
| `object` | string | Always `"chat"` |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

---

## Context Management

| Method | Best For | Key Behavior |
|--------|----------|-------------|
| `previousChatId` | Simple back-and-forth | Chains individual chats sequentially; requires tracking last chat ID |
| `sessionId` | Complex multi-step workflows | Groups interactions under a persistent session; auto-expires after 24 hours |

---

## Webhook Events

The Chat API triggers these webhook events (configure in Dashboard under "Server Messaging"):

- `chat.created` -- Fired when a new chat conversation starts
- `chat.deleted` -- Fired when a chat conversation is deleted

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Chats (5 endpoints) with full examples
