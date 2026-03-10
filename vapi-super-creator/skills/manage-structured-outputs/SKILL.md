---
name: manage-structured-outputs
description: Create and manage structured outputs in Vapi to extract structured data from call conversations using AI or regex patterns. Use when setting up post-call data extraction, configuring structured data schemas, or running extraction on call transcripts.
---

# Manage Structured Outputs Skill

This skill covers creating, configuring, and managing structured outputs in Vapi. Structured outputs let you extract structured data from call conversations using AI-based extraction or regex patterns -- useful for post-call analysis, data capture, and automated processing.

> **See also:** `create-assistant` (configuring assistants), `create-call` (making calls to generate transcripts), `create-tool` (adding tools to assistants)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- For AI-based extraction: a supported model provider (openai, anthropic, google, etc.)
- For regex extraction: a valid regular expression pattern

---

## Quick Start

### Create a Structured Output via cURL

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
        "urgency": { "type": "string", "enum": ["low", "medium", "high"], "description": "Urgency level of the issue" }
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

### Create a Structured Output via TypeScript

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

---

## CRUD Operations

### Create a Structured Output

See Quick Start above for full examples. Two types are supported:

**AI-based extraction** (`type: "ai"`): Uses an LLM to analyze the transcript and extract data according to your JSON Schema. Best for unstructured or varied conversations.

**Regex extraction** (`type: "regex"`): Uses a regular expression pattern to extract data. Best for consistently formatted data like phone numbers, dates, or order IDs.

### List Structured Outputs

```bash
# List all structured outputs
curl https://api.vapi.ai/structured-output \
  -H "Authorization: Bearer $VAPI_API_KEY"

# With pagination and filtering
curl "https://api.vapi.ai/structured-output?limit=10&page=1&sortOrder=desc&name=call_summary" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get a Structured Output

```bash
curl https://api.vapi.ai/structured-output/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update a Structured Output

```bash
curl -X PATCH https://api.vapi.ai/structured-output/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "description": "Updated description for extraction",
    "model": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "temperature": 0.0,
      "maxTokens": 1000
    }
  }'
```

### Delete a Structured Output

```bash
curl -X DELETE https://api.vapi.ai/structured-output/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

---

## Run Structured Output

The Run endpoint processes input text through a structured output configuration and returns extracted data. You can provide raw text or reference a call by ID.

### Run Against Raw Text

```bash
curl -X POST https://api.vapi.ai/structured-output/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "structuredOutputId": "your-structured-output-id",
    "input": "Hi, my name is John Smith. I have a leaking pipe in my kitchen. It is pretty urgent. Can you send someone out tomorrow, March 15th?"
  }'
```

### Run Against a Call Transcript

```bash
curl -X POST https://api.vapi.ai/structured-output/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "structuredOutputId": "your-structured-output-id",
    "input": "Full call transcript text here...",
    "callId": "call-id-for-reference"
  }'
```

### Example Response

```json
{
  "customerName": "John Smith",
  "issueType": "leaking pipe",
  "appointmentDate": "2026-03-15",
  "urgency": "high"
}
```

---

## Common Patterns

### AI-Based Extraction (Recommended for Most Cases)

Use AI extraction when the data you need is embedded in natural conversation and may be expressed in various ways.

```json
{
  "type": "ai",
  "name": "lead_qualification",
  "description": "Extract lead qualification data from a sales call",
  "schema": {
    "type": "object",
    "properties": {
      "companyName": { "type": "string", "description": "Name of the prospect company" },
      "budget": { "type": "number", "description": "Stated budget in USD" },
      "timeline": { "type": "string", "description": "When they want to start" },
      "decisionMaker": { "type": "boolean", "description": "Whether the caller is the decision maker" },
      "painPoints": {
        "type": "array",
        "items": { "type": "string" },
        "description": "List of pain points mentioned"
      }
    },
    "required": ["companyName"]
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.0,
    "maxTokens": 800
  }
}
```

### Regex Extraction

Use regex extraction for consistently formatted data like phone numbers, email addresses, or reference codes.

```json
{
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
}
```

### Running Extraction on Call Transcripts

A typical workflow: create a structured output, make calls, then run extraction on the transcripts.

**Step 1:** Create the structured output (see Quick Start).

**Step 2:** After a call completes, retrieve the transcript:
```bash
curl https://api.vapi.ai/call/{callId} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Step 3:** Run the structured output against the transcript:
```bash
curl -X POST https://api.vapi.ai/structured-output/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "structuredOutputId": "your-structured-output-id",
    "input": "The full call transcript text...",
    "callId": "the-call-id"
  }'
```

### Using Different Model Providers

```json
// OpenAI
"model": { "provider": "openai", "model": "gpt-4o", "temperature": 0.1, "maxTokens": 500 }

// Anthropic
"model": { "provider": "anthropic", "model": "claude-sonnet-4-20250514", "temperature": 0.0, "maxTokens": 500 }

// Anthropic via Bedrock
"model": { "provider": "anthropic-bedrock", "model": "anthropic.claude-3-sonnet-20240229-v1:0", "temperature": 0.0, "maxTokens": 500 }

// Google
"model": { "provider": "google", "model": "gemini-1.5-pro", "temperature": 0.1, "maxTokens": 500 }

// Custom LLM
"model": { "provider": "custom-llm", "model": "your-model-id", "temperature": 0.0, "maxTokens": 500 }
```

---

## Best Practices

1. **Use low temperature** (0.0--0.1) for extraction tasks to get consistent, deterministic results
2. **Write detailed schema descriptions** -- the AI model uses property descriptions to understand what to extract
3. **Mark required fields** in your JSON Schema to ensure critical data is always extracted
4. **Use enums** for fields with known possible values (e.g., urgency levels, categories)
5. **Test with sample transcripts** using the `/structured-output/run` endpoint before deploying to production
6. **Use regex for structured patterns** like phone numbers, emails, or IDs -- it is faster and more reliable for formatted data

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Structured Outputs (6 endpoints) with cURL, Python, and TypeScript examples
