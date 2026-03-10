---
name: manage-analytics
description: Query call and subscription analytics in Vapi to track costs, duration, concurrency, and performance metrics. Use when building dashboards, monitoring call costs, analyzing usage patterns, or tracking concurrent calls.
---

# Manage Analytics

This skill covers querying call and subscription analytics in Vapi. Use it to track costs, monitor concurrency, analyze call duration, and build dashboards from your voice AI usage data.

> **See also:** `create-call` (making calls to generate data), `setup-webhook` (real-time event tracking)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- Existing call data to query (at least one completed call)

---

## Quick Start

### Basic Cost Query via cURL

```bash
curl -X POST https://api.vapi.ai/analytics \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "queries": [
      {
        "name": "total-cost",
        "table": "call",
        "operations": [
          { "operation": "sum", "column": "cost" }
        ]
      }
    ]
  }'
```

### Basic Cost Query via Python

```python
import requests

url = "https://api.vapi.ai/analytics"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "queries": [
        {
            "name": "total-cost",
            "table": "call",
            "operations": [
                {"operation": "sum", "column": "cost"}
            ],
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
results = response.json()
for query_result in results:
    print(f"{query_result['name']}: {query_result['result']}")
```

### Basic Cost Query via TypeScript

```typescript
const response = await fetch("https://api.vapi.ai/analytics", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    queries: [
      {
        name: "total-cost",
        table: "call",
        operations: [{ operation: "sum", column: "cost" }],
      },
    ],
  }),
});

const results = await response.json();
results.forEach((r: any) => console.log(`${r.name}:`, r.result));
```

---

## Common Patterns

### Cost Analysis

Track total and average call costs over a time period:

```json
{
  "queries": [
    {
      "name": "cost-analysis",
      "table": "call",
      "operations": [
        { "operation": "sum", "column": "cost", "alias": "totalCost" },
        { "operation": "avg", "column": "cost", "alias": "avgCost" },
        { "operation": "count", "column": "id", "alias": "totalCalls" }
      ],
      "timeRange": {
        "start": "2026-03-01T00:00:00Z",
        "end": "2026-03-10T23:59:59Z",
        "timezone": "America/New_York"
      }
    }
  ]
}
```

### Concurrency Monitoring

Track concurrent call usage to understand peak demand:

```json
{
  "queries": [
    {
      "name": "concurrency-stats",
      "table": "call",
      "operations": [
        { "operation": "max", "column": "concurrency", "alias": "peakConcurrency" },
        { "operation": "avg", "column": "concurrency", "alias": "avgConcurrency" }
      ],
      "timeRange": {
        "start": "2026-03-01T00:00:00Z",
        "end": "2026-03-10T23:59:59Z"
      }
    }
  ]
}
```

### Grouped by Assistant

Break down metrics by assistant to compare performance:

```json
{
  "queries": [
    {
      "name": "per-assistant-stats",
      "table": "call",
      "operations": [
        { "operation": "sum", "column": "cost", "alias": "totalCost" },
        { "operation": "avg", "column": "duration", "alias": "avgDuration" },
        { "operation": "count", "column": "id", "alias": "callCount" }
      ],
      "groupBy": ["assistantId"]
    }
  ]
}
```

### Time-Series Data

Get cost trends over time using the `history` operation with step intervals:

```json
{
  "queries": [
    {
      "name": "daily-cost-trend",
      "table": "call",
      "operations": [
        { "operation": "history", "column": "cost" }
      ],
      "timeRange": {
        "start": "2026-03-01T00:00:00Z",
        "end": "2026-03-10T23:59:59Z",
        "step": "day",
        "timezone": "America/New_York"
      }
    }
  ]
}
```

### Cost Breakdown by Component

Analyze costs broken down by LLM, STT, TTS, and Vapi fees:

```json
{
  "queries": [
    {
      "name": "cost-breakdown",
      "table": "call",
      "operations": [
        { "operation": "sum", "column": "cost", "alias": "totalCost" },
        { "operation": "sum", "column": "costBreakdown.llm", "alias": "llmCost" },
        { "operation": "sum", "column": "costBreakdown.stt", "alias": "sttCost" },
        { "operation": "sum", "column": "costBreakdown.tts", "alias": "ttsCost" },
        { "operation": "sum", "column": "costBreakdown.vapi", "alias": "vapiCost" }
      ],
      "timeRange": {
        "start": "2026-03-01T00:00:00Z",
        "end": "2026-03-10T23:59:59Z"
      }
    }
  ]
}
```

### Calls Grouped by End Reason

Understand why calls are ending:

```json
{
  "queries": [
    {
      "name": "end-reasons",
      "table": "call",
      "operations": [
        { "operation": "count", "column": "id", "alias": "callCount" }
      ],
      "groupBy": ["endedReason"]
    }
  ]
}
```

### Multiple Queries in One Request

Send multiple analytics queries in a single API call:

```bash
curl -X POST https://api.vapi.ai/analytics \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "queries": [
      {
        "name": "cost-summary",
        "table": "call",
        "operations": [
          { "operation": "sum", "column": "cost" }
        ]
      },
      {
        "name": "call-count",
        "table": "call",
        "operations": [
          { "operation": "count", "column": "id" }
        ]
      },
      {
        "name": "avg-duration",
        "table": "call",
        "operations": [
          { "operation": "avg", "column": "duration" }
        ]
      }
    ]
  }'
```

---

## Available Columns

| Column | Description |
|--------|-------------|
| `id` | Call identifier (useful with `count` operation) |
| `cost` | Total call cost in USD |
| `costBreakdown.llm` | LLM/model cost component |
| `costBreakdown.stt` | Speech-to-text cost component |
| `costBreakdown.tts` | Text-to-speech cost component |
| `costBreakdown.vapi` | Vapi platform fee component |
| `duration` | Call duration in seconds |
| `concurrency` | Number of concurrent calls at that time |
| `minutesUsed` | Call duration in minutes |

## Operations

| Operation | Description |
|-----------|-------------|
| `sum` | Sum of all values in the column |
| `avg` | Average of all values in the column |
| `count` | Count of records |
| `min` | Minimum value in the column |
| `max` | Maximum value in the column |
| `history` | Time-series data points (requires `timeRange` with `step`) |

## GroupBy Options

| GroupBy Value | Description |
|---------------|-------------|
| `type` | Call type (inbound, outbound, web) |
| `assistantId` | Group by assistant |
| `endedReason` | Group by call end reason |
| `analysis.successEvaluation` | Group by success/failure evaluation |
| `status` | Group by call status |

## TimeRange Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start` | string | No | Start of time range (ISO 8601) |
| `end` | string | No | End of time range (ISO 8601) |
| `step` | string | No | Time bucket size for `history` operation |
| `timezone` | string | No | IANA timezone (e.g., `America/New_York`) |

**Step values:** `second`, `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year`, `decade`, `century`, `millennium`

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Analytics (1 endpoint) with full parameter details and examples

## Related Skills

- See the `setup-api-key` skill if you need to configure your API key first.
- See the `create-call` skill to generate call data for analytics.
- See the `setup-webhook` skill for real-time call event monitoring.
