# Scorecards API Reference

**Base URL:** `https://api.vapi.ai`
**Base Path:** `/observability/scorecard`
**Authentication:** Bearer token via `Authorization` header.

---

## Endpoints

### 1. List Scorecards

```
GET /observability/scorecard
```

Returns a paginated list of scorecards for the authenticated organization.

**Query Parameters:**

| Parameter | Type   | Description                  |
|-----------|--------|------------------------------|
| page      | number | Page number (default: 1)     |
| limit     | number | Items per page (default: 20) |

**cURL:**

```bash
curl "https://api.vapi.ai/observability/scorecard?page=1&limit=10" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

response = requests.get(
    "https://api.vapi.ai/observability/scorecard",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 10},
)
scorecards = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(
  "https://api.vapi.ai/observability/scorecard?page=1&limit=10",
  {
    headers: { Authorization: `Bearer ${VAPI_API_KEY}` },
  }
);
const scorecards = await response.json();
```

---

### 2. Create Scorecard

```
POST /observability/scorecard
```

Creates a new scorecard.

**Request Body:**

| Field        | Type     | Required | Description                                      |
|--------------|----------|----------|--------------------------------------------------|
| name         | string   | Yes      | Name of the scorecard                            |
| description  | string   | No       | Description of the scorecard                     |
| metrics      | array    | Yes      | Array of metric objects (at least one required)  |
| assistantIds | string[] | No       | UUIDs of assistants to scope this scorecard to   |

**Metric Object:**

| Field              | Type   | Required | Description                                        |
|--------------------|--------|----------|----------------------------------------------------|
| structuredOutputId | string | Yes      | UUID of the structured output to evaluate          |
| conditions         | array  | Yes      | Array of condition objects (at least one required)  |

**Condition Object:**

| Field      | Type             | Required | Description                                          |
|------------|------------------|----------|------------------------------------------------------|
| type       | string           | Yes      | Must be `"comparator"`                               |
| comparator | string           | Yes      | One of: `=`, `!=`, `>`, `<`, `>=`, `<=`             |
| value      | number \| boolean | Yes      | The value to compare the structured output against   |
| points     | number           | Yes      | Points awarded when this condition matches (0-100)   |

**Validation Rules:**
- Points across all conditions within a single metric must sum to exactly 100.
- Each referenced structured output must have a type of `number` or `boolean`.

**cURL:**

```bash
curl -X POST "https://api.vapi.ai/observability/scorecard" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Issue Resolution",
    "description": "Scores whether the agent resolved the issue",
    "metrics": [
      {
        "structuredOutputId": "abc12345-def6-7890-abcd-ef1234567890",
        "conditions": [
          { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
          { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
        ]
      }
    ],
    "assistantIds": ["11111111-2222-3333-4444-555555555555"]
  }'
```

**Python:**

```python
import requests

payload = {
    "name": "Issue Resolution",
    "description": "Scores whether the agent resolved the issue",
    "metrics": [
        {
            "structuredOutputId": "abc12345-def6-7890-abcd-ef1234567890",
            "conditions": [
                {"type": "comparator", "comparator": "=", "value": True, "points": 100},
                {"type": "comparator", "comparator": "=", "value": False, "points": 0},
            ],
        }
    ],
    "assistantIds": ["11111111-2222-3333-4444-555555555555"],
}

response = requests.post(
    "https://api.vapi.ai/observability/scorecard",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
)
scorecard = response.json()
```

**TypeScript:**

```typescript
const payload = {
  name: "Issue Resolution",
  description: "Scores whether the agent resolved the issue",
  metrics: [
    {
      structuredOutputId: "abc12345-def6-7890-abcd-ef1234567890",
      conditions: [
        { type: "comparator", comparator: "=", value: true, points: 100 },
        { type: "comparator", comparator: "=", value: false, points: 0 },
      ],
    },
  ],
  assistantIds: ["11111111-2222-3333-4444-555555555555"],
};

const response = await fetch("https://api.vapi.ai/observability/scorecard", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(payload),
});
const scorecard = await response.json();
```

---

### 3. Get Scorecard

```
GET /observability/scorecard/{id}
```

Retrieves a single scorecard by ID.

**Path Parameters:**

| Parameter | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| id        | string | Yes      | UUID of the scorecard |

**cURL:**

```bash
curl "https://api.vapi.ai/observability/scorecard/SCORECARD_UUID" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

scorecard_id = "SCORECARD_UUID"
response = requests.get(
    f"https://api.vapi.ai/observability/scorecard/{scorecard_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
scorecard = response.json()
```

**TypeScript:**

```typescript
const scorecardId = "SCORECARD_UUID";
const response = await fetch(
  `https://api.vapi.ai/observability/scorecard/${scorecardId}`,
  {
    headers: { Authorization: `Bearer ${VAPI_API_KEY}` },
  }
);
const scorecard = await response.json();
```

---

### 4. Delete Scorecard

```
DELETE /observability/scorecard/{id}
```

Deletes a scorecard by ID.

**Path Parameters:**

| Parameter | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| id        | string | Yes      | UUID of the scorecard |

**cURL:**

```bash
curl -X DELETE "https://api.vapi.ai/observability/scorecard/SCORECARD_UUID" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

scorecard_id = "SCORECARD_UUID"
response = requests.delete(
    f"https://api.vapi.ai/observability/scorecard/{scorecard_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
```

**TypeScript:**

```typescript
const scorecardId = "SCORECARD_UUID";
const response = await fetch(
  `https://api.vapi.ai/observability/scorecard/${scorecardId}`,
  {
    method: "DELETE",
    headers: { Authorization: `Bearer ${VAPI_API_KEY}` },
  }
);
```

---

### 5. Update Scorecard

```
PATCH /observability/scorecard/{id}
```

Partially updates a scorecard. All fields are optional.

**Path Parameters:**

| Parameter | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| id        | string | Yes      | UUID of the scorecard |

**Request Body (all fields optional):**

| Field        | Type     | Description                                      |
|--------------|----------|--------------------------------------------------|
| name         | string   | Updated name                                     |
| description  | string   | Updated description                              |
| metrics      | array    | Replacement array of metric objects               |
| assistantIds | string[] | Replacement array of assistant UUIDs              |

When updating `metrics`, the entire metrics array is replaced. Provide the full desired set of metrics.

**cURL:**

```bash
curl -X PATCH "https://api.vapi.ai/observability/scorecard/SCORECARD_UUID" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Scorecard Name",
    "description": "Updated description",
    "metrics": [
      {
        "structuredOutputId": "abc12345-def6-7890-abcd-ef1234567890",
        "conditions": [
          { "type": "comparator", "comparator": ">=", "value": 4, "points": 100 },
          { "type": "comparator", "comparator": "<", "value": 4, "points": 0 }
        ]
      }
    ]
  }'
```

**Python:**

```python
import requests

scorecard_id = "SCORECARD_UUID"
payload = {
    "name": "Updated Scorecard Name",
    "description": "Updated description",
}

response = requests.patch(
    f"https://api.vapi.ai/observability/scorecard/{scorecard_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
)
scorecard = response.json()
```

**TypeScript:**

```typescript
const scorecardId = "SCORECARD_UUID";
const payload = {
  name: "Updated Scorecard Name",
  description: "Updated description",
};

const response = await fetch(
  `https://api.vapi.ai/observability/scorecard/${scorecardId}`,
  {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${VAPI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  }
);
const scorecard = await response.json();
```

---

## Response Schema

All scorecard responses share this structure:

| Field        | Type     | Description                                         |
|--------------|----------|-----------------------------------------------------|
| id           | string   | UUID of the scorecard                               |
| orgId        | string   | UUID of the organization that owns the scorecard    |
| name         | string   | Name of the scorecard                               |
| description  | string   | Description of the scorecard (may be null)          |
| metrics      | array    | Array of metric objects                             |
| assistantIds | string[] | Array of assistant UUIDs linked to this scorecard   |
| createdAt    | string   | ISO 8601 timestamp of creation                      |
| updatedAt    | string   | ISO 8601 timestamp of last update                   |

**Example Response:**

```json
{
  "id": "99999999-aaaa-bbbb-cccc-dddddddddddd",
  "orgId": "org-uuid-here",
  "name": "Issue Resolution",
  "description": "Scores whether the agent resolved the issue",
  "metrics": [
    {
      "structuredOutputId": "abc12345-def6-7890-abcd-ef1234567890",
      "conditions": [
        { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
        { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
      ]
    }
  ],
  "assistantIds": ["11111111-2222-3333-4444-555555555555"],
  "createdAt": "2026-03-10T12:00:00.000Z",
  "updatedAt": "2026-03-10T12:00:00.000Z"
}
```
