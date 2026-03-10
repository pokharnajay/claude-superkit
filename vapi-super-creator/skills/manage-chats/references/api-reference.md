# Vapi Chats API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 5 endpoints in the Chats API for creating, retrieving, listing, and deleting text-based chat conversations, plus an OpenAI-compatible chat completions endpoint.

---

## Table of Contents

- [Chats API](#chats-api)
  - [1. List Chats](#1-list-chats)
  - [2. Create Chat](#2-create-chat)
  - [3. Get Chat](#3-get-chat)
  - [4. Delete Chat](#4-delete-chat)
  - [5. Create Chat (OpenAI Compatible)](#5-create-chat-openai-compatible)
- [Chat Object Schema](#chat-object-schema)

---

## Chats API

### 1. List Chats

Retrieves a paginated list of all chat conversations in the organization.

#### HTTP Request

```
GET https://api.vapi.ai/chat
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | number | No | Page number for pagination |
| `limit` | number | No | Number of results per page |
| `sortOrder` | string | No | Sort order: `asc` or `desc` |
| `createdAtGt` | string | No | Filter: created after this ISO 8601 timestamp |
| `createdAtLt` | string | No | Filter: created before this ISO 8601 timestamp |
| `createdAtGe` | string | No | Filter: created at or after this ISO 8601 timestamp |
| `createdAtLe` | string | No | Filter: created at or before this ISO 8601 timestamp |
| `updatedAtGt` | string | No | Filter: updated after this ISO 8601 timestamp |
| `updatedAtLt` | string | No | Filter: updated before this ISO 8601 timestamp |
| `updatedAtGe` | string | No | Filter: updated at or after this ISO 8601 timestamp |
| `updatedAtLe` | string | No | Filter: updated at or before this ISO 8601 timestamp |

#### Response

- **200 OK** -- Array of Chat objects

#### cURL Example

```bash
curl https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination and filtering:**

```bash
curl "https://api.vapi.ai/chat?page=1&limit=10&sortOrder=desc&createdAtGt=2026-01-01T00:00:00Z" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/chat"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}
params = {
    "page": 1,
    "limit": 10,
    "sortOrder": "desc",
}

response = requests.get(url, headers=headers, params=params)
chats = response.json()

for c in chats:
    print(f"ID: {c['id']}, Assistant: {c.get('assistantId', 'N/A')}, Created: {c['createdAt']}")
```

#### TypeScript Example

```typescript
const params = new URLSearchParams({
  page: "1",
  limit: "10",
  sortOrder: "desc",
});

const response = await fetch(`https://api.vapi.ai/chat?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const chats = await response.json();
chats.forEach((c: any) => {
  console.log(`ID: ${c.id}, Assistant: ${c.assistantId ?? "N/A"}, Created: ${c.createdAt}`);
});
```

#### Example Response

```json
[
  {
    "id": "chat_abc123",
    "orgId": "org_xyz789",
    "assistantId": "asst_def456",
    "sessionId": null,
    "name": null,
    "messages": [
      {
        "role": "user",
        "content": "Hi, I need help with my account"
      }
    ],
    "output": [
      {
        "role": "assistant",
        "content": "I'd be happy to help with your account! What specific issue are you experiencing?"
      }
    ],
    "object": "chat",
    "createdAt": "2026-03-10T09:30:00.000Z",
    "updatedAt": "2026-03-10T09:30:01.000Z"
  }
]
```

---

### 2. Create Chat

Creates a new chat conversation by sending a message to an assistant, squad, or workflow. Returns the assistant's response along with the chat object.

#### HTTP Request

```
POST https://api.vapi.ai/chat
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | string | Yes | The user's message text |
| `assistantId` | string | Conditional | ID of the assistant to chat with. Required if `assistant`, `squadId`, `squad`, `workflowId`, `workflow`, and `sessionId` are not provided |
| `assistant` | object | Conditional | Inline assistant configuration (model, system prompt, etc.). Use instead of `assistantId` |
| `assistantOverrides` | object | No | Override assistant properties for this chat (e.g., `variableValues`, model settings) |
| `squadId` | string | Conditional | ID of the squad to chat with |
| `squad` | object | Conditional | Inline squad configuration |
| `workflowId` | string | Conditional | ID of the workflow to chat with |
| `workflow` | object | Conditional | Inline workflow configuration |
| `previousChatId` | string | No | ID of the previous chat for multi-turn context. Mutually exclusive with `sessionId` |
| `sessionId` | string | No | Session ID for persistent conversations. Mutually exclusive with `previousChatId` |

**`assistantOverrides` object:**

| Field | Type | Description |
|-------|------|-------------|
| `variableValues` | object | Key-value pairs for dynamic variables referenced in the assistant's system prompt via `{{variableName}}` syntax |
| `model` | object | Override the model configuration |
| `firstMessage` | string | Override the assistant's first message |

#### Response

- **201 Created** -- Chat object with the assistant's response

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_def456",
    "input": "What are your business hours?"
  }'
```

**With dynamic variables:**

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_def456",
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

**Multi-turn conversation:**

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_def456",
    "previousChatId": "chat_abc123",
    "input": "I forgot my password and cannot log in"
  }'
```

**With inline assistant (no pre-built assistant):**

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
            "content": "You are a helpful customer support agent for TechFlow Solutions."
          }
        ]
      }
    },
    "input": "How do I reset my password?"
  }'
```

**With a session:**

```bash
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session_xyz789",
    "input": "Hello, I need technical support"
  }'
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/chat"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# Basic chat
payload = {
    "assistantId": "asst_def456",
    "input": "What are your business hours?",
}

response = requests.post(url, headers=headers, json=payload)
chat = response.json()

print(f"Chat ID: {chat['id']}")
print(f"Assistant: {chat['output'][0]['content']}")

# Multi-turn follow-up
follow_up = {
    "assistantId": "asst_def456",
    "previousChatId": chat["id"],
    "input": "Are you open on weekends?",
}

response = requests.post(url, headers=headers, json=follow_up)
chat2 = response.json()
print(f"Follow-up: {chat2['output'][0]['content']}")
```

#### TypeScript Example

```typescript
const url = "https://api.vapi.ai/chat";
const headers = {
  Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
  "Content-Type": "application/json",
};

// Basic chat
const response = await fetch(url, {
  method: "POST",
  headers,
  body: JSON.stringify({
    assistantId: "asst_def456",
    input: "What are your business hours?",
  }),
});

const chat = await response.json();
console.log(`Chat ID: ${chat.id}`);
console.log(`Assistant: ${chat.output[0].content}`);

// Multi-turn follow-up
const followUp = await fetch(url, {
  method: "POST",
  headers,
  body: JSON.stringify({
    assistantId: "asst_def456",
    previousChatId: chat.id,
    input: "Are you open on weekends?",
  }),
});

const chat2 = await followUp.json();
console.log(`Follow-up: ${chat2.output[0].content}`);
```

#### Example Response

```json
{
  "id": "chat_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "sessionId": null,
  "name": null,
  "messages": [
    {
      "role": "user",
      "content": "What are your business hours?"
    }
  ],
  "output": [
    {
      "role": "assistant",
      "content": "Our business hours are Monday through Friday, 9 AM to 5 PM EST. We're closed on weekends and public holidays. Is there anything else I can help with?"
    }
  ],
  "object": "chat",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:01.000Z"
}
```

---

### 3. Get Chat

Retrieves a single chat conversation by its ID.

#### HTTP Request

```
GET https://api.vapi.ai/chat/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique chat identifier |

#### Response

- **200 OK** -- Chat object

#### cURL Example

```bash
curl https://api.vapi.ai/chat/chat_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

chat_id = "chat_abc123"
url = f"https://api.vapi.ai/chat/{chat_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.get(url, headers=headers)
chat = response.json()

print(f"Chat ID: {chat['id']}")
print(f"Assistant ID: {chat['assistantId']}")
print(f"User said: {chat['messages'][0]['content']}")
print(f"Assistant said: {chat['output'][0]['content']}")
print(f"Created: {chat['createdAt']}")
```

#### TypeScript Example

```typescript
const chatId = "chat_abc123";

const response = await fetch(`https://api.vapi.ai/chat/${chatId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const chat = await response.json();
console.log(`Chat ID: ${chat.id}`);
console.log(`Assistant ID: ${chat.assistantId}`);
console.log(`User said: ${chat.messages[0].content}`);
console.log(`Assistant said: ${chat.output[0].content}`);
console.log(`Created: ${chat.createdAt}`);
```

#### Example Response

```json
{
  "id": "chat_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "sessionId": null,
  "name": null,
  "messages": [
    {
      "role": "user",
      "content": "What are your business hours?"
    }
  ],
  "output": [
    {
      "role": "assistant",
      "content": "Our business hours are Monday through Friday, 9 AM to 5 PM EST. We're closed on weekends and public holidays. Is there anything else I can help with?"
    }
  ],
  "object": "chat",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:01.000Z"
}
```

---

### 4. Delete Chat

Deletes a chat conversation by its ID. Returns the deleted chat object.

#### HTTP Request

```
DELETE https://api.vapi.ai/chat/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique chat identifier |

#### Response

- **200 OK** -- Deleted Chat object

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/chat/chat_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

chat_id = "chat_abc123"
url = f"https://api.vapi.ai/chat/{chat_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.delete(url, headers=headers)
deleted_chat = response.json()
print(f"Deleted chat: {deleted_chat['id']}")
```

#### TypeScript Example

```typescript
const chatId = "chat_abc123";

const response = await fetch(`https://api.vapi.ai/chat/${chatId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const deletedChat = await response.json();
console.log(`Deleted chat: ${deletedChat.id}`);
```

#### Example Response

```json
{
  "id": "chat_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "sessionId": null,
  "name": null,
  "messages": [
    {
      "role": "user",
      "content": "What are your business hours?"
    }
  ],
  "output": [
    {
      "role": "assistant",
      "content": "Our business hours are Monday through Friday, 9 AM to 5 PM EST."
    }
  ],
  "object": "chat",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:01.000Z"
}
```

---

### 5. Create Chat (OpenAI Compatible)

Provides an OpenAI-compatible chat completions endpoint. The `model` field maps to a Vapi assistant ID, squad ID, or workflow ID. This allows using Vapi as a drop-in replacement for OpenAI in existing code or with the OpenAI SDK.

#### HTTP Request

```
POST https://api.vapi.ai/chat/openai
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | Yes | The Vapi assistant ID, squad ID, or workflow ID to use. Maps to the OpenAI `model` field |
| `messages` | array | Yes | Array of message objects in OpenAI format (`{role, content}`). Roles: `system`, `user`, `assistant` |
| `stream` | boolean | No | Enable streaming responses (Server-Sent Events). Default: `false` |
| `temperature` | number | No | Sampling temperature (0-2). Higher values make output more random |
| `max_tokens` | number | No | Maximum number of tokens to generate |

#### Response

- **200 OK** -- OpenAI-compatible chat completion response
- When `stream: true`, returns Server-Sent Events (SSE) with chunked responses

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/chat/openai \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "asst_def456",
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
    "model": "asst_def456",
    "messages": [
      {"role": "user", "content": "Tell me a story about a robot"}
    ],
    "stream": true
  }'
```

**With conversation history:**

```bash
curl -X POST https://api.vapi.ai/chat/openai \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "asst_def456",
    "messages": [
      {"role": "user", "content": "My name is Alice"},
      {"role": "assistant", "content": "Hello Alice! How can I help you today?"},
      {"role": "user", "content": "What is my name?"}
    ]
  }'
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/chat/openai"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# Non-streaming
payload = {
    "model": "asst_def456",
    "messages": [
        {"role": "user", "content": "What is the weather today?"}
    ],
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

**Using the OpenAI SDK:**

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-vapi-api-key",
    base_url="https://api.vapi.ai/chat",
)

# Non-streaming
response = client.chat.completions.create(
    model="asst_def456",
    messages=[{"role": "user", "content": "What is the weather today?"}],
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="asst_def456",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

#### TypeScript Example

```typescript
const url = "https://api.vapi.ai/chat/openai";
const headers = {
  Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
  "Content-Type": "application/json",
};

// Non-streaming
const response = await fetch(url, {
  method: "POST",
  headers,
  body: JSON.stringify({
    model: "asst_def456",
    messages: [{ role: "user", content: "What is the weather today?" }],
  }),
});

const result = await response.json();
console.log(result.choices[0].message.content);
```

**Using the OpenAI SDK:**

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "your-vapi-api-key",
  baseURL: "https://api.vapi.ai/chat",
});

// Non-streaming
const response = await client.chat.completions.create({
  model: "asst_def456",
  messages: [{ role: "user", content: "What is the weather today?" }],
});
console.log(response.choices[0].message.content);

// Streaming
const stream = await client.chat.completions.create({
  model: "asst_def456",
  messages: [{ role: "user", content: "Tell me a story" }],
  stream: true,
});
for await (const chunk of stream) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}
```

#### Example Response (Non-Streaming)

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1710072000,
  "model": "asst_def456",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I don't have access to real-time weather data, but I can help you find the weather for your location. What city are you in?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 30,
    "total_tokens": 42
  }
}
```

#### Example Response (Streaming)

```
data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1710072000,"model":"asst_def456","choices":[{"index":0,"delta":{"role":"assistant","content":"I"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1710072000,"model":"asst_def456","choices":[{"index":0,"delta":{"content":" don't"},"finish_reason":null}]}

data: {"id":"chatcmpl-abc123","object":"chat.completion.chunk","created":1710072000,"model":"asst_def456","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

---

## Chat Object Schema

The Chat object is returned by the List, Create, Get, and Delete endpoints.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique chat identifier |
| `orgId` | string | Organization ID that owns the chat |
| `assistantId` | string \| null | ID of the assistant that processed the chat |
| `sessionId` | string \| null | Session identifier if using session-based conversations |
| `name` | string \| null | Optional display name for the chat |
| `messages` | array | Array of user input messages. Each message has `role` (string) and `content` (string) |
| `output` | array | Array of assistant response messages. Each message has `role` (string) and `content` (string) |
| `object` | string | Always `"chat"` |
| `createdAt` | string | ISO 8601 timestamp of when the chat was created |
| `updatedAt` | string | ISO 8601 timestamp of when the chat was last updated |

### Message Object

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | The message role: `user`, `assistant`, or `system` |
| `content` | string | The text content of the message |
