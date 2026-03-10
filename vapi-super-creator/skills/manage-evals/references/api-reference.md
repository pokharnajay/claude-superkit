# Evals API Reference

Base URL: `https://api.vapi.ai`

All endpoints require the `Authorization: Bearer <VAPI_API_KEY>` header.

---

## Evals API

Base path: `/eval`

---

### 1. List Evals

**`GET /eval`**

Returns a paginated list of evaluations.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | number | Page number (starts at 1) |
| `limit` | number | Results per page |
| `sortOrder` | string | `asc` or `desc` |
| `createdAtGt` | string | Filter: created after (ISO 8601) |
| `createdAtLt` | string | Filter: created before (ISO 8601) |
| `updatedAtGt` | string | Filter: updated after (ISO 8601) |
| `updatedAtLt` | string | Filter: updated before (ISO 8601) |

**cURL:**

```bash
curl "https://api.vapi.ai/eval?page=1&limit=20&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

response = requests.get(
    "https://api.vapi.ai/eval",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 20, "sortOrder": "desc"},
)
evals = response.json()
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/eval?page=1&limit=20&sortOrder=desc", {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const evals = await response.json();
```

**Response:** Array of Eval objects.

---

### 2. Create Eval

**`POST /eval`**

Creates a new evaluation with a mock conversation and judge plans.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Eval name (max 80 characters) |
| `description` | string | Yes | Eval description (max 500 characters) |
| `type` | string | Yes | Must be `"chat.mockConversation"` |
| `messages` | array | Yes | Array of message objects defining the conversation |

**Message Types:**

Each message has a `role` and type-specific fields:

**User message:**
```json
{
  "role": "user",
  "content": "The user's message text"
}
```

**Assistant message (with judge plan):**
```json
{
  "role": "assistant",
  "judgePlan": { ... }
}
```

**System message:**
```json
{
  "role": "system",
  "content": "System prompt or context"
}
```

**Tool message:**
```json
{
  "role": "tool",
  "content": "Tool response content"
}
```

**Judge Plan Types:**

**Exact Match (`type: "exact"`):**
```json
{
  "type": "exact",
  "content": "Expected exact response string",
  "toolCalls": [
    {
      "name": "functionName",
      "parameters": {
        "param1": "value1"
      }
    }
  ]
}
```
- `content` (string, optional) - Expected exact text match
- `toolCalls` (array, optional) - Expected tool calls with name and parameters

**Regex Match (`type: "regex"`):**
```json
{
  "type": "regex",
  "content": {
    "pattern": "regex-pattern"
  },
  "toolCalls": [
    {
      "name": "functionName",
      "parameters": {
        "param1": "value1"
      }
    }
  ]
}
```
- `content.pattern` (string, optional) - Regex pattern to match against the response
- `toolCalls` (array, optional) - Expected tool calls with name and parameters

**AI Judge (`type: "ai"`):**
```json
{
  "type": "ai",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0,
    "maxTokens": 500,
    "messages": [
      {
        "role": "system",
        "content": "Instructions for the AI judge"
      }
    ]
  }
}
```
- `model.provider` (string, required) - `"openai"` or `"anthropic"`
- `model.model` (string, required) - Model identifier (e.g., `"gpt-4o"`, `"claude-sonnet-4-20250514"`)
- `model.temperature` (number, optional) - Sampling temperature
- `model.maxTokens` (number, optional) - Maximum tokens for the judge response
- `model.messages` (array, required) - System/user messages instructing the judge

**cURL:**

```bash
curl -X POST https://api.vapi.ai/eval \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Order Lookup Test",
    "description": "Verify assistant handles order lookup correctly",
    "type": "chat.mockConversation",
    "messages": [
      {
        "role": "system",
        "content": "You are a customer support agent for an e-commerce store."
      },
      {
        "role": "user",
        "content": "What is the status of order 12345?"
      },
      {
        "role": "assistant",
        "judgePlan": {
          "type": "exact",
          "toolCalls": [
            {
              "name": "lookupOrder",
              "parameters": {
                "orderId": "12345"
              }
            }
          ]
        }
      },
      {
        "role": "tool",
        "content": "{\"orderId\": \"12345\", \"status\": \"shipped\", \"trackingNumber\": \"TRK-789\"}"
      },
      {
        "role": "assistant",
        "judgePlan": {
          "type": "regex",
          "content": {
            "pattern": "(?i)(shipped|tracking|TRK-789)"
          }
        }
      }
    ]
  }'
```

**Python:**

```python
import requests

payload = {
    "name": "Order Lookup Test",
    "description": "Verify assistant handles order lookup correctly",
    "type": "chat.mockConversation",
    "messages": [
        {"role": "system", "content": "You are a customer support agent."},
        {"role": "user", "content": "What is the status of order 12345?"},
        {
            "role": "assistant",
            "judgePlan": {
                "type": "exact",
                "toolCalls": [
                    {"name": "lookupOrder", "parameters": {"orderId": "12345"}}
                ],
            },
        },
        {
            "role": "tool",
            "content": '{"orderId": "12345", "status": "shipped", "trackingNumber": "TRK-789"}',
        },
        {
            "role": "assistant",
            "judgePlan": {
                "type": "regex",
                "content": {"pattern": "(?i)(shipped|tracking|TRK-789)"},
            },
        },
    ],
}

response = requests.post(
    "https://api.vapi.ai/eval",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
)
eval_obj = response.json()
print(f"Created eval: {eval_obj['id']}")
```

**TypeScript:**

```typescript
const payload = {
  name: "Order Lookup Test",
  description: "Verify assistant handles order lookup correctly",
  type: "chat.mockConversation",
  messages: [
    { role: "system", content: "You are a customer support agent." },
    { role: "user", content: "What is the status of order 12345?" },
    {
      role: "assistant",
      judgePlan: {
        type: "exact",
        toolCalls: [{ name: "lookupOrder", parameters: { orderId: "12345" } }],
      },
    },
    {
      role: "tool",
      content: JSON.stringify({ orderId: "12345", status: "shipped", trackingNumber: "TRK-789" }),
    },
    {
      role: "assistant",
      judgePlan: {
        type: "regex",
        content: { pattern: "(?i)(shipped|tracking|TRK-789)" },
      },
    },
  ],
};

const response = await fetch("https://api.vapi.ai/eval", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(payload),
});
const evalObj = await response.json();
console.log(`Created eval: ${evalObj.id}`);
```

**Response:** Eval object with `id`, `name`, `description`, `type`, `messages`, `createdAt`, `updatedAt`.

---

### 3. Get Eval

**`GET /eval/{id}`**

Retrieves a single eval by ID.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Eval ID |

**cURL:**

```bash
curl https://api.vapi.ai/eval/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/eval/{eval_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
eval_obj = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/${evalId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const evalObj = await response.json();
```

**Response:** Eval object.

---

### 4. Delete Eval

**`DELETE /eval/{id}`**

Deletes an eval by ID.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Eval ID |

**cURL:**

```bash
curl -X DELETE https://api.vapi.ai/eval/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/eval/{eval_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/${evalId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deleted = await response.json();
```

**Response:** Deleted Eval object.

---

### 5. Update Eval

**`PATCH /eval/{id}`**

Updates an existing eval. All fields are optional.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Eval ID |

**Request Body (all optional):**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Updated name (max 80 characters) |
| `description` | string | Updated description (max 500 characters) |
| `messages` | array | Updated messages array |

**cURL:**

```bash
curl -X PATCH https://api.vapi.ai/eval/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Eval Name",
    "description": "Updated description of the eval"
  }'
```

**Python:**

```python
response = requests.patch(
    f"https://api.vapi.ai/eval/{eval_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Updated Eval Name",
        "description": "Updated description of the eval",
    },
)
updated = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/${evalId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Updated Eval Name",
    description: "Updated description of the eval",
  }),
});
const updated = await response.json();
```

**Response:** Updated Eval object.

---

## Eval Runs API

Base path: `/eval/run`

---

### 6. List Eval Runs

**`GET /eval/run`**

Returns a paginated list of eval runs.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | number | Page number (starts at 1) |
| `limit` | number | Results per page |
| `sortOrder` | string | `asc` or `desc` |
| `createdAtGt` | string | Filter: created after (ISO 8601) |
| `createdAtLt` | string | Filter: created before (ISO 8601) |
| `updatedAtGt` | string | Filter: updated after (ISO 8601) |
| `updatedAtLt` | string | Filter: updated before (ISO 8601) |

**cURL:**

```bash
curl "https://api.vapi.ai/eval/run?page=1&limit=20&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    "https://api.vapi.ai/eval/run",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 20, "sortOrder": "desc"},
)
runs = response.json()
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/eval/run?page=1&limit=20&sortOrder=desc", {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const runs = await response.json();
```

**Response:** Array of Eval Run objects.

---

### 7. Create Eval Run

**`POST /eval/run`**

Starts a new eval run against an assistant or squad.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `evalId` | string | Yes | ID of the eval to run |
| `target` | object | Yes | Target to evaluate |
| `target.type` | string | Yes | `"assistant"` or `"squad"` |
| `target.assistantId` | string | Yes* | Assistant ID (*required when type is `"assistant"`) |
| `assistantOverrides` | object | No | Override assistant settings for this run |
| `scorerIds` | array | No | Array of scorer IDs to use for additional scoring |

**cURL:**

```bash
curl -X POST https://api.vapi.ai/eval/run \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "evalId": "eval-id-here",
    "target": {
      "type": "assistant",
      "assistantId": "assistant-id-here"
    }
  }'
```

**With overrides and scorers:**

```bash
curl -X POST https://api.vapi.ai/eval/run \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "evalId": "eval-id-here",
    "target": {
      "type": "assistant",
      "assistantId": "assistant-id-here"
    },
    "assistantOverrides": {
      "model": {
        "provider": "openai",
        "model": "gpt-4o"
      }
    },
    "scorerIds": ["scorer-id-1", "scorer-id-2"]
  }'
```

**Python:**

```python
response = requests.post(
    "https://api.vapi.ai/eval/run",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "evalId": eval_id,
        "target": {
            "type": "assistant",
            "assistantId": assistant_id,
        },
    },
)
run = response.json()
print(f"Run started: {run['id']} — Status: {run['status']}")
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/eval/run", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    evalId,
    target: { type: "assistant", assistantId },
  }),
});
const run = await response.json();
console.log(`Run started: ${run.id} — Status: ${run.status}`);
```

**Response:** Eval Run object.

---

### 8. Get Eval Run

**`GET /eval/run/{id}`**

Retrieves a single eval run by ID.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Eval Run ID |

**cURL:**

```bash
curl https://api.vapi.ai/eval/run/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/eval/run/{run_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
run = response.json()
print(f"Status: {run['status']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/run/${runId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const run = await response.json();
console.log(`Status: ${run.status}`);
```

**Response:** Eval Run object.

---

### 9. Delete Eval Run

**`DELETE /eval/run/{id}`**

Deletes an eval run by ID.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Eval Run ID |

**cURL:**

```bash
curl -X DELETE https://api.vapi.ai/eval/run/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/eval/run/{run_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted = response.json()
print(f"Deleted run: {deleted['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/run/${runId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deleted = await response.json();
console.log(`Deleted run: ${deleted.id}`);
```

**Response:** Deleted Eval Run object.

---

## Response Schemas

### Eval Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique eval identifier |
| `orgId` | string | Organization ID |
| `name` | string | Eval name (max 80 characters) |
| `description` | string | Eval description (max 500 characters) |
| `type` | string | Always `"chat.mockConversation"` |
| `messages` | array | Array of message objects with roles and judge plans |
| `object` | string | Always `"eval"` |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

### Eval Run Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique eval run identifier |
| `orgId` | string | Organization ID |
| `evalId` | string | ID of the eval being run |
| `status` | string | `"queued"`, `"running"`, or `"ended"` |
| `endedReason` | string | Why the run ended (see below) |
| `results` | array | Array of result objects with scores and verdicts |
| `callId` | string | ID of the call created for this run |
| `target` | object | Target configuration (type, assistantId) |
| `assistantOverrides` | object | Any overrides applied to this run |
| `scorerIds` | array | Scorer IDs used for this run |
| `object` | string | Always `"eval.run"` |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

### Eval Run `endedReason` Values

| Value | Description |
|-------|-------------|
| `mockConversation.done` | The mock conversation completed successfully |
| `error` | An error occurred during the run |
| `timeout` | The run exceeded the time limit |
| `cancelled` | The run was cancelled |
| `aborted` | The run was aborted |
