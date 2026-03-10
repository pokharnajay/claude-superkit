---
name: manage-insights
description: Create and manage reporting insights in Vapi to analyze call data with charts, metrics, and formulas. Use when building dashboards, tracking call volume, measuring conversion rates, or analyzing assistant performance.
---

# Manage Insights (Reporting)

This skill covers creating, running, and managing reporting insights in Vapi. Insights let you build dashboards with bar charts, line charts, pie charts, and text metrics to analyze call data, track KPIs, and measure assistant performance.

## Prerequisites

- Vapi account with API key configured (see the `setup-api-key` skill)
- At least some call data in your account to query against
- Familiarity with the call data model (columns like `status`, `duration`, `cost`, `assistantId`)

## Quick Start — Create a Bar Chart Insight

### cURL

```bash
curl -X POST https://api.vapi.ai/reporting/insight \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Calls Per Day",
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

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({
    token: process.env.VAPI_API_KEY!
});

const insight = await vapi.reporting.insight.create({
    name: "Calls Per Day",
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
});

console.log("Insight ID:", insight.id);
```

### Python (Server SDK)

```python
import os
from vapi import VapiClient

client = VapiClient(token=os.environ["VAPI_API_KEY"])

insight = client.reporting.insight.create(
    name="Calls Per Day",
    type="bar",
    queries=[
        {
            "name": "dailyCalls",
            "type": "vapiql-json",
            "table": "call",
            "column": "id",
            "operation": "count",
            "groupBy": "startedAt"
        }
    ],
    time_range={
        "start": "-7d",
        "end": "now",
        "step": "day",
        "timezone": "America/New_York"
    }
)

print(f"Insight ID: {insight.id}")
```

## Operations

### Create an Insight

```bash
curl -X POST https://api.vapi.ai/reporting/insight \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "My Insight",
    "type": "bar",
    "queries": [ ... ],
    "timeRange": { "start": "-30d", "end": "now", "step": "day", "timezone": "UTC" }
  }'
```

### List Insights

```bash
curl https://api.vapi.ai/reporting/insight \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get a Specific Insight

```bash
curl https://api.vapi.ai/reporting/insight/<insight-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update an Insight

```bash
curl -X PATCH https://api.vapi.ai/reporting/insight/<insight-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Insight Name",
    "timeRange": { "start": "-14d", "end": "now", "step": "day", "timezone": "UTC" }
  }'
```

### Delete an Insight

```bash
curl -X DELETE https://api.vapi.ai/reporting/insight/<insight-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Run an Insight

Execute a saved insight and retrieve the computed results:

```bash
curl -X POST https://api.vapi.ai/reporting/insight/<insight-id>/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "formatPlan": {
      "format": "recharts"
    }
  }'
```

You can override the time range at run time without modifying the saved insight:

```bash
curl -X POST https://api.vapi.ai/reporting/insight/<insight-id>/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "formatPlan": { "format": "recharts" },
    "timeRangeOverride": {
      "start": "-24h",
      "end": "now",
      "step": "hour",
      "timezone": "America/Chicago"
    }
  }'
```

### Preview an Insight (Without Saving)

Test an insight configuration without persisting it:

```bash
curl -X POST https://api.vapi.ai/reporting/insight/preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "insight": {
      "name": "Test Insight",
      "type": "line",
      "queries": [
        {
          "name": "callVolume",
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
        "timezone": "UTC"
      }
    }
  }'
```

## Common Patterns

### Bar Chart — Calls by Status

```json
{
  "name": "Calls by Status",
  "type": "bar",
  "queries": [
    {
      "name": "statusBreakdown",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "status"
    }
  ],
  "timeRange": {
    "start": "-30d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Line Chart — Call Volume Over Time

```json
{
  "name": "Call Volume Trend",
  "type": "line",
  "queries": [
    {
      "name": "dailyVolume",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "startedAt"
    }
  ],
  "timeRange": {
    "start": "-30d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Pie Chart — Calls by Ended Reason

```json
{
  "name": "End Reasons Distribution",
  "type": "pie",
  "queries": [
    {
      "name": "endReasons",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "endedReason"
    }
  ],
  "timeRange": {
    "start": "-30d",
    "end": "now",
    "step": "month",
    "timezone": "UTC"
  }
}
```

### Text Insight — Total Call Cost

```json
{
  "name": "Total Spend (Last 30 Days)",
  "type": "text",
  "queries": [
    {
      "name": "totalCost",
      "type": "vapiql-json",
      "table": "call",
      "column": "cost",
      "operation": "sum"
    }
  ],
  "timeRange": {
    "start": "-30d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Text Insight with Formula — Conversion Rate

Use formulas to compute derived metrics from multiple queries:

```json
{
  "name": "Conversion Rate",
  "type": "text",
  "queries": [
    {
      "name": "totalCalls",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count"
    },
    {
      "name": "successCalls",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "filters": [
        {
          "column": "endedReason",
          "operator": "=",
          "value": "assistant-ended-call"
        }
      ]
    }
  ],
  "formulas": [
    {
      "name": "conversionRate",
      "expression": "({{successCalls}} / {{totalCalls}}) * 100"
    }
  ],
  "timeRange": {
    "start": "-30d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Filtering by Assistant

```json
{
  "name": "Sales Bot Performance",
  "type": "line",
  "queries": [
    {
      "name": "salesCalls",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "startedAt",
      "filters": [
        {
          "column": "assistantId",
          "operator": "=",
          "value": "your-assistant-id"
        }
      ]
    }
  ],
  "timeRange": {
    "start": "-7d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Filtering by Campaign

```json
{
  "name": "Campaign Call Duration",
  "type": "bar",
  "queries": [
    {
      "name": "avgDuration",
      "type": "vapiql-json",
      "table": "call",
      "column": "duration",
      "operation": "average",
      "groupBy": "startedAt",
      "filters": [
        {
          "column": "campaignId",
          "operator": "=",
          "value": "your-campaign-id"
        }
      ]
    }
  ],
  "timeRange": {
    "start": "-30d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Multiple Queries — Compare Assistants

```json
{
  "name": "Assistant Comparison",
  "type": "bar",
  "queries": [
    {
      "name": "assistantA",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "startedAt",
      "filters": [
        { "column": "assistantId", "operator": "=", "value": "assistant-a-id" }
      ]
    },
    {
      "name": "assistantB",
      "type": "vapiql-json",
      "table": "call",
      "column": "id",
      "operation": "count",
      "groupBy": "startedAt",
      "filters": [
        { "column": "assistantId", "operator": "=", "value": "assistant-b-id" }
      ]
    }
  ],
  "timeRange": {
    "start": "-7d",
    "end": "now",
    "step": "day",
    "timezone": "UTC"
  }
}
```

### Average Latency Monitoring

```json
{
  "name": "Model Latency Trend",
  "type": "line",
  "queries": [
    {
      "name": "avgModelLatency",
      "type": "vapiql-json",
      "table": "call",
      "column": "averageModelLatency",
      "operation": "average",
      "groupBy": "startedAt"
    },
    {
      "name": "avgVoiceLatency",
      "type": "vapiql-json",
      "table": "call",
      "column": "averageVoiceLatency",
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
```

## VapiQL Query Reference

### Tables

| Table | Description |
|-------|-------------|
| `call` | The primary table containing all call records |

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `id` | special | Unique call identifier (use with `count`) |
| `assistantId` | string | ID of the assistant used |
| `workflowId` | string | ID of the workflow used |
| `squadId` | string | ID of the squad used |
| `phoneNumberId` | string | ID of the phone number used |
| `type` | string | Call type (inboundPhoneCall, outboundPhoneCall, webCall) |
| `customerNumber` | string | Customer's phone number |
| `status` | string | Call status (queued, ringing, in-progress, ended) |
| `endedReason` | string | Why the call ended |
| `campaignId` | string | Campaign the call belongs to |
| `duration` | number | Call duration in seconds |
| `cost` | number | Total cost of the call |
| `averageModelLatency` | number | Average LLM response latency (ms) |
| `averageVoiceLatency` | number | Average TTS latency (ms) |
| `averageTranscriberLatency` | number | Average STT latency (ms) |
| `averageTurnLatency` | number | Average full turn latency (ms) |
| `startedAt` | date | When the call started |
| `endedAt` | date | When the call ended |
| `artifact.structuredOutputs[OutputID]` | special | Structured output extracted from the call |

### Operations

| Operation | Description | Works With |
|-----------|-------------|------------|
| `count` | Count of records | Any column (typically `id`) |
| `sum` | Sum of values | Number columns |
| `average` | Average of values | Number columns |
| `min` | Minimum value | Number columns |
| `max` | Maximum value | Number columns |

### Filter Operators

**String columns:**

| Operator | Description |
|----------|-------------|
| `=` | Equals |
| `!=` | Not equals |
| `contains` | Contains substring |
| `not_contains` | Does not contain substring |

**Number columns:**

| Operator | Description |
|----------|-------------|
| `=` | Equals |
| `!=` | Not equals |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

**Date columns:**

| Operator | Description |
|----------|-------------|
| `=` | Equals |
| `!=` | Not equals |
| `>` | After |
| `<` | Before |
| `>=` | On or after |
| `<=` | On or before |

### groupBy Options

You can group results by any string or date column. Common groupBy values:

- `startedAt` — Group by time period (combined with `step` in `timeRange`)
- `status` — Group by call status
- `endedReason` — Group by end reason
- `assistantId` — Group by assistant
- `type` — Group by call type
- `campaignId` — Group by campaign
- `phoneNumberId` — Group by phone number

### Time Range

| Field | Type | Description |
|-------|------|-------------|
| `start` | string | ISO 8601 datetime or relative: `-7d`, `-24h`, `-30d` |
| `end` | string | ISO 8601 datetime or `now` |
| `step` | string | Bucket size: `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year` |
| `timezone` | string | IANA timezone (e.g., `America/New_York`, `UTC`) |

### Formulas

Formulas use MathJS syntax and reference queries by name with `{{queryName}}`:

```
({{successCalls}} / {{totalCalls}}) * 100
{{totalRevenue}} - {{totalCost}}
{{completedCalls}} / {{totalCalls}}
```

## References

- [API Reference](references/api-reference.md) — Complete REST API docs for Insights (7 endpoints)

## Related Skills

- See the `setup-api-key` skill if you need to configure your API key first.
- See the `create-assistant` skill to build assistants whose performance you want to track.
- See the `create-call` skill for making calls that generate the data insights analyze.
