# Vapi Tools API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 6 endpoints in the Tools API for creating, managing, and testing custom tools that extend Vapi voice assistant capabilities.

---

## Table of Contents

- [Tools API](#tools-api)
  - [1. Create Tool](#1-create-tool)
  - [2. List Tools](#2-list-tools)
  - [3. Get Tool](#3-get-tool)
  - [4. Update Tool](#4-update-tool)
  - [5. Delete Tool](#5-delete-tool)
  - [6. Test Code Tool Execution](#6-test-code-tool-execution)
- [Tool Schemas](#tool-schemas)
  - [Function Tool Schema](#function-tool-schema)
  - [Code Tool Schema](#code-tool-schema)
  - [Tool Messages Configuration](#tool-messages-configuration)
- [Adding Tools to Assistants](#adding-tools-to-assistants)
- [Security Best Practices](#security-best-practices)

---

## Tools API

### 1. Create Tool

Creates a new tool that can be attached to voice assistants. Supports two primary tool types: **function tools** (server-side webhook) and **code tools** (inline TypeScript execution).

#### HTTP Request

```
POST https://api.vapi.ai/tool
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Common Request Body Parameters

These parameters apply to all tool types.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | Yes | Tool type: `"function"` or `"code"`. Other types include `"transferCall"`, `"endCall"`, `"dtmf"`, `"ghl"`, `"make"`, `"output"`. |
| `name` | string | Yes | Descriptive identifier for the tool. Used by the AI model to understand when to invoke it. |
| `description` | string | Yes | Explanation of what the tool does. The AI uses this to decide when to call the tool. |
| `parameters` | object | Yes | JSON Schema object defining the input parameters the AI should extract from the conversation. |
| `async` | boolean | No | Whether the tool runs asynchronously (default: `false`). When `true`, the assistant continues speaking without waiting for the tool result. |
| `messages` | array | No | Custom messages spoken during different tool execution states. See [Tool Messages Configuration](#tool-messages-configuration). |

#### Function Tool Additional Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `function` | object | Yes | Function configuration containing `name`, `description`, and `parameters`. |
| `function.name` | string | Yes | Name of the function (used internally by the model). |
| `function.description` | string | Yes | Description of what the function does. |
| `function.parameters` | object | Yes | JSON Schema for the function's input parameters. |
| `server` | object | Yes | Server configuration for the webhook endpoint. |
| `server.url` | string | Yes | The HTTPS URL that Vapi will POST to when the tool is invoked. |
| `server.secret` | string | No | Secret used to sign webhook payloads for verification. |
| `server.timeoutSeconds` | number | No | Timeout in seconds for the server response (default: 20). |

#### Code Tool Additional Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | string | Yes | TypeScript code to execute. Has access to `args` (parameters) and `env` (environment variables). Must return a value. |
| `environmentVariables` | array | No | Array of `{name, value}` objects for securely storing API keys and secrets. Accessible via `env` in the code. |
| `maxTokens` | number | No | Token limit for the tool response (default: 100). |
| `timeout` | number | No | Execution timeout in seconds (max: 60). |

#### Request Body: Function Tool

```json
{
  "type": "function",
  "name": "get_weather",
  "description": "Retrieves current weather information for any location. Call this when the user asks about weather conditions.",
  "function": {
    "name": "get_weather",
    "description": "Get weather data for a specified location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city or location to get weather for (e.g., 'San Francisco, CA')"
        },
        "units": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "Temperature units preference"
        }
      },
      "required": ["location"]
    }
  },
  "server": {
    "url": "https://your-server.com/api/weather",
    "secret": "your-webhook-secret",
    "timeoutSeconds": 10
  },
  "messages": [
    {
      "type": "request-start",
      "content": "Let me check the weather for you."
    },
    {
      "type": "request-complete",
      "content": "Here's what I found."
    },
    {
      "type": "request-failed",
      "content": "I'm sorry, I wasn't able to get the weather information right now."
    },
    {
      "type": "request-response-delayed",
      "content": "Still checking the weather, one moment please."
    }
  ]
}
```

#### Request Body: Code Tool

```json
{
  "type": "code",
  "name": "get_customer",
  "description": "Retrieves customer information by their ID from the internal database. Call this when you need to look up customer details.",
  "code": "const { customerId } = args;\nconst { API_KEY, API_BASE_URL } = env;\n\nconst response = await fetch(`${API_BASE_URL}/customers/${customerId}`, {\n  headers: { \"Authorization\": `Bearer ${API_KEY}` }\n});\n\nif (!response.ok) {\n  return { error: \"Customer not found\" };\n}\n\nreturn await response.json();",
  "parameters": {
    "type": "object",
    "properties": {
      "customerId": {
        "type": "string",
        "description": "The unique customer identifier"
      }
    },
    "required": ["customerId"]
  },
  "environmentVariables": [
    {
      "name": "API_KEY",
      "value": "your-api-key-here"
    },
    {
      "name": "API_BASE_URL",
      "value": "https://api.yourservice.com"
    }
  ]
}
```

#### Response: `201 Created`

```json
{
  "id": "tool_abc123",
  "orgId": "org_xyz789",
  "type": "function",
  "name": "get_weather",
  "description": "Retrieves current weather information for any location.",
  "function": {
    "name": "get_weather",
    "description": "Get weather data for a specified location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city or location to get weather for"
        }
      },
      "required": ["location"]
    }
  },
  "server": {
    "url": "https://your-server.com/api/weather",
    "timeoutSeconds": 10
  },
  "messages": [
    {
      "type": "request-start",
      "content": "Let me check the weather for you."
    }
  ],
  "createdAt": "2026-03-02T10:00:00.000Z",
  "updatedAt": "2026-03-02T10:00:00.000Z"
}
```

#### cURL Example: Function Tool

```bash
curl -X POST https://api.vapi.ai/tool \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "function",
    "name": "get_weather",
    "description": "Retrieves current weather information for any location.",
    "function": {
      "name": "get_weather",
      "description": "Get weather data for a specified location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city or location to get weather for"
          }
        },
        "required": ["location"]
      }
    },
    "server": {
      "url": "https://your-server.com/api/weather"
    }
  }'
```

#### cURL Example: Code Tool

```bash
curl -X POST https://api.vapi.ai/tool \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "code",
    "name": "get_customer",
    "description": "Retrieves customer information by their ID.",
    "code": "const { customerId } = args;\nconst { API_KEY, API_BASE_URL } = env;\n\nconst response = await fetch(`${API_BASE_URL}/customers/${customerId}`, {\n  headers: { \"Authorization\": `Bearer ${API_KEY}` }\n});\n\nif (!response.ok) {\n  return { error: \"Customer not found\" };\n}\n\nreturn await response.json();",
    "parameters": {
      "type": "object",
      "properties": {
        "customerId": {
          "type": "string",
          "description": "The unique customer identifier"
        }
      },
      "required": ["customerId"]
    },
    "environmentVariables": [
      { "name": "API_KEY", "value": "your-api-key-here" },
      { "name": "API_BASE_URL", "value": "https://api.yourservice.com" }
    ]
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// Create a function tool
const functionTool = await vapi.tools.create({
  type: "function",
  name: "get_weather",
  description: "Retrieves current weather information for any location.",
  function: {
    name: "get_weather",
    description: "Get weather data for a specified location",
    parameters: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "The city or location to get weather for",
        },
      },
      required: ["location"],
    },
  },
  server: {
    url: "https://your-server.com/api/weather",
    secret: "your-webhook-secret",
  },
  messages: [
    {
      type: "request-start",
      content: "Let me check the weather for you.",
    },
    {
      type: "request-failed",
      content: "Sorry, I couldn't get the weather right now.",
    },
  ],
});

console.log("Function Tool ID:", functionTool.id);

// Create a code tool
const codeTool = await vapi.tools.create({
  type: "code",
  name: "calculate_discount",
  description: "Calculates discount based on customer tier and order amount.",
  code: `const { tier, amount } = args;
const discounts = { premium: 0.20, standard: 0.10, basic: 0.05 };
const rate = discounts[tier] || 0;
const discount = amount * rate;
return { originalAmount: amount, discountRate: rate, discountAmount: discount, finalAmount: amount - discount };`,
  parameters: {
    type: "object",
    properties: {
      tier: {
        type: "string",
        enum: ["premium", "standard", "basic"],
        description: "Customer tier level",
      },
      amount: {
        type: "number",
        description: "Order amount in dollars",
      },
    },
    required: ["tier", "amount"],
  },
});

console.log("Code Tool ID:", codeTool.id);
```

#### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/tool"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}

# Create a function tool
function_tool_payload = {
    "type": "function",
    "name": "get_weather",
    "description": "Retrieves current weather information for any location.",
    "function": {
        "name": "get_weather",
        "description": "Get weather data for a specified location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location to get weather for",
                }
            },
            "required": ["location"],
        },
    },
    "server": {
        "url": "https://your-server.com/api/weather",
        "secret": "your-webhook-secret",
    },
}

response = requests.post(url, json=function_tool_payload, headers=headers)
function_tool = response.json()
print(f"Function Tool ID: {function_tool['id']}")

# Create a code tool
code_tool_payload = {
    "type": "code",
    "name": "get_customer",
    "description": "Retrieves customer information by their ID.",
    "code": (
        'const { customerId } = args;\n'
        'const { API_KEY, API_BASE_URL } = env;\n'
        '\n'
        'const response = await fetch(`${API_BASE_URL}/customers/${customerId}`, {\n'
        '  headers: { "Authorization": `Bearer ${API_KEY}` }\n'
        '});\n'
        '\n'
        'if (!response.ok) {\n'
        '  return { error: "Customer not found" };\n'
        '}\n'
        '\n'
        'return await response.json();'
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "customerId": {
                "type": "string",
                "description": "The unique customer identifier",
            }
        },
        "required": ["customerId"],
    },
    "environmentVariables": [
        {"name": "API_KEY", "value": "your-api-key-here"},
        {"name": "API_BASE_URL", "value": "https://api.yourservice.com"},
    ],
}

response = requests.post(url, json=code_tool_payload, headers=headers)
code_tool = response.json()
print(f"Code Tool ID: {code_tool['id']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/create](https://docs.vapi.ai/api-reference/tools/create)

---

### 2. List Tools

Retrieves a paginated list of all tools in your organization.

#### HTTP Request

```
GET https://api.vapi.ai/tool
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | number | No | Maximum number of tools to return (default: 100). |
| `offset` | number | No | Number of tools to skip for pagination. |
| `createdAtGt` | string | No | Filter tools created after this ISO 8601 timestamp. |
| `createdAtLt` | string | No | Filter tools created before this ISO 8601 timestamp. |
| `createdAtGe` | string | No | Filter tools created at or after this ISO 8601 timestamp. |
| `createdAtLe` | string | No | Filter tools created at or before this ISO 8601 timestamp. |
| `updatedAtGt` | string | No | Filter tools updated after this ISO 8601 timestamp. |
| `updatedAtLt` | string | No | Filter tools updated before this ISO 8601 timestamp. |
| `updatedAtGe` | string | No | Filter tools updated at or after this ISO 8601 timestamp. |
| `updatedAtLe` | string | No | Filter tools updated at or before this ISO 8601 timestamp. |

#### Response: `200 OK`

```json
[
  {
    "id": "tool_abc123",
    "orgId": "org_xyz789",
    "type": "function",
    "name": "get_weather",
    "description": "Retrieves current weather information for any location.",
    "function": {
      "name": "get_weather",
      "description": "Get weather data for a specified location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": { "type": "string" }
        },
        "required": ["location"]
      }
    },
    "server": {
      "url": "https://your-server.com/api/weather"
    },
    "createdAt": "2026-03-01T10:00:00.000Z",
    "updatedAt": "2026-03-01T10:00:00.000Z"
  },
  {
    "id": "tool_def456",
    "orgId": "org_xyz789",
    "type": "code",
    "name": "get_customer",
    "description": "Retrieves customer information by their ID.",
    "code": "const { customerId } = args;...",
    "parameters": {
      "type": "object",
      "properties": {
        "customerId": { "type": "string" }
      },
      "required": ["customerId"]
    },
    "createdAt": "2026-03-02T08:00:00.000Z",
    "updatedAt": "2026-03-02T08:00:00.000Z"
  }
]
```

#### cURL Example

```bash
# List all tools
curl -X GET "https://api.vapi.ai/tool" \
  -H "Authorization: Bearer $VAPI_API_KEY"

# List with pagination
curl -X GET "https://api.vapi.ai/tool?limit=20&offset=0" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const tools = await vapi.tools.list({
  limit: 50,
});

for (const tool of tools) {
  console.log(`${tool.id} | ${tool.type} | ${tool.name}`);
}
```

#### Python Example

```python
import requests
import os

url = "https://api.vapi.ai/tool"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}
params = {
    "limit": 50,
    "offset": 0,
}

response = requests.get(url, headers=headers, params=params)
tools = response.json()

for tool in tools:
    print(f"{tool['id']} | {tool['type']} | {tool['name']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/list](https://docs.vapi.ai/api-reference/tools/list)

---

### 3. Get Tool

Retrieves a single tool by its ID, including its full configuration.

#### HTTP Request

```
GET https://api.vapi.ai/tool/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the tool to retrieve. |

#### Response: `200 OK`

```json
{
  "id": "tool_abc123",
  "orgId": "org_xyz789",
  "type": "function",
  "name": "get_weather",
  "description": "Retrieves current weather information for any location.",
  "function": {
    "name": "get_weather",
    "description": "Get weather data for a specified location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city or location to get weather for"
        },
        "units": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "Temperature units preference"
        }
      },
      "required": ["location"]
    }
  },
  "server": {
    "url": "https://your-server.com/api/weather",
    "timeoutSeconds": 10
  },
  "messages": [
    {
      "type": "request-start",
      "content": "Let me check the weather for you."
    },
    {
      "type": "request-failed",
      "content": "Sorry, I couldn't get the weather right now."
    }
  ],
  "async": false,
  "createdAt": "2026-03-01T10:00:00.000Z",
  "updatedAt": "2026-03-01T10:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X GET https://api.vapi.ai/tool/tool_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const tool = await vapi.tools.get("tool_abc123");

console.log("Name:", tool.name);
console.log("Type:", tool.type);
console.log("Description:", tool.description);

if (tool.type === "function") {
  console.log("Server URL:", tool.server?.url);
  console.log("Parameters:", JSON.stringify(tool.function?.parameters, null, 2));
} else if (tool.type === "code") {
  console.log("Code:", tool.code);
  console.log(
    "Env Vars:",
    tool.environmentVariables?.map((e) => e.name).join(", ")
  );
}
```

#### Python Example

```python
import requests
import os
import json

tool_id = "tool_abc123"
url = f"https://api.vapi.ai/tool/{tool_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}

response = requests.get(url, headers=headers)
tool = response.json()

print(f"Name: {tool['name']}")
print(f"Type: {tool['type']}")
print(f"Description: {tool['description']}")

if tool["type"] == "function":
    print(f"Server URL: {tool.get('server', {}).get('url')}")
    print(f"Parameters: {json.dumps(tool.get('function', {}).get('parameters'), indent=2)}")
elif tool["type"] == "code":
    print(f"Code: {tool.get('code', '')[:200]}...")
    env_vars = [ev["name"] for ev in tool.get("environmentVariables", [])]
    print(f"Env Vars: {', '.join(env_vars)}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/get](https://docs.vapi.ai/api-reference/tools/get)

---

### 4. Update Tool

Updates an existing tool's configuration. All fields are optional; only provided fields are updated.

#### HTTP Request

```
PATCH https://api.vapi.ai/tool/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the tool to update. |

#### Request Body Parameters

Same schema as [Create Tool](#1-create-tool) but all fields are optional. Only provided fields are updated.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Updated tool name. |
| `description` | string | No | Updated description. |
| `function` | object | No | Updated function configuration (function tools only). |
| `server` | object | No | Updated server configuration (function tools only). |
| `code` | string | No | Updated TypeScript code (code tools only). |
| `parameters` | object | No | Updated JSON Schema parameters. |
| `environmentVariables` | array | No | Updated environment variables (code tools only). |
| `messages` | array | No | Updated tool messages. |
| `async` | boolean | No | Updated async setting. |

#### Request Body

```json
{
  "description": "Retrieves current weather information for any location worldwide, including temperature, humidity, and wind speed.",
  "server": {
    "url": "https://new-server.com/api/v2/weather",
    "timeoutSeconds": 15
  },
  "messages": [
    {
      "type": "request-start",
      "content": "Checking the weather for you now."
    },
    {
      "type": "request-failed",
      "content": "I'm having trouble getting weather data. Please try again later."
    }
  ]
}
```

#### Response: `200 OK`

```json
{
  "id": "tool_abc123",
  "orgId": "org_xyz789",
  "type": "function",
  "name": "get_weather",
  "description": "Retrieves current weather information for any location worldwide, including temperature, humidity, and wind speed.",
  "function": {
    "name": "get_weather",
    "description": "Get weather data for a specified location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": { "type": "string" }
      },
      "required": ["location"]
    }
  },
  "server": {
    "url": "https://new-server.com/api/v2/weather",
    "timeoutSeconds": 15
  },
  "createdAt": "2026-03-01T10:00:00.000Z",
  "updatedAt": "2026-03-02T14:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/tool/tool_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Retrieves current weather information for any location worldwide.",
    "server": {
      "url": "https://new-server.com/api/v2/weather",
      "timeoutSeconds": 15
    }
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const updatedTool = await vapi.tools.update("tool_abc123", {
  description:
    "Retrieves current weather information for any location worldwide.",
  server: {
    url: "https://new-server.com/api/v2/weather",
    timeoutSeconds: 15,
  },
  messages: [
    {
      type: "request-start",
      content: "Checking the weather for you now.",
    },
  ],
});

console.log("Updated:", updatedTool.updatedAt);
console.log("New server URL:", updatedTool.server?.url);
```

#### Python Example

```python
import requests
import os

tool_id = "tool_abc123"
url = f"https://api.vapi.ai/tool/{tool_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "description": "Retrieves current weather information for any location worldwide.",
    "server": {
        "url": "https://new-server.com/api/v2/weather",
        "timeoutSeconds": 15,
    },
    "messages": [
        {
            "type": "request-start",
            "content": "Checking the weather for you now.",
        }
    ],
}

response = requests.patch(url, json=payload, headers=headers)
updated_tool = response.json()
print(f"Updated: {updated_tool['updatedAt']}")
print(f"New server URL: {updated_tool.get('server', {}).get('url')}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/update](https://docs.vapi.ai/api-reference/tools/update)

---

### 5. Delete Tool

Permanently deletes a tool. If the tool is currently attached to any assistants, it should be removed from those assistants first.

#### HTTP Request

```
DELETE https://api.vapi.ai/tool/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique ID of the tool to delete. |

#### Response: `200 OK`

```json
{
  "id": "tool_abc123",
  "orgId": "org_xyz789",
  "type": "function",
  "name": "get_weather",
  "description": "Retrieves current weather information for any location.",
  "createdAt": "2026-03-01T10:00:00.000Z",
  "updatedAt": "2026-03-01T10:00:00.000Z"
}
```

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/tool/tool_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const deletedTool = await vapi.tools.delete("tool_abc123");
console.log("Deleted tool:", deletedTool.id, deletedTool.name);
```

#### Python Example

```python
import requests
import os

tool_id = "tool_abc123"
url = f"https://api.vapi.ai/tool/{tool_id}"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
}

response = requests.delete(url, headers=headers)
deleted_tool = response.json()
print(f"Deleted tool: {deleted_tool['id']} ({deleted_tool['name']})")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/delete](https://docs.vapi.ai/api-reference/tools/delete)

---

### 6. Test Code Tool Execution

Tests a code tool's execution in a sandbox environment without deploying it. Use this endpoint to validate your TypeScript code, debug issues, and verify that environment variables and parameters work correctly before attaching the tool to an assistant.

#### HTTP Request

```
POST https://api.vapi.ai/tool/code/test
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | Yes | Must be `"code"`. |
| `name` | string | Yes | Name of the tool being tested. |
| `description` | string | Yes | Description of the tool being tested. |
| `code` | string | Yes | TypeScript code to execute. Has access to `args` and `env` objects. |
| `parameters` | object | Yes | JSON Schema defining the test input parameters. |
| `environmentVariables` | array | No | Array of `{name, value}` objects for environment variables accessible via `env`. |

#### Request Body

```json
{
  "type": "code",
  "name": "get_customer",
  "description": "Retrieves customer information by ID",
  "code": "const { customerId } = args;\nconst { API_KEY, API_BASE_URL } = env;\n\nif (!customerId) {\n  return { error: \"Customer ID is required\" };\n}\n\nconsole.log(`Looking up customer: ${customerId}`);\n\nreturn {\n  customerId,\n  name: \"John Doe\",\n  email: \"john@example.com\",\n  status: \"active\"\n};",
  "parameters": {
    "type": "object",
    "properties": {
      "customerId": {
        "type": "string",
        "description": "The unique customer identifier"
      }
    },
    "required": ["customerId"]
  },
  "environmentVariables": [
    { "name": "API_KEY", "value": "test-key-123" },
    { "name": "API_BASE_URL", "value": "https://api.example.com" }
  ]
}
```

#### Response: `200 OK`

```json
{
  "success": true,
  "result": {
    "customerId": "cust_123",
    "name": "John Doe",
    "email": "john@example.com",
    "status": "active"
  },
  "error": null,
  "logs": "Looking up customer: cust_123",
  "executionTimeMs": 45.2
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the code executed without errors. |
| `result` | object | The value returned by your code. Empty object `{}` if no return value. |
| `error` | string or null | Error message if execution failed. `null` on success. |
| `logs` | string | All `console.log()` output captured during execution. |
| `executionTimeMs` | number | How long the code took to execute in milliseconds. |

#### Error Response Example

```json
{
  "success": false,
  "result": {},
  "error": "ReferenceError: unknownVariable is not defined",
  "logs": "",
  "executionTimeMs": 2.1
}
```

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/tool/code/test \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "code",
    "name": "get_customer",
    "description": "Retrieves customer information by ID",
    "code": "const { customerId } = args;\nconst { API_KEY } = env;\n\nif (!customerId) {\n  return { error: \"Customer ID is required\" };\n}\n\nconsole.log(`Looking up customer: ${customerId}`);\n\nreturn {\n  customerId,\n  name: \"John Doe\",\n  email: \"john@example.com\",\n  status: \"active\"\n};",
    "parameters": {
      "type": "object",
      "properties": {
        "customerId": {
          "type": "string",
          "description": "The unique customer identifier"
        }
      },
      "required": ["customerId"]
    },
    "environmentVariables": [
      { "name": "API_KEY", "value": "test-key-123" }
    ]
  }'
```

#### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// Test a code tool before creating it
const testResult = await vapi.tools.testCodeExecution({
  type: "code",
  name: "calculate_discount",
  description: "Calculates discount based on customer tier and order amount",
  code: `
    const { tier, amount } = args;
    const discounts = { premium: 0.20, standard: 0.10, basic: 0.05 };
    const rate = discounts[tier] || 0;
    const discount = amount * rate;
    console.log(\`Tier: \${tier}, Rate: \${rate}, Amount: \${amount}\`);
    return {
      originalAmount: amount,
      discountRate: rate,
      discountAmount: discount,
      finalAmount: amount - discount
    };
  `,
  parameters: {
    type: "object",
    properties: {
      tier: {
        type: "string",
        enum: ["premium", "standard", "basic"],
        description: "Customer tier level",
      },
      amount: {
        type: "number",
        description: "Order amount in dollars",
      },
    },
    required: ["tier", "amount"],
  },
});

console.log("Success:", testResult.success);
console.log("Result:", JSON.stringify(testResult.result, null, 2));
console.log("Logs:", testResult.logs);
console.log("Execution Time:", testResult.executionTimeMs, "ms");

if (testResult.error) {
  console.error("Error:", testResult.error);
}
```

#### Python Example

```python
import requests
import os
import json

url = "https://api.vapi.ai/tool/code/test"
headers = {
    "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
    "Content-Type": "application/json",
}
payload = {
    "type": "code",
    "name": "calculate_discount",
    "description": "Calculates discount based on customer tier and order amount",
    "code": (
        "const { tier, amount } = args;\n"
        "const discounts = { premium: 0.20, standard: 0.10, basic: 0.05 };\n"
        "const rate = discounts[tier] || 0;\n"
        "const discount = amount * rate;\n"
        "console.log(`Tier: ${tier}, Rate: ${rate}, Amount: ${amount}`);\n"
        "return {\n"
        "  originalAmount: amount,\n"
        "  discountRate: rate,\n"
        "  discountAmount: discount,\n"
        "  finalAmount: amount - discount\n"
        "};"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "tier": {
                "type": "string",
                "enum": ["premium", "standard", "basic"],
                "description": "Customer tier level",
            },
            "amount": {
                "type": "number",
                "description": "Order amount in dollars",
            },
        },
        "required": ["tier", "amount"],
    },
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

print(f"Success: {result['success']}")
print(f"Result: {json.dumps(result['result'], indent=2)}")
print(f"Logs: {result['logs']}")
print(f"Execution Time: {result['executionTimeMs']}ms")

if result.get("error"):
    print(f"Error: {result['error']}")
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/tool-controller-test-code-execution](https://docs.vapi.ai/api-reference/tools/tool-controller-test-code-execution)

---

### 7. Discover MCP Child Tools

Discovers available tools from an MCP (Model Context Protocol) server that has been configured as a tool in Vapi. Use this to dynamically discover what capabilities are available from your MCP providers, verify MCP server connectivity, or build interfaces that adapt based on available tools.

#### HTTP Request

```
POST https://api.vapi.ai/tool/{id}/mcp-children
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The ID of the MCP tool from which to discover child tools. |

#### Response: `200 OK`

Returns an array of `McpTool` objects representing the available tools from the MCP server.

```json
[
  {
    "type": "function",
    "name": "search_docs",
    "description": "Search documentation for relevant information",
    "parameters": {
      "type": "object",
      "properties": {
        "query": { "type": "string", "description": "Search query" }
      },
      "required": ["query"]
    }
  }
]
```

#### cURL Example

```bash
curl -X POST "https://api.vapi.ai/tool/{id}/mcp-children" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json"
```

#### Python Example

```python
import requests, os

response = requests.post(
    f"https://api.vapi.ai/tool/{tool_id}/mcp-children",
    headers={"Authorization": f"Bearer {os.environ['VAPI_API_KEY']}"},
)
child_tools = response.json()
for tool in child_tools:
    print(f"Discovered: {tool['name']} - {tool.get('description', '')}")
```

#### TypeScript Example

```typescript
const response = await fetch(
  `https://api.vapi.ai/tool/${toolId}/mcp-children`,
  {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
  }
);
const childTools = await response.json();
console.log(`Discovered ${childTools.length} MCP child tools`);
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/tools/tool-controller-mcp-child-tools-discover](https://docs.vapi.ai/api-reference/tools/tool-controller-mcp-child-tools-discover)

---

## Tool Schemas

### Function Tool Schema

Function tools call an external HTTP endpoint (your server) when the AI decides to invoke the tool during a conversation. Vapi sends a POST request to your server URL with the extracted parameters.

```json
{
  "type": "function",
  "name": "string (required)",
  "description": "string (required) - Tell the AI when to use this tool",
  "function": {
    "name": "string (required) - Internal function name",
    "description": "string (required) - What the function does",
    "parameters": {
      "type": "object",
      "properties": {
        "paramName": {
          "type": "string | number | boolean | array | object",
          "description": "string - Parameter description for the AI",
          "enum": ["optional", "restricted", "values"]
        }
      },
      "required": ["paramName"]
    }
  },
  "server": {
    "url": "string (required) - HTTPS webhook endpoint",
    "secret": "string (optional) - Webhook signing secret",
    "timeoutSeconds": "number (optional, default: 20)"
  },
  "async": "boolean (optional, default: false)",
  "messages": [
    {
      "type": "request-start | request-complete | request-failed | request-response-delayed",
      "content": "string - Message spoken to the user"
    }
  ]
}
```

**How Function Tools Work:**

1. The AI model determines it should call the tool based on the conversation context.
2. Vapi sends a POST request to `server.url` with the extracted parameters.
3. Your server processes the request and returns a JSON response.
4. The AI uses the response to continue the conversation.

**Webhook Request Payload (sent to your server):**

```json
{
  "message": {
    "type": "tool-calls",
    "toolCallList": [
      {
        "id": "call_xyz",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"location\": \"San Francisco\"}"
        }
      }
    ]
  }
}
```

**Expected Response from Your Server:**

```json
{
  "results": [
    {
      "toolCallId": "call_xyz",
      "result": "The weather in San Francisco is 65 degrees and sunny."
    }
  ]
}
```

---

### Code Tool Schema

Code tools execute TypeScript code directly on Vapi's serverless infrastructure. They have access to `args` (extracted parameters) and `env` (environment variables) and can use `fetch()` for HTTP requests.

```json
{
  "type": "code",
  "name": "string (required)",
  "description": "string (required) - Tell the AI when to use this tool",
  "code": "string (required) - TypeScript code with access to `args` and `env`",
  "parameters": {
    "type": "object",
    "properties": {
      "paramName": {
        "type": "string | number | boolean | array | object",
        "description": "string - Parameter description for the AI"
      }
    },
    "required": ["paramName"]
  },
  "environmentVariables": [
    {
      "name": "string - Variable name (accessed via env.NAME)",
      "value": "string - Variable value (stored securely)"
    }
  ],
  "maxTokens": "number (optional, default: 100)",
  "timeout": "number (optional, max: 60 seconds)"
}
```

**Code Tool Capabilities:**

- Full TypeScript/JavaScript execution environment.
- `args` object: Contains the parameters extracted by the AI from the conversation.
- `env` object: Contains your environment variables (API keys, URLs, etc.).
- `fetch()`: Available for making HTTP requests to external APIs.
- `console.log()`: Available for debugging (output captured in `logs` field when testing).
- Must return a value (the return value is passed back to the AI).

**Code Tool Example with HTTP Request:**

```typescript
// Available globals: args, env, fetch, console
const { customerId } = args;
const { API_KEY, API_BASE_URL } = env;

const response = await fetch(`${API_BASE_URL}/customers/${customerId}`, {
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
});

if (!response.ok) {
  return { error: `Customer lookup failed: ${response.status}` };
}

const customer = await response.json();
return {
  name: customer.name,
  email: customer.email,
  plan: customer.subscription.plan,
  status: customer.status,
};
```

---

### Tool Messages Configuration

Configure custom messages that the assistant speaks during different stages of tool execution.

| Message Type | When Triggered | Description |
|--------------|----------------|-------------|
| `request-start` | Tool call begins | Spoken when the tool starts executing. Use to acknowledge the user's request. |
| `request-complete` | Tool call finishes successfully | Spoken after the tool returns a result. |
| `request-failed` | Tool call fails | Spoken when the tool encounters an error. |
| `request-response-delayed` | Tool response takes too long | Spoken when the tool takes longer than expected. Keeps the user engaged. |

**Example Messages Configuration:**

```json
{
  "messages": [
    {
      "type": "request-start",
      "content": "Let me look that up for you."
    },
    {
      "type": "request-complete",
      "content": "I found the information."
    },
    {
      "type": "request-failed",
      "content": "I'm sorry, I wasn't able to complete that request right now. Can I help you with something else?"
    },
    {
      "type": "request-response-delayed",
      "content": "This is taking a moment longer than expected. Please hold on."
    }
  ]
}
```

---

## Adding Tools to Assistants

After creating tools, attach them to assistants using the `toolIds` array in the assistant configuration.

### Using toolIds (Recommended for Reusable Tools)

```json
{
  "name": "Customer Support Assistant",
  "model": {
    "provider": "openai",
    "model": "gpt-4o"
  },
  "toolIds": [
    "tool_abc123",
    "tool_def456",
    "tool_ghi789"
  ]
}
```

### Using Inline Tools (For One-Off Configurations)

```json
{
  "name": "Weather Assistant",
  "model": {
    "provider": "openai",
    "model": "gpt-4o"
  },
  "tools": [
    {
      "type": "function",
      "name": "get_weather",
      "description": "Get weather for a location",
      "function": {
        "name": "get_weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": { "type": "string" }
          },
          "required": ["location"]
        }
      },
      "server": {
        "url": "https://your-server.com/api/weather"
      }
    }
  ]
}
```

### Attaching Tools via API

```bash
# Add tools to an existing assistant
curl -X PATCH https://api.vapi.ai/assistant/asst_abc123 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "toolIds": ["tool_abc123", "tool_def456"]
  }'
```

```typescript
// TypeScript SDK
const assistant = await vapi.assistants.update("asst_abc123", {
  toolIds: ["tool_abc123", "tool_def456"],
});
```

```python
# Python
response = requests.patch(
    f"https://api.vapi.ai/assistant/asst_abc123",
    json={"toolIds": ["tool_abc123", "tool_def456"]},
    headers={"Authorization": f"Bearer {os.environ['VAPI_API_KEY']}"},
)
```

---

## Security Best Practices

### 1. Use Environment Variables for Secrets

Never hardcode API keys, tokens, or credentials in your tool code. Always use `environmentVariables`.

```json
{
  "type": "code",
  "code": "const { API_KEY } = env;\n// Use API_KEY instead of hardcoding",
  "environmentVariables": [
    { "name": "API_KEY", "value": "sk-your-secret-key" }
  ]
}
```

### 2. Use Webhook Secrets for Function Tools

Sign and verify webhook payloads to ensure requests genuinely come from Vapi.

```json
{
  "server": {
    "url": "https://your-server.com/api/webhook",
    "secret": "your-strong-webhook-secret"
  }
}
```

Your server should verify the `x-vapi-signature` header on incoming requests.

### 3. Validate Input Parameters

Always validate parameters in your code tools before using them.

```typescript
const { customerId } = args;
if (!customerId || typeof customerId !== "string") {
  return { error: "Valid customer ID is required" };
}
```

### 4. Set Appropriate Timeouts

Configure reasonable timeouts to prevent hanging requests.

```json
{
  "server": {
    "url": "https://your-server.com/api/endpoint",
    "timeoutSeconds": 10
  }
}
```

### 5. Use HTTPS Endpoints Only

Always use HTTPS URLs for function tool server endpoints. Vapi will reject HTTP URLs.

### 6. Limit Code Tool Scope

Keep code tools focused on a single task. Avoid overly complex tools that try to do too many things. This makes them easier to debug, test, and maintain.

### 7. Test Before Deploying

Always use the [Test Code Tool Execution](#6-test-code-tool-execution) endpoint to validate code tools before attaching them to production assistants. Test with various inputs including edge cases and invalid data.

```bash
# Test with valid input
curl -X POST https://api.vapi.ai/tool/code/test \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "type": "code", "name": "test", "description": "test", "code": "return { ok: true };", "parameters": { "type": "object", "properties": {} } }'

# Verify success === true before deploying
```

### 8. Handle Errors Gracefully

Return user-friendly error messages that the AI can relay to the caller.

```typescript
try {
  const response = await fetch(`${env.API_URL}/data`);
  if (!response.ok) {
    return { error: "Unable to retrieve data at this time" };
  }
  return await response.json();
} catch (e) {
  return { error: "Service temporarily unavailable" };
}
```
