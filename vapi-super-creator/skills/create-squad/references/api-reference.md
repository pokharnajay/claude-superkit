# Vapi Squads API Reference

Complete API reference for managing Vapi squads. Squads enable multi-assistant workflows where assistants can hand off conversations to each other. All endpoints are REST API only -- there are no CLI equivalents for squad operations.

**Base URL:** `https://api.vapi.ai`
**Authentication:** `Authorization: Bearer $VAPI_API_KEY`

---

## Table of Contents

1. [Create Squad](#1-create-squad)
2. [List Squads](#2-list-squads)
3. [Get Squad](#3-get-squad)
4. [Update Squad](#4-update-squad)
5. [Delete Squad](#5-delete-squad)
6. [Handoff Destination Example](#handoff-destination-example)
7. [Squad as Handoff Destination](#squad-as-handoff-destination)
8. [Common Response Schema](#common-response-schema)

---

## 1. Create Squad

Create a new squad with a set of member assistants and define how they hand off between each other.

**Doc Reference:** [https://docs.vapi.ai/api-reference/squads/create](https://docs.vapi.ai/api-reference/squads/create)

> **Note:** There is no CLI equivalent for this endpoint. Use the REST API directly.

### HTTP Request

```
POST https://api.vapi.ai/squad
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |
| Content-Type    | string | Yes      | `application/json`                   |

### Request Body (CreateSquadDTO)

| Field                  | Type     | Required | Description                                                                                     |
|------------------------|----------|----------|-------------------------------------------------------------------------------------------------|
| name                   | string   | No       | Human-readable name for the squad.                                                              |
| members                | array    | Yes      | Array of squad member objects. Each member defines an assistant and its handoff destinations.    |
| membersOverrides       | object   | No       | Overrides applied to all members in the squad (e.g., shared transcriber, model, voice settings).|

### Member Object Schema

Each member in the `members` array has the following structure:

| Field                    | Type     | Required | Description                                                                                             |
|--------------------------|----------|----------|---------------------------------------------------------------------------------------------------------|
| assistantId              | string   | No*      | ID of an existing assistant to use as this member. Provide either `assistantId` or `assistant`, not both.|
| assistant                | object   | No*      | Inline assistant definition (full CreateAssistantDTO). Provide either `assistantId` or `assistant`, not both. |
| assistantDestinations    | array    | No       | Array of handoff destinations this member can transfer to. Defines the conversation flow between members.|
| assistantOverrides       | object   | No       | Overrides applied to this specific member's assistant configuration.                                     |

> *One of `assistantId` or `assistant` is required per member.

### Assistant Destination Object Schema

Each entry in `assistantDestinations` defines a handoff target:

| Field            | Type     | Required | Description                                                                                                 |
|------------------|----------|----------|-------------------------------------------------------------------------------------------------------------|
| type             | string   | Yes      | Destination type. Use `"assistant"` for assistant-to-assistant handoff within the squad.                     |
| assistantName    | string   | Yes      | The `name` of the target assistant within the squad. Must match the `name` field of another squad member's assistant. |
| description      | string   | No       | Description of when/why to transfer to this destination. Helps the LLM decide when to hand off.             |
| transferMode     | string   | No       | How conversation history is handled during transfer. See Transfer Modes below.                               |
| message          | string   | No       | A message spoken to the caller during the transfer (e.g., "Let me transfer you to our billing department."). |

### Transfer Modes

| Mode                                                          | Description                                                                                                  |
|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| `rolling-history`                                             | **Default.** The full conversation history is passed to the next assistant. The new assistant sees everything.|
| `swap-system-message-in-history`                              | Replaces the system message in the history with the new assistant's system prompt, preserving conversation turns. |
| `delete-history`                                              | Clears all conversation history. The next assistant starts fresh with no prior context.                       |
| `swap-system-message-in-history-and-remove-transfer-tool-messages` | Swaps the system message and also removes any transfer tool call messages from the history.                   |

### Members Overrides Object

The `membersOverrides` object accepts any fields from the assistant configuration and applies them to all members:

| Field            | Type     | Required | Description                                                      |
|------------------|----------|----------|------------------------------------------------------------------|
| transcriber      | object   | No       | Shared transcriber configuration for all members.                |
| model            | object   | No       | Shared model configuration for all members.                      |
| voice            | object   | No       | Shared voice configuration for all members.                      |
| firstMessage     | string   | No       | Shared first message for all members.                            |
| silenceTimeoutSeconds | number | No    | Shared silence timeout for all members.                          |
| maxDurationSeconds | number | No       | Shared max duration for all members.                             |
| backgroundSound  | string   | No       | Shared background sound for all members.                         |
| backchannelingEnabled | boolean | No   | Shared backchanneling setting for all members.                   |
| server           | object   | No       | Shared webhook server configuration for all members.             |

### Request Body Example

```json
{
  "name": "Customer Service Squad",
  "members": [
    {
      "assistant": {
        "name": "Receptionist",
        "firstMessage": "Hello! Welcome to Acme Corp. How can I direct your call today?",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are the receptionist at Acme Corp. Greet callers and determine if they need sales, support, or billing. Transfer them to the appropriate department."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "21m00Tcm4TlvDq8ikWAM"
        },
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Sales Agent",
          "description": "Transfer to sales when the caller wants to learn about products, pricing, or make a purchase.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you to our sales team. One moment please."
        },
        {
          "type": "assistant",
          "assistantName": "Support Agent",
          "description": "Transfer to support when the caller has a technical issue, needs help with their account, or has a complaint.",
          "transferMode": "swap-system-message-in-history",
          "message": "I'll connect you with our support team right away."
        }
      ]
    },
    {
      "assistant": {
        "name": "Sales Agent",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are a sales agent at Acme Corp. Help callers learn about products and pricing. Be persuasive but not pushy."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "pNInz6obpgDQGcFmaJgB"
        },
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Receptionist",
          "description": "Transfer back to receptionist if the caller needs a different department.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you back to our main line."
        }
      ]
    },
    {
      "assistant": {
        "name": "Support Agent",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are a technical support agent at Acme Corp. Help callers resolve issues with their products and accounts. Be patient and thorough."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "EXAVITQu4vr4xnSDxMaL"
        },
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Receptionist",
          "description": "Transfer back to receptionist if the caller needs a different department.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you back to our main line."
        }
      ]
    }
  ],
  "membersOverrides": {
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-2",
      "language": "en"
    },
    "silenceTimeoutSeconds": 30,
    "maxDurationSeconds": 1800,
    "backchannelingEnabled": true
  }
}
```

### Response

**Status:** `201 Created`

Returns the created Squad object.

```json
{
  "id": "squad_abcdef1234567890",
  "orgId": "org_abcdef1234567890",
  "name": "Customer Service Squad",
  "members": [
    {
      "assistant": {
        "id": "asta_receptionist123",
        "name": "Receptionist",
        "firstMessage": "Hello! Welcome to Acme Corp. How can I direct your call today?",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are the receptionist at Acme Corp..."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "21m00Tcm4TlvDq8ikWAM"
        },
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Sales Agent",
          "description": "Transfer to sales when the caller wants to learn about products, pricing, or make a purchase.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you to our sales team. One moment please."
        },
        {
          "type": "assistant",
          "assistantName": "Support Agent",
          "description": "Transfer to support when the caller has a technical issue, needs help with their account, or has a complaint.",
          "transferMode": "swap-system-message-in-history",
          "message": "I'll connect you with our support team right away."
        }
      ]
    },
    {
      "assistant": {
        "id": "asta_sales456",
        "name": "Sales Agent",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are a sales agent at Acme Corp..."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "pNInz6obpgDQGcFmaJgB"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Receptionist",
          "description": "Transfer back to receptionist if the caller needs a different department.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you back to our main line."
        }
      ]
    },
    {
      "assistant": {
        "id": "asta_support789",
        "name": "Support Agent",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are a technical support agent at Acme Corp..."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "EXAVITQu4vr4xnSDxMaL"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Receptionist",
          "description": "Transfer back to receptionist if the caller needs a different department.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you back to our main line."
        }
      ]
    }
  ],
  "membersOverrides": {
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-2",
      "language": "en"
    },
    "silenceTimeoutSeconds": 30,
    "maxDurationSeconds": 1800,
    "backchannelingEnabled": true
  },
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X POST "https://api.vapi.ai/squad" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Service Squad",
    "members": [
      {
        "assistant": {
          "name": "Receptionist",
          "firstMessage": "Hello! Welcome to Acme Corp. How can I direct your call today?",
          "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "systemPrompt": "You are the receptionist at Acme Corp. Greet callers and determine if they need sales or support."
          },
          "voice": {
            "provider": "11labs",
            "voiceId": "21m00Tcm4TlvDq8ikWAM"
          }
        },
        "assistantDestinations": [
          {
            "type": "assistant",
            "assistantName": "Sales Agent",
            "description": "Transfer to sales for product and pricing inquiries.",
            "transferMode": "rolling-history",
            "message": "Let me transfer you to our sales team."
          },
          {
            "type": "assistant",
            "assistantName": "Support Agent",
            "description": "Transfer to support for technical issues.",
            "transferMode": "swap-system-message-in-history",
            "message": "Connecting you with support now."
          }
        ]
      },
      {
        "assistant": {
          "name": "Sales Agent",
          "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "systemPrompt": "You are a sales agent at Acme Corp."
          },
          "voice": {
            "provider": "11labs",
            "voiceId": "pNInz6obpgDQGcFmaJgB"
          }
        },
        "assistantDestinations": [
          {
            "type": "assistant",
            "assistantName": "Receptionist",
            "description": "Transfer back if caller needs a different department.",
            "transferMode": "rolling-history",
            "message": "Transferring you back."
          }
        ]
      },
      {
        "assistant": {
          "name": "Support Agent",
          "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "systemPrompt": "You are a technical support agent at Acme Corp."
          },
          "voice": {
            "provider": "11labs",
            "voiceId": "EXAVITQu4vr4xnSDxMaL"
          }
        },
        "assistantDestinations": [
          {
            "type": "assistant",
            "assistantName": "Receptionist",
            "description": "Transfer back if caller needs a different department.",
            "transferMode": "rolling-history",
            "message": "Transferring you back."
          }
        ]
      }
    ],
    "membersOverrides": {
      "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "en"
      },
      "silenceTimeoutSeconds": 30,
      "maxDurationSeconds": 1800
    }
  }'
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const squad = await client.squads.create({
  name: "Customer Service Squad",
  members: [
    {
      assistant: {
        name: "Receptionist",
        firstMessage: "Hello! Welcome to Acme Corp. How can I direct your call today?",
        model: {
          provider: "openai",
          model: "gpt-4o",
          systemPrompt: "You are the receptionist at Acme Corp. Greet callers and determine if they need sales or support.",
        },
        voice: {
          provider: "11labs",
          voiceId: "21m00Tcm4TlvDq8ikWAM",
        },
      },
      assistantDestinations: [
        {
          type: "assistant",
          assistantName: "Sales Agent",
          description: "Transfer to sales for product and pricing inquiries.",
          transferMode: "rolling-history",
          message: "Let me transfer you to our sales team.",
        },
        {
          type: "assistant",
          assistantName: "Support Agent",
          description: "Transfer to support for technical issues.",
          transferMode: "swap-system-message-in-history",
          message: "Connecting you with support now.",
        },
      ],
    },
    {
      assistant: {
        name: "Sales Agent",
        model: {
          provider: "openai",
          model: "gpt-4o",
          systemPrompt: "You are a sales agent at Acme Corp.",
        },
        voice: {
          provider: "11labs",
          voiceId: "pNInz6obpgDQGcFmaJgB",
        },
      },
      assistantDestinations: [
        {
          type: "assistant",
          assistantName: "Receptionist",
          description: "Transfer back if caller needs a different department.",
          transferMode: "rolling-history",
          message: "Transferring you back.",
        },
      ],
    },
    {
      assistant: {
        name: "Support Agent",
        model: {
          provider: "openai",
          model: "gpt-4o",
          systemPrompt: "You are a technical support agent at Acme Corp.",
        },
        voice: {
          provider: "11labs",
          voiceId: "EXAVITQu4vr4xnSDxMaL",
        },
      },
      assistantDestinations: [
        {
          type: "assistant",
          assistantName: "Receptionist",
          description: "Transfer back if caller needs a different department.",
          transferMode: "rolling-history",
          message: "Transferring you back.",
        },
      ],
    },
  ],
  membersOverrides: {
    transcriber: {
      provider: "deepgram",
      model: "nova-2",
      language: "en",
    },
    silenceTimeoutSeconds: 30,
    maxDurationSeconds: 1800,
  },
});

console.log("Created squad:", squad.id);
console.log("Members count:", squad.members.length);
```

### Python Example

```python
import requests
import os
import json

url = "https://api.vapi.ai/squad"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "name": "Customer Service Squad",
    "members": [
        {
            "assistant": {
                "name": "Receptionist",
                "firstMessage": "Hello! Welcome to Acme Corp. How can I direct your call today?",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "systemPrompt": "You are the receptionist at Acme Corp. Greet callers and determine if they need sales or support."
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "21m00Tcm4TlvDq8ikWAM"
                }
            },
            "assistantDestinations": [
                {
                    "type": "assistant",
                    "assistantName": "Sales Agent",
                    "description": "Transfer to sales for product and pricing inquiries.",
                    "transferMode": "rolling-history",
                    "message": "Let me transfer you to our sales team."
                },
                {
                    "type": "assistant",
                    "assistantName": "Support Agent",
                    "description": "Transfer to support for technical issues.",
                    "transferMode": "swap-system-message-in-history",
                    "message": "Connecting you with support now."
                }
            ]
        },
        {
            "assistant": {
                "name": "Sales Agent",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "systemPrompt": "You are a sales agent at Acme Corp."
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "pNInz6obpgDQGcFmaJgB"
                }
            },
            "assistantDestinations": [
                {
                    "type": "assistant",
                    "assistantName": "Receptionist",
                    "description": "Transfer back if caller needs a different department.",
                    "transferMode": "rolling-history",
                    "message": "Transferring you back."
                }
            ]
        },
        {
            "assistant": {
                "name": "Support Agent",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "systemPrompt": "You are a technical support agent at Acme Corp."
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "EXAVITQu4vr4xnSDxMaL"
                }
            },
            "assistantDestinations": [
                {
                    "type": "assistant",
                    "assistantName": "Receptionist",
                    "description": "Transfer back if caller needs a different department.",
                    "transferMode": "rolling-history",
                    "message": "Transferring you back."
                }
            ]
        }
    ],
    "membersOverrides": {
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "en"
        },
        "silenceTimeoutSeconds": 30,
        "maxDurationSeconds": 1800
    }
}

response = requests.post(url, headers=headers, json=payload)
squad = response.json()

print(f"Created squad: {squad['id']}")
print(f"Members count: {len(squad['members'])}")
```

---

## 2. List Squads

Retrieve a paginated list of all squads in your organization.

**Doc Reference:** [https://docs.vapi.ai/api-reference/squads/list](https://docs.vapi.ai/api-reference/squads/list)

> **Note:** There is no CLI equivalent for this endpoint. Use the REST API directly.

### HTTP Request

```
GET https://api.vapi.ai/squad
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |

### Query Parameters

| Parameter     | Type     | Required | Default | Description                                           |
|---------------|----------|----------|---------|-------------------------------------------------------|
| limit         | number   | No       | 100     | Maximum number of squads to return.                    |
| createdAtGt   | datetime | No       | -       | Return squads created after this datetime (exclusive). ISO 8601 format. |
| createdAtLt   | datetime | No       | -       | Return squads created before this datetime (exclusive). ISO 8601 format. |
| createdAtGe   | datetime | No       | -       | Return squads created at or after this datetime (inclusive). ISO 8601 format. |
| createdAtLe   | datetime | No       | -       | Return squads created at or before this datetime (inclusive). ISO 8601 format. |
| updatedAtGt   | datetime | No       | -       | Return squads updated after this datetime (exclusive). ISO 8601 format. |
| updatedAtLt   | datetime | No       | -       | Return squads updated before this datetime (exclusive). ISO 8601 format. |
| updatedAtGe   | datetime | No       | -       | Return squads updated at or after this datetime (inclusive). ISO 8601 format. |
| updatedAtLe   | datetime | No       | -       | Return squads updated at or before this datetime (inclusive). ISO 8601 format. |

### Response

**Status:** `200 OK`

Returns an array of Squad objects.

```json
[
  {
    "id": "squad_abcdef1234567890",
    "orgId": "org_abcdef1234567890",
    "name": "Customer Service Squad",
    "members": [
      {
        "assistant": {
          "id": "asta_receptionist123",
          "name": "Receptionist"
        },
        "assistantDestinations": [
          {
            "type": "assistant",
            "assistantName": "Sales Agent",
            "transferMode": "rolling-history"
          }
        ]
      }
    ],
    "createdAt": "2025-01-15T10:30:00.000Z",
    "updatedAt": "2025-01-15T10:30:00.000Z"
  }
]
```

### cURL Example

```bash
curl -X GET "https://api.vapi.ai/squad?limit=10" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

With date filters:

```bash
curl -X GET "https://api.vapi.ai/squad?limit=50&createdAtGt=2025-01-01T00:00:00.000Z&createdAtLt=2025-06-01T00:00:00.000Z" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

// List all squads (default limit: 100)
const squads = await client.squads.list();

// List with filters
const filteredSquads = await client.squads.list({
  limit: 10,
  createdAtGt: "2025-01-01T00:00:00.000Z",
});

console.log(`Found ${squads.length} squads`);
for (const squad of squads) {
  console.log(`- ${squad.name} (${squad.id}): ${squad.members.length} members`);
}
```

### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/squad"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
params = {
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)
squads = response.json()

print(f"Found {len(squads)} squads")
for squad in squads:
    print(f"- {squad['name']} ({squad['id']}): {len(squad['members'])} members")
```

---

## 3. Get Squad

Retrieve a single squad by its ID, including all member configurations and handoff destinations.

**Doc Reference:** [https://docs.vapi.ai/api-reference/squads/get](https://docs.vapi.ai/api-reference/squads/get)

> **Note:** There is no CLI equivalent for this endpoint. Use the REST API directly.

### HTTP Request

```
GET https://api.vapi.ai/squad/{id}
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |

### Path Parameters

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| id        | string | Yes      | The unique identifier of the squad. |

### Response

**Status:** `200 OK`

Returns the full Squad object.

```json
{
  "id": "squad_abcdef1234567890",
  "orgId": "org_abcdef1234567890",
  "name": "Customer Service Squad",
  "members": [
    {
      "assistant": {
        "id": "asta_receptionist123",
        "name": "Receptionist",
        "firstMessage": "Hello! Welcome to Acme Corp.",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are the receptionist..."
        },
        "voice": {
          "provider": "11labs",
          "voiceId": "21m00Tcm4TlvDq8ikWAM"
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Sales Agent",
          "description": "Transfer to sales for product inquiries.",
          "transferMode": "rolling-history",
          "message": "Let me transfer you to sales."
        }
      ]
    },
    {
      "assistant": {
        "id": "asta_sales456",
        "name": "Sales Agent",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "systemPrompt": "You are a sales agent..."
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Receptionist",
          "description": "Transfer back if caller needs a different department.",
          "transferMode": "rolling-history"
        }
      ]
    }
  ],
  "membersOverrides": {
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-2"
    }
  },
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X GET "https://api.vapi.ai/squad/squad_abcdef1234567890" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const squad = await client.squads.get("squad_abcdef1234567890");

console.log("Squad name:", squad.name);
console.log("Members:");
for (const member of squad.members) {
  console.log(`  - ${member.assistant?.name || member.assistantId}`);
  if (member.assistantDestinations) {
    for (const dest of member.assistantDestinations) {
      console.log(`    -> Can transfer to: ${dest.assistantName} (${dest.transferMode})`);
    }
  }
}
```

### Python Example

```python
import requests
import os

squad_id = "squad_abcdef1234567890"
url = f"https://api.vapi.ai/squad/{squad_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
squad = response.json()

print(f"Squad name: {squad['name']}")
print("Members:")
for member in squad["members"]:
    assistant = member.get("assistant", {})
    name = assistant.get("name", member.get("assistantId", "Unknown"))
    print(f"  - {name}")
    for dest in member.get("assistantDestinations", []):
        print(f"    -> Can transfer to: {dest['assistantName']} ({dest.get('transferMode', 'rolling-history')})")
```

---

## 4. Update Squad

Update an existing squad. Uses PATCH semantics -- only include the fields you want to change.

**Doc Reference:** [https://docs.vapi.ai/api-reference/squads/update](https://docs.vapi.ai/api-reference/squads/update)

> **Note:** There is no CLI equivalent for this endpoint. Use the REST API directly.

### HTTP Request

```
PATCH https://api.vapi.ai/squad/{id}
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |
| Content-Type    | string | Yes      | `application/json`                   |

### Path Parameters

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| id        | string | Yes      | The unique identifier of the squad. |

### Request Body (UpdateSquadDTO)

The body accepts the same fields as `CreateSquadDTO`. Only include the fields you want to update. All fields are optional.

| Field                  | Type     | Required | Description                                                                |
|------------------------|----------|----------|----------------------------------------------------------------------------|
| name                   | string   | No       | Updated squad name.                                                        |
| members                | array    | No       | Updated members array (replaces entire members list).                      |
| membersOverrides       | object   | No       | Updated member overrides (replaces entire overrides object).               |

> Note: When updating `members`, the entire members array is replaced. Include all desired members, not just changed ones.

### Request Body Example

```json
{
  "name": "Updated Customer Service Squad",
  "membersOverrides": {
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-3"
    },
    "silenceTimeoutSeconds": 45,
    "maxDurationSeconds": 3600
  }
}
```

### Response

**Status:** `200 OK`

Returns the full updated Squad object.

```json
{
  "id": "squad_abcdef1234567890",
  "orgId": "org_abcdef1234567890",
  "name": "Updated Customer Service Squad",
  "members": [
    {
      "assistant": {
        "id": "asta_receptionist123",
        "name": "Receptionist"
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Sales Agent",
          "transferMode": "rolling-history"
        }
      ]
    }
  ],
  "membersOverrides": {
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-3"
    },
    "silenceTimeoutSeconds": 45,
    "maxDurationSeconds": 3600
  },
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-16T14:22:00.000Z"
}
```

### cURL Example

```bash
curl -X PATCH "https://api.vapi.ai/squad/squad_abcdef1234567890" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Customer Service Squad",
    "membersOverrides": {
      "transcriber": {
        "provider": "deepgram",
        "model": "nova-3"
      },
      "silenceTimeoutSeconds": 45,
      "maxDurationSeconds": 3600
    }
  }'
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const updatedSquad = await client.squads.update("squad_abcdef1234567890", {
  name: "Updated Customer Service Squad",
  membersOverrides: {
    transcriber: {
      provider: "deepgram",
      model: "nova-3",
    },
    silenceTimeoutSeconds: 45,
    maxDurationSeconds: 3600,
  },
});

console.log("Updated squad:", updatedSquad.name);
console.log("New updatedAt:", updatedSquad.updatedAt);
```

### Python Example

```python
import requests
import os
import json

squad_id = "squad_abcdef1234567890"
url = f"https://api.vapi.ai/squad/{squad_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "name": "Updated Customer Service Squad",
    "membersOverrides": {
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-3"
        },
        "silenceTimeoutSeconds": 45,
        "maxDurationSeconds": 3600
    }
}

response = requests.patch(url, headers=headers, json=payload)
updated_squad = response.json()

print(f"Updated squad: {updated_squad['name']}")
print(f"New updatedAt: {updated_squad['updatedAt']}")
```

---

## 5. Delete Squad

Permanently delete a squad by its ID. This action cannot be undone. The member assistants themselves are not deleted.

**Doc Reference:** [https://docs.vapi.ai/api-reference/squads/delete](https://docs.vapi.ai/api-reference/squads/delete)

> **Note:** There is no CLI equivalent for this endpoint. Use the REST API directly.

### HTTP Request

```
DELETE https://api.vapi.ai/squad/{id}
```

### Headers

| Header          | Type   | Required | Description                          |
|-----------------|--------|----------|--------------------------------------|
| Authorization   | string | Yes      | Bearer token: `Bearer $VAPI_API_KEY` |

### Path Parameters

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| id        | string | Yes      | The unique identifier of the squad. |

### Response

**Status:** `200 OK`

Returns the deleted Squad object.

```json
{
  "id": "squad_abcdef1234567890",
  "orgId": "org_abcdef1234567890",
  "name": "Customer Service Squad",
  "members": [
    {
      "assistant": {
        "id": "asta_receptionist123",
        "name": "Receptionist"
      },
      "assistantDestinations": []
    }
  ],
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X DELETE "https://api.vapi.ai/squad/squad_abcdef1234567890" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

const deletedSquad = await client.squads.delete("squad_abcdef1234567890");

console.log("Deleted squad:", deletedSquad.id);
console.log("Name was:", deletedSquad.name);
```

### Python Example

```python
import requests
import os

squad_id = "squad_abcdef1234567890"
url = f"https://api.vapi.ai/squad/{squad_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.delete(url, headers=headers)
deleted_squad = response.json()

print(f"Deleted squad: {deleted_squad['id']}")
print(f"Name was: {deleted_squad['name']}")
```

---

## Handoff Destination Example

This example shows how to configure a squad member with multiple handoff destinations, using different transfer modes for different scenarios.

### Multi-Destination Receptionist

```json
{
  "assistant": {
    "name": "Front Desk",
    "firstMessage": "Thank you for calling Acme Corp. I can help you reach the right department.",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "systemPrompt": "You are a front desk receptionist. Determine the caller's need and transfer them:\n- Sales: product info, pricing, new accounts\n- Support: technical issues, bugs, account problems\n- Billing: invoices, payments, refunds\n- HR: job openings, employment verification"
    }
  },
  "assistantDestinations": [
    {
      "type": "assistant",
      "assistantName": "Sales Agent",
      "description": "Transfer when the caller asks about products, pricing, demos, or wants to open a new account.",
      "transferMode": "rolling-history",
      "message": "Great, I'll connect you with our sales team who can help you with that."
    },
    {
      "type": "assistant",
      "assistantName": "Support Agent",
      "description": "Transfer when the caller has a technical issue, bug report, or needs help with their existing account.",
      "transferMode": "swap-system-message-in-history",
      "message": "Let me get you over to our support team. They'll take great care of you."
    },
    {
      "type": "assistant",
      "assistantName": "Billing Agent",
      "description": "Transfer when the caller asks about invoices, payments, billing disputes, or refunds.",
      "transferMode": "swap-system-message-in-history-and-remove-transfer-tool-messages",
      "message": "I'll transfer you to our billing department right away."
    },
    {
      "type": "assistant",
      "assistantName": "HR Agent",
      "description": "Transfer when the caller asks about job openings, applications, or employment verification.",
      "transferMode": "delete-history",
      "message": "I'll connect you with our HR department."
    }
  ]
}
```

### Using Existing Assistant IDs

You can reference pre-created assistants by ID instead of defining them inline:

```json
{
  "name": "Pre-built Squad",
  "members": [
    {
      "assistantId": "asta_receptionist_existing_id",
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Sales Agent",
          "description": "Transfer for sales inquiries.",
          "transferMode": "rolling-history"
        }
      ]
    },
    {
      "assistantId": "asta_sales_existing_id",
      "assistantOverrides": {
        "firstMessage": "Hi! I hear you're interested in our products. How can I help?"
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Receptionist",
          "description": "Transfer back for other departments."
        }
      ]
    }
  ]
}
```

---

## Squad as Handoff Destination

When creating a call, you can use a squad as the call handler. The first member in the `members` array is the initial assistant that answers the call. Subsequent members are reached via handoff destinations.

### Starting a Call with a Squad

To start a call using a squad, reference the squad ID in the call creation request:

```bash
curl -X POST "https://api.vapi.ai/call" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "squadId": "squad_abcdef1234567890",
    "phoneNumberId": "phn_1234567890abcdef",
    "customer": {
      "number": "+11234567890"
    }
  }'
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const client = new VapiClient({ token: process.env.VAPI_API_KEY });

// Create a call using a squad
const call = await client.calls.create({
  squadId: "squad_abcdef1234567890",
  phoneNumberId: "phn_1234567890abcdef",
  customer: {
    number: "+11234567890",
  },
});

console.log("Call started:", call.id);
console.log("Squad:", call.squadId);
```

### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/call"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "squadId": "squad_abcdef1234567890",
    "phoneNumberId": "phn_1234567890abcdef",
    "customer": {
        "number": "+11234567890"
    }
}

response = requests.post(url, headers=headers, json=payload)
call = response.json()

print(f"Call started: {call['id']}")
print(f"Squad: {call['squadId']}")
```

### Inline Squad in Call Creation

You can also define the entire squad inline when creating a call, without creating it as a separate resource first:

```json
{
  "squad": {
    "members": [
      {
        "assistant": {
          "name": "Greeter",
          "firstMessage": "Hello! How can I help?",
          "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "systemPrompt": "Greet and route callers."
          },
          "voice": {
            "provider": "11labs",
            "voiceId": "21m00Tcm4TlvDq8ikWAM"
          }
        },
        "assistantDestinations": [
          {
            "type": "assistant",
            "assistantName": "Specialist",
            "description": "Transfer for detailed help.",
            "transferMode": "rolling-history",
            "message": "Let me connect you with a specialist."
          }
        ]
      },
      {
        "assistant": {
          "name": "Specialist",
          "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "systemPrompt": "You are a specialist. Provide detailed help."
          },
          "voice": {
            "provider": "11labs",
            "voiceId": "pNInz6obpgDQGcFmaJgB"
          }
        },
        "assistantDestinations": []
      }
    ],
    "membersOverrides": {
      "transcriber": {
        "provider": "deepgram",
        "model": "nova-2"
      }
    }
  },
  "phoneNumberId": "phn_1234567890abcdef",
  "customer": {
    "number": "+11234567890"
  }
}
```

---

## Common Response Schema

All squad endpoints return or operate on the **Squad object**. Below are the key fields present in every Squad response.

| Field                  | Type     | Description                                                                                  |
|------------------------|----------|----------------------------------------------------------------------------------------------|
| id                     | string   | Unique identifier for the squad (prefixed with `squad_`).                                    |
| orgId                  | string   | Organization ID that owns this squad.                                                        |
| name                   | string   | Human-readable name of the squad.                                                            |
| members                | array    | Array of member objects, each containing an assistant and its handoff destinations.           |
| members[].assistantId  | string   | ID of the referenced assistant (if using an existing assistant).                             |
| members[].assistant    | object   | Inline assistant definition or resolved assistant object.                                    |
| members[].assistantDestinations | array | Array of handoff destinations this member can transfer to.                              |
| members[].assistantDestinations[].type | string | Destination type (`"assistant"`).                                                  |
| members[].assistantDestinations[].assistantName | string | Name of the target assistant within the squad.                                  |
| members[].assistantDestinations[].description | string | Description of when to transfer.                                                  |
| members[].assistantDestinations[].transferMode | string | How conversation history is handled during transfer.                              |
| members[].assistantDestinations[].message | string | Message spoken during the transfer.                                                    |
| members[].assistantOverrides | object | Per-member overrides for the assistant configuration.                                   |
| membersOverrides       | object   | Overrides applied to all members in the squad.                                               |
| createdAt              | string   | ISO 8601 timestamp of when the squad was created.                                            |
| updatedAt              | string   | ISO 8601 timestamp of when the squad was last updated.                                       |
