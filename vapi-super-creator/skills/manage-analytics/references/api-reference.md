# Vapi Analytics API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers the single analytics endpoint for querying call and subscription metrics.

---

## Table of Contents

- [1. Create Analytics Queries](#1-create-analytics-queries)
- [Query Object Schema](#query-object-schema)
- [Operation Object Schema](#operation-object-schema)
- [TimeRange Object Schema](#timerange-object-schema)
- [Response Schema](#response-schema)
- [Examples](#examples)

---

## 1. Create Analytics Queries

Executes one or more analytics queries against call or subscription data.

### HTTP Request

```
POST https://api.vapi.ai/analytics
```

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `queries` | array | Yes | Array of query objects to execute |

---

## Query Object Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Identifier for this query in the response |
| `table` | string | Yes | Data source: `call` or `subscription` |
| `operations` | array | Yes | Array of operation objects to perform |
| `groupBy` | array | No | Array of fields to group results by |
| `timeRange` | object | No | Time range filter and bucketing configuration |

### Table Values

| Table | Description |
|-------|-------------|
| `call` | Query call data (costs, duration, concurrency, etc.) |
| `subscription` | Query subscription/billing data |

### GroupBy Values

| Value | Description |
|-------|-------------|
| `type` | Call type (inbound, outbound, web) |
| `assistantId` | Group by assistant identifier |
| `endedReason` | Group by call end reason |
| `analysis.successEvaluation` | Group by success/failure evaluation |
| `status` | Group by call status |

---

## Operation Object Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | Aggregation type: `sum`, `avg`, `count`, `min`, `max`, or `history` |
| `column` | string | Yes | Column to aggregate (see available columns below) |
| `alias` | string | No | Custom name for this metric in the response |

### Available Operations

| Operation | Description |
|-----------|-------------|
| `sum` | Sum of all values in the column |
| `avg` | Average of all values in the column |
| `count` | Count of records matching the criteria |
| `min` | Minimum value in the column |
| `max` | Maximum value in the column |
| `history` | Time-series data points (requires `timeRange` with `step`) |

### Available Columns

| Column | Description |
|--------|-------------|
| `id` | Call identifier (typically used with `count`) |
| `cost` | Total call cost in USD |
| `costBreakdown.llm` | LLM/model cost component |
| `costBreakdown.stt` | Speech-to-text cost component |
| `costBreakdown.tts` | Text-to-speech cost component |
| `costBreakdown.vapi` | Vapi platform fee component |
| `duration` | Call duration in seconds |
| `concurrency` | Number of concurrent calls |
| `minutesUsed` | Call duration in minutes |

---

## TimeRange Object Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start` | string | No | Start of range in ISO 8601 format (e.g., `2026-03-01T00:00:00Z`) |
| `end` | string | No | End of range in ISO 8601 format (e.g., `2026-03-10T23:59:59Z`) |
| `step` | string | No | Time bucket size for the `history` operation |
| `timezone` | string | No | IANA timezone identifier (e.g., `America/New_York`) |

### Step Values

| Step | Description |
|------|-------------|
| `second` | Per-second buckets |
| `minute` | Per-minute buckets |
| `hour` | Hourly buckets |
| `day` | Daily buckets |
| `week` | Weekly buckets |
| `month` | Monthly buckets |
| `quarter` | Quarterly buckets |
| `year` | Yearly buckets |
| `decade` | Per-decade buckets |
| `century` | Per-century buckets |
| `millennium` | Per-millennium buckets |

---

## Response Schema

The endpoint returns an array of result objects, one per query submitted.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The query name matching the request |
| `timeRange` | object | The time range applied (echoed back) |
| `result` | array | Array of result row objects |

### Result Row Object

Each row in the `result` array contains:

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Timestamp for the data point (for `history` operations) |
| *metric fields* | number | One field per operation, keyed by `alias` or default naming |

---

## Examples

### Example 1: Basic Cost Query

Query total call cost for the current month.

```bash
curl -X POST https://api.vapi.ai/analytics \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "queries": [
      {
        "name": "monthly-cost",
        "table": "call",
        "operations": [
          { "operation": "sum", "column": "cost", "alias": "totalCost" },
          { "operation": "count", "column": "id", "alias": "totalCalls" }
        ],
        "timeRange": {
          "start": "2026-03-01T00:00:00Z",
          "end": "2026-03-31T23:59:59Z",
          "timezone": "America/New_York"
        }
      }
    ]
  }'
```

**Response:**

```json
[
  {
    "name": "monthly-cost",
    "timeRange": {
      "start": "2026-03-01T00:00:00Z",
      "end": "2026-03-31T23:59:59Z"
    },
    "result": [
      {
        "totalCost": 142.57,
        "totalCalls": 1283
      }
    ]
  }
]
```

### Example 2: Concurrency Monitoring

Track peak and average concurrency over the past week.

```bash
curl -X POST https://api.vapi.ai/analytics \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "queries": [
      {
        "name": "concurrency-stats",
        "table": "call",
        "operations": [
          { "operation": "max", "column": "concurrency", "alias": "peakConcurrency" },
          { "operation": "avg", "column": "concurrency", "alias": "avgConcurrency" },
          { "operation": "history", "column": "concurrency" }
        ],
        "timeRange": {
          "start": "2026-03-03T00:00:00Z",
          "end": "2026-03-10T23:59:59Z",
          "step": "hour",
          "timezone": "America/New_York"
        }
      }
    ]
  }'
```

**Response:**

```json
[
  {
    "name": "concurrency-stats",
    "timeRange": {
      "start": "2026-03-03T00:00:00Z",
      "end": "2026-03-10T23:59:59Z",
      "step": "hour"
    },
    "result": [
      {
        "date": "2026-03-03T00:00:00Z",
        "peakConcurrency": 8,
        "avgConcurrency": 3.2,
        "concurrency": 4
      },
      {
        "date": "2026-03-03T01:00:00Z",
        "peakConcurrency": 8,
        "avgConcurrency": 3.2,
        "concurrency": 2
      }
    ]
  }
]
```

### Example 3: Grouped Analysis by Assistant

Compare cost and call volume across different assistants.

```bash
curl -X POST https://api.vapi.ai/analytics \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "queries": [
      {
        "name": "per-assistant",
        "table": "call",
        "operations": [
          { "operation": "sum", "column": "cost", "alias": "totalCost" },
          { "operation": "avg", "column": "duration", "alias": "avgDuration" },
          { "operation": "count", "column": "id", "alias": "callCount" },
          { "operation": "sum", "column": "costBreakdown.llm", "alias": "llmCost" },
          { "operation": "sum", "column": "costBreakdown.tts", "alias": "ttsCost" }
        ],
        "groupBy": ["assistantId"],
        "timeRange": {
          "start": "2026-03-01T00:00:00Z",
          "end": "2026-03-10T23:59:59Z",
          "timezone": "America/New_York"
        }
      }
    ]
  }'
```

**Response:**

```json
[
  {
    "name": "per-assistant",
    "timeRange": {
      "start": "2026-03-01T00:00:00Z",
      "end": "2026-03-10T23:59:59Z"
    },
    "result": [
      {
        "assistantId": "assistant-uuid-1",
        "totalCost": 87.32,
        "avgDuration": 245.6,
        "callCount": 812,
        "llmCost": 42.15,
        "ttsCost": 28.90
      },
      {
        "assistantId": "assistant-uuid-2",
        "totalCost": 55.25,
        "avgDuration": 180.3,
        "callCount": 471,
        "llmCost": 25.40,
        "ttsCost": 18.22
      }
    ]
  }
]
```
