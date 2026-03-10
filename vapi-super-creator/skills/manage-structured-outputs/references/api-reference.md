# Vapi Structured Outputs API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 6 endpoints in the Structured Outputs API for creating, managing, running, and deleting structured output configurations that extract structured data from call conversations.

---

## Table of Contents

- [Structured Outputs API](#structured-outputs-api)
  - [1. List Structured Outputs](#1-list-structured-outputs)
  - [2. Create Structured Output](#2-create-structured-output)
  - [3. Get Structured Output](#3-get-structured-output)
  - [4. Delete Structured Output](#4-delete-structured-output)
  - [5. Update Structured Output](#5-update-structured-output)
  - [6. Run Structured Output](#6-run-structured-output)
- [Object Schema](#object-schema)
- [Model Configuration](#model-configuration)

---

## Structured Outputs API

### 1. List Structured Outputs

Retrieves a paginated list of structured outputs for your organization.

#### HTTP Request

```
GET https://api.vapi.ai/structured-output
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | No | Filter by structured output ID |
| `name` | string | No | Filter by name |
| `page` | number | No | Page number for pagination (default: 1) |
| `limit` | number | No | Number of results per page (default: 20) |
| `sortOrder` | string | No | Sort order: `asc` or `desc` (default: `desc`) |
| `createdAtGte` | string | No | Filter by creation date >= this value (ISO 8601) |
| `createdAtLte` | string | No | Filter by creation date <= this value (ISO 8601) |
| `updatedAtGte` | string | No | Filter by update date >= this value (ISO 8601) |
| `updatedAtLte` | string | No | Filter by update date <= this value (ISO 8601) |

#### cURL Example

```bash
# List all structured outputs
curl https://api.vapi.ai/structured-output \
  -H "Authorization: Bearer $VAPI_API_KEY"

# With filters and pagination
curl "https://api.vapi.ai/structured-output?limit=10&page=1&sortOrder=desc&name=call_summary" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}"
}

# List all
response = requests.get("https://api.vapi.ai/structured-output", headers=headers)
structured_outputs = response.json()

# With filters
params = {"limit": 10, "page": 1, "sortOrder": "desc", "name": "call_summary"}
response = requests.get("https://api.vapi.ai/structured-output", headers=headers, params=params)
structured_outputs = response.json()
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/structured-output?limit=10&page=1", {
  headers: {
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  }
});

const structuredOutputs = await response.json();
```

#### Response: `200 OK`

```json
[
  {
    "id": "so_abc123",
    "orgId": "org_xyz789",
    "type": "ai",
    "name": "call_summary_extraction",
    "description": "Extract key details from a plumbing service call",
    "schema": {
      "type": "object",
      "properties": {
        "customerName": { "type": "string", "description": "Full name of the customer" },
        "issueType": { "type": "string", "description": "Type of plumbing issue reported" }
      },
      "required": ["customerName", "issueType"]
    },
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "temperature": 0.1,
      "maxTokens": 500
    },
    "createdAt": "2026-03-10T12:00:00.000Z",
    "updatedAt": "2026-03-10T12:00:00.000Z"
  }
]
```

---

### 2. Create Structured Output

Creates a new structured output configuration for extracting data from call transcripts.

#### HTTP Request

```
POST https://api.vapi.ai/structured-output
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | Yes | Extraction type: `"ai"` or `"regex"` |
| `name` | string | Yes | Descriptive name for the structured output |
| `description` | string | No | Explanation of what data this structured output extracts |
| `schema` | object | Yes | JSON Schema object defining the structure of the extracted data |
| `model` | object | No | Model configuration for AI-based extraction (required when `type` is `"ai"`) |
| `model.provider` | string | No | Model provider: `"openai"`, `"anthropic"`, `"anthropic-bedrock"`, `"google"`, `"custom-llm"` |
| `model.model` | string | No | Model identifier (e.g., `"gpt-4o"`, `"claude-sonnet-4-20250514"`) |
| `model.temperature` | number | No | Sampling temperature (0.0--2.0). Lower values produce more deterministic results. |
| `model.maxTokens` | number | No | Maximum tokens for the model response |
| `regex` | string | No | Regular expression pattern for regex-based extraction (required when `type` is `"regex"`) |

#### cURL Example: AI-Based Extraction

```bash
curl -X POST https://api.vapi.ai/structured-output \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "type": "ai",
    "name": "call_summary_extraction",
    "description": "Extract key details from a plumbing service call",
    "schema": {
      "type": "object",
      "properties": {
        "customerName": { "type": "string", "description": "Full name of the customer" },
        "issueType": { "type": "string", "description": "Type of plumbing issue reported" },
        "appointmentDate": { "type": "string", "description": "Scheduled appointment date in YYYY-MM-DD format" },
        "urgency": { "type": "string", "enum": ["low", "medium", "high"], "description": "Urgency level" }
      },
      "required": ["customerName", "issueType"]
    },
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "temperature": 0.1,
      "maxTokens": 500
    }
  }'
```

#### cURL Example: Regex-Based Extraction

```bash
curl -X POST https://api.vapi.ai/structured-output \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "type": "regex",
    "name": "extract_phone_number",
    "description": "Extract phone numbers from call transcript",
    "schema": {
      "type": "object",
      "properties": {
        "phoneNumber": { "type": "string", "description": "Phone number found in transcript" }
      }
    },
    "regex": "\\b(\\+?1?[-.]?\\(?\\d{3}\\)?[-.]?\\d{3}[-.]?\\d{4})\\b"
  }'
```

#### Python Example

```python
import requests
import json

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

# AI-based extraction
payload = {
    "type": "ai",
    "name": "call_summary_extraction",
    "description": "Extract key details from a plumbing service call",
    "schema": {
        "type": "object",
        "properties": {
            "customerName": {"type": "string", "description": "Full name of the customer"},
            "issueType": {"type": "string", "description": "Type of plumbing issue reported"},
            "appointmentDate": {"type": "string", "description": "Scheduled appointment date"},
            "urgency": {"type": "string", "enum": ["low", "medium", "high"]}
        },
        "required": ["customerName", "issueType"]
    },
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "temperature": 0.1,
        "maxTokens": 500
    }
}

response = requests.post(
    "https://api.vapi.ai/structured-output",
    headers=headers,
    json=payload
)
structured_output = response.json()
print(f"Created: {structured_output['id']}")
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/structured-output", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  },
  body: JSON.stringify({
    type: "ai",
    name: "call_summary_extraction",
    description: "Extract key details from a plumbing service call",
    schema: {
      type: "object",
      properties: {
        customerName: { type: "string", description: "Full name of the customer" },
        issueType: { type: "string", description: "Type of plumbing issue reported" },
        appointmentDate: { type: "string", description: "Scheduled appointment date" },
        urgency: { type: "string", enum: ["low", "medium", "high"] }
      },
      required: ["customerName", "issueType"]
    },
    model: {
      provider: "openai",
      model: "gpt-4o",
      temperature: 0.1,
      maxTokens: 500
    }
  })
});

const structuredOutput = await response.json();
console.log("Created:", structuredOutput.id);
```

#### Response: `201 Created`

```json
{
  "id": "so_abc123",
  "orgId": "org_xyz789",
  "type": "ai",
  "name": "call_summary_extraction",
  "description": "Extract key details from a plumbing service call",
  "schema": {
    "type": "object",
    "properties": {
      "customerName": { "type": "string", "description": "Full name of the customer" },
      "issueType": { "type": "string", "description": "Type of plumbing issue reported" },
      "appointmentDate": { "type": "string", "description": "Scheduled appointment date in YYYY-MM-DD format" },
      "urgency": { "type": "string", "enum": ["low", "medium", "high"], "description": "Urgency level" }
    },
    "required": ["customerName", "issueType"]
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.1,
    "maxTokens": 500
  },
  "createdAt": "2026-03-10T12:00:00.000Z",
  "updatedAt": "2026-03-10T12:00:00.000Z"
}
```

---

### 3. Get Structured Output

Retrieves a single structured output by ID.

#### HTTP Request

```
GET https://api.vapi.ai/structured-output/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The structured output ID |

#### cURL Example

```bash
curl https://api.vapi.ai/structured-output/so_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.get(
    "https://api.vapi.ai/structured-output/so_abc123",
    headers=headers
)
structured_output = response.json()
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/structured-output/so_abc123", {
  headers: {
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  }
});

const structuredOutput = await response.json();
```

#### Response: `200 OK`

Returns the full structured output object (same schema as the Create response).

---

### 4. Delete Structured Output

Permanently deletes a structured output by ID.

#### HTTP Request

```
DELETE https://api.vapi.ai/structured-output/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The structured output ID |

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/structured-output/so_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.delete(
    "https://api.vapi.ai/structured-output/so_abc123",
    headers=headers
)
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/structured-output/so_abc123", {
  method: "DELETE",
  headers: {
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  }
});
```

#### Response: `200 OK`

Returns the deleted structured output object.

---

### 5. Update Structured Output

Updates an existing structured output. All fields are optional -- only include the fields you want to change.

#### HTTP Request

```
PATCH https://api.vapi.ai/structured-output/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The structured output ID |

#### Request Body Parameters

All fields from the Create endpoint are accepted, but all are optional.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | No | Extraction type: `"ai"` or `"regex"` |
| `name` | string | No | Updated name |
| `description` | string | No | Updated description |
| `schema` | object | No | Updated JSON Schema |
| `model` | object | No | Updated model configuration |
| `regex` | string | No | Updated regex pattern |

#### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/structured-output/so_abc123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "description": "Updated extraction for plumbing service calls",
    "model": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "temperature": 0.0,
      "maxTokens": 1000
    }
  }'
```

#### Python Example

```python
import requests

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "description": "Updated extraction for plumbing service calls",
    "model": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-20250514",
        "temperature": 0.0,
        "maxTokens": 1000
    }
}

response = requests.patch(
    "https://api.vapi.ai/structured-output/so_abc123",
    headers=headers,
    json=payload
)
updated = response.json()
```

#### TypeScript Example

```typescript
const response = await fetch("https://api.vapi.ai/structured-output/so_abc123", {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  },
  body: JSON.stringify({
    description: "Updated extraction for plumbing service calls",
    model: {
      provider: "anthropic",
      model: "claude-sonnet-4-20250514",
      temperature: 0.0,
      maxTokens: 1000
    }
  })
});

const updated = await response.json();
```

#### Response: `200 OK`

Returns the updated structured output object.

---

### 6. Run Structured Output

Executes a structured output against input text and returns the extracted data. Optionally links the result to a specific call.

#### HTTP Request

```
POST https://api.vapi.ai/structured-output/run
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `structuredOutputId` | string | Yes | ID of the structured output to run |
| `input` | string | Yes | The text to extract data from (e.g., a call transcript) |
| `callId` | string | No | Optional call ID to associate the extraction result with |

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/structured-output/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "structuredOutputId": "so_abc123",
    "input": "Hi, my name is John Smith. I have a leaking pipe in my kitchen. It is pretty urgent. Can you send someone out tomorrow, March 15th?"
  }'
```

#### cURL Example: With Call ID

```bash
curl -X POST https://api.vapi.ai/structured-output/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "structuredOutputId": "so_abc123",
    "input": "Full call transcript text goes here...",
    "callId": "call_def456"
  }'
```

#### Python Example

```python
import requests

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

# Run against raw text
payload = {
    "structuredOutputId": "so_abc123",
    "input": "Hi, my name is John Smith. I have a leaking pipe in my kitchen. It is pretty urgent. Can you send someone out tomorrow, March 15th?"
}

response = requests.post(
    "https://api.vapi.ai/structured-output/run",
    headers=headers,
    json=payload
)
extracted_data = response.json()
print(extracted_data)

# Run against a call transcript with callId
payload_with_call = {
    "structuredOutputId": "so_abc123",
    "input": "Full call transcript...",
    "callId": "call_def456"
}

response = requests.post(
    "https://api.vapi.ai/structured-output/run",
    headers=headers,
    json=payload_with_call
)
extracted_data = response.json()
```

#### TypeScript Example

```typescript
// Run against raw text
const response = await fetch("https://api.vapi.ai/structured-output/run", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  },
  body: JSON.stringify({
    structuredOutputId: "so_abc123",
    input: "Hi, my name is John Smith. I have a leaking pipe in my kitchen. It is pretty urgent. Can you send someone out tomorrow, March 15th?"
  })
});

const extractedData = await response.json();
console.log(extractedData);

// Run with callId
const responseWithCall = await fetch("https://api.vapi.ai/structured-output/run", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${process.env.VAPI_API_KEY}`
  },
  body: JSON.stringify({
    structuredOutputId: "so_abc123",
    input: "Full call transcript...",
    callId: "call_def456"
  })
});

const result = await responseWithCall.json();
```

#### Response: `200 OK`

Returns the extracted structured data matching the configured schema:

```json
{
  "customerName": "John Smith",
  "issueType": "leaking pipe",
  "appointmentDate": "2026-03-15",
  "urgency": "high"
}
```

---

## Object Schema

The Structured Output object contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the structured output |
| `name` | string | Descriptive name |
| `description` | string | Explanation of what data is extracted |
| `type` | string | Extraction type: `"ai"` or `"regex"` |
| `schema` | object | JSON Schema defining the structure of extracted data |
| `model` | object | Model configuration (for AI-based extraction) |
| `model.provider` | string | Model provider (see [Model Configuration](#model-configuration)) |
| `model.model` | string | Model identifier |
| `model.temperature` | number | Sampling temperature |
| `model.maxTokens` | number | Maximum tokens for the response |
| `regex` | string | Regular expression pattern (for regex-based extraction) |
| `orgId` | string | Organization ID |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

### Example Object

```json
{
  "id": "so_abc123",
  "orgId": "org_xyz789",
  "type": "ai",
  "name": "call_summary_extraction",
  "description": "Extract key details from a plumbing service call",
  "schema": {
    "type": "object",
    "properties": {
      "customerName": { "type": "string", "description": "Full name of the customer" },
      "issueType": { "type": "string", "description": "Type of plumbing issue reported" },
      "appointmentDate": { "type": "string", "description": "Scheduled appointment date in YYYY-MM-DD format" },
      "urgency": { "type": "string", "enum": ["low", "medium", "high"], "description": "Urgency level" }
    },
    "required": ["customerName", "issueType"]
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.1,
    "maxTokens": 500
  },
  "createdAt": "2026-03-10T12:00:00.000Z",
  "updatedAt": "2026-03-10T12:00:00.000Z"
}
```

---

## Model Configuration

Supported model providers for AI-based structured output extraction:

| Provider | Value | Example Models |
|----------|-------|----------------|
| OpenAI | `"openai"` | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` |
| Anthropic | `"anthropic"` | `claude-sonnet-4-20250514`, `claude-3-haiku-20240307` |
| Anthropic Bedrock | `"anthropic-bedrock"` | `anthropic.claude-3-sonnet-20240229-v1:0` |
| Google | `"google"` | `gemini-1.5-pro`, `gemini-1.5-flash` |
| Custom LLM | `"custom-llm"` | Your custom model identifier |

### Model Configuration Example

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.1,
    "maxTokens": 500
  }
}
```

**Tips:**
- Use `temperature: 0.0` or `temperature: 0.1` for extraction tasks to get consistent results
- Set `maxTokens` high enough to accommodate the full extracted schema
- For cost-sensitive workloads, consider smaller models like `gpt-4o-mini` or `claude-3-haiku-20240307`
