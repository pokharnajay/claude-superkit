# Vapi Sessions API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 5 endpoints in the Sessions API for creating, retrieving, listing, updating, and deleting persistent conversation sessions.

---

## Table of Contents

- [Sessions API](#sessions-api)
  - [1. List Sessions](#1-list-sessions)
  - [2. Create Session](#2-create-session)
  - [3. Get Session](#3-get-session)
  - [4. Delete Session](#4-delete-session)
  - [5. Update Session](#5-update-session)
- [Session Object Schema](#session-object-schema)

---

## Sessions API

### 1. List Sessions

Retrieves a paginated list of all sessions in the organization.

#### HTTP Request

```
GET https://api.vapi.ai/session
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
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
| `assistantId` | string | No | Filter by assistant ID |

#### Response

- **200 OK** -- Array of Session objects

#### cURL Example

```bash
curl https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination and filtering:**

```bash
curl "https://api.vapi.ai/session?limit=10&sortOrder=desc&createdAtGt=2026-01-01T00:00:00Z" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/session"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}
params = {
    "limit": 10,
    "sortOrder": "desc",
}

response = requests.get(url, headers=headers, params=params)
sessions = response.json()

for s in sessions:
    print(f"ID: {s['id']}, Status: {s['status']}, Assistant: {s.get('assistantId')}")
```

#### TypeScript Example

```typescript
const params = new URLSearchParams({
  limit: "10",
  sortOrder: "desc",
});

const response = await fetch(`https://api.vapi.ai/session?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const sessions = await response.json();
sessions.forEach((s: any) => {
  console.log(`ID: ${s.id}, Status: ${s.status}, Assistant: ${s.assistantId}`);
});
```

#### Example Response

```json
[
  {
    "id": "session_abc123",
    "orgId": "org_xyz789",
    "assistantId": "asst_def456",
    "name": "Customer Support Session",
    "status": "active",
    "expirationSeconds": 86400,
    "messages": [],
    "costs": [],
    "createdAt": "2026-03-10T10:00:00.000Z",
    "updatedAt": "2026-03-10T10:00:00.000Z"
  }
]
```

---

### 2. Create Session

Creates a new persistent conversation session for an assistant. The session stores the assistant's configuration and maintains conversation history across multiple chat interactions.

#### HTTP Request

```
POST https://api.vapi.ai/session
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body (CreateSessionDTO)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assistantId` | string | No | ID of the assistant to associate with the session. Mutually exclusive with `assistant` |
| `assistant` | object | No | Inline assistant configuration (transient). Mutually exclusive with `assistantId` |
| `assistantOverrides` | object | No | Overrides for the assistant configuration, including `variableValues` |
| `name` | string | No | Session name (max 40 characters) |
| `status` | string | No | Initial session status: `active` or `completed` |
| `expirationSeconds` | number | No | Session expiration in seconds (default: 86400 = 24 hours) |
| `messages` | array | No | Initial array of chat messages |

##### assistantOverrides Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `variableValues` | object | No | Key-value pairs for template variable substitution (e.g., `{{name}}` placeholders) |
| *(other fields)* | various | No | Any assistant configuration fields to override |

#### Response

- **201 Created** -- Session object

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_def456",
    "name": "Billing Support",
    "expirationSeconds": 86400
  }'
```

**With assistant overrides and variable values:**

```bash
curl -X POST https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_def456",
    "assistantOverrides": {
      "variableValues": {
        "name": "John Smith",
        "company": "Acme Corp"
      }
    }
  }'
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/session"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "assistantId": "asst_def456",
    "name": "Billing Support",
    "expirationSeconds": 86400,
}

response = requests.post(url, headers=headers, json=payload)
session = response.json()
print(f"Created session: {session['id']} — Status: {session['status']}")
```

**With variable values:**

```python
payload = {
    "assistantId": "asst_def456",
    "assistantOverrides": {
        "variableValues": {
            "name": "John Smith",
            "company": "Acme Corp",
        }
    },
}
response = requests.post(url, headers=headers, json=payload)
session = response.json()
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/session", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    assistantId: "asst_def456",
    name: "Billing Support",
    expirationSeconds: 86400,
  }),
});

const session = await response.json();
console.log(`Created session: ${session.id} — Status: ${session.status}`);
```

**With variable values:**

```typescript
const response = await fetch("https://api.vapi.ai/session", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    assistantId: "asst_def456",
    assistantOverrides: {
      variableValues: {
        name: "John Smith",
        company: "Acme Corp",
      },
    },
  }),
});

const session = await response.json();
console.log(`Created session: ${session.id}`);
```

#### Example Response

```json
{
  "id": "session_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "name": "Billing Support",
  "status": "active",
  "expirationSeconds": 86400,
  "messages": [],
  "costs": [],
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:00.000Z"
}
```

---

### 3. Get Session

Retrieves a single session by its ID, including the full conversation history and cost breakdown.

#### HTTP Request

```
GET https://api.vapi.ai/session/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique session identifier |

#### Response

- **200 OK** -- Session object

#### cURL Example

```bash
curl https://api.vapi.ai/session/session_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

session_id = "session_abc123"
url = f"https://api.vapi.ai/session/{session_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.get(url, headers=headers)
session = response.json()

print(f"ID: {session['id']}")
print(f"Status: {session['status']}")
print(f"Messages: {len(session.get('messages', []))}")
print(f"Costs: {session.get('costs', [])}")
```

#### TypeScript Example

```typescript
const sessionId = "session_abc123";

const response = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const session = await response.json();
console.log(`ID: ${session.id}`);
console.log(`Status: ${session.status}`);
console.log(`Messages: ${session.messages?.length ?? 0}`);
```

#### Example Response

```json
{
  "id": "session_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "name": "Billing Support",
  "status": "active",
  "expirationSeconds": 86400,
  "messages": [
    {
      "role": "user",
      "message": "Hello, I need help with billing"
    },
    {
      "role": "assistant",
      "content": "I'd be happy to help you with billing. Could you tell me your account number?"
    }
  ],
  "costs": [
    {
      "type": "model",
      "promptTokens": 150,
      "completionTokens": 45,
      "cost": 0.0012
    }
  ],
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:05:30.000Z"
}
```

---

### 4. Delete Session

Deletes a session by its ID. Returns the deleted session object.

#### HTTP Request

```
DELETE https://api.vapi.ai/session/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique session identifier |

#### Response

- **200 OK** -- Deleted Session object

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/session/session_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

session_id = "session_abc123"
url = f"https://api.vapi.ai/session/{session_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.delete(url, headers=headers)
deleted_session = response.json()
print(f"Deleted session: {deleted_session['id']}")
```

#### TypeScript Example

```typescript
const sessionId = "session_abc123";

const response = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const deletedSession = await response.json();
console.log(`Deleted session: ${deletedSession.id}`);
```

#### Example Response

```json
{
  "id": "session_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "name": "Billing Support",
  "status": "active",
  "expirationSeconds": 86400,
  "messages": [],
  "costs": [],
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:00.000Z"
}
```

---

### 5. Update Session

Updates a session's properties including name, status, expiration time, and messages.

#### HTTP Request

```
PATCH https://api.vapi.ai/session/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique session identifier |

#### Request Body (UpdateSessionDTO)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | New session name (max 40 characters) |
| `status` | string | No | New status: `active` or `completed` |
| `expirationSeconds` | number | No | Session expiration in seconds (default: 86400) |
| `messages` | array | No | Updated array of chat messages |

##### Messages Array Items

The `messages` array accepts objects of the following types:

**UserMessage:**

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Always `"user"` |
| `message` | string | The user's message text |
| `time` | number | Timestamp of the message |
| `endTime` | number | End timestamp |
| `secondsFromStart` | number | Seconds from session start |
| `duration` | number | Duration of the message |

**AssistantMessage:**

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Always `"assistant"` |
| `content` | string | The assistant's response text |
| `tool_calls` | array | Tool calls made by the assistant |

**SystemMessage:**

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Always `"system"` |
| `content` | string | System prompt content |

**DeveloperMessage:**

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Always `"developer"` |
| `content` | string | Developer message content |

**ToolMessage:**

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Always `"tool"` |
| `content` | string | Tool response content |
| `tool_call_id` | string | ID of the associated tool call |

#### Response

- **200 OK** -- Updated Session object

#### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/session/session_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Support Session",
    "status": "active",
    "expirationSeconds": 172800
  }'
```

**Mark session as completed:**

```bash
curl -X PATCH https://api.vapi.ai/session/session_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{"status": "completed"}'
```

**Update messages:**

```bash
curl -X PATCH https://api.vapi.ai/session/session_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful billing assistant."},
      {"role": "user", "message": "What is my balance?"},
      {"role": "assistant", "content": "Your current balance is $150.00."}
    ]
  }'
```

#### Python Example

```python
import requests

session_id = "session_abc123"
url = f"https://api.vapi.ai/session/{session_id}"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# Update name and extend expiration
payload = {
    "name": "Updated Support Session",
    "expirationSeconds": 172800,
}
response = requests.patch(url, headers=headers, json=payload)
updated_session = response.json()
print(f"Updated: {updated_session['name']}")

# Mark session as completed
payload = {"status": "completed"}
response = requests.patch(url, headers=headers, json=payload)
completed_session = response.json()
print(f"Session status: {completed_session['status']}")
```

#### TypeScript Example

```typescript
const sessionId = "session_abc123";

// Update name and extend expiration
const response = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Updated Support Session",
    expirationSeconds: 172800,
  }),
});

const updatedSession = await response.json();
console.log(`Updated: ${updatedSession.name}`);

// Mark session as completed
const completeResponse = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ status: "completed" }),
});

const completedSession = await completeResponse.json();
console.log(`Session status: ${completedSession.status}`);
```

#### Example Response

```json
{
  "id": "session_abc123",
  "orgId": "org_xyz789",
  "assistantId": "asst_def456",
  "name": "Updated Support Session",
  "status": "active",
  "expirationSeconds": 172800,
  "messages": [
    {
      "role": "user",
      "message": "Hello, I need help with billing"
    },
    {
      "role": "assistant",
      "content": "I'd be happy to help you with billing. Could you tell me your account number?"
    }
  ],
  "costs": [
    {
      "type": "model",
      "promptTokens": 150,
      "completionTokens": 45,
      "cost": 0.0012
    }
  ],
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T15:30:00.000Z"
}
```

---

## Session Object Schema

The Session object is returned by all session endpoints.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique session identifier |
| `orgId` | string | Organization ID that owns the session |
| `assistantId` | string | ID of the associated assistant |
| `name` | string | Session name (max 40 characters) |
| `status` | string | Session status: `active` or `completed` |
| `expirationSeconds` | number | Session expiration time in seconds (default: 86400) |
| `messages` | array | Array of chat messages (UserMessage, AssistantMessage, SystemMessage, ToolMessage, DeveloperMessage) |
| `costs` | array | Array of cost breakdown items (see below) |
| `createdAt` | string | ISO 8601 timestamp of when the session was created |
| `updatedAt` | string | ISO 8601 timestamp of when the session was last updated |

### Status Values

| Status | Description |
|--------|-------------|
| `active` | Session is available for new chats |
| `completed` | Session is closed and cannot accept new chats |

### Cost Components

**ModelCost:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"model"` |
| `model` | object | Model used during the chat |
| `promptTokens` | number | Number of prompt tokens used |
| `completionTokens` | number | Number of completion tokens used |
| `cachedPromptTokens` | number | Number of cached prompt tokens (optional) |
| `cost` | number | Cost in USD |

**AnalysisCost:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"analysis"` |
| `analysisType` | string | One of: `summary`, `structuredData`, `successEvaluation`, `structuredOutput` |
| `model` | object | Model used for analysis |
| `promptTokens` | number | Number of prompt tokens used |
| `completionTokens` | number | Number of completion tokens used |
| `cachedPromptTokens` | number | Number of cached prompt tokens (optional) |
| `cost` | number | Cost in USD |

**SessionCost:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"session"` |
| `cost` | number | Cost in USD |
