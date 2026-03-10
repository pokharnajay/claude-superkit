---
name: manage-campaigns
description: Create and manage outbound calling campaigns in Vapi to make automated calls at scale. Use when setting up batch outbound calls, scheduling call campaigns, managing campaign status, or running automated outreach with voice assistants.
---

# Manage Campaigns Skill

This skill covers creating, retrieving, updating, and deleting outbound calling campaigns in Vapi. Campaigns allow you to systematically call a list of contacts using a configured voice assistant, with support for scheduling, concurrency control, and dynamic personalization.

> **See also:** `create-assistant` (configuring the assistant that handles calls), `create-phone-number` (setting up outbound phone numbers), `create-call` (individual outbound calls)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- An existing assistant (or squad/workflow) configured for outbound calls
- A phone number from a supported provider (Twilio recommended; Vapi free numbers are not compatible with campaigns)
- A list of customer phone numbers in E.164 format

---

## Quick Start

### Create a Campaign via cURL

```bash
curl -X POST https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Outreach Campaign",
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customers": [
      { "number": "+14151234567", "name": "John Doe" },
      { "number": "+14159876543", "name": "Jane Smith" }
    ],
    "maxConcurrentCalls": 5
  }'
```

### Create a Campaign via Python

```python
import requests

url = "https://api.vapi.ai/campaign"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "name": "Customer Outreach Campaign",
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customers": [
        {"number": "+14151234567", "name": "John Doe"},
        {"number": "+14159876543", "name": "Jane Smith"},
    ],
    "maxConcurrentCalls": 5,
}

response = requests.post(url, headers=headers, json=payload)
campaign = response.json()
print(f"Campaign created: {campaign['id']} — Status: {campaign['status']}")
```

### Create a Campaign via TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/campaign", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Customer Outreach Campaign",
    assistantId: "your-assistant-id",
    phoneNumberId: "your-phone-number-id",
    customers: [
      { number: "+14151234567", name: "John Doe" },
      { number: "+14159876543", name: "Jane Smith" },
    ],
    maxConcurrentCalls: 5,
  }),
});

const campaign = await response.json();
console.log(`Campaign created: ${campaign.id} — Status: ${campaign.status}`);
```

---

## CRUD Operations

### List All Campaigns

```bash
curl https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Filter by status:**

```bash
curl "https://api.vapi.ai/campaign?status=in-progress&sortOrder=desc&limit=10" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

response = requests.get(
    "https://api.vapi.ai/campaign",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"status": "in-progress", "sortOrder": "desc", "limit": 10},
)
campaigns = response.json()
for c in campaigns:
    print(f"{c['name']} — {c['status']} — ID: {c['id']}")
```

**TypeScript:**

```typescript
const params = new URLSearchParams({
  status: "in-progress",
  sortOrder: "desc",
  limit: "10",
});

const response = await fetch(`https://api.vapi.ai/campaign?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const campaigns = await response.json();
campaigns.forEach((c: any) => console.log(`${c.name} — ${c.status} — ID: ${c.id}`));
```

### Get a Specific Campaign

```bash
curl https://api.vapi.ai/campaign/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/campaign/{campaign_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
campaign = response.json()
print(f"{campaign['name']} — {campaign['status']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/campaign/${campaignId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const campaign = await response.json();
console.log(`${campaign.name} — ${campaign.status}`);
```

### Update a Campaign

```bash
curl -X PATCH https://api.vapi.ai/campaign/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Campaign Name",
    "maxConcurrentCalls": 10
  }'
```

**Python:**

```python
response = requests.patch(
    f"https://api.vapi.ai/campaign/{campaign_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={"name": "Updated Campaign Name", "maxConcurrentCalls": 10},
)
updated = response.json()
print(f"Updated: {updated['name']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/campaign/${campaignId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ name: "Updated Campaign Name", maxConcurrentCalls: 10 }),
});
const updated = await response.json();
console.log(`Updated: ${updated.name}`);
```

### Delete a Campaign

```bash
curl -X DELETE https://api.vapi.ai/campaign/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/campaign/{campaign_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted = response.json()
print(f"Deleted campaign: {deleted['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/campaign/${campaignId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deleted = await response.json();
console.log(`Deleted campaign: ${deleted.id}`);
```

---

## Common Patterns

### Create a Campaign with a Phone List and Schedule

```python
import requests

payload = {
    "name": "Appointment Reminders - March 2026",
    "assistantId": "asst_abc123",
    "phoneNumberId": "pn_xyz789",
    "customers": [
        {"number": "+14151234567", "name": "Alice Johnson", "appointmentDate": "2026-03-15"},
        {"number": "+14159876543", "name": "Bob Williams", "appointmentDate": "2026-03-16"},
        {"number": "+12125551234", "name": "Carol Davis", "appointmentDate": "2026-03-17"},
    ],
    "schedule": {
        "startTime": "2026-03-14T09:00:00Z",
        "endTime": "2026-03-14T17:00:00Z",
        "timezone": "America/New_York",
    },
    "maxConcurrentCalls": 3,
}

response = requests.post(
    "https://api.vapi.ai/campaign",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
)
campaign = response.json()
print(f"Scheduled campaign: {campaign['id']} — Status: {campaign['status']}")
```

Dynamic variables like `{{name}}` and `{{appointmentDate}}` in the customer objects are accessible in the assistant's prompt via double-bracket syntax.

### Schedule a Campaign for Later Execution

```bash
curl -X POST https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekend Promo Outreach",
    "assistantId": "asst_abc123",
    "phoneNumberId": "pn_xyz789",
    "customers": [
      { "number": "+14151234567", "name": "Customer A" },
      { "number": "+14159876543", "name": "Customer B" }
    ],
    "schedule": {
      "startTime": "2026-03-14T10:00:00Z",
      "endTime": "2026-03-14T16:00:00Z",
      "timezone": "America/Los_Angeles"
    },
    "maxConcurrentCalls": 5
  }'
```

### Monitor Campaign Status

Poll a campaign to track its progress through the lifecycle:

```python
import requests
import time

campaign_id = "your-campaign-id"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

while True:
    response = requests.get(
        f"https://api.vapi.ai/campaign/{campaign_id}",
        headers=headers,
    )
    campaign = response.json()
    status = campaign["status"]
    print(f"Status: {status}")

    if status == "ended":
        print("Campaign complete.")
        print(f"  Total customers: {len(campaign.get('customers', []))}")
        break
    elif status == "in-progress":
        print("Campaign is running...")

    time.sleep(10)
```

### Create a Campaign with Assistant Overrides

Override model, voice, or transcriber settings for a specific campaign without modifying the base assistant:

```bash
curl -X POST https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales Follow-Up",
    "assistantId": "asst_abc123",
    "phoneNumberId": "pn_xyz789",
    "customers": [
      { "number": "+14151234567", "name": "Lead A", "product": "Enterprise Plan" }
    ],
    "assistantOverrides": {
      "model": {
        "provider": "openai",
        "model": "gpt-4o"
      },
      "voice": {
        "provider": "11labs",
        "voiceId": "voice_abc"
      }
    },
    "maxConcurrentCalls": 10
  }'
```

### List Campaigns by Status

```python
import requests

headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

# Get all scheduled campaigns
scheduled = requests.get(
    "https://api.vapi.ai/campaign",
    headers=headers,
    params={"status": "scheduled"},
).json()
print(f"Scheduled campaigns: {len(scheduled)}")

# Get all in-progress campaigns
active = requests.get(
    "https://api.vapi.ai/campaign",
    headers=headers,
    params={"status": "in-progress"},
).json()
print(f"Active campaigns: {len(active)}")

# Get all ended campaigns
ended = requests.get(
    "https://api.vapi.ai/campaign",
    headers=headers,
    params={"status": "ended"},
).json()
print(f"Completed campaigns: {len(ended)}")
```

---

## Campaign Object Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique campaign identifier |
| `orgId` | string | Organization ID |
| `name` | string | Campaign display name |
| `assistantId` | string | ID of the assistant handling calls (mutually exclusive with `squadId` and `workflowId`) |
| `squadId` | string | ID of the squad handling calls (mutually exclusive with `assistantId` and `workflowId`) |
| `workflowId` | string | ID of the workflow handling calls (mutually exclusive with `assistantId` and `squadId`) |
| `phoneNumberId` | string | ID of the outbound phone number |
| `customers` | array | List of customer objects with `number` (required, E.164) and optional dynamic variables |
| `schedule` | object | Scheduling config with `startTime`, `endTime`, `timezone` |
| `status` | string | Campaign status: `scheduled`, `in-progress`, or `ended` |
| `maxConcurrentCalls` | number | Maximum simultaneous calls (subject to org concurrency limits) |
| `assistantOverrides` | object | Optional overrides for model, transcriber, voice, and other assistant config |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

### Status Values

| Status | Description |
|--------|-------------|
| `scheduled` | Campaign is created and scheduled but has not started calling yet |
| `in-progress` | Campaign is actively making calls to customers |
| `ended` | Campaign has completed all calls or was manually stopped |

### Customer Object Format

Each entry in the `customers` array must include at minimum a `number` field in E.164 format. Additional fields become dynamic variables accessible in the assistant prompt via `{{fieldName}}` syntax.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `number` | string | Yes | Phone number in E.164 format (e.g., `+14151234567`) |
| `name` | string | No | Customer name (accessible as `{{name}}` in prompt) |
| *custom fields* | string | No | Any additional key-value pairs become template variables |

**E.164 format rules:** `+[country code][subscriber number]` -- maximum 15 digits, no spaces or special characters.

---

## Concurrency and Limits

- `maxConcurrentCalls` controls how many calls run simultaneously within a campaign
- Campaign concurrency is bounded by your organization's overall concurrency limit
- If the org limit is 10, setting `maxConcurrentCalls: 20` will still cap at 10 simultaneous calls
- Remaining calls are queued and started as slots become available
- Contact Vapi support to increase your organization's concurrency limit

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Campaigns (5 endpoints) with full examples
