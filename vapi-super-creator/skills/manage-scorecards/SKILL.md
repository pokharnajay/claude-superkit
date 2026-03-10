---
name: manage-scorecards
description: "Create and manage observability scorecards in Vapi to score call quality based on structured output metrics. Use when setting up call quality monitoring, defining scoring criteria, or linking scorecards to assistants."
---

# Manage Observability Scorecards

Scorecards let you define scoring criteria for calls based on structured output values. Each scorecard contains one or more metrics, and each metric references a structured output and defines conditions that award points. Points across all conditions in a metric must sum to 100.

## Quick Start

Create a scorecard that scores whether the agent resolved the customer's issue:

```bash
curl -X POST "https://api.vapi.ai/observability/scorecard" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Issue Resolution",
    "description": "Scores whether the agent resolved the customer issue",
    "metrics": [
      {
        "structuredOutputId": "SO_UUID_HERE",
        "conditions": [
          { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
          { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
        ]
      }
    ],
    "assistantIds": ["ASSISTANT_UUID_HERE"]
  }'
```

## CRUD Operations

### List Scorecards

```bash
curl "https://api.vapi.ai/observability/scorecard" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

Supports pagination via `page` and `limit` query parameters, and filtering.

### Create a Scorecard

```bash
curl -X POST "https://api.vapi.ai/observability/scorecard" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Call Quality Score",
    "description": "Overall call quality based on multiple metrics",
    "metrics": [
      {
        "structuredOutputId": "UUID_OF_STRUCTURED_OUTPUT",
        "conditions": [
          { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
          { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
        ]
      }
    ],
    "assistantIds": ["ASSISTANT_UUID"]
  }'
```

**Required fields:** `name`, `metrics` (with at least one metric containing `structuredOutputId` and `conditions`).

**Rules:**
- Points across all conditions in a single metric must sum to exactly 100.
- Each referenced structured output must have a `number` or `boolean` type.

### Get a Scorecard

```bash
curl "https://api.vapi.ai/observability/scorecard/{id}" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update a Scorecard

```bash
curl -X PATCH "https://api.vapi.ai/observability/scorecard/{id}" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Scorecard Name",
    "description": "Updated description"
  }'
```

All fields are optional on update.

### Delete a Scorecard

```bash
curl -X DELETE "https://api.vapi.ai/observability/scorecard/{id}" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Common Patterns

### Boolean Scoring

Score a yes/no outcome from a structured output (e.g., "Did the agent greet the customer?"):

```json
{
  "name": "Greeting Check",
  "metrics": [
    {
      "structuredOutputId": "greeting-output-uuid",
      "conditions": [
        { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
        { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
      ]
    }
  ]
}
```

### Numeric Thresholds

Score a numeric structured output using range-based conditions (e.g., customer satisfaction rating 1-5):

```json
{
  "name": "Satisfaction Rating",
  "metrics": [
    {
      "structuredOutputId": "satisfaction-score-uuid",
      "conditions": [
        { "type": "comparator", "comparator": ">=", "value": 4, "points": 100 },
        { "type": "comparator", "comparator": ">=", "value": 3, "points": 60 },
        { "type": "comparator", "comparator": ">=", "value": 2, "points": 30 },
        { "type": "comparator", "comparator": "<", "value": 2, "points": 0 }
      ]
    }
  ]
}
```

Note: When using numeric thresholds, conditions are evaluated in order. Structure them so that the first matching condition is the one that applies, and ensure all condition points still sum to the intended total. If conditions are mutually exclusive (non-overlapping ranges), their points must sum to 100.

### Multi-Metric Scorecards

Combine multiple structured outputs into a single scorecard for a holistic quality score:

```json
{
  "name": "Overall Call Quality",
  "description": "Composite score across greeting, resolution, and sentiment",
  "metrics": [
    {
      "structuredOutputId": "greeting-check-uuid",
      "conditions": [
        { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
        { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
      ]
    },
    {
      "structuredOutputId": "issue-resolved-uuid",
      "conditions": [
        { "type": "comparator", "comparator": "=", "value": true, "points": 100 },
        { "type": "comparator", "comparator": "=", "value": false, "points": 0 }
      ]
    },
    {
      "structuredOutputId": "sentiment-score-uuid",
      "conditions": [
        { "type": "comparator", "comparator": ">=", "value": 4, "points": 100 },
        { "type": "comparator", "comparator": ">=", "value": 2, "points": 50 },
        { "type": "comparator", "comparator": "<", "value": 2, "points": 0 }
      ]
    }
  ],
  "assistantIds": ["assistant-uuid-1", "assistant-uuid-2"]
}
```

## How Scorecards Link to Structured Outputs

Scorecards bridge the gap between raw call data and actionable quality scores:

1. **Structured Outputs** are defined on an assistant to extract specific values from calls (e.g., "Was the issue resolved?" as a boolean, or "Customer satisfaction" as a number 1-5). These are computed after each call ends.

2. **Scorecard Metrics** reference structured outputs by their `structuredOutputId`. Each metric defines conditions that map structured output values to point scores.

3. **Conditions** use comparators (`=`, `!=`, `>`, `<`, `>=`, `<=`) to evaluate the structured output value and assign points. Points in all conditions for a single metric must total 100.

4. **Assistant Linking** via `assistantIds` scopes the scorecard to specific assistants. Only calls handled by those assistants are scored by the scorecard.

The flow is: **Call completes -> Structured outputs are extracted -> Scorecard conditions are evaluated -> Points are assigned per metric.**
