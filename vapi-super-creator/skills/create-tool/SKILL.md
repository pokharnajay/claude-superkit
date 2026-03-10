---
name: create-tool
description: Create custom tools for Vapi voice assistants including function tools, API request tools, transfer call tools, end call tools, DTMF, voicemail, and integrations with Google Calendar, Sheets, Slack, and more. Use when adding capabilities to voice agents, building tool servers, or integrating external APIs.
---

# Create Tool Skill

This skill covers creating, configuring, and managing tools for Vapi voice assistants. Tools let assistants take actions during calls — check availability, book appointments, transfer calls, look up data, send notifications, and more.

> **See also:** `create-assistant` (attaching tools to assistants), `setup-webhook` (server URL configuration), `create-call` (testing tools in calls)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- For custom tools: a server endpoint to handle tool calls (or use ngrok for local testing)

---

## Quick Start

### Create a Tool via cURL

```bash
curl -X POST https://api.vapi.ai/tool \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "type": "function",
    "function": {
      "name": "check_appointment",
      "description": "Check if a time slot is available for a service visit",
      "parameters": {
        "type": "object",
        "properties": {
          "date": { "type": "string", "description": "Date in YYYY-MM-DD format" },
          "time": { "type": "string", "description": "Time in HH:MM format" }
        },
        "required": ["date", "time"]
      }
    },
    "server": {
      "url": "https://your-api.com/check-appointment"
    },
    "messages": [
      { "type": "request-start", "content": "Let me check that for you..." },
      { "type": "request-complete", "content": "I found the information." },
      { "type": "request-failed", "content": "I'\''m having trouble checking that right now." }
    ]
  }'
```

### Create a Tool via TypeScript Server SDK

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const tool = await vapi.tools.create({
  type: "function",
  function: {
    name: "get_weather",
    description: "Get current weather for a location",
    parameters: {
      type: "object",
      properties: {
        location: { type: "string", description: "City name" }
      },
      required: ["location"]
    }
  },
  server: { url: "https://your-server.com/api/tools" }
});
```

---

## Tool Types

### endCall Tool (MANDATORY)

**Every assistant MUST include the `endCall` tool.** This is a built-in Vapi tool that allows the assistant to programmatically end the call when the conversation is complete. Without it, the assistant cannot hang up and calls will run until `maxDurationSeconds` or the caller hangs up.

Always add this to the model's `tools` array:
```json
{
  "model": {
    "tools": [
      {
        "type": "endCall"
      }
    ]
  }
}
```

The system prompt must instruct the assistant to trigger this tool when the caller says goodbye or the conversation is complete (this is already covered in the [Critical Rules] section of every prompt).

### Custom Function Tools (webhook-based)

Custom tools let the assistant call your server to perform actions (check availability, book appointments, look up data, etc.).

**Creating via Dashboard (Recommended):**
1. Open [Vapi Dashboard](https://dashboard.vapi.ai) -> click **Tools** in sidebar -> **Create Tool**
2. Configure:
   - **Tool Type:** Select "Function"
   - **Tool Name:** Descriptive name (e.g., "Appointment Checker")
   - **Function Name:** The identifier (e.g., `check_appointment`)
   - **Description:** What the tool does (the LLM uses this to decide when to call it)
   - **Parameters:** Define input parameters with types, descriptions, and required fields
   - **Server URL:** Your endpoint that handles the tool call
3. Configure **Messages** (what the assistant says during tool execution):
   - **Request Start:** "Let me check that for you..."
   - **Request Complete:** "I found the information."
   - **Request Failed:** "I'm having trouble checking that right now."
   - **Request Delayed:** "There's a slight delay, one moment..."
4. Advanced settings: async mode, timeout, error handling

**Creating via API:** See the Quick Start section above for the full cURL example.

### API Request Tool (direct HTTP calls)

For simpler integrations that don't need a custom server:
```json
{
  "type": "apiRequest",
  "method": "POST",
  "url": "https://api.example.com/endpoint",
  "name": "fetch_customer_data",
  "description": "Fetches customer information by phone number",
  "body": {
    "type": "object",
    "properties": {
      "phone": { "type": "string" }
    }
  }
}
```

### Transfer Call Tool

Transfer the caller to another phone number, SIP endpoint, or assistant.

**Transfer to a phone number:**
```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+1234567890",
      "message": "Transferring you to our billing department now.",
      "description": "Transfer to billing department when customer has billing questions"
    }
  ],
  "function": {
    "name": "transfer_to_billing",
    "description": "Transfer the caller to the billing department"
  }
}
```

**Transfer via SIP:**
```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "sip",
      "sipUri": "sip:billing@company.com",
      "description": "Transfer to billing via SIP"
    }
  ]
}
```

### DTMF Tool

Press phone keypad digits to navigate IVR menus or enter codes:
```json
{
  "type": "dtmf",
  "function": {
    "name": "press_digits",
    "description": "Press phone keypad digits to navigate phone menus",
    "parameters": {
      "type": "object",
      "properties": {
        "digits": {
          "type": "string",
          "description": "Digits to press (0-9, *, #)"
        }
      },
      "required": ["digits"]
    }
  }
}
```

### Voicemail Tool

Leave a voicemail message when the call reaches voicemail:
```json
{
  "type": "voicemail",
  "function": {
    "name": "leave_voicemail",
    "description": "Leave a voicemail message"
  }
}
```

### Google Calendar Tool

Schedule meetings and events on Google Calendar:
```json
{
  "type": "google.calendar.event.create",
  "function": {
    "name": "create_calendar_event",
    "description": "Schedule a meeting on Google Calendar"
  }
}
```

### Google Sheets Tool

Log call data or append rows to a Google Sheet:
```json
{
  "type": "google.sheets.row.append",
  "function": {
    "name": "log_to_sheet",
    "description": "Log call data to a Google Sheet"
  }
}
```

### Slack Tool

Send notifications or messages to Slack channels:
```json
{
  "type": "slack.message.send",
  "function": {
    "name": "notify_slack",
    "description": "Send a notification to Slack"
  }
}
```

### MCP Tool

Connect to an MCP (Model Context Protocol) server:
```json
{
  "type": "mcp",
  "server": {
    "url": "https://your-mcp-server.com"
  }
}
```

### Integration Tools

- `make` -- Trigger Make.com scenarios
- `ghl` -- GoHighLevel integrations

---

## Attaching Tools to Assistants

### Option A -- Reference pre-created tools by ID (recommended for reuse across assistants)

```json
{
  "model": {
    "toolIds": ["your-tool-id-here"]
  }
}
```

### Option B -- Inline tool definitions (for assistant-specific tools)

```json
{
  "model": {
    "tools": [
      {
        "type": "endCall"
      },
      {
        "type": "function",
        "function": {
          "name": "check_appointment",
          "description": "Check if a time slot is available",
          "parameters": {
            "type": "object",
            "properties": {
              "date": { "type": "string", "description": "Date in YYYY-MM-DD format" },
              "time": { "type": "string", "description": "Time in HH:MM format" }
            },
            "required": ["date", "time"]
          }
        },
        "server": {
          "url": "https://your-api.com/check-appointment"
        },
        "messages": [
          { "type": "request-start", "content": "Let me check that for you..." },
          { "type": "request-complete", "content": "I found the information." },
          { "type": "request-failed", "content": "I'm having trouble checking that right now." }
        ]
      }
    ]
  }
}
```

---

## Tool Server Implementation

When the assistant calls a custom function tool, Vapi POSTs to your server URL. Your server processes the request and returns a result the assistant can use.

> **Full reference:** See `references/tool-server.md` for complete request/response payloads, Python Flask example, and serverless deployment.

### Server Request Format

```json
{
  "message": {
    "type": "tool-calls",
    "toolCallList": [
      {
        "id": "toolu_01DTPAzUm5Gk3zxrpJ969oMF",
        "name": "check_appointment",
        "arguments": {
          "date": "2026-03-15",
          "time": "10:00"
        }
      }
    ]
  }
}
```

### Server Response Format

```json
{
  "results": [
    {
      "toolCallId": "toolu_01DTPAzUm5Gk3zxrpJ969oMF",
      "result": "The 10 AM slot on March 15th is available."
    }
  ]
}
```

- `toolCallId` -- Must match the `id` from the request
- `result` -- String that the assistant reads or uses to respond to the caller

### Express.js Server Example

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/tools", async (req, res) => {
  const { message } = req.body;
  const results = [];

  for (const toolCall of message.toolCallList) {
    try {
      const result = await handleTool(toolCall.name, toolCall.arguments);
      results.push({ toolCallId: toolCall.id, result });
    } catch (error) {
      results.push({
        toolCallId: toolCall.id,
        result: `Error: ${error.message}`,
      });
    }
  }

  res.json({ results });
});

async function handleTool(name: string, args: Record<string, any>): Promise<string> {
  switch (name) {
    case "get_weather":
      return `Weather in ${args.location}: 65°F, sunny`;

    case "book_appointment":
      return `Appointment booked for ${args.date} at ${args.time}`;

    case "lookup_order":
      return `Order ${args.orderNumber}: Shipped, arriving tomorrow`;

    default:
      return `Unknown tool: ${name}`;
  }
}

app.listen(3000, () => console.log("Tool server on port 3000"));
```

### Testing Tools Locally

```bash
# Start a tunnel (e.g., with ngrok) to expose your local server
ngrok http 3000

# Copy the https://xxxx.ngrok.io URL and set it as your tool's server URL
```

**Important:** Configure your tool's server URL to use the tunnel's public URL for testing.

---

## Async Tools

For long-running operations (sending emails, generating reports, etc.), mark tools as async so the assistant keeps talking while the tool runs in the background:

```json
{
  "type": "function",
  "async": true,
  "function": {
    "name": "send_email",
    "description": "Send a confirmation email (runs in background)"
  },
  "server": {
    "url": "https://your-server.com/api/tools"
  }
}
```

When `async` is `true`, the assistant does not wait for the tool result before continuing the conversation. Use this for actions where the caller does not need to hear the result immediately.

---

## Tool Messages

Tool messages control what the assistant says while a tool is executing. They provide a natural conversational experience during potentially slow operations.

```json
{
  "messages": [
    {
      "type": "request-start",
      "content": "One moment while I look that up..."
    },
    {
      "type": "request-complete",
      "content": "Got it!"
    },
    {
      "type": "request-failed",
      "content": "Sorry, I couldn't complete that action."
    },
    {
      "type": "request-response-delayed",
      "content": "This is taking a bit longer than usual, please hold.",
      "timingMilliseconds": 5000
    }
  ]
}
```

- **request-start** -- Spoken immediately when the tool call begins
- **request-complete** -- Spoken when the tool returns successfully
- **request-failed** -- Spoken when the tool call fails or times out
- **request-response-delayed** -- Spoken if the tool has not responded after `timingMilliseconds`

---

## Managing Tools via API

```bash
# List all tools
curl https://api.vapi.ai/tool \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Get a specific tool
curl https://api.vapi.ai/tool/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Update a tool
curl -X PATCH https://api.vapi.ai/tool/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{ "function": { "description": "Updated description" } }'

# Delete a tool
curl -X DELETE https://api.vapi.ai/tool/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

---

## Error Handling Best Practices

1. Always return a `results` array, even for errors
2. Return user-friendly error messages (the assistant reads them to the caller)
3. Set reasonable timeouts (Vapi has a default tool timeout)
4. For long operations, use async tools so the assistant keeps talking
5. Include `request-failed` messages so the assistant can gracefully handle failures

## References

- [API Reference](references/api-reference.md) — REST API docs for Tools (6 endpoints) with examples
- [Built-in Tools](references/builtin-tools.md) — endCall, transferCall (blind/warm/assistant-based), SMS, DTMF, apiRequest
- [Code Tools](references/code-tools.md) — Serverless TypeScript execution on Vapi infrastructure
- [Custom Function Tools](references/custom-tools.md) — Webhook format, troubleshooting, sync vs async
- [Integration Tools](references/integrations.md) — Google Calendar, Google Sheets, Slack, MCP, GoHighLevel
- [Voicemail Tool](references/voicemail.md) — Tool vs automatic detection, provider comparison
- [Tool Encryption](references/encryption.md) — RSA-OAEP-256 argument encryption with decryption code
- [Client-Side Tools](references/client-side-tools.md) — Web SDK browser-only tools
- [Tool Config](references/tool-config.md) — Rejection plans, conditional messages
- [Tool Server](references/tool-server.md) — Express.js, Flask, Vercel server examples

## Red Flags — Common Mistakes

| Temptation | Why It Fails |
|------------|-------------|
| "I'll hardcode the server URL later" | Tools without server URLs silently fail. Set `server.url` at creation time. |
| "Parameters don't need descriptions" | The AI reads parameter descriptions to know WHAT to ask the caller. No description = wrong data collected. |
| "I'll skip request-start/failed messages" | Without them, the caller hears dead silence while the tool runs. Always add filler messages. |
| "One generic tool can handle everything" | Overloaded tools confuse the AI. One tool = one action. |
| "I don't need to test the webhook handler" | If your handler returns the wrong format, the tool silently fails mid-call. Test with curl first. |

## Required Sub-Skills

- **REQUIRED:** `vapi-voice-ai:setup-webhook` — When creating function tools that need a server endpoint
- **REQUIRED:** `vapi-voice-ai:create-assistant` — Tools must be attached to an assistant to work
- **RECOMMENDED:** `vapi-voice-ai:create-call` — Test tools by making a real call
