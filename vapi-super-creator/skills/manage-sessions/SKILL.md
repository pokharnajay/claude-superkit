---
name: manage-sessions
description: Create and manage persistent conversation sessions in Vapi that maintain context across multiple calls or chats. Use when building multi-turn conversations that span multiple interactions, maintaining caller context between calls, or creating persistent conversation threads.
---

# Manage Sessions Skill

This skill covers creating, retrieving, updating, and deleting persistent conversation sessions in Vapi. Sessions group multiple chats together and maintain conversation history and context across interactions with the same assistant, making them ideal for complex workflows and long-running conversations.

> **See also:** `create-assistant` (creating assistants to attach sessions to), `create-call` (initiating calls that can use sessions)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- An existing assistant ID to associate with the session

---

## Quick Start

### Create a Session via cURL

```bash
curl -X POST https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id"
  }'
```

### Create a Session via Python

```python
import requests

url = "https://api.vapi.ai/session"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "assistantId": "your-assistant-id",
}

response = requests.post(url, headers=headers, json=payload)
session = response.json()
print(f"Session created: {session['id']} — Status: {session['status']}")
```

### Create a Session via TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/session", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    assistantId: "your-assistant-id",
  }),
});

const session = await response.json();
console.log(`Session created: ${session.id} — Status: ${session.status}`);
```

---

## CRUD Operations

### List All Sessions

```bash
curl https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination and filtering:**

```bash
curl "https://api.vapi.ai/session?limit=20&createdAtGt=2026-01-01T00:00:00Z&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

response = requests.get(
    "https://api.vapi.ai/session",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"limit": 20, "sortOrder": "desc"},
)
sessions = response.json()
for s in sessions:
    print(f"{s['id']} — Status: {s['status']}")
```

**TypeScript:**

```typescript
const params = new URLSearchParams({
  limit: "20",
  sortOrder: "desc",
});

const response = await fetch(`https://api.vapi.ai/session?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const sessions = await response.json();
sessions.forEach((s: any) => console.log(`${s.id} — Status: ${s.status}`));
```

### Create a Session

```bash
curl -X POST https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id",
    "name": "Customer Support Session",
    "expirationSeconds": 86400
  }'
```

**With assistant overrides and variable values:**

```bash
curl -X POST https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id",
    "assistantOverrides": {
      "variableValues": {
        "name": "John",
        "company": "Acme Corp"
      }
    }
  }'
```

**Python:**

```python
import requests

response = requests.post(
    "https://api.vapi.ai/session",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "assistantId": "your-assistant-id",
        "name": "Customer Support Session",
        "expirationSeconds": 86400,
    },
)
session = response.json()
print(f"Created: {session['id']} — Status: {session['status']}")
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/session", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    assistantId: "your-assistant-id",
    name: "Customer Support Session",
    expirationSeconds: 86400,
  }),
});
const session = await response.json();
console.log(`Created: ${session.id} — Status: ${session.status}`);
```

### Get a Specific Session

```bash
curl https://api.vapi.ai/session/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/session/{session_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
session = response.json()
print(f"Session: {session['id']} — Status: {session['status']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const session = await response.json();
console.log(`Session: ${session.id} — Status: ${session.status}`);
```

### Update a Session

Update session name, status, expiration, or messages:

```bash
curl -X PATCH https://api.vapi.ai/session/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Session Name",
    "status": "active",
    "expirationSeconds": 172800
  }'
```

**Python:**

```python
response = requests.patch(
    f"https://api.vapi.ai/session/{session_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Updated Session Name",
        "status": "active",
        "expirationSeconds": 172800,
    },
)
updated_session = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Updated Session Name",
    status: "active",
    expirationSeconds: 172800,
  }),
});
const updatedSession = await response.json();
```

### Delete a Session

```bash
curl -X DELETE https://api.vapi.ai/session/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/session/{session_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted_session = response.json()
print(f"Deleted: {deleted_session['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/session/${sessionId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deletedSession = await response.json();
console.log(`Deleted: ${deletedSession.id}`);
```

---

## Common Patterns

### Create a Session with an Assistant and Use It for Chat

Create a session and then send chat messages using the session ID instead of the assistant ID:

```bash
# 1. Create a session
SESSION_RESPONSE=$(curl -s -X POST https://api.vapi.ai/session \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"assistantId": "your-assistant-id"}')

SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.id')

# 2. Send a chat message using the session
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\": \"$SESSION_ID\", \"input\": \"Hello, I need help with billing\"}"

# 3. Send a follow-up message (context is maintained automatically)
curl -X POST https://api.vapi.ai/chat \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"sessionId\": \"$SESSION_ID\", \"input\": \"What was my last invoice amount?\"}"
```

### Create a Session with Variable Values

Bake in personalized variable values at session creation time. These persist for the session's lifetime:

```python
import requests

# Create session with variables substituted into the assistant template
response = requests.post(
    "https://api.vapi.ai/session",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "assistantId": "your-assistant-id",
        "assistantOverrides": {
            "variableValues": {
                "name": "John Smith",
                "company": "Acme Corp",
                "plan": "Enterprise",
            }
        },
    },
)
session = response.json()

# All chats in this session will have the variables pre-substituted
# You CANNOT change variableValues in individual chat requests
print(f"Session {session['id']} created with personalized context")
```

### Multi-Assistant Workflow with Separate Sessions

Sessions are tied to a single assistant. For multi-assistant workflows, create separate sessions:

```typescript
const sessions = new Map<string, string>();

async function sendToAssistant(assistantId: string, input: string) {
  let sessionId = sessions.get(assistantId);

  if (!sessionId) {
    const response = await fetch("https://api.vapi.ai/session", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ assistantId }),
    });
    const session = await response.json();
    sessionId = session.id;
    sessions.set(assistantId, sessionId!);
  }

  // Use sessionId for the chat request
  const chatResponse = await fetch("https://api.vapi.ai/chat", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sessionId, input }),
  });

  return chatResponse.json();
}
```

### Complete a Session When Done

Mark a session as completed to prevent further chats:

```python
import requests

# Mark session as completed
response = requests.patch(
    f"https://api.vapi.ai/session/{session_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={"status": "completed"},
)
session = response.json()
print(f"Session {session['id']} is now {session['status']}")
```

### Extend Session Expiration

Sessions expire after 24 hours by default. Extend the expiration if needed:

```bash
curl -X PATCH https://api.vapi.ai/session/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{"expirationSeconds": 172800}'
```

---

## Key Concepts

### Session vs previousChatId

Vapi offers two mutually exclusive approaches for maintaining conversation context:

| Method | Use Case | Persistence |
|--------|----------|-------------|
| **sessionId** | Complex multi-step workflows, long-running conversations | Groups multiple chats under a persistent session |
| **previousChatId** | Simple back-and-forth conversations | Links individual chats in sequence |

You **cannot** use both `sessionId` and `previousChatId` in the same request. They are mutually exclusive.

### Session Lifecycle

- **Status values:** `active` (accepting new chats) or `completed` (closed, no new chats)
- **Default expiration:** 24 hours (86400 seconds), configurable via `expirationSeconds`
- **Scope:** Each session is tied to one assistant
- **Automatic management:** Web chat widgets and SMS channels automatically create and manage sessions

### Webhook Events

Sessions support three webhook events (configure in Dashboard > Assistant > Server Messaging):

- **`session.created`** -- Triggered when a new session is created
- **`session.updated`** -- Triggered when a session is updated
- **`session.deleted`** -- Triggered when a session is deleted

### Variable Substitution

When creating a session with `assistantOverrides.variableValues`, the system substitutes all template placeholders (e.g., `{{name}}`) with actual values and stores the pre-substituted configuration. These values persist for the session's lifetime and cannot be changed in individual chat requests.

---

## Session Object Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique session identifier |
| `orgId` | string | Organization ID |
| `assistantId` | string | Associated assistant ID |
| `name` | string | Session name (max 40 characters) |
| `status` | string | `active` or `completed` |
| `expirationSeconds` | number | Session expiration in seconds (default: 86400) |
| `messages` | array | Array of chat messages in the session |
| `costs` | array | Cost breakdown (ModelCost, AnalysisCost, SessionCost) |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Sessions (5 endpoints) with full examples
