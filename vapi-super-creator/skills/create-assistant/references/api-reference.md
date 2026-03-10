# Vapi Assistants API Reference

Complete API reference for managing Vapi assistants. All endpoints support REST API calls, TypeScript SDK, and Python.

**Base URL:** `https://api.vapi.ai`
**Authentication:** `Authorization: Bearer $VAPI_API_KEY`

---

## Table of Contents

1. [List Assistants](#1-list-assistants)
2. [Create Assistant](#2-create-assistant)
3. [Get Assistant](#3-get-assistant)
4. [Update Assistant](#4-update-assistant)
5. [Delete Assistant](#5-delete-assistant)
6. [Common Response Schema](#common-response-schema)

---

## 1. List Assistants

Retrieve a paginated list of all assistants in your organization.

**Doc Reference:** [https://docs.vapi.ai/api-reference/assistants/list](https://docs.vapi.ai/api-reference/assistants/list)

### HTTP Request

```
GET https://api.vapi.ai/assistant
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |

### Query Parameters

| Parameter     | Type     | Required | Default | Description                                           |
|---------------|----------|----------|---------|-------------------------------------------------------|
| limit         | number   | No       | 100     | Maximum number of assistants to return.                |
| createdAtGt   | datetime | No       | -       | Return assistants created after this datetime (exclusive). ISO 8601 format. |
| createdAtLt   | datetime | No       | -       | Return assistants created before this datetime (exclusive). ISO 8601 format. |
| createdAtGe   | datetime | No       | -       | Return assistants created at or after this datetime (inclusive). ISO 8601 format. |
| createdAtLe   | datetime | No       | -       | Return assistants created at or before this datetime (inclusive). ISO 8601 format. |
| updatedAtGt   | datetime | No       | -       | Return assistants updated after this datetime (exclusive). ISO 8601 format. |
| updatedAtLt   | datetime | No       | -       | Return assistants updated before this datetime (exclusive). ISO 8601 format. |
| updatedAtGe   | datetime | No       | -       | Return assistants updated at or after this datetime (inclusive). ISO 8601 format. |
| updatedAtLe   | datetime | No       | -       | Return assistants updated at or before this datetime (inclusive). ISO 8601 format. |

### Response

**Status:** `200 OK`

Returns an array of Assistant objects.

```json
[
  {
    "id": "asta_1234567890abcdef",
    "orgId": "org_abcdef1234567890",
    "name": "My Assistant",
    "firstMessage": "Hello! How can I help you today?",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "systemPrompt": "You are a helpful assistant."
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "21m00Tcm4TlvDq8ikWAM"
    },
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-2"
    },
    "createdAt": "2025-01-15T10:30:00.000Z",
    "updatedAt": "2025-01-15T10:30:00.000Z"
  }
]
```

### cURL Example

```bash
curl -X GET "https://api.vapi.ai/assistant?limit=10" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

With date filters:

```bash
curl -X GET "https://api.vapi.ai/assistant?limit=50&createdAtGt=2025-01-01T00:00:00.000Z&createdAtLt=2025-06-01T00:00:00.000Z" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

// List all assistants (default limit: 100)
const assistants = await client.assistants.list();

// List with filters
const filteredAssistants = await client.assistants.list({
  limit: 10,
  createdAtGt: "2025-01-01T00:00:00.000Z",
  createdAtLt: "2025-06-01T00:00:00.000Z",
});

console.log(assistants);
```

### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/assistant"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
params = {
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)
assistants = response.json()

print(assistants)
```

---

## 2. Create Assistant

Create a new assistant with a full configuration including model, voice, transcriber, tools, hooks, and more.

**Doc Reference:** [https://docs.vapi.ai/api-reference/assistants/create](https://docs.vapi.ai/api-reference/assistants/create)

### HTTP Request

```
POST https://api.vapi.ai/assistant
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |
| Content-Type    | string | Yes      | `application/json`                   |

### Request Body (CreateAssistantDTO)

| Field                         | Type     | Required | Description                                                                                  |
|-------------------------------|----------|----------|----------------------------------------------------------------------------------------------|
| name                          | string   | No       | Human-readable name for the assistant.                                                       |
| firstMessage                  | string   | No       | The first message the assistant says when a call starts. Set to `null` for the assistant to wait for the user to speak first. |
| firstMessageMode              | string   | No       | Controls when the first message is spoken. Values: `assistant-speaks-first`, `assistant-speaks-first-with-model-generated-message`, `assistant-waits-for-user`. |
| model                         | object   | No       | LLM configuration object.                                                                    |
| model.provider                | string   | Yes*     | Model provider: `openai`, `anthropic`, `google`, `groq`, `together-ai`, `anyscale`, `custom-llm`, `vapi`, etc. |
| model.model                   | string   | Yes*     | Model identifier (e.g., `gpt-4o`, `claude-3-5-sonnet-20241022`, `gemini-2.0-flash`).        |
| model.systemPrompt            | string   | No       | System prompt / instructions for the model.                                                  |
| model.temperature             | number   | No       | Temperature for generation (0.0 - 2.0).                                                      |
| model.maxTokens               | number   | No       | Maximum number of tokens to generate.                                                         |
| model.emotionRecognitionEnabled | boolean | No       | Enable emotion recognition in the model context.                                              |
| model.tools                   | array    | No       | Array of tool configurations available to the model.                                          |
| model.knowledgeBase           | object   | No       | Knowledge base configuration for RAG.                                                         |
| voice                         | object   | No       | Voice configuration object.                                                                   |
| voice.provider                | string   | Yes*     | Voice provider: `11labs`, `azure`, `cartesia`, `deepgram`, `lmnt`, `neets`, `openai`, `playht`, `rime-ai`, `tavus`, etc. |
| voice.voiceId                 | string   | Yes*     | Provider-specific voice identifier.                                                           |
| voice.speed                   | number   | No       | Speech speed multiplier.                                                                      |
| voice.stability               | number   | No       | Voice stability (provider-specific, e.g., ElevenLabs 0-1).                                   |
| voice.similarityBoost         | number   | No       | Similarity boost (provider-specific, e.g., ElevenLabs 0-1).                                  |
| voice.fillerInjectionEnabled  | boolean  | No       | Enable filler word injection (e.g., "um", "uh").                                              |
| transcriber                   | object   | No       | Transcriber configuration object.                                                             |
| transcriber.provider          | string   | Yes*     | Transcriber provider: `deepgram`, `talkscriber`, `gladia`, `assembly-ai`, `custom-transcriber`. |
| transcriber.model             | string   | No       | Transcriber model (e.g., `nova-2`, `nova-3`).                                                 |
| transcriber.language          | string   | No       | Language code (e.g., `en`, `es`, `fr`).                                                       |
| transcriber.keywords          | array    | No       | Array of keyword strings to boost in transcription.                                           |
| tools                         | array    | No       | Array of tool objects the assistant can use (functions, GHL, make, transfer calls, etc.).      |
| hooks                         | array    | No       | Array of hook objects for event-driven actions (e.g., `on:call:starting`, `on:assistant:message:complete`). |
| silenceTimeoutSeconds         | number   | No       | Timeout in seconds for silence before ending the call.                                        |
| maxDurationSeconds            | number   | No       | Maximum duration of the call in seconds.                                                      |
| backgroundSound               | string   | No       | Background ambient sound: `off`, `office`.                                                    |
| backchannelingEnabled         | boolean  | No       | Enable backchanneling (e.g., "mm-hmm", "right").                                              |
| backgroundDenoisingEnabled    | boolean  | No       | Enable background noise denoising.                                                            |
| modelOutputInMessagesEnabled  | boolean  | No       | Include model output in message events.                                                       |
| hipaaEnabled                  | boolean  | No       | Enable HIPAA-compliant mode.                                                                  |
| transportConfigurations       | array    | No       | Transport-specific configurations.                                                            |
| credentials                   | array    | No       | Credential overrides for providers.                                                           |
| server                        | object   | No       | Server configuration for webhooks (`url`, `secret`, `timeoutSeconds`, `headers`).             |
| analysisPlan                  | object   | No       | Post-call analysis plan (summary, structuredData, successEvaluation).                         |
| artifactPlan                  | object   | No       | Artifact capture plan (recording, video, transcript, etc.).                                   |
| messagePlan                   | object   | No       | Message plan for idle messages configuration.                                                 |
| startSpeakingPlan             | object   | No       | Plan for when the assistant should start speaking.                                            |
| stopSpeakingPlan              | object   | No       | Plan for when the assistant should stop speaking.                                             |
| endCallPhrases                | array    | No       | Array of phrases that trigger end of call.                                                    |
| metadata                      | object   | No       | Arbitrary key-value metadata.                                                                 |

> Fields marked `Yes*` are required when their parent object is provided.

### Request Body Example

```json
{
  "name": "Customer Support Agent",
  "firstMessage": "Hello! Thank you for calling. How can I assist you today?",
  "firstMessageMode": "assistant-speaks-first",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "systemPrompt": "You are a friendly and professional customer support agent for Acme Corp. Help users with their questions about products, orders, and returns. Be concise and helpful.",
    "temperature": 0.7,
    "maxTokens": 500,
    "emotionRecognitionEnabled": true
  },
  "voice": {
    "provider": "11labs",
    "voiceId": "21m00Tcm4TlvDq8ikWAM",
    "stability": 0.5,
    "similarityBoost": 0.75
  },
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-2",
    "language": "en"
  },
  "silenceTimeoutSeconds": 30,
  "maxDurationSeconds": 600,
  "backgroundSound": "office",
  "backchannelingEnabled": true,
  "backgroundDenoisingEnabled": true,
  "hipaaEnabled": false,
  "server": {
    "url": "https://your-server.com/vapi-webhook",
    "secret": "your-webhook-secret"
  },
  "analysisPlan": {
    "summaryPlan": {
      "enabled": true
    },
    "successEvaluationPlan": {
      "enabled": true,
      "rubric": "AutomaticRubric"
    }
  },
  "endCallPhrases": ["goodbye", "bye bye", "end call"],
  "metadata": {
    "department": "support",
    "version": "1.0"
  }
}
```

### Response

**Status:** `201 Created`

Returns the created Assistant object.

```json
{
  "id": "asta_1234567890abcdef",
  "orgId": "org_abcdef1234567890",
  "name": "Customer Support Agent",
  "firstMessage": "Hello! Thank you for calling. How can I assist you today?",
  "firstMessageMode": "assistant-speaks-first",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "systemPrompt": "You are a friendly and professional customer support agent for Acme Corp. Help users with their questions about products, orders, and returns. Be concise and helpful.",
    "temperature": 0.7,
    "maxTokens": 500,
    "emotionRecognitionEnabled": true
  },
  "voice": {
    "provider": "11labs",
    "voiceId": "21m00Tcm4TlvDq8ikWAM",
    "stability": 0.5,
    "similarityBoost": 0.75
  },
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-2",
    "language": "en"
  },
  "silenceTimeoutSeconds": 30,
  "maxDurationSeconds": 600,
  "backgroundSound": "office",
  "backchannelingEnabled": true,
  "backgroundDenoisingEnabled": true,
  "hipaaEnabled": false,
  "server": {
    "url": "https://your-server.com/vapi-webhook",
    "secret": "your-webhook-secret"
  },
  "analysisPlan": {
    "summaryPlan": {
      "enabled": true
    },
    "successEvaluationPlan": {
      "enabled": true,
      "rubric": "AutomaticRubric"
    }
  },
  "endCallPhrases": ["goodbye", "bye bye", "end call"],
  "metadata": {
    "department": "support",
    "version": "1.0"
  },
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X POST "https://api.vapi.ai/assistant" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support Agent",
    "firstMessage": "Hello! Thank you for calling. How can I assist you today?",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "systemPrompt": "You are a friendly customer support agent.",
      "temperature": 0.7
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "21m00Tcm4TlvDq8ikWAM"
    },
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-2",
      "language": "en"
    },
    "silenceTimeoutSeconds": 30,
    "maxDurationSeconds": 600,
    "endCallPhrases": ["goodbye", "bye bye"]
  }'
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const assistant = await client.assistants.create({
  name: "Customer Support Agent",
  firstMessage: "Hello! Thank you for calling. How can I assist you today?",
  model: {
    provider: "openai",
    model: "gpt-4o",
    systemPrompt: "You are a friendly customer support agent.",
    temperature: 0.7,
    maxTokens: 500,
    emotionRecognitionEnabled: true,
  },
  voice: {
    provider: "11labs",
    voiceId: "21m00Tcm4TlvDq8ikWAM",
    stability: 0.5,
    similarityBoost: 0.75,
  },
  transcriber: {
    provider: "deepgram",
    model: "nova-2",
    language: "en",
  },
  silenceTimeoutSeconds: 30,
  maxDurationSeconds: 600,
  backgroundSound: "office",
  backchannelingEnabled: true,
  backgroundDenoisingEnabled: true,
  endCallPhrases: ["goodbye", "bye bye"],
  metadata: {
    department: "support",
    version: "1.0",
  },
});

console.log("Created assistant:", assistant.id);
```

### Python Example

```python
import requests
import os
import json

url = "https://api.vapi.ai/assistant"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "name": "Customer Support Agent",
    "firstMessage": "Hello! Thank you for calling. How can I assist you today?",
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "systemPrompt": "You are a friendly customer support agent.",
        "temperature": 0.7,
        "maxTokens": 500,
        "emotionRecognitionEnabled": True
    },
    "voice": {
        "provider": "11labs",
        "voiceId": "21m00Tcm4TlvDq8ikWAM",
        "stability": 0.5,
        "similarityBoost": 0.75
    },
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "en"
    },
    "silenceTimeoutSeconds": 30,
    "maxDurationSeconds": 600,
    "backgroundSound": "office",
    "backchannelingEnabled": True,
    "backgroundDenoisingEnabled": True,
    "endCallPhrases": ["goodbye", "bye bye"],
    "metadata": {
        "department": "support",
        "version": "1.0"
    }
}

response = requests.post(url, headers=headers, json=payload)
assistant = response.json()

print(f"Created assistant: {assistant['id']}")
```

---

## 3. Get Assistant

Retrieve a single assistant by its ID.

**Doc Reference:** [https://docs.vapi.ai/api-reference/assistants/get](https://docs.vapi.ai/api-reference/assistants/get)

### HTTP Request

```
GET https://api.vapi.ai/assistant/{id}
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |

### Path Parameters

| Parameter | Type   | Required | Description                             |
|-----------|--------|----------|-----------------------------------------|
| id        | string | Yes      | The unique identifier of the assistant. |

### Response

**Status:** `200 OK`

Returns the full Assistant object.

```json
{
  "id": "asta_1234567890abcdef",
  "orgId": "org_abcdef1234567890",
  "name": "Customer Support Agent",
  "firstMessage": "Hello! Thank you for calling. How can I assist you today?",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "systemPrompt": "You are a friendly customer support agent."
  },
  "voice": {
    "provider": "11labs",
    "voiceId": "21m00Tcm4TlvDq8ikWAM"
  },
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-2"
  },
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X GET "https://api.vapi.ai/assistant/asta_1234567890abcdef" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const assistant = await client.assistants.get("asta_1234567890abcdef");

console.log("Assistant name:", assistant.name);
console.log("Model:", assistant.model?.model);
console.log("Voice:", assistant.voice?.voiceId);
```

### Python Example

```python
import requests
import os

assistant_id = "asta_1234567890abcdef"
url = f"https://api.vapi.ai/assistant/{assistant_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
assistant = response.json()

print(f"Assistant name: {assistant['name']}")
print(f"Model: {assistant['model']['model']}")
print(f"Voice: {assistant['voice']['voiceId']}")
```

---

## 4. Update Assistant

Update an existing assistant. Uses PATCH semantics - only include the fields you want to change. Unspecified fields remain unchanged.

**Doc Reference:** [https://docs.vapi.ai/api-reference/assistants/update](https://docs.vapi.ai/api-reference/assistants/update)

### HTTP Request

```
PATCH https://api.vapi.ai/assistant/{id}
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |
| Content-Type    | string | Yes      | `application/json`                   |

### Path Parameters

| Parameter | Type   | Required | Description                             |
|-----------|--------|----------|-----------------------------------------|
| id        | string | Yes      | The unique identifier of the assistant. |

### Request Body (UpdateAssistantDTO)

The body accepts the same fields as `CreateAssistantDTO`. Only include the fields you want to update. All fields are optional.

| Field                         | Type     | Required | Description                                                      |
|-------------------------------|----------|----------|------------------------------------------------------------------|
| name                          | string   | No       | Updated assistant name.                                          |
| firstMessage                  | string   | No       | Updated first message.                                           |
| firstMessageMode              | string   | No       | Updated first message mode.                                      |
| model                         | object   | No       | Updated model configuration (replaces entire model object).      |
| voice                         | object   | No       | Updated voice configuration (replaces entire voice object).      |
| transcriber                   | object   | No       | Updated transcriber configuration.                               |
| tools                         | array    | No       | Updated tools array.                                             |
| hooks                         | array    | No       | Updated hooks array.                                             |
| silenceTimeoutSeconds         | number   | No       | Updated silence timeout.                                         |
| maxDurationSeconds            | number   | No       | Updated max call duration.                                       |
| backgroundSound               | string   | No       | Updated background sound.                                        |
| backchannelingEnabled         | boolean  | No       | Updated backchanneling setting.                                  |
| backgroundDenoisingEnabled    | boolean  | No       | Updated background denoising setting.                            |
| server                        | object   | No       | Updated server/webhook configuration.                            |
| analysisPlan                  | object   | No       | Updated analysis plan.                                           |
| artifactPlan                  | object   | No       | Updated artifact plan.                                           |
| endCallPhrases                | array    | No       | Updated end call phrases.                                        |
| metadata                      | object   | No       | Updated metadata.                                                |

> Note: When updating nested objects like `model`, `voice`, or `transcriber`, the entire sub-object is replaced. Include all desired fields in the nested object, not just the changed ones.

### Request Body Example

```json
{
  "name": "Updated Support Agent",
  "firstMessage": "Hi there! Welcome to Acme Corp support. What can I help you with?",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "systemPrompt": "You are an updated, more professional customer support agent for Acme Corp.",
    "temperature": 0.5
  },
  "silenceTimeoutSeconds": 45,
  "maxDurationSeconds": 900
}
```

### Response

**Status:** `200 OK`

Returns the full updated Assistant object.

```json
{
  "id": "asta_1234567890abcdef",
  "orgId": "org_abcdef1234567890",
  "name": "Updated Support Agent",
  "firstMessage": "Hi there! Welcome to Acme Corp support. What can I help you with?",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "systemPrompt": "You are an updated, more professional customer support agent for Acme Corp.",
    "temperature": 0.5
  },
  "voice": {
    "provider": "11labs",
    "voiceId": "21m00Tcm4TlvDq8ikWAM"
  },
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-2"
  },
  "silenceTimeoutSeconds": 45,
  "maxDurationSeconds": 900,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-16T14:22:00.000Z"
}
```

### cURL Example

```bash
curl -X PATCH "https://api.vapi.ai/assistant/asta_1234567890abcdef" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Support Agent",
    "firstMessage": "Hi there! Welcome to Acme Corp support. What can I help you with?",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "systemPrompt": "You are an updated, more professional customer support agent.",
      "temperature": 0.5
    },
    "silenceTimeoutSeconds": 45,
    "maxDurationSeconds": 900
  }'
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const updatedAssistant = await client.assistants.update("asta_1234567890abcdef", {
  name: "Updated Support Agent",
  firstMessage: "Hi there! Welcome to Acme Corp support. What can I help you with?",
  model: {
    provider: "openai",
    model: "gpt-4o",
    systemPrompt: "You are an updated, more professional customer support agent.",
    temperature: 0.5,
  },
  silenceTimeoutSeconds: 45,
  maxDurationSeconds: 900,
});

console.log("Updated assistant:", updatedAssistant.name);
console.log("New updatedAt:", updatedAssistant.updatedAt);
```

### Python Example

```python
import requests
import os
import json

assistant_id = "asta_1234567890abcdef"
url = f"https://api.vapi.ai/assistant/{assistant_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "name": "Updated Support Agent",
    "firstMessage": "Hi there! Welcome to Acme Corp support. What can I help you with?",
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "systemPrompt": "You are an updated, more professional customer support agent.",
        "temperature": 0.5
    },
    "silenceTimeoutSeconds": 45,
    "maxDurationSeconds": 900
}

response = requests.patch(url, headers=headers, json=payload)
updated_assistant = response.json()

print(f"Updated assistant: {updated_assistant['name']}")
print(f"New updatedAt: {updated_assistant['updatedAt']}")
```

---

## 5. Delete Assistant

Permanently delete an assistant by its ID. This action cannot be undone.

**Doc Reference:** [https://docs.vapi.ai/api-reference/assistants/delete](https://docs.vapi.ai/api-reference/assistants/delete)

### HTTP Request

```
DELETE https://api.vapi.ai/assistant/{id}
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |

### Path Parameters

| Parameter | Type   | Required | Description                             |
|-----------|--------|----------|-----------------------------------------|
| id        | string | Yes      | The unique identifier of the assistant. |

### Response

**Status:** `200 OK`

Returns the deleted Assistant object.

```json
{
  "id": "asta_1234567890abcdef",
  "orgId": "org_abcdef1234567890",
  "name": "Customer Support Agent",
  "firstMessage": "Hello! Thank you for calling. How can I assist you today?",
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "systemPrompt": "You are a friendly customer support agent."
  },
  "voice": {
    "provider": "11labs",
    "voiceId": "21m00Tcm4TlvDq8ikWAM"
  },
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-2"
  },
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X DELETE "https://api.vapi.ai/assistant/asta_1234567890abcdef" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const deletedAssistant = await client.assistants.delete("asta_1234567890abcdef");

console.log("Deleted assistant:", deletedAssistant.id);
console.log("Name was:", deletedAssistant.name);
```

### Python Example

```python
import requests
import os

assistant_id = "asta_1234567890abcdef"
url = f"https://api.vapi.ai/assistant/{assistant_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.delete(url, headers=headers)
deleted_assistant = response.json()

print(f"Deleted assistant: {deleted_assistant['id']}")
print(f"Name was: {deleted_assistant['name']}")
```

---

## Common Response Schema

All assistant endpoints return or operate on the **Assistant object**. Below are the key fields present in every Assistant response.

| Field                         | Type     | Description                                                                                  |
|-------------------------------|----------|----------------------------------------------------------------------------------------------|
| id                            | string   | Unique identifier for the assistant (prefixed with `asta_`).                                 |
| orgId                         | string   | Organization ID that owns this assistant.                                                    |
| name                          | string   | Human-readable name of the assistant.                                                        |
| firstMessage                  | string   | The first message the assistant speaks when a call starts. `null` if assistant waits for user.|
| firstMessageMode              | string   | Controls when the first message is delivered.                                                |
| model                         | object   | LLM configuration including provider, model name, system prompt, temperature, and tools.     |
| model.provider                | string   | LLM provider identifier (e.g., `openai`, `anthropic`, `google`).                            |
| model.model                   | string   | Specific model name (e.g., `gpt-4o`, `claude-3-5-sonnet-20241022`).                         |
| model.systemPrompt            | string   | System prompt / instructions given to the LLM.                                               |
| model.temperature             | number   | Generation temperature.                                                                      |
| model.maxTokens               | number   | Maximum tokens for generation.                                                                |
| model.emotionRecognitionEnabled | boolean | Whether emotion recognition is enabled.                                                      |
| model.tools                   | array    | Tools available to the model.                                                                 |
| voice                         | object   | Voice synthesis configuration.                                                                |
| voice.provider                | string   | Voice provider identifier (e.g., `11labs`, `openai`, `cartesia`).                            |
| voice.voiceId                 | string   | Provider-specific voice ID.                                                                   |
| transcriber                   | object   | Speech-to-text configuration.                                                                 |
| transcriber.provider          | string   | Transcriber provider identifier (e.g., `deepgram`).                                          |
| transcriber.model             | string   | Transcriber model name (e.g., `nova-2`).                                                      |
| transcriber.language          | string   | Transcription language code.                                                                  |
| tools                         | array    | Array of tool configurations attached to the assistant.                                       |
| hooks                         | array    | Array of hook configurations for event-driven actions.                                        |
| silenceTimeoutSeconds         | number   | Seconds of silence before the call ends.                                                      |
| maxDurationSeconds            | number   | Maximum call duration in seconds.                                                             |
| backgroundSound               | string   | Background ambient sound setting.                                                             |
| backchannelingEnabled         | boolean  | Whether backchanneling is enabled.                                                            |
| backgroundDenoisingEnabled    | boolean  | Whether background denoising is enabled.                                                      |
| hipaaEnabled                  | boolean  | Whether HIPAA-compliant mode is enabled.                                                      |
| server                        | object   | Webhook server configuration.                                                                 |
| analysisPlan                  | object   | Post-call analysis configuration.                                                             |
| artifactPlan                  | object   | Artifact capture configuration.                                                               |
| endCallPhrases                | array    | Phrases that trigger call termination.                                                        |
| metadata                      | object   | Arbitrary key-value metadata.                                                                 |
| createdAt                     | string   | ISO 8601 timestamp of when the assistant was created.                                         |
| updatedAt                     | string   | ISO 8601 timestamp of when the assistant was last updated.                                    |
