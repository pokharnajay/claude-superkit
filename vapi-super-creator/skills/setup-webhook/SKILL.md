---
name: setup-webhook
description: Configure Vapi server URLs and webhooks to receive real-time call events, transcripts, tool calls, and end-of-call reports. Use when setting up webhook endpoints, building tool servers, or integrating Vapi events into your application.
---

# Setup Webhook

Configure Vapi server URLs (webhooks) to receive real-time call events, handle tool calls, and process end-of-call reports. Server URLs are **bidirectional** -- your server receives events from Vapi and can respond with data that influences call behavior.

## Overview

When Vapi processes a call, it sends HTTP POST requests to your server URL at key moments: when a tool is called, when a transcript updates, when a call ends, etc. For some events your server's response body is fed back into the call, making webhooks a two-way integration point rather than a passive listener.

## Where to Set Server URLs

Server URLs can be configured at four levels. Vapi resolves them in priority order (highest to lowest):

| Priority | Level | How to Set |
|----------|-------|------------|
| 1 (highest) | **Tool server URL** | Set `server.url` on an individual tool definition. |
| 2 | **Assistant server URL** | Set `server.url` on the assistant. |
| 3 | **Phone Number server URL** | Set `server.url` on the phone number. |
| 4 (lowest) | **Organization server URL** | Set in the Vapi Dashboard under organization settings. |

### On an Assistant (API)

```bash
curl -X PATCH https://api.vapi.ai/assistant/{assistant-id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "server": {
      "url": "https://your-server.com/webhook/vapi",
      "timeoutSeconds": 20,
      "headers": {
        "X-Custom-Header": "value"
      }
    },
    "serverMessages": [
      "end-of-call-report",
      "tool-calls",
      "transfer-destination-request",
      "conversation-update"
    ]
  }'
```

### On a Phone Number (API)

```bash
curl -X PATCH https://api.vapi.ai/phone-number/{phone-number-id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "serverUrl": "https://your-server.com/webhook/vapi",
    "serverUrlSecret": "your-hmac-secret"
  }'
```

### Organization Level

Set via the Vapi Dashboard under **Organization Settings > Server URL**. This acts as the fallback for all calls that do not have a more specific server URL configured.

## Event Types

Vapi sends the following event types to your server URL. Configure which ones you receive using the `serverMessages` array on the assistant.

| Event | Description | Expects Response? |
|-------|-------------|-------------------|
| `assistant-request` | Sent at call start; your server returns the assistant config dynamically. | **Yes** -- return assistant JSON. |
| `tool-calls` | One or more tools were invoked by the LLM; your server executes them. | **Yes** -- return tool results. |
| `transfer-destination-request` | Assistant requests a transfer; your server returns the destination. | **Yes** -- return transfer destination. |
| `end-of-call-report` | Call has ended; contains full transcript, summary, cost, duration. | No |
| `status-update` | Call status changed (e.g., ringing, in-progress, ended). | No |
| `conversation-update` | New message added to the conversation (real-time transcript). | No |
| `transcript` | Partial or final transcript segment from the transcriber. | No |

## Webhook Server Examples

### Express.js (Node.js)

```javascript
const express = require("express");
const crypto = require("crypto");
const app = express();

app.use(express.json());

const VAPI_SECRET = process.env.VAPI_WEBHOOK_SECRET;

// Optional: verify HMAC signature
function verifySignature(req) {
  if (!VAPI_SECRET) return true;
  const signature = req.headers["x-vapi-signature"];
  if (!signature) return false;
  const expected = crypto
    .createHmac("sha256", VAPI_SECRET)
    .update(JSON.stringify(req.body))
    .digest("hex");
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}

app.post("/webhook/vapi", (req, res) => {
  if (!verifySignature(req)) {
    return res.status(401).json({ error: "Invalid signature" });
  }

  const { message } = req.body;

  switch (message.type) {
    case "assistant-request":
      // Dynamically return assistant config
      return res.json({
        assistant: {
          name: "Dynamic Assistant",
          firstMessage: "Hello! How can I help?",
          model: {
            provider: "openai",
            model: "gpt-4.1",
            messages: [
              { role: "system", content: "You are a helpful assistant." },
            ],
          },
          voice: { provider: "vapi", voiceId: "Lily" },
        },
      });

    case "tool-calls":
      // Execute tool calls and return results
      const toolResults = message.toolCallList.map((toolCall) => {
        // Implement your tool logic here
        return {
          toolCallId: toolCall.id,
          result: JSON.stringify({ success: true, data: "Tool result here" }),
        };
      });
      return res.json({ results: toolResults });

    case "end-of-call-report":
      // Process the end-of-call report
      console.log("Call ended:", {
        callId: message.call?.id,
        duration: message.durationSeconds,
        cost: message.cost,
        summary: message.summary,
        transcript: message.transcript,
      });
      return res.json({});

    case "status-update":
      console.log("Call status:", message.status);
      return res.json({});

    case "conversation-update":
      // Real-time transcript updates
      console.log("Conversation update:", message.messagesOpenAIFormatted);
      return res.json({});

    case "transfer-destination-request":
      // Return transfer destination dynamically
      return res.json({
        destination: {
          type: "number",
          number: "+11234567890",
          message: "Transferring you now.",
        },
      });

    default:
      console.log("Unhandled event type:", message.type);
      return res.json({});
  }
});

app.listen(3000, () => console.log("Vapi webhook server running on port 3000"));
```

### Python (Flask)

```python
import hashlib
import hmac
import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

VAPI_SECRET = os.environ.get("VAPI_WEBHOOK_SECRET", "")


def verify_signature(req):
    if not VAPI_SECRET:
        return True
    signature = req.headers.get("x-vapi-signature", "")
    expected = hmac.new(
        VAPI_SECRET.encode(),
        json.dumps(req.json, separators=(",", ":")).encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


@app.route("/webhook/vapi", methods=["POST"])
def webhook():
    if not verify_signature(request):
        return jsonify({"error": "Invalid signature"}), 401

    message = request.json.get("message", {})
    msg_type = message.get("type")

    if msg_type == "assistant-request":
        return jsonify({
            "assistant": {
                "name": "Dynamic Assistant",
                "firstMessage": "Hello! How can I help?",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4.1",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."}
                    ],
                },
                "voice": {"provider": "vapi", "voiceId": "Lily"},
            }
        })

    elif msg_type == "tool-calls":
        tool_results = []
        for tool_call in message.get("toolCallList", []):
            # Implement your tool logic here
            tool_results.append({
                "toolCallId": tool_call["id"],
                "result": json.dumps({"success": True, "data": "Tool result here"}),
            })
        return jsonify({"results": tool_results})

    elif msg_type == "end-of-call-report":
        call = message.get("call", {})
        print(f"Call ended: id={call.get('id')}, "
              f"duration={message.get('durationSeconds')}s, "
              f"cost=${message.get('cost')}")
        return jsonify({})

    elif msg_type == "status-update":
        print(f"Call status: {message.get('status')}")
        return jsonify({})

    elif msg_type == "conversation-update":
        print(f"Conversation update: {message.get('messagesOpenAIFormatted')}")
        return jsonify({})

    elif msg_type == "transfer-destination-request":
        return jsonify({
            "destination": {
                "type": "number",
                "number": "+11234567890",
                "message": "Transferring you now.",
            }
        })

    else:
        print(f"Unhandled event type: {msg_type}")
        return jsonify({})


if __name__ == "__main__":
    app.run(port=3000, debug=True)
```

## Webhook Authentication

Vapi signs webhook payloads with **HMAC-SHA256** using a secret you configure. The signature is sent in the `x-vapi-signature` HTTP header.

### Setting the Secret

Set `serverUrlSecret` on the assistant, phone number, or organization. Vapi will include the HMAC signature on every webhook request.

### Verifying the Signature (Node.js)

```javascript
const crypto = require("crypto");

function verifyWebhook(payload, signature, secret) {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(JSON.stringify(payload))
    .digest("hex");
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}

// Usage in middleware
app.use("/webhook/vapi", (req, res, next) => {
  const signature = req.headers["x-vapi-signature"];
  if (!verifyWebhook(req.body, signature, process.env.VAPI_WEBHOOK_SECRET)) {
    return res.status(401).json({ error: "Invalid signature" });
  }
  next();
});
```

### Verifying the Signature (Python)

```python
import hashlib
import hmac
import json

def verify_webhook(payload: dict, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        json.dumps(payload, separators=(",", ":")).encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

## Local Development

During development you need to expose your local server to the internet so Vapi can reach it.

### Using ngrok

```bash
# Start ngrok tunnel
ngrok http 3000

# Copy the https://xxxx.ngrok.io URL and set it as your server URL
```

## End-of-Call Report Fields

The `end-of-call-report` event contains detailed information about the completed call:

| Field | Type | Description |
|-------|------|-------------|
| `call` | object | Full call object with ID, type, status, timestamps. |
| `transcript` | string | Full conversation transcript as plain text. |
| `messages` | array | Structured message array (role + content). |
| `messagesOpenAIFormatted` | array | Messages in OpenAI chat format. |
| `summary` | string | LLM-generated summary of the call. |
| `durationSeconds` | number | Total call duration in seconds. |
| `cost` | number | Total cost of the call in USD. |
| `costBreakdown` | object | Breakdown of costs by component (STT, LLM, TTS, transport, etc.). |
| `recordingUrl` | string | URL to the call recording (if recording is enabled). |
| `stereoRecordingUrl` | string | URL to the stereo recording (separate channels for agent and caller). |
| `analysis` | object | Structured analysis results if analysis plan is configured. |
| `artifact` | object | Contains messages, transcript, and recording URLs. |
| `startedAt` | string | ISO 8601 timestamp when the call started. |
| `endedAt` | string | ISO 8601 timestamp when the call ended. |
| `endedReason` | string | Why the call ended (e.g., "assistant-ended-call", "customer-hung-up"). |

## Server Configuration Reference

Full server configuration object used on assistants:

```json
{
  "server": {
    "url": "https://your-server.com/webhook/vapi",
    "timeoutSeconds": 20,
    "headers": {
      "X-Custom-Header": "value",
      "Authorization": "Bearer your-internal-token"
    },
    "secret": "your-hmac-secret"
  },
  "serverMessages": [
    "end-of-call-report",
    "tool-calls",
    "transfer-destination-request",
    "conversation-update",
    "status-update",
    "transcript"
  ]
}
```

- `server.url` -- the HTTPS endpoint Vapi sends events to.
- `server.timeoutSeconds` -- how long Vapi waits for your server to respond before timing out (default 20s).
- `server.headers` -- custom headers included on every request (useful for internal auth).
- `server.secret` -- HMAC secret for signature verification.
- `serverMessages` -- array of event types you want to receive. Only listed types are sent.

## References

- [API Reference](references/api-reference.md) — Complete webhook docs: Server Messages (9 types), Client Messages, authentication, and best practices
- [Server URL Events](references/webhook-events.md) — All event types with payload schemas

## Related Skills

- **create-assistant** -- set the server URL when creating an assistant.
- **create-tool** -- tools of type `function` trigger `tool-calls` events to your webhook.
- **create-call** -- initiate calls that generate webhook events.
- **create-squad** -- squad calls send events to the same webhook infrastructure.
- **create-phone-number** -- set a phone-number-level server URL as a fallback.

## Red Flags — Common Mistakes

| Temptation | Why It Fails |
|------------|-------------|
| "HTTP is fine for testing" | Vapi requires HTTPS. Use ngrok for local dev. |
| "I'll handle all events in one if/else" | Missing event types = silent failures. Handle each `message.type` explicitly. |
| "I don't need the secret for verification" | Without HMAC verification, anyone can send fake events to your endpoint. |
| "20s timeout is enough" | Long API calls (CRM lookups, DB queries) can exceed it. Set `timeoutSeconds` appropriately. |
| "I'll just return a string" | Vapi expects `{ results: [...] }` format. Wrong format = tool failure mid-call. |

## Required Sub-Skills

- **REQUIRED:** `vapi-voice-ai:setup-api-key` — API key needed to configure server URLs on assistants
- **RECOMMENDED:** `vapi-voice-ai:create-tool` — Tools are the primary reason you need webhooks
- **RECOMMENDED:** `vapi-voice-ai:create-call` — Test webhook events with a real call
