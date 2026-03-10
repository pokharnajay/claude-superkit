# Vapi Campaigns API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 5 endpoints in the Campaigns API for creating, retrieving, updating, and deleting outbound calling campaigns.

---

## Table of Contents

- [Campaigns API](#campaigns-api)
  - [1. List Campaigns](#1-list-campaigns)
  - [2. Create Campaign](#2-create-campaign)
  - [3. Get Campaign](#3-get-campaign)
  - [4. Delete Campaign](#4-delete-campaign)
  - [5. Update Campaign](#5-update-campaign)
- [Campaign Object Schema](#campaign-object-schema)

---

## Campaigns API

### 1. List Campaigns

Retrieves a paginated list of all campaigns in the organization. Supports filtering by status.

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
| `status` | string | No | Filter by campaign status: `scheduled`, `in-progress`, or `ended` |
| `page` | number | No | Page number for pagination |
| `limit` | number | No | Number of results per page (default: 100) |
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

- **200 OK** -- Array of Campaign objects

#### cURL Example

```bash
curl https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With status filter and pagination:**

```bash
curl "https://api.vapi.ai/campaign?status=in-progress&limit=10&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/campaign"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}
params = {
    "status": "in-progress",
    "limit": 10,
    "sortOrder": "desc",
}

response = requests.get(url, headers=headers, params=params)
campaigns = response.json()

for c in campaigns:
    print(f"ID: {c['id']}, Name: {c['name']}, Status: {c['status']}")
```

#### TypeScript Example

```typescript
const params = new URLSearchParams({
  status: "in-progress",
  limit: "10",
  sortOrder: "desc",
});

const response = await fetch(`https://api.vapi.ai/campaign?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const campaigns = await response.json();
campaigns.forEach((c: any) => {
  console.log(`ID: ${c.id}, Name: ${c.name}, Status: ${c.status}`);
});
```

#### Example Response

```json
[
  {
    "id": "camp_abc123",
    "orgId": "org_xyz789",
    "name": "Customer Outreach Campaign",
    "assistantId": "asst_def456",
    "phoneNumberId": "pn_ghi789",
    "customers": [
      { "number": "+14151234567", "name": "John Doe" },
      { "number": "+14159876543", "name": "Jane Smith" }
    ],
    "status": "in-progress",
    "maxConcurrentCalls": 5,
    "createdAt": "2026-03-01T10:00:00.000Z",
    "updatedAt": "2026-03-01T10:05:00.000Z"
  }
]
```

---

### 2. Create Campaign

Creates a new outbound calling campaign. You must provide an assistant (or squad/workflow), a phone number, and a list of customers to call.

#### HTTP Request

```
POST https://api.vapi.ai/campaign
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display name for the campaign |
| `assistantId` | string | Conditional | ID of the assistant to handle calls. Mutually exclusive with `squadId` and `workflowId` |
| `squadId` | string | Conditional | ID of the squad to handle calls. Mutually exclusive with `assistantId` and `workflowId` |
| `workflowId` | string | Conditional | ID of the workflow to handle calls. Mutually exclusive with `assistantId` and `squadId` |
| `phoneNumberId` | string | Yes | ID of the phone number to use for outbound calls |
| `customers` | array | Yes | Array of customer objects. Each must have a `number` field in E.164 format. Additional fields become dynamic variables |
| `schedule` | object | No | Scheduling configuration (see Schedule Object below) |
| `maxConcurrentCalls` | number | No | Maximum number of simultaneous calls |
| `assistantOverrides` | object | No | Override assistant config (model, transcriber, voice, etc.) for this campaign |

**Schedule Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `startTime` | string | Yes | ISO 8601 timestamp for when to start calling |
| `endTime` | string | Yes | ISO 8601 timestamp for when to stop calling |
| `timezone` | string | No | IANA timezone string (e.g., `America/New_York`) |

**Customer Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `number` | string | Yes | Phone number in E.164 format (e.g., `+14151234567`) |
| `name` | string | No | Customer name |
| *custom fields* | string | No | Any additional key-value pairs become template variables accessible via `{{fieldName}}` |

**Assistant Overrides Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | object | No | Override the LLM model configuration (provider, model, temperature, etc.) |
| `transcriber` | object | No | Override the transcriber configuration (provider, language, etc.) |
| `voice` | object | No | Override the voice configuration (provider, voiceId, etc.) |
| `firstMessage` | string | No | Override the assistant's first message |
| `recordingEnabled` | boolean | No | Enable/disable call recording for this campaign |

#### Response

- **201 Created** -- Campaign object

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/campaign \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Demo Outreach",
    "assistantId": "asst_def456",
    "phoneNumberId": "pn_ghi789",
    "customers": [
      { "number": "+14151234567", "name": "John Doe", "product": "Enterprise" },
      { "number": "+14159876543", "name": "Jane Smith", "product": "Pro" }
    ],
    "schedule": {
      "startTime": "2026-03-15T09:00:00Z",
      "endTime": "2026-03-15T17:00:00Z",
      "timezone": "America/New_York"
    },
    "maxConcurrentCalls": 5
  }'
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/campaign"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "name": "Product Demo Outreach",
    "assistantId": "asst_def456",
    "phoneNumberId": "pn_ghi789",
    "customers": [
        {"number": "+14151234567", "name": "John Doe", "product": "Enterprise"},
        {"number": "+14159876543", "name": "Jane Smith", "product": "Pro"},
    ],
    "schedule": {
        "startTime": "2026-03-15T09:00:00Z",
        "endTime": "2026-03-15T17:00:00Z",
        "timezone": "America/New_York",
    },
    "maxConcurrentCalls": 5,
}

response = requests.post(url, headers=headers, json=payload)
campaign = response.json()

print(f"Campaign ID: {campaign['id']}")
print(f"Status: {campaign['status']}")
print(f"Customers: {len(campaign['customers'])}")
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/campaign", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Product Demo Outreach",
    assistantId: "asst_def456",
    phoneNumberId: "pn_ghi789",
    customers: [
      { number: "+14151234567", name: "John Doe", product: "Enterprise" },
      { number: "+14159876543", name: "Jane Smith", product: "Pro" },
    ],
    schedule: {
      startTime: "2026-03-15T09:00:00Z",
      endTime: "2026-03-15T17:00:00Z",
      timezone: "America/New_York",
    },
    maxConcurrentCalls: 5,
  }),
});

const campaign = await response.json();
console.log(`Campaign ID: ${campaign.id}`);
console.log(`Status: ${campaign.status}`);
console.log(`Customers: ${campaign.customers.length}`);
```

#### Example Response

```json
{
  "id": "camp_abc123",
  "orgId": "org_xyz789",
  "name": "Product Demo Outreach",
  "assistantId": "asst_def456",
  "phoneNumberId": "pn_ghi789",
  "customers": [
    { "number": "+14151234567", "name": "John Doe", "product": "Enterprise" },
    { "number": "+14159876543", "name": "Jane Smith", "product": "Pro" }
  ],
  "schedule": {
    "startTime": "2026-03-15T09:00:00Z",
    "endTime": "2026-03-15T17:00:00Z",
    "timezone": "America/New_York"
  },
  "status": "scheduled",
  "maxConcurrentCalls": 5,
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:00.000Z"
}
```

---

### 3. Get Campaign

Retrieves a single campaign by its ID, including current status and customer list.

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
| `id` | string | Yes | The unique campaign identifier |

#### Response

- **200 OK** -- Campaign object

#### cURL Example

```bash
curl https://api.vapi.ai/campaign/camp_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

campaign_id = "camp_abc123"
url = f"https://api.vapi.ai/campaign/{campaign_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.get(url, headers=headers)
campaign = response.json()

print(f"Name: {campaign['name']}")
print(f"Status: {campaign['status']}")
print(f"Customers: {len(campaign['customers'])}")
print(f"Max Concurrent Calls: {campaign.get('maxConcurrentCalls', 'N/A')}")
```

#### TypeScript Example

```typescript
const campaignId = "camp_abc123";

const response = await fetch(`https://api.vapi.ai/campaign/${campaignId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const campaign = await response.json();
console.log(`Name: ${campaign.name}`);
console.log(`Status: ${campaign.status}`);
console.log(`Customers: ${campaign.customers.length}`);
console.log(`Max Concurrent Calls: ${campaign.maxConcurrentCalls ?? "N/A"}`);
```

#### Example Response

```json
{
  "id": "camp_abc123",
  "orgId": "org_xyz789",
  "name": "Product Demo Outreach",
  "assistantId": "asst_def456",
  "phoneNumberId": "pn_ghi789",
  "customers": [
    { "number": "+14151234567", "name": "John Doe", "product": "Enterprise" },
    { "number": "+14159876543", "name": "Jane Smith", "product": "Pro" }
  ],
  "schedule": {
    "startTime": "2026-03-15T09:00:00Z",
    "endTime": "2026-03-15T17:00:00Z",
    "timezone": "America/New_York"
  },
  "status": "in-progress",
  "maxConcurrentCalls": 5,
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-15T09:00:05.000Z"
}
```

---

### 4. Delete Campaign

Deletes a campaign by its ID. Returns the deleted campaign object.

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
| `id` | string | Yes | The unique campaign identifier |

#### Response

- **200 OK** -- Deleted Campaign object

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/campaign/camp_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

campaign_id = "camp_abc123"
url = f"https://api.vapi.ai/campaign/{campaign_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.delete(url, headers=headers)
deleted = response.json()
print(f"Deleted campaign: {deleted['id']} ({deleted['name']})")
```

#### TypeScript Example

```typescript
const campaignId = "camp_abc123";

const response = await fetch(`https://api.vapi.ai/campaign/${campaignId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const deleted = await response.json();
console.log(`Deleted campaign: ${deleted.id} (${deleted.name})`);
```

#### Example Response

```json
{
  "id": "camp_abc123",
  "orgId": "org_xyz789",
  "name": "Product Demo Outreach",
  "assistantId": "asst_def456",
  "phoneNumberId": "pn_ghi789",
  "customers": [
    { "number": "+14151234567", "name": "John Doe", "product": "Enterprise" },
    { "number": "+14159876543", "name": "Jane Smith", "product": "Pro" }
  ],
  "status": "ended",
  "maxConcurrentCalls": 5,
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T16:30:00.000Z"
}
```

---

### 5. Update Campaign

Updates an existing campaign's properties. Use this to modify the name, customer list, schedule, concurrency settings, or assistant overrides.

#### HTTP Request

```
PATCH https://api.vapi.ai/campaign/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique campaign identifier |

#### Request Body

All fields are optional. Only include the fields you want to update.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Updated campaign name |
| `assistantId` | string | No | Updated assistant ID |
| `squadId` | string | No | Updated squad ID |
| `workflowId` | string | No | Updated workflow ID |
| `phoneNumberId` | string | No | Updated phone number ID |
| `customers` | array | No | Updated customer list (replaces entire list) |
| `schedule` | object | No | Updated schedule configuration |
| `maxConcurrentCalls` | number | No | Updated max concurrent calls |
| `assistantOverrides` | object | No | Updated assistant overrides (model, transcriber, voice, etc.) |

#### Response

- **200 OK** -- Updated Campaign object

#### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/campaign/camp_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Campaign Name",
    "maxConcurrentCalls": 10,
    "customers": [
      { "number": "+14151234567", "name": "John Doe" },
      { "number": "+14159876543", "name": "Jane Smith" },
      { "number": "+12125551234", "name": "New Customer" }
    ]
  }'
```

#### Python Example

```python
import requests

campaign_id = "camp_abc123"
url = f"https://api.vapi.ai/campaign/{campaign_id}"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "name": "Updated Campaign Name",
    "maxConcurrentCalls": 10,
    "customers": [
        {"number": "+14151234567", "name": "John Doe"},
        {"number": "+14159876543", "name": "Jane Smith"},
        {"number": "+12125551234", "name": "New Customer"},
    ],
}

response = requests.patch(url, headers=headers, json=payload)
updated = response.json()

print(f"Updated: {updated['name']}")
print(f"Customers: {len(updated['customers'])}")
print(f"Max Concurrent: {updated['maxConcurrentCalls']}")
```

#### TypeScript Example

```typescript
const campaignId = "camp_abc123";

const response = await fetch(`https://api.vapi.ai/campaign/${campaignId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    name: "Updated Campaign Name",
    maxConcurrentCalls: 10,
    customers: [
      { number: "+14151234567", name: "John Doe" },
      { number: "+14159876543", name: "Jane Smith" },
      { number: "+12125551234", name: "New Customer" },
    ],
  }),
});

const updated = await response.json();
console.log(`Updated: ${updated.name}`);
console.log(`Customers: ${updated.customers.length}`);
console.log(`Max Concurrent: ${updated.maxConcurrentCalls}`);
```

#### Example Response

```json
{
  "id": "camp_abc123",
  "orgId": "org_xyz789",
  "name": "Updated Campaign Name",
  "assistantId": "asst_def456",
  "phoneNumberId": "pn_ghi789",
  "customers": [
    { "number": "+14151234567", "name": "John Doe" },
    { "number": "+14159876543", "name": "Jane Smith" },
    { "number": "+12125551234", "name": "New Customer" }
  ],
  "status": "scheduled",
  "maxConcurrentCalls": 10,
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T16:45:00.000Z"
}
```

---

## Campaign Object Schema

The Campaign object is returned by all campaign endpoints.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique campaign identifier |
| `orgId` | string | Organization ID that owns the campaign |
| `name` | string | Display name of the campaign |
| `assistantId` | string \| null | ID of the assistant handling calls (mutually exclusive with `squadId`, `workflowId`) |
| `squadId` | string \| null | ID of the squad handling calls (mutually exclusive with `assistantId`, `workflowId`) |
| `workflowId` | string \| null | ID of the workflow handling calls (mutually exclusive with `assistantId`, `squadId`) |
| `phoneNumberId` | string | ID of the phone number used for outbound calls |
| `customers` | array | Array of customer objects, each with `number` (E.164) and optional dynamic variable fields |
| `schedule` | object \| null | Schedule configuration with `startTime`, `endTime`, and optional `timezone` |
| `status` | string | Campaign status: `scheduled`, `in-progress`, or `ended` |
| `maxConcurrentCalls` | number \| null | Maximum simultaneous calls allowed for this campaign |
| `assistantOverrides` | object \| null | Optional overrides for model, transcriber, voice, and other assistant settings |
| `createdAt` | string | ISO 8601 timestamp of when the campaign was created |
| `updatedAt` | string | ISO 8601 timestamp of when the campaign was last updated |

### Status Values

| Status | Description |
|--------|-------------|
| `scheduled` | Campaign is created and scheduled but has not started calling yet |
| `in-progress` | Campaign is actively making calls to the customer list |
| `ended` | Campaign has completed all calls or was manually stopped |

### Customer Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `number` | string | Yes | Phone number in E.164 format (`+[country code][subscriber number]`, max 15 digits) |
| `name` | string | No | Customer name, accessible as `{{name}}` in assistant prompt |
| *custom fields* | string | No | Additional key-value pairs become template variables (`{{fieldName}}`) |

### Schedule Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `startTime` | string | Yes | ISO 8601 timestamp for when calling should begin |
| `endTime` | string | Yes | ISO 8601 timestamp for when calling should stop |
| `timezone` | string | No | IANA timezone (e.g., `America/New_York`, `Europe/London`) |
