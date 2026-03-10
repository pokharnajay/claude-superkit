---
name: manage-evals
description: Create and manage evaluations in Vapi to test assistant performance with mock conversations, judge plans, and scoring. Use when testing assistants, setting up QA workflows, running eval benchmarks, or validating conversation flows.
---

# Manage Evaluations Skill

This skill covers creating, running, and managing evaluations (evals) in Vapi. Evals let you define mock conversations with expected outcomes, then run them against assistants to validate behavior. Each eval message can include a judge plan that scores the assistant's response using exact matching, regex patterns, or AI-based evaluation.

> **See also:** `create-assistant` (building assistants to evaluate), `create-tool` (tools that evals can validate)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- At least one assistant created to evaluate against

---

## Quick Start

### Create an Eval via cURL

```bash
curl -X POST https://api.vapi.ai/eval \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Greeting Check",
    "description": "Verify assistant greets the user appropriately",
    "type": "chat.mockConversation",
    "messages": [
      {
        "role": "user",
        "content": "Hello"
      },
      {
        "role": "assistant",
        "judgePlan": {
          "type": "regex",
          "content": {
            "pattern": "(?i)(hello|hi|hey|welcome)"
          }
        }
      }
    ]
  }'
```

### Create an Eval via Python

```python
import requests

url = "https://api.vapi.ai/eval"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "name": "Greeting Check",
    "description": "Verify assistant greets the user appropriately",
    "type": "chat.mockConversation",
    "messages": [
        {"role": "user", "content": "Hello"},
        {
            "role": "assistant",
            "judgePlan": {
                "type": "regex",
                "content": {
                    "pattern": "(?i)(hello|hi|hey|welcome)"
                },
            },
        },
    ],
}

response = requests.post(url, headers=headers, json=payload)
eval_obj = response.json()
print(f"Eval created: {eval_obj['id']}")
```

### Create an Eval via TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/eval", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Greeting Check",
    description: "Verify assistant greets the user appropriately",
    type: "chat.mockConversation",
    messages: [
      { role: "user", content: "Hello" },
      {
        role: "assistant",
        judgePlan: {
          type: "regex",
          content: { pattern: "(?i)(hello|hi|hey|welcome)" },
        },
      },
    ],
  }),
});

const evalObj = await response.json();
console.log(`Eval created: ${evalObj.id}`);
```

---

## Eval CRUD Operations

### List All Evals

```bash
curl https://api.vapi.ai/eval \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination:**

```bash
curl "https://api.vapi.ai/eval?page=1&limit=20&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    "https://api.vapi.ai/eval",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 20, "sortOrder": "desc"},
)
evals = response.json()
for e in evals:
    print(f"{e['name']} — {e['id']}")
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/eval?page=1&limit=20&sortOrder=desc", {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const evals = await response.json();
evals.forEach((e: any) => console.log(`${e.name} — ${e.id}`));
```

### Get a Specific Eval

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
print(f"{eval_obj['name']} — {len(eval_obj['messages'])} messages")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/${evalId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const evalObj = await response.json();
console.log(`${evalObj.name} — ${evalObj.messages.length} messages`);
```

### Update an Eval

```bash
curl -X PATCH https://api.vapi.ai/eval/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Greeting Check",
    "description": "Updated description"
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
        "name": "Updated Greeting Check",
        "description": "Updated description",
    },
)
updated_eval = response.json()
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
    name: "Updated Greeting Check",
    description: "Updated description",
  }),
});
const updatedEval = await response.json();
```

### Delete an Eval

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
deleted_eval = response.json()
print(f"Deleted: {deleted_eval['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/eval/${evalId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deletedEval = await response.json();
console.log(`Deleted: ${deletedEval.id}`);
```

---

## Eval Run Operations

### Create an Eval Run

Run an eval against an assistant:

```bash
curl -X POST https://api.vapi.ai/eval/run \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "evalId": "your-eval-id",
    "target": {
      "type": "assistant",
      "assistantId": "your-assistant-id"
    }
  }'
```

**With assistant overrides and scorer IDs:**

```bash
curl -X POST https://api.vapi.ai/eval/run \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "evalId": "your-eval-id",
    "target": {
      "type": "assistant",
      "assistantId": "your-assistant-id"
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
print(f"Eval run started: {run['id']} — Status: {run['status']}")
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
console.log(`Eval run started: ${run.id} — Status: ${run.status}`);
```

### List Eval Runs

```bash
curl "https://api.vapi.ai/eval/run?page=1&limit=20" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    "https://api.vapi.ai/eval/run",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 20},
)
runs = response.json()
for r in runs:
    print(f"{r['id']} — {r['status']} — {r.get('endedReason', 'running')}")
```

### Get an Eval Run

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
if run["status"] == "ended":
    print(f"Ended reason: {run['endedReason']}")
    for result in run.get("results", []):
        print(f"  Result: {result}")
```

### Delete an Eval Run

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
deleted_run = response.json()
print(f"Deleted run: {deleted_run['id']}")
```

---

## Common Patterns

### Exact Matching

Check that the assistant's response matches an exact string:

```json
{
  "role": "assistant",
  "judgePlan": {
    "type": "exact",
    "content": "Welcome to Acme Corp! How can I help you today?"
  }
}
```

With tool call validation:

```json
{
  "role": "assistant",
  "judgePlan": {
    "type": "exact",
    "content": "Let me look that up for you.",
    "toolCalls": [
      {
        "name": "lookupOrder",
        "parameters": {
          "orderId": "12345"
        }
      }
    ]
  }
}
```

### Regex Matching

Validate the response matches a pattern:

```json
{
  "role": "assistant",
  "judgePlan": {
    "type": "regex",
    "content": {
      "pattern": "(?i)your order (number|#)?\\s*\\d+ (is|has been) (shipped|delivered)"
    }
  }
}
```

With tool call validation:

```json
{
  "role": "assistant",
  "judgePlan": {
    "type": "regex",
    "content": {
      "pattern": "(?i)(scheduled|booked|confirmed)"
    },
    "toolCalls": [
      {
        "name": "createAppointment",
        "parameters": {
          "date": "2026-03-15"
        }
      }
    ]
  }
}
```

### AI Judge

Use an AI model to evaluate the assistant's response:

```json
{
  "role": "assistant",
  "judgePlan": {
    "type": "ai",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "temperature": 0,
      "maxTokens": 500,
      "messages": [
        {
          "role": "system",
          "content": "You are an eval judge. Score the assistant's response on a scale of 1-5 for helpfulness, accuracy, and tone. Return a JSON object with scores and a pass/fail verdict. Pass requires all scores >= 3."
        }
      ]
    }
  }
}
```

Using Anthropic as the judge:

```json
{
  "role": "assistant",
  "judgePlan": {
    "type": "ai",
    "model": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "temperature": 0,
      "maxTokens": 500,
      "messages": [
        {
          "role": "system",
          "content": "Evaluate whether the assistant's response correctly addresses the customer's billing question. Respond with PASS or FAIL followed by a brief explanation."
        }
      ]
    }
  }
}
```

### Tool Call Validation

Verify the assistant calls the right tool with the right parameters:

```json
{
  "type": "chat.mockConversation",
  "messages": [
    {
      "role": "user",
      "content": "Book an appointment for tomorrow at 3pm"
    },
    {
      "role": "assistant",
      "judgePlan": {
        "type": "exact",
        "toolCalls": [
          {
            "name": "bookAppointment",
            "parameters": {
              "date": "2026-03-11",
              "time": "15:00"
            }
          }
        ]
      }
    }
  ]
}
```

### Multi-Turn Conversation Eval

Test a full conversation flow:

```json
{
  "name": "Booking Flow",
  "description": "Test the full appointment booking conversation",
  "type": "chat.mockConversation",
  "messages": [
    {
      "role": "system",
      "content": "You are a dental office receptionist."
    },
    {
      "role": "user",
      "content": "I'd like to schedule a cleaning"
    },
    {
      "role": "assistant",
      "judgePlan": {
        "type": "regex",
        "content": {
          "pattern": "(?i)(when|what day|what time|available|prefer)"
        }
      }
    },
    {
      "role": "user",
      "content": "Tomorrow at 2pm"
    },
    {
      "role": "assistant",
      "judgePlan": {
        "type": "ai",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "temperature": 0,
          "maxTokens": 200,
          "messages": [
            {
              "role": "system",
              "content": "Check that the assistant confirms the appointment details (cleaning, tomorrow, 2pm) and asks for the patient's name or confirms booking. Return PASS or FAIL."
            }
          ]
        }
      }
    }
  ]
}
```

### Run Eval and Poll for Results

```python
import requests
import time

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# Create the eval run
run_response = requests.post(
    "https://api.vapi.ai/eval/run",
    headers=headers,
    json={
        "evalId": eval_id,
        "target": {"type": "assistant", "assistantId": assistant_id},
    },
)
run = run_response.json()
run_id = run["id"]
print(f"Eval run started: {run_id}")

# Poll until complete
while True:
    status_response = requests.get(
        f"https://api.vapi.ai/eval/run/{run_id}",
        headers=headers,
    )
    run = status_response.json()
    print(f"Status: {run['status']}")

    if run["status"] == "ended":
        print(f"Ended reason: {run['endedReason']}")
        print(f"Results: {run.get('results', [])}")
        if run.get("callId"):
            print(f"Call ID: {run['callId']}")
        break

    time.sleep(3)
```

---

## Judge Plan Types

| Type | Description | Use Case |
|------|-------------|----------|
| `exact` | Exact string match on content and/or tool calls | Deterministic responses, specific tool invocations |
| `regex` | Regex pattern match on content, optional tool call match | Flexible text matching, keyword presence checks |
| `ai` | AI model evaluates the response quality | Subjective quality, tone, completeness, complex criteria |

### Judge Plan Structure

**Exact judge:**
```json
{
  "type": "exact",
  "content": "exact expected string",
  "toolCalls": [{"name": "toolName", "parameters": {...}}]
}
```

**Regex judge:**
```json
{
  "type": "regex",
  "content": {"pattern": "regex-pattern-here"},
  "toolCalls": [{"name": "toolName", "parameters": {...}}]
}
```

**AI judge:**
```json
{
  "type": "ai",
  "model": {
    "provider": "openai|anthropic",
    "model": "model-name",
    "temperature": 0,
    "maxTokens": 500,
    "messages": [{"role": "system", "content": "Judging instructions"}]
  }
}
```

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Evals and Eval Runs (9 endpoints) with full examples
