# Vapi Insights (Reporting) API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 7 endpoints for the Insights API used to create, manage, and execute reporting insights.

---

## Table of Contents

- [Insights API](#insights-api)
  - [1. List Insights](#1-list-insights)
  - [2. Create Insight](#2-create-insight)
  - [3. Get Insight](#3-get-insight)
  - [4. Delete Insight](#4-delete-insight)
  - [5. Update Insight](#5-update-insight)
  - [6. Run Insight](#6-run-insight)
  - [7. Preview Insight](#7-preview-insight)
- [Schemas](#schemas)
  - [Query Object](#query-object)
  - [Filter Object](#filter-object)
  - [TimeRange Object](#timerange-object)
  - [Formula Object](#formula-object)
  - [Available Call Columns](#available-call-columns)
  - [Filter Operators](#filter-operators)

---

## Insights API

### 1. List Insights

List all insights for your organization (paginated).

#### HTTP Request

```
GET https://api.vapi.ai/reporting/insight
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | number | No | Number of results per page (default: 100) |
| `createdAtGt` | string | No | Return items created after this ISO 8601 datetime |
| `createdAtLt` | string | No | Return items created before this ISO 8601 datetime |
| `createdAtGe` | string | No | Return items created at or after this ISO 8601 datetime |
| `createdAtLe` | string | No | Return items created at or before this ISO 8601 datetime |
| `updatedAtGt` | string | No | Return items updated after this ISO 8601 datetime |
| `updatedAtLt` | string | No | Return items updated before this ISO 8601 datetime |
| `updatedAtGe` | string | No | Return items updated at or after this ISO 8601 datetime |
| `updatedAtLe` | string | No | Return items updated at or before this ISO 8601 datetime |

#### cURL

```bash
curl https://api.vapi.ai/reporting/insight \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python

```python
import os
import requests

response = requests.get(
    "https://api.vapi.ai/reporting/insight",
    headers={"Authorization": f"Bearer {os.environ['VAPI_API_KEY']}"}
)
insights = response.json()
for insight in insights:
    print(f"{insight['id']}: {insight['name']} ({insight['type']})")
```

#### TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/reporting/insight", {
    headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` }
});
const insights = await response.json();
insights.forEach((i: any) => console.log(`${i.id}: ${i.name} (${i.type})`));
```

#### Response

```json
[
  {
    "id": "insight-id-uuid",
    "orgId": "org-id",
    "name": "Calls Per Day",
    "type": "bar",
    "queries": [ ... ],
    "timeRange": { ... },
    "createdAt": "2026-03-01T00:00:00.000Z",
    "updatedAt": "2026-03-01T00:00:00.000Z"
  }
]
```

---

### 2. Create Insight

Create a new reporting insight.

#### HTTP Request

```
POST https://api.vapi.ai/reporting/insight
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name for the insight |
| `type` | string | Yes | Chart type: `bar`, `line`, `pie`, or `text` |
| `queries` | array | Yes | Array of [Query objects](#query-object) defining the data to fetch |
| `formulas` | array | No | Array of [Formula objects](#formula-object) for derived metrics |
| `timeRange` | object | Yes | [TimeRange object](#timerange-object) defining the date range and granularity |
| `metadata` | object | No | Arbitrary key-value metadata for your own use |

#### cURL

```bash
curl -X POST https://api.vapi.ai/reporting/insight \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Daily Call Volume",
    "type": "bar",
    "queries": [
      {
        "name": "dailyCalls",
        "type": "vapiql-json",
        "table": "call",
        "column": "id",
        "operation": "count",
        "groupBy": "startedAt"
      }
    ],
    "timeRange": {
      "start": "-7d",
      "end": "now",
      "step": "day",
      "timezone": "America/New_York"
    }
  }'
```

#### Python

```python
import os
import requests

response = requests.post(
    "https://api.vapi.ai/reporting/insight",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "name": "Daily Call Volume",
        "type": "bar",
        "queries": [
            {
                "name": "dailyCalls",
                "type": "vapiql-json",
                "table": "call",
                "column": "id",
                "operation": "count",
                "groupBy": "startedAt"
            }
        ],
        "timeRange": {
            "start": "-7d",
            "end": "now",
            "step": "day",
            "timezone": "America/New_York"
        }
    }
)
insight = response.json()
print(f"Created insight: {insight['id']}")
```

#### TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/reporting/insight", {
    method: "POST",
    headers: {
        Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: "Daily Call Volume",
        type: "bar",
        queries: [
            {
                name: "dailyCalls",
                type: "vapiql-json",
                table: "call",
                column: "id",
                operation: "count",
                groupBy: "startedAt"
            }
        ],
        timeRange: {
            start: "-7d",
            end: "now",
            step: "day",
            timezone: "America/New_York"
        }
    })
});
const insight = await response.json();
console.log("Created insight:", insight.id);
```

#### Response

```json
{
  "id": "insight-id-uuid",
  "orgId": "org-id",
  "name": "Daily Call Volume",
  "type": "bar",
  "queries": [
    {
      "name": "dailyCalls",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "startedAt"
    }
  ],
  "timeRange": {
    "start": "-7d",
    "end": "now",
    "step": "day",
    "timezone": "America/New_York"
  },
  "createdAt": "2026-03-10T12:00:00.000Z",
  "updatedAt": "2026-03-10T12:00:00.000Z"
}
```

---

### 3. Get Insight

Retrieve a single insight by ID.

#### HTTP Request

```
GET https://api.vapi.ai/reporting/insight/{id}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The insight ID |

#### cURL

```bash
curl https://api.vapi.ai/reporting/insight/insight-id-uuid \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python

```python
import os
import requests

insight_id = "insight-id-uuid"
response = requests.get(
    f"https://api.vapi.ai/reporting/insight/{insight_id}",
    headers={"Authorization": f"Bearer {os.environ['VAPI_API_KEY']}"}
)
insight = response.json()
print(f"Insight: {insight['name']} ({insight['type']})")
```

#### TypeScript

```typescript
const insightId = "insight-id-uuid";
const response = await fetch(
    `https://api.vapi.ai/reporting/insight/${insightId}`,
    { headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` } }
);
const insight = await response.json();
console.log(`Insight: ${insight.name} (${insight.type})`);
```

#### Response

Returns the full insight object (same schema as Create response).

---

### 4. Delete Insight

Delete an insight by ID.

#### HTTP Request

```
DELETE https://api.vapi.ai/reporting/insight/{id}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The insight ID |

#### cURL

```bash
curl -X DELETE https://api.vapi.ai/reporting/insight/insight-id-uuid \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python

```python
import os
import requests

insight_id = "insight-id-uuid"
response = requests.delete(
    f"https://api.vapi.ai/reporting/insight/{insight_id}",
    headers={"Authorization": f"Bearer {os.environ['VAPI_API_KEY']}"}
)
print(f"Deleted: {response.status_code}")
```

#### TypeScript

```typescript
const insightId = "insight-id-uuid";
const response = await fetch(
    `https://api.vapi.ai/reporting/insight/${insightId}`,
    {
        method: "DELETE",
        headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` }
    }
);
console.log("Deleted:", response.status);
```

---

### 5. Update Insight

Partially update an existing insight. Only the fields you include in the request body will be changed.

#### HTTP Request

```
PATCH https://api.vapi.ai/reporting/insight/{id}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The insight ID |

#### Request Body Parameters

All fields are optional. Only provided fields will be updated.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Updated display name |
| `type` | string | Updated chart type: `bar`, `line`, `pie`, or `text` |
| `queries` | array | Updated array of [Query objects](#query-object) |
| `formulas` | array | Updated array of [Formula objects](#formula-object) |
| `timeRange` | object | Updated [TimeRange object](#timerange-object) |
| `metadata` | object | Updated metadata |

#### cURL

```bash
curl -X PATCH https://api.vapi.ai/reporting/insight/insight-id-uuid \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Weekly Call Volume",
    "timeRange": {
      "start": "-30d",
      "end": "now",
      "step": "week",
      "timezone": "UTC"
    }
  }'
```

#### Python

```python
import os
import requests

insight_id = "insight-id-uuid"
response = requests.patch(
    f"https://api.vapi.ai/reporting/insight/{insight_id}",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "name": "Weekly Call Volume",
        "timeRange": {
            "start": "-30d",
            "end": "now",
            "step": "week",
            "timezone": "UTC"
        }
    }
)
updated = response.json()
print(f"Updated: {updated['name']}")
```

#### TypeScript

```typescript
const insightId = "insight-id-uuid";
const response = await fetch(
    `https://api.vapi.ai/reporting/insight/${insightId}`,
    {
        method: "PATCH",
        headers: {
            Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: "Weekly Call Volume",
            timeRange: {
                start: "-30d",
                end: "now",
                step: "week",
                timezone: "UTC"
            }
        })
    }
);
const updated = await response.json();
console.log("Updated:", updated.name);
```

#### Response

Returns the full updated insight object.

---

### 6. Run Insight

Execute a saved insight and return the computed results. Use this to get the actual chart/metric data.

#### HTTP Request

```
POST https://api.vapi.ai/reporting/insight/{id}/run
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The insight ID |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `formatPlan` | object | No | Controls the output format |
| `formatPlan.format` | string | No | `raw` for raw data or `recharts` for Recharts-compatible format |
| `timeRangeOverride` | object | No | Override the saved time range for this run only |
| `timeRangeOverride.start` | string | No | Override start (ISO 8601 or relative like `-7d`) |
| `timeRangeOverride.end` | string | No | Override end (ISO 8601 or `now`) |
| `timeRangeOverride.step` | string | No | Override step: `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year` |
| `timeRangeOverride.timezone` | string | No | Override timezone (IANA format) |

#### cURL

```bash
# Basic run with recharts format
curl -X POST https://api.vapi.ai/reporting/insight/insight-id-uuid/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "formatPlan": {
      "format": "recharts"
    }
  }'
```

```bash
# Run with time range override
curl -X POST https://api.vapi.ai/reporting/insight/insight-id-uuid/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "formatPlan": {
      "format": "recharts"
    },
    "timeRangeOverride": {
      "start": "-24h",
      "end": "now",
      "step": "hour",
      "timezone": "America/Chicago"
    }
  }'
```

#### Python

```python
import os
import requests

insight_id = "insight-id-uuid"

# Basic run
response = requests.post(
    f"https://api.vapi.ai/reporting/insight/{insight_id}/run",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "formatPlan": {"format": "recharts"}
    }
)
results = response.json()
print(results)

# Run with time range override
response = requests.post(
    f"https://api.vapi.ai/reporting/insight/{insight_id}/run",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "formatPlan": {"format": "recharts"},
        "timeRangeOverride": {
            "start": "-24h",
            "end": "now",
            "step": "hour",
            "timezone": "America/Chicago"
        }
    }
)
results = response.json()
print(results)
```

#### TypeScript

```typescript
const insightId = "insight-id-uuid";

// Basic run
const response = await fetch(
    `https://api.vapi.ai/reporting/insight/${insightId}/run`,
    {
        method: "POST",
        headers: {
            Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            formatPlan: { format: "recharts" }
        })
    }
);
const results = await response.json();
console.log(results);

// Run with time range override
const overrideResponse = await fetch(
    `https://api.vapi.ai/reporting/insight/${insightId}/run`,
    {
        method: "POST",
        headers: {
            Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            formatPlan: { format: "recharts" },
            timeRangeOverride: {
                start: "-24h",
                end: "now",
                step: "hour",
                timezone: "America/Chicago"
            }
        })
    }
);
const overrideResults = await overrideResponse.json();
console.log(overrideResults);
```

---

### 7. Preview Insight

Test an insight configuration without saving it. Returns the same result format as Run but does not persist the insight.

#### HTTP Request

```
POST https://api.vapi.ai/reporting/insight/preview
```

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `insight` | object | Yes | Full insight configuration object (same fields as Create) |
| `insight.name` | string | Yes | Display name |
| `insight.type` | string | Yes | Chart type: `bar`, `line`, `pie`, or `text` |
| `insight.queries` | array | Yes | Array of [Query objects](#query-object) |
| `insight.formulas` | array | No | Array of [Formula objects](#formula-object) |
| `insight.timeRange` | object | Yes | [TimeRange object](#timerange-object) |

#### cURL

```bash
curl -X POST https://api.vapi.ai/reporting/insight/preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "insight": {
      "name": "Test: Average Call Duration",
      "type": "line",
      "queries": [
        {
          "name": "avgDuration",
          "type": "vapiql-json",
          "table": "call",
          "column": "duration",
          "operation": "average",
          "groupBy": "startedAt"
        }
      ],
      "timeRange": {
        "start": "-7d",
        "end": "now",
        "step": "day",
        "timezone": "UTC"
      }
    }
  }'
```

#### Python

```python
import os
import requests

response = requests.post(
    "https://api.vapi.ai/reporting/insight/preview",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json"
    },
    json={
        "insight": {
            "name": "Test: Average Call Duration",
            "type": "line",
            "queries": [
                {
                    "name": "avgDuration",
                    "type": "vapiql-json",
                    "table": "call",
                    "column": "duration",
                    "operation": "average",
                    "groupBy": "startedAt"
                }
            ],
            "timeRange": {
                "start": "-7d",
                "end": "now",
                "step": "day",
                "timezone": "UTC"
            }
        }
    }
)
preview = response.json()
print(preview)
```

#### TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/reporting/insight/preview", {
    method: "POST",
    headers: {
        Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        insight: {
            name: "Test: Average Call Duration",
            type: "line",
            queries: [
                {
                    name: "avgDuration",
                    type: "vapiql-json",
                    table: "call",
                    column: "duration",
                    operation: "average",
                    groupBy: "startedAt"
                }
            ],
            timeRange: {
                start: "-7d",
                end: "now",
                step: "day",
                timezone: "UTC"
            }
        }
    })
});
const preview = await response.json();
console.log(preview);
```

---

## Schemas

### Query Object

Each query defines a single data series to fetch from the call table.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for this query (used in formulas as `{{name}}`) |
| `type` | string | Yes | Must be `vapiql-json` |
| `table` | string | Yes | Must be `call` |
| `column` | string | Yes | The column to aggregate. See [Available Call Columns](#available-call-columns). |
| `operation` | string | Yes | Aggregation: `count`, `sum`, `average`, `min`, or `max` |
| `filters` | array | No | Array of [Filter objects](#filter-object) to narrow results |
| `groupBy` | string | No | Column to group results by (e.g., `startedAt`, `status`, `assistantId`) |
| `orderBy` | string | No | Column to order results by |

#### Example

```json
{
  "name": "successfulCalls",
  "type": "vapiql-json",
  "table": "call",
  "column": "id",
  "operation": "count",
  "filters": [
    {
      "column": "status",
      "operator": "=",
      "value": "ended"
    },
    {
      "column": "endedReason",
      "operator": "=",
      "value": "assistant-ended-call"
    }
  ],
  "groupBy": "startedAt"
}
```

---

### Filter Object

Filters narrow the rows included in a query.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `column` | string | Yes | The column to filter on |
| `operator` | string | Yes | The comparison operator (see [Filter Operators](#filter-operators)) |
| `value` | string/number | Yes | The value to compare against |

#### Example

```json
{
  "column": "assistantId",
  "operator": "=",
  "value": "5b0a4a08-133c-4146-9315-0984f8c6be80"
}
```

---

### TimeRange Object

Defines the date window and time granularity for the insight.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `start` | string | Yes | Start of the range. ISO 8601 datetime or relative format: `-7d`, `-24h`, `-30d`, `-1y` |
| `end` | string | Yes | End of the range. ISO 8601 datetime or `now` |
| `step` | string | Yes | Time bucket size: `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year` |
| `timezone` | string | Yes | IANA timezone string (e.g., `UTC`, `America/New_York`, `Europe/London`) |

#### Relative Time Shortcuts

| Format | Meaning |
|--------|---------|
| `-24h` | 24 hours ago |
| `-7d` | 7 days ago |
| `-30d` | 30 days ago |
| `-90d` | 90 days ago |
| `-1y` | 1 year ago |
| `now` | Current time |

#### Example

```json
{
  "start": "-30d",
  "end": "now",
  "step": "day",
  "timezone": "America/New_York"
}
```

---

### Formula Object

Formulas compute derived metrics from query results using MathJS expressions.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Name for this formula result |
| `expression` | string | Yes | MathJS expression using `{{queryName}}` placeholders |

#### Example

```json
{
  "name": "conversionRate",
  "expression": "({{successCalls}} / {{totalCalls}}) * 100"
}
```

#### More Formula Examples

```
{{totalRevenue}} - {{totalCost}}
({{answeredCalls}} / {{totalCalls}}) * 100
{{avgDuration}} / 60
({{completedCalls}} + {{transferredCalls}}) / {{totalCalls}}
```

---

### Available Call Columns

#### String Columns

| Column | Description |
|--------|-------------|
| `assistantId` | ID of the assistant that handled the call |
| `workflowId` | ID of the workflow used |
| `squadId` | ID of the squad used |
| `phoneNumberId` | ID of the phone number used |
| `type` | Call type: `inboundPhoneCall`, `outboundPhoneCall`, `webCall` |
| `customerNumber` | Customer's phone number |
| `status` | Call status: `queued`, `ringing`, `in-progress`, `ended` |
| `endedReason` | Reason the call ended (e.g., `customer-ended-call`, `assistant-ended-call`) |
| `campaignId` | ID of the campaign the call belongs to |

#### Number Columns

| Column | Description |
|--------|-------------|
| `duration` | Call duration in seconds |
| `cost` | Total cost of the call in USD |
| `averageModelLatency` | Average LLM response latency in milliseconds |
| `averageVoiceLatency` | Average text-to-speech latency in milliseconds |
| `averageTranscriberLatency` | Average speech-to-text latency in milliseconds |
| `averageTurnLatency` | Average full conversation turn latency in milliseconds |

#### Date Columns

| Column | Description |
|--------|-------------|
| `startedAt` | When the call started (ISO 8601) |
| `endedAt` | When the call ended (ISO 8601) |

#### Special Columns

| Column | Description |
|--------|-------------|
| `id` | Unique call identifier — typically used with `count` operation |
| `artifact.structuredOutputs[OutputID]` | Access structured output values extracted from the call. Replace `OutputID` with your structured output ID. |

---

### Filter Operators

#### String Column Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `{"column": "status", "operator": "=", "value": "ended"}` |
| `!=` | Not equals | `{"column": "endedReason", "operator": "!=", "value": "pipeline-error"}` |
| `contains` | Contains substring | `{"column": "customerNumber", "operator": "contains", "value": "+1415"}` |
| `not_contains` | Does not contain | `{"column": "endedReason", "operator": "not_contains", "value": "error"}` |

#### Number Column Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `{"column": "duration", "operator": "=", "value": 0}` |
| `!=` | Not equals | `{"column": "cost", "operator": "!=", "value": 0}` |
| `>` | Greater than | `{"column": "duration", "operator": ">", "value": 60}` |
| `<` | Less than | `{"column": "cost", "operator": "<", "value": 1.0}` |
| `>=` | Greater than or equal | `{"column": "duration", "operator": ">=", "value": 30}` |
| `<=` | Less than or equal | `{"column": "averageModelLatency", "operator": "<=", "value": 500}` |

#### Date Column Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `{"column": "startedAt", "operator": "=", "value": "2026-03-01"}` |
| `!=` | Not equals | `{"column": "startedAt", "operator": "!=", "value": "2026-03-01"}` |
| `>` | After | `{"column": "startedAt", "operator": ">", "value": "2026-03-01T00:00:00Z"}` |
| `<` | Before | `{"column": "endedAt", "operator": "<", "value": "2026-03-10T00:00:00Z"}` |
| `>=` | On or after | `{"column": "startedAt", "operator": ">=", "value": "2026-01-01"}` |
| `<=` | On or before | `{"column": "endedAt", "operator": "<=", "value": "2026-12-31"}` |
