# Vapi Calls, Campaigns & Analytics API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 11 endpoints across three API groups: Calls (5), Campaigns (5), and Analytics (1).

---

## Table of Contents

- [Calls API](#calls-api)
  - [1. Create Call](#1-create-call)
  - [2. List Calls](#2-list-calls)
  - [3. Get Call](#3-get-call)
  - [4. Update Call](#4-update-call)
  - [5. Delete Call](#5-delete-call)
  - [Call Response Schema](#call-response-schema)
- [Campaigns API](#campaigns-api)
  - [6. Create Campaign](#6-create-campaign)
  - [7. List Campaigns](#7-list-campaigns)
  - [8. Get Campaign](#8-get-campaign)
  - [9. Update Campaign](#9-update-campaign)
  - [10. Delete Campaign](#10-delete-campaign)
  - [Campaign Response Schema](#campaign-response-schema)
- [Analytics API](#analytics-api)
  - [11. Create Analytics Queries](#11-create-analytics-queries)

---

## Calls API

### 1. Create Call

Creates a new outbound phone call, web call, or scheduled call.

#### HTTP Request

```
POST https://api.vapi.ai/call
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `assistantId` | string | Conditional | ID of an existing assistant to use. Provide either `assistantId` or `assistant`, not both. |
| `assistant` | object | Conditional | Full transient assistant configuration object. Use instead of `assistantId` for one-off calls. |
| `squadId` | string | Conditional | ID of an existing squad for multi-assistant calls. |
| `squad` | object | Conditional | Full transient squad configuration. Use instead of `squadId` for one-off squad calls. |
| `phoneNumberId` | string | Required (phone) | ID of the Vapi phone number to use for outbound calls. |
| `customer` | object | Required (phone) | Customer information for the call. |
| `customer.number` | string | Required (phone) | Phone number to call in E.164 format (e.g., `+12345678913`). |
| `customer.name` | string | No | Customer name for reference. |
| `customer.extension` | string | No | Phone extension to dial after connection. |
| `customers` | array | No | Array of customer objects for batch calling. |
| `name` | string | No | Friendly name for the call (your reference only). |
| `type` | string | No | Call type: `inboundPhoneCall`, `outboundPhoneCall`, `webCall`, `vapi.websocketCall`. |
| `schedulePlan` | object | No | Schedule the call for a future time. |
| `schedulePlan.earliestAt` | string | No | ISO 8601 earliest time to start the call. |
| `schedulePlan.latestAt` | string | No | ISO 8601 latest time to start the call. |
| `metadata` | object | No | Arbitrary key-value metadata attached to the call. |
| `assistantOverrides` | object | No | Override specific assistant settings for this call only. |

#### Request Body: Outbound Phone Call

```json
{
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customer": {
    "number": "+12345678913",
    "name": "John Doe"
  },
  "metadata": {
    "campaignId": "summer-promo",
    "leadSource": "website"
  }
}
```

#### Request Body: Web Call

```json
{
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "type": "webCall"
}
```

#### Request Body: Squad Call

```json
{
  "squad": {
    "members": [
      {
        "assistant": {
          "name": "Emma",
          "model": { "model": "gpt-4o", "provider": "openai" },
          "voice": { "voiceId": "emma", "provider": "azure" },
          "transcriber": { "provider": "deepgram" },
          "firstMessage": "Hi, I am Emma, what is your name?",
          "firstMessageMode": "assistant-speaks-first"
        }
      },
      {
        "assistantId": "your-existing-assistant-id"
      }
    ]
  },
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customer": {
    "number": "+12345678913"
  }
}
```

#### Request Body: Scheduled Call

```json
{
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customer": {
    "number": "+12345678913"
  },
  "schedulePlan": {
    "earliestAt": "2026-03-15T09:00:00.000Z",
    "latestAt": "2026-03-15T17:00:00.000Z"
  }
}
```

#### Response: `201 Created`

```json
{
  "id": "call_abc123",
  "orgId": "org_xyz789",
  "type": "outboundPhoneCall",
  "status": "queued",
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customer": {
    "number": "+12345678913",
    "name": "John Doe"
  },
  "listenUrl": "wss://api.vapi.ai/call/listen/call_abc123",
  "controlUrl": "wss://api.vapi.ai/call/control/call_abc123",
  "createdAt": "2026-03-02T10:30:00.000Z",
  "updatedAt": "2026-03-02T10:30:00.000Z"
}
```

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
    "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
    "customer": {
      "number": "+12345678913"
    }
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// Outbound phone call
const call = await vapi.calls.create({
  assistantId: "5b0a4a08-133c-4146-9315-0984f8c6be80",
  phoneNumberId: "42b4b25d-031e-4786-857f-63b346c9580f",
  customer: {
    number: "+12345678913",
    name: "John Doe",
  },
  metadata: {
    campaignId: "summer-promo",
  },
});

console.log("Call ID:", call.id);
console.log("Status:", call.status);
console.log("Listen URL:", call.listenUrl);
```

#### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/call"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
    "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
    "customer": {
        "number": "+12345678913",
        "name": "John Doe",
    },
    "metadata": {
        "campaignId": "summer-promo",
    },
}

response = requests.post(url, json=payload, headers=headers)
call = response.json()
print(f"Call ID: {call['id']}")
print(f"Status: {call['status']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/calls/create](https://docs.vapi.ai/api-reference/calls/create)

---

### 2. List Calls

Retrieves a paginated list of calls with optional date-range filtering.

#### HTTP Request

```
GET https://api.vapi.ai/call
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | number | No | Maximum number of calls to return (default: 100). |
| `createdAtGt` | string | No | Filter calls created after this ISO 8601 timestamp (exclusive). |
| `createdAtLt` | string | No | Filter calls created before this ISO 8601 timestamp (exclusive). |
| `createdAtGe` | string | No | Filter calls created at or after this ISO 8601 timestamp (inclusive). |
| `createdAtLe` | string | No | Filter calls created at or before this ISO 8601 timestamp (inclusive). |
| `updatedAtGt` | string | No | Filter calls updated after this ISO 8601 timestamp (exclusive). |
| `updatedAtLt` | string | No | Filter calls updated before this ISO 8601 timestamp (exclusive). |
| `updatedAtGe` | string | No | Filter calls updated at or after this ISO 8601 timestamp (inclusive). |
| `updatedAtLe` | string | No | Filter calls updated at or before this ISO 8601 timestamp (inclusive). |

#### Response: `200 OK`

```json
[
  {
    "id": "call_abc123",
    "orgId": "org_xyz789",
    "type": "outboundPhoneCall",
    "status": "ended",
    "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
    "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
    "customer": {
      "number": "+12345678913"
    },
    "endedReason": "assistant-ended-call",
    "transcript": "AI: Hello! How can I help you?...",
    "recordingUrl": "https://storage.vapi.ai/recordings/call_abc123.wav",
    "summary": "The caller asked about pricing...",
    "cost": 0.15,
    "costBreakdown": {
      "transport": 0.02,
      "stt": 0.01,
      "llm": 0.10,
      "tts": 0.02
    },
    "createdAt": "2026-03-01T10:30:00.000Z",
    "updatedAt": "2026-03-01T10:35:00.000Z"
  }
]
```

#### cURL Example

```bash
# List all calls
curl -X GET "https://api.vapi.ai/call" \
  -H "Authorization: Bearer $VAPI_API_KEY"

# List calls with date filter and limit
curl -X GET "https://api.vapi.ai/call?limit=50&createdAtGe=2026-03-01T00:00:00.000Z&createdAtLe=2026-03-02T23:59:59.000Z" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// List recent calls
const calls = await vapi.calls.list({
  limit: 50,
  createdAtGe: "2026-03-01T00:00:00.000Z",
  createdAtLe: "2026-03-02T23:59:59.000Z",
});

for (const call of calls) {
  console.log(`${call.id} | ${call.status} | ${call.type}`);
}
```

#### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/call"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}
params = {
    "limit": 50,
    "createdAtGe": "2026-03-01T00:00:00.000Z",
    "createdAtLe": "2026-03-02T23:59:59.000Z",
}

response = requests.get(url, headers=headers, params=params)
calls = response.json()

for call in calls:
    print(f"{call['id']} | {call['status']} | {call['type']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/calls/list](https://docs.vapi.ai/api-reference/calls/list)

---

### 3. Get Call

Retrieves a single call by its ID, including full transcript, recording URL, summary, and cost breakdown.

#### HTTP Request

```
GET https://api.vapi.ai/call/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the call to retrieve. |

#### Response: `200 OK`

```json
{
  "id": "call_abc123",
  "orgId": "org_xyz789",
  "type": "outboundPhoneCall",
  "status": "ended",
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customer": {
    "number": "+12345678913",
    "name": "John Doe"
  },
  "endedReason": "assistant-ended-call",
  "transcript": "AI: Hello! How can I help you today?\nUser: I'd like to know about your pricing.\nAI: Of course! We have three tiers...",
  "recordingUrl": "https://storage.vapi.ai/recordings/call_abc123.wav",
  "summary": "The caller inquired about pricing. The assistant explained the three pricing tiers and the caller expressed interest in the Pro plan.",
  "cost": 0.15,
  "costBreakdown": {
    "transport": 0.02,
    "stt": 0.01,
    "llm": 0.10,
    "tts": 0.02
  },
  "messages": [
    {
      "role": "assistant",
      "content": "Hello! How can I help you today?",
      "time": 1709371800000
    },
    {
      "role": "user",
      "content": "I'd like to know about your pricing.",
      "time": 1709371805000
    }
  ],
  "metadata": {
    "campaignId": "summer-promo"
  },
  "createdAt": "2026-03-01T10:30:00.000Z",
  "updatedAt": "2026-03-01T10:35:00.000Z"
}
```

#### cURL Example

```bash
curl -X GET https://api.vapi.ai/call/call_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const call = await vapi.calls.get("call_abc123");

console.log("Status:", call.status);
console.log("Transcript:", call.transcript);
console.log("Recording:", call.recordingUrl);
console.log("Summary:", call.summary);
console.log("Cost:", call.cost);
console.log("Cost Breakdown:", JSON.stringify(call.costBreakdown, null, 2));
```

#### Python Example

```python
import requests
import os

call_id = "call_abc123"
url = f"https://api.vapi.ai/call/{call_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}

response = requests.get(url, headers=headers)
call = response.json()

print(f"Status: {call['status']}")
print(f"Transcript: {call.get('transcript', 'N/A')}")
print(f"Recording: {call.get('recordingUrl', 'N/A')}")
print(f"Summary: {call.get('summary', 'N/A')}")
print(f"Cost: ${call.get('cost', 0):.2f}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/calls/get](https://docs.vapi.ai/api-reference/calls/get)

---

### 4. Update Call

Updates a call's metadata or properties.
#### HTTP Request

```
PATCH https://api.vapi.ai/call/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the call to update. |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Updated friendly name for the call. |
| `metadata` | object | No | Updated arbitrary key-value metadata. |

#### Request Body

```json
{
  "name": "Follow-up call with John",
  "metadata": {
    "campaignId": "summer-promo",
    "outcome": "interested",
    "followUp": true
  }
}
```

#### Response: `200 OK`

```json
{
  "id": "call_abc123",
  "orgId": "org_xyz789",
  "type": "outboundPhoneCall",
  "status": "ended",
  "name": "Follow-up call with John",
  "metadata": {
    "campaignId": "summer-promo",
    "outcome": "interested",
    "followUp": true
  },
  "createdAt": "2026-03-01T10:30:00.000Z",
  "updatedAt": "2026-03-02T08:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/call/call_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Follow-up call with John",
    "metadata": {
      "outcome": "interested",
      "followUp": true
    }
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const updatedCall = await vapi.calls.update("call_abc123", {
  name: "Follow-up call with John",
  metadata: {
    outcome: "interested",
    followUp: true,
  },
});

console.log("Updated:", updatedCall.updatedAt);
```

#### Python Example

```python
import requests
import os

call_id = "call_abc123"
url = f"https://api.vapi.ai/call/{call_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "name": "Follow-up call with John",
    "metadata": {
        "outcome": "interested",
        "followUp": True,
    },
}

response = requests.patch(url, json=payload, headers=headers)
updated_call = response.json()
print(f"Updated: {updated_call['updatedAt']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/calls/update](https://docs.vapi.ai/api-reference/calls/update)

---

### 5. Delete Call

Permanently deletes a call and its associated data.
#### HTTP Request

```
DELETE https://api.vapi.ai/call/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the call to delete. |

#### Response: `200 OK`

```json
{
  "id": "call_abc123",
  "orgId": "org_xyz789",
  "type": "outboundPhoneCall",
  "status": "ended",
  "createdAt": "2026-03-01T10:30:00.000Z",
  "updatedAt": "2026-03-01T10:35:00.000Z"
}
```

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/call/call_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const deletedCall = await vapi.calls.delete("call_abc123");
console.log("Deleted call:", deletedCall.id);
```

#### Python Example

```python
import requests
import os

call_id = "call_abc123"
url = f"https://api.vapi.ai/call/{call_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}

response = requests.delete(url, headers=headers)
deleted_call = response.json()
print(f"Deleted call: {deleted_call['id']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/calls/delete](https://docs.vapi.ai/api-reference/calls/delete)

---

### Call Response Schema

Complete schema for the Call object returned by all Calls API endpoints.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the call. |
| `orgId` | string | Organization ID that owns the call. |
| `type` | string | Call type: `outboundPhoneCall`, `inboundPhoneCall`, `webCall`, `vapi.websocketCall`. |
| `status` | string | Current status: `queued`, `ringing`, `in-progress`, `forwarding`, `ended`. |
| `assistantId` | string | ID of the assistant used for the call. |
| `squadId` | string | ID of the squad used (if multi-assistant call). |
| `phoneNumberId` | string | ID of the phone number used. |
| `customer` | object | Customer information: `number`, `name`, `extension`. |
| `name` | string | Friendly name for the call. |
| `endedReason` | string | Reason the call ended (e.g., `assistant-ended-call`, `customer-ended-call`, `silence-timed-out`, `max-duration-reached`, `pipeline-error-openai-llm-failed`). |
| `transcript` | string | Full text transcript of the conversation. |
| `recordingUrl` | string | URL to the call recording audio file. |
| `stereoRecordingUrl` | string | URL to the stereo recording (separate channels for AI and user). |
| `summary` | string | AI-generated summary of the call. |
| `cost` | number | Total cost of the call in USD. |
| `costBreakdown` | object | Detailed cost breakdown by service: `transport`, `stt`, `llm`, `tts`, `vapi`. |
| `messages` | array | Array of message objects with `role`, `content`, and `time`. |
| `listenUrl` | string | WebSocket URL for real-time audio streaming (available while call is active). |
| `controlUrl` | string | WebSocket URL for real-time call control (available while call is active). |
| `metadata` | object | Arbitrary key-value metadata attached to the call. |
| `analysis` | object | Post-call analysis results including `successEvaluation`, `structuredData`. |
| `createdAt` | string | ISO 8601 timestamp when the call was created. |
| `updatedAt` | string | ISO 8601 timestamp when the call was last updated. |
| `startedAt` | string | ISO 8601 timestamp when the call was answered. |
| `endedAt` | string | ISO 8601 timestamp when the call ended. |

---

## Campaigns API

### 6. Create Campaign

Creates a new outbound calling campaign with an assistant, phone number, customer list, and optional scheduling.

#### HTTP Request

```
POST https://api.vapi.ai/campaign
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of the campaign for identification. |
| `assistantId` | string | Conditional | ID of the assistant to use for all calls. Provide `assistantId` or `assistant`. |
| `assistant` | object | Conditional | Full transient assistant configuration for the campaign. |
| `phoneNumberId` | string | Yes | ID of the phone number to make calls from. |
| `customers` | array | Yes | Array of customer objects to call. Each must have a `number` in E.164 format. |
| `customers[].number` | string | Yes | Customer phone number in E.164 format. |
| `customers[].name` | string | No | Customer name. |
| `customers[].metadata` | object | No | Per-customer metadata passed to the assistant. |
| `schedulePlan` | object | No | Scheduling configuration for the campaign. |
| `schedulePlan.earliestAt` | string | No | ISO 8601 earliest time to start making calls. |
| `schedulePlan.latestAt` | string | No | ISO 8601 latest time to stop making calls. |
| `maxConcurrentCalls` | number | No | Maximum number of simultaneous calls. |

#### Request Body

```json
{
  "name": "Customer Outreach Campaign",
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customers": [
    {
      "number": "+12345678901",
      "name": "Alice Johnson",
      "metadata": { "tier": "premium" }
    },
    {
      "number": "+12345678902",
      "name": "Bob Smith",
      "metadata": { "tier": "standard" }
    },
    {
      "number": "+12345678903",
      "name": "Carol Williams"
    }
  ],
  "schedulePlan": {
    "earliestAt": "2026-03-15T09:00:00.000Z",
    "latestAt": "2026-03-15T17:00:00.000Z"
  }
}
```

#### Response: `201 Created`

```json
{
  "id": "campaign_def456",
  "orgId": "org_xyz789",
  "name": "Customer Outreach Campaign",
  "status": "scheduled",
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customers": [
    { "number": "+12345678901", "name": "Alice Johnson" },
    { "number": "+12345678902", "name": "Bob Smith" },
    { "number": "+12345678903", "name": "Carol Williams" }
  ],
  "schedulePlan": {
    "earliestAt": "2026-03-15T09:00:00.000Z",
    "latestAt": "2026-03-15T17:00:00.000Z"
  },
  "createdAt": "2026-03-02T12:00:00.000Z",
  "updatedAt": "2026-03-02T12:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Outreach Campaign",
    "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
    "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
    "customers": [
      { "number": "+12345678901", "name": "Alice Johnson" },
      { "number": "+12345678902", "name": "Bob Smith" }
    ],
    "schedulePlan": {
      "earliestAt": "2026-03-15T09:00:00.000Z",
      "latestAt": "2026-03-15T17:00:00.000Z"
    }
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const campaign = await vapi.campaigns.create({
  name: "Customer Outreach Campaign",
  assistantId: "5b0a4a08-133c-4146-9315-0984f8c6be80",
  phoneNumberId: "42b4b25d-031e-4786-857f-63b346c9580f",
  customers: [
    { number: "+12345678901", name: "Alice Johnson" },
    { number: "+12345678902", name: "Bob Smith" },
  ],
  schedulePlan: {
    earliestAt: "2026-03-15T09:00:00.000Z",
    latestAt: "2026-03-15T17:00:00.000Z",
  },
});

console.log("Campaign ID:", campaign.id);
console.log("Status:", campaign.status);
```

#### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/campaign"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "name": "Customer Outreach Campaign",
    "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
    "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
    "customers": [
        {"number": "+12345678901", "name": "Alice Johnson"},
        {"number": "+12345678902", "name": "Bob Smith"},
    ],
    "schedulePlan": {
        "earliestAt": "2026-03-15T09:00:00.000Z",
        "latestAt": "2026-03-15T17:00:00.000Z",
    },
}

response = requests.post(url, json=payload, headers=headers)
campaign = response.json()
print(f"Campaign ID: {campaign['id']}")
print(f"Status: {campaign['status']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/campaigns/campaign-controller-create](https://docs.vapi.ai/api-reference/campaigns/campaign-controller-create)

---

### 7. List Campaigns

Retrieves a paginated list of campaigns with optional filtering by status and date range.

#### HTTP Request

```
GET https://api.vapi.ai/campaign
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | No | Filter by specific campaign ID. |
| `status` | string | No | Filter by status: `scheduled`, `in-progress`, `ended`. |
| `page` | number | No | Page number for pagination (default: 1). |
| `limit` | number | No | Maximum items per page (default: 100). |
| `sortOrder` | string | No | Sort order: `ASC` or `DESC` (default: `DESC`). |
| `createdAtGt` | string | No | Filter campaigns created after this ISO 8601 timestamp. |
| `createdAtLt` | string | No | Filter campaigns created before this ISO 8601 timestamp. |
| `createdAtGe` | string | No | Filter campaigns created at or after this ISO 8601 timestamp. |
| `createdAtLe` | string | No | Filter campaigns created at or before this ISO 8601 timestamp. |
| `updatedAtGt` | string | No | Filter campaigns updated after this ISO 8601 timestamp. |
| `updatedAtLt` | string | No | Filter campaigns updated before this ISO 8601 timestamp. |
| `updatedAtGe` | string | No | Filter campaigns updated at or after this ISO 8601 timestamp. |
| `updatedAtLe` | string | No | Filter campaigns updated at or before this ISO 8601 timestamp. |

#### Response: `200 OK`

```json
[
  {
    "id": "campaign_def456",
    "orgId": "org_xyz789",
    "name": "Customer Outreach Campaign",
    "status": "in-progress",
    "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
    "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
    "createdAt": "2026-03-02T12:00:00.000Z",
    "updatedAt": "2026-03-02T14:30:00.000Z"
  },
  {
    "id": "campaign_ghi789",
    "orgId": "org_xyz789",
    "name": "Appointment Reminders",
    "status": "ended",
    "endedReason": "campaign.ended.success",
    "createdAt": "2026-02-28T08:00:00.000Z",
    "updatedAt": "2026-02-28T17:00:00.000Z"
  }
]
```

#### cURL Example

```bash
# List all campaigns
curl -X GET "https://api.vapi.ai/campaign" \
  -H "Authorization: Bearer $VAPI_API_KEY"

# List in-progress campaigns with pagination
curl -X GET "https://api.vapi.ai/campaign?status=in-progress&limit=50&sortOrder=DESC" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const campaigns = await vapi.campaigns.list({
  status: "in-progress",
  limit: 50,
  sortOrder: "DESC",
});

for (const campaign of campaigns) {
  console.log(`${campaign.id} | ${campaign.name} | ${campaign.status}`);
}
```

#### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/campaign"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}
params = {
    "status": "in-progress",
    "limit": 50,
    "sortOrder": "DESC",
}

response = requests.get(url, headers=headers, params=params)
campaigns = response.json()

for campaign in campaigns:
    print(f"{campaign['id']} | {campaign['name']} | {campaign['status']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/campaigns/campaign-controller-find-all](https://docs.vapi.ai/api-reference/campaigns/campaign-controller-find-all)

---

### 8. Get Campaign

Retrieves a single campaign by its ID.
#### HTTP Request

```
GET https://api.vapi.ai/campaign/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the campaign to retrieve. |

#### Response: `200 OK`

```json
{
  "id": "campaign_def456",
  "orgId": "org_xyz789",
  "name": "Customer Outreach Campaign",
  "status": "in-progress",
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customers": [
    { "number": "+12345678901", "name": "Alice Johnson" },
    { "number": "+12345678902", "name": "Bob Smith" },
    { "number": "+12345678903", "name": "Carol Williams" }
  ],
  "schedulePlan": {
    "earliestAt": "2026-03-15T09:00:00.000Z",
    "latestAt": "2026-03-15T17:00:00.000Z"
  },
  "createdAt": "2026-03-02T12:00:00.000Z",
  "updatedAt": "2026-03-02T14:30:00.000Z"
}
```

#### cURL Example

```bash
curl -X GET https://api.vapi.ai/campaign/campaign_def456 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const campaign = await vapi.campaigns.get("campaign_def456");

console.log("Name:", campaign.name);
console.log("Status:", campaign.status);
console.log("Customers:", campaign.customers.length);
```

#### Python Example

```python
import requests
import os

campaign_id = "campaign_def456"
url = f"https://api.vapi.ai/campaign/{campaign_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}

response = requests.get(url, headers=headers)
campaign = response.json()

print(f"Name: {campaign['name']}")
print(f"Status: {campaign['status']}")
print(f"Customers: {len(campaign.get('customers', []))}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/campaigns/campaign-controller-find-one](https://docs.vapi.ai/api-reference/campaigns/campaign-controller-find-one)

---

### 9. Update Campaign

Updates an existing campaign's configuration.
#### HTTP Request

```
PUT https://api.vapi.ai/campaign/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the campaign to update. |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Updated campaign name. |
| `assistantId` | string | No | Updated assistant ID. |
| `phoneNumberId` | string | No | Updated phone number ID. |
| `customers` | array | No | Updated customer list. |
| `schedulePlan` | object | No | Updated scheduling configuration. |
| `maxConcurrentCalls` | number | No | Updated max concurrent calls. |

#### Request Body

```json
{
  "name": "Customer Outreach Campaign - Updated",
  "customers": [
    { "number": "+12345678901", "name": "Alice Johnson" },
    { "number": "+12345678902", "name": "Bob Smith" },
    { "number": "+12345678903", "name": "Carol Williams" },
    { "number": "+12345678904", "name": "Dave Brown" }
  ],
  "schedulePlan": {
    "earliestAt": "2026-03-16T09:00:00.000Z",
    "latestAt": "2026-03-16T17:00:00.000Z"
  }
}
```

#### Response: `200 OK`

```json
{
  "id": "campaign_def456",
  "orgId": "org_xyz789",
  "name": "Customer Outreach Campaign - Updated",
  "status": "scheduled",
  "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
  "phoneNumberId": "42b4b25d-031e-4786-857f-63b346c9580f",
  "customers": [
    { "number": "+12345678901", "name": "Alice Johnson" },
    { "number": "+12345678902", "name": "Bob Smith" },
    { "number": "+12345678903", "name": "Carol Williams" },
    { "number": "+12345678904", "name": "Dave Brown" }
  ],
  "createdAt": "2026-03-02T12:00:00.000Z",
  "updatedAt": "2026-03-02T16:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X PUT https://api.vapi.ai/campaign/campaign_def456 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Outreach Campaign - Updated",
    "customers": [
      { "number": "+12345678901", "name": "Alice Johnson" },
      { "number": "+12345678904", "name": "Dave Brown" }
    ]
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const updatedCampaign = await vapi.campaigns.update("campaign_def456", {
  name: "Customer Outreach Campaign - Updated",
  customers: [
    { number: "+12345678901", name: "Alice Johnson" },
    { number: "+12345678904", name: "Dave Brown" },
  ],
});

console.log("Updated:", updatedCampaign.name);
```

#### Python Example

```python
import requests
import os

campaign_id = "campaign_def456"
url = f"https://api.vapi.ai/campaign/{campaign_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "name": "Customer Outreach Campaign - Updated",
    "customers": [
        {"number": "+12345678901", "name": "Alice Johnson"},
        {"number": "+12345678904", "name": "Dave Brown"},
    ],
}

response = requests.put(url, json=payload, headers=headers)
updated_campaign = response.json()
print(f"Updated: {updated_campaign['name']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/campaigns/campaign-controller-update](https://docs.vapi.ai/api-reference/campaigns/campaign-controller-update)

---

### 10. Delete Campaign

Permanently deletes a campaign.
#### HTTP Request

```
DELETE https://api.vapi.ai/campaign/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the campaign to delete. |

#### Response: `200 OK`

```json
{
  "id": "campaign_def456",
  "orgId": "org_xyz789",
  "name": "Customer Outreach Campaign",
  "status": "ended",
  "endedReason": "campaign.scheduled.ended-by-user",
  "createdAt": "2026-03-02T12:00:00.000Z",
  "updatedAt": "2026-03-02T18:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/campaign/campaign_def456 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const deletedCampaign = await vapi.campaigns.delete("campaign_def456");
console.log("Deleted campaign:", deletedCampaign.id);
```

#### Python Example

```python
import requests
import os

campaign_id = "campaign_def456"
url = f"https://api.vapi.ai/campaign/{campaign_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}

response = requests.delete(url, headers=headers)
deleted_campaign = response.json()
print(f"Deleted campaign: {deleted_campaign['id']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/campaigns/campaign-controller-remove](https://docs.vapi.ai/api-reference/campaigns/campaign-controller-remove)

---

### Campaign Response Schema

Complete schema for the Campaign object returned by all Campaigns API endpoints.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the campaign. |
| `orgId` | string | Organization ID that owns the campaign. |
| `name` | string | Name of the campaign. |
| `status` | string | Campaign status: `scheduled`, `in-progress`, `ended`. |
| `assistantId` | string | ID of the assistant used for campaign calls. |
| `phoneNumberId` | string | ID of the phone number used for outbound calls. |
| `customers` | array | Array of customer objects with `number`, `name`, and optional `metadata`. |
| `schedulePlan` | object | Schedule configuration with `earliestAt` and `latestAt` ISO 8601 timestamps. |
| `maxConcurrentCalls` | number | Maximum simultaneous calls allowed. |
| `endedReason` | string | Reason the campaign ended: `campaign.scheduled.ended-by-user`, `campaign.in-progress.ended-by-user`, `campaign.ended.success`. |
| `createdAt` | string | ISO 8601 timestamp when the campaign was created. |
| `updatedAt` | string | ISO 8601 timestamp when the campaign was last updated. |

---

## Analytics API

### 11. Create Analytics Queries

Executes analytics queries to retrieve aggregated metrics about your calls and subscriptions. This endpoint uses `POST` (not `GET`) to allow complex query structures in the request body.
#### HTTP Request

```
POST https://api.vapi.ai/analytics
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `queries` | array | Yes | Array of `AnalyticsQuery` objects to execute. |

#### AnalyticsQuery Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `table` | string | Yes | Table to query: `call` or `subscription`. |
| `name` | string | Yes | Name to identify this query in the response. |
| `operations` | array | Yes | Array of aggregation operations to perform. |
| `groupBy` | string | No | Column to group results by: `type`, `assistantId`, `endedReason`, `analysis.successEvaluation`, `status`. |
| `groupByVariableValue` | array | No | Array of variable value keys to group by. |
| `timeRange` | object | No | Time range filter for the query. |

#### Operation Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | Aggregation type: `sum`, `avg`, `count`, `min`, `max`, `history`. |
| `column` | string | Yes | Column to aggregate: `cost`, `duration`, `concurrency`, `id` (for count). |
| `alias` | string | No | Custom name for the result column. |

#### TimeRange Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start` | string | No | ISO 8601 start date (defaults to 7 days ago). |
| `end` | string | No | ISO 8601 end date (defaults to now). |
| `step` | string | No | Time aggregation step: `second`, `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year`. |
| `timezone` | string | No | Timezone for the query (defaults to `UTC`). |

#### Request Body: Daily Call Costs

```json
{
  "queries": [
    {
      "name": "Daily Call Costs",
      "table": "call",
      "timeRange": {
        "start": "2026-02-01T00:00:00.000Z",
        "end": "2026-02-28T23:59:59.999Z",
        "step": "day"
      },
      "operations": [
        {
          "operation": "sum",
          "column": "cost",
          "alias": "totalCost"
        }
      ],
      "groupBy": "assistantId"
    }
  ]
}
```

#### Request Body: Multiple Queries

```json
{
  "queries": [
    {
      "name": "Total Calls by Type",
      "table": "call",
      "timeRange": {
        "start": "2026-01-01T00:00:00.000Z",
        "end": "2026-03-01T00:00:00.000Z",
        "step": "month"
      },
      "operations": [
        {
          "operation": "count",
          "column": "id",
          "alias": "callCount"
        }
      ],
      "groupBy": "type"
    },
    {
      "name": "Average Call Duration",
      "table": "call",
      "timeRange": {
        "start": "2026-02-01T00:00:00.000Z",
        "end": "2026-03-01T00:00:00.000Z"
      },
      "operations": [
        {
          "operation": "avg",
          "column": "duration",
          "alias": "avgDuration"
        },
        {
          "operation": "max",
          "column": "duration",
          "alias": "maxDuration"
        },
        {
          "operation": "min",
          "column": "duration",
          "alias": "minDuration"
        }
      ]
    },
    {
      "name": "Ended Reason Breakdown",
      "table": "call",
      "operations": [
        {
          "operation": "count",
          "column": "id",
          "alias": "count"
        }
      ],
      "groupBy": "endedReason"
    }
  ]
}
```

#### Response: `200 OK`

```json
[
  {
    "name": "Daily Call Costs",
    "timeRange": {
      "start": "2026-02-01T00:00:00.000Z",
      "end": "2026-02-28T23:59:59.999Z",
      "step": "day"
    },
    "result": [
      {
        "date": "2026-02-01",
        "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
        "totalCost": 12.50
      },
      {
        "date": "2026-02-02",
        "assistantId": "5b0a4a08-133c-4146-9315-0984f8c6be80",
        "totalCost": 8.75
      }
    ]
  }
]
```

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/analytics \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [{
      "name": "Daily Call Costs",
      "table": "call",
      "timeRange": {
        "start": "2026-02-01T00:00:00.000Z",
        "end": "2026-02-28T23:59:59.999Z",
        "step": "day"
      },
      "operations": [{
        "operation": "sum",
        "column": "cost",
        "alias": "totalCost"
      }],
      "groupBy": "assistantId"
    }]
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const analytics = await vapi.analytics.get({
  queries: [
    {
      name: "Daily Call Costs",
      table: "call",
      timeRange: {
        start: "2026-02-01T00:00:00.000Z",
        end: "2026-02-28T23:59:59.999Z",
        step: "day",
      },
      operations: [
        {
          operation: "sum",
          column: "cost",
          alias: "totalCost",
        },
      ],
      groupBy: "assistantId",
    },
    {
      name: "Call Count by Type",
      table: "call",
      operations: [
        {
          operation: "count",
          column: "id",
          alias: "callCount",
        },
      ],
      groupBy: "type",
    },
  ],
});

for (const query of analytics) {
  console.log(`Query: ${query.name}`);
  console.log("Results:", JSON.stringify(query.result, null, 2));
}
```

#### Python Example

```python
import requests
import os
import json

url = "https://api.vapi.ai/analytics"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "queries": [
        {
            "name": "Daily Call Costs",
            "table": "call",
            "timeRange": {
                "start": "2026-02-01T00:00:00.000Z",
                "end": "2026-02-28T23:59:59.999Z",
                "step": "day",
            },
            "operations": [
                {
                    "operation": "sum",
                    "column": "cost",
                    "alias": "totalCost",
                }
            ],
            "groupBy": "assistantId",
        },
        {
            "name": "Call Count by Type",
            "table": "call",
            "operations": [
                {
                    "operation": "count",
                    "column": "id",
                    "alias": "callCount",
                }
            ],
            "groupBy": "type",
        },
    ],
}

response = requests.post(url, json=payload, headers=headers)
analytics = response.json()

for query in analytics:
    print(f"Query: {query['name']}")
    print(f"Results: {json.dumps(query['result'], indent=2)}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/analytics/get](https://docs.vapi.ai/api-reference/analytics/get)
