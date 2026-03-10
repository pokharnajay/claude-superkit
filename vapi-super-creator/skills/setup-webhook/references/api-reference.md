# Webhook API Reference

> **Base URL:** Your own server URL (Vapi sends requests TO you)
> **Authentication:** HMAC-SHA256 signature via `x-vapi-signature` header

---

## Table of Contents

- [Overview](#overview)
- [1. Server Message (Webhook)](#1-server-message-webhook)
  - [assistant-request](#assistant-request)
  - [tool-calls](#tool-calls)
  - [status-update](#status-update)
  - [end-of-call-report](#end-of-call-report)
  - [transcript](#transcript)
  - [speech-update](#speech-update)
  - [conversation-update](#conversation-update)
  - [transfer-destination-request](#transfer-destination-request)
  - [knowledge-base-request](#knowledge-base-request)
- [2. Client Message](#2-client-message)
- [Webhook Authentication](#webhook-authentication)
- [Server URL Priority](#server-url-priority)
- [Best Practices](#best-practices)

---

## Overview

Vapi uses webhooks (called "Server Messages") to communicate with your backend during voice AI calls. When events occur -- an inbound call arrives, a tool is invoked, a transcript is generated, or a call ends -- Vapi sends an HTTP POST request to your configured server URL.

There are two categories of messages:

1. **Server Messages** -- Sent from Vapi to YOUR server via HTTP POST. These are the webhooks you implement.
2. **Client Messages** -- Sent from Vapi to client-side SDKs (Web, iOS, Android) via WebSocket. No server needed.

---

## 1. Server Message (Webhook)

Vapi sends server messages as HTTP POST requests to your configured server URL during call lifecycle events. Some messages require a response (synchronous); others are fire-and-forget (asynchronous).

### HTTP Request (All Server Messages)

Vapi sends every server message as:

```
POST <your-server-url>
```

### Headers (Sent by Vapi)

| Header              | Value                                       | Description                                                |
|---------------------|---------------------------------------------|------------------------------------------------------------|
| `Content-Type`      | `application/json`                          | Always JSON.                                               |
| `x-vapi-signature`  | `string`                                    | HMAC-SHA256 signature for verifying request authenticity.   |

### Common Request Body Structure

Every server message has this top-level structure:

```json
{
  "message": {
    "type": "string - The message type (e.g., 'assistant-request', 'tool-calls', 'status-update', etc.)",
    "call": "object - The full Call object for context",
    "timestamp": "string - ISO 8601 timestamp of the event",
    "...": "Additional fields specific to the message type"
  }
}
```

---

### assistant-request

Sent when an inbound call arrives on a phone number that has **no assistant or squad assigned**. Your server must respond with an assistant configuration so Vapi knows how to handle the call.

**Direction:** Vapi --> Your Server
**Response Required:** YES (within 7.5 seconds)

#### When It Fires

- An inbound call arrives on a phone number.
- The phone number has no `assistantId` and no `squadId` set.
- A server URL is configured (on the phone number, or at the org level).

#### Request Body

```json
{
  "message": {
    "type": "assistant-request",
    "call": {
      "id": "call_abc123",
      "orgId": "org_xyz789",
      "type": "inboundPhoneCall",
      "phoneNumberId": "phn_abc123",
      "phoneCallProvider": "twilio",
      "phoneCallProviderId": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "customer": {
        "number": "+14085559876"
      },
      "status": "ringing",
      "createdAt": "2025-01-15T10:30:00.000Z",
      "updatedAt": "2025-01-15T10:30:00.000Z"
    },
    "phoneNumber": {
      "id": "phn_abc123",
      "number": "+14155551234",
      "provider": "twilio"
    },
    "customer": {
      "number": "+14085559876"
    },
    "timestamp": "2025-01-15T10:30:00.000Z"
  }
}
```

#### Response Options

You MUST respond with one of the following JSON bodies within **7.5 seconds**. If you do not respond in time, the call is dropped.

**Option 1: Inline assistant configuration**

```json
{
  "assistant": {
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful receptionist for Acme Corp..."
        }
      ]
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "paula"
    },
    "firstMessage": "Hello! Thank you for calling Acme Corp. How can I help you today?"
  }
}
```

**Option 2: Reference an existing assistant by ID**

```json
{
  "assistantId": "asst_abc123def456"
}
```

**Option 3: Reject the call with an error**

```json
{
  "error": "We are currently closed. Please call back during business hours."
}
```

#### cURL Example (Simulating the Webhook)

To test your handler, you can simulate the webhook locally:

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "assistant-request",
      "call": {
        "id": "call_test123",
        "type": "inboundPhoneCall",
        "customer": { "number": "+14085559876" }
      },
      "customer": { "number": "+14085559876" },
      "timestamp": "2025-01-15T10:30:00.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "assistant-request") {
    const callerNumber = message.customer?.number;

    // Dynamic routing based on caller
    if (callerNumber === "+14085559876") {
      // Known VIP -- use a specific assistant
      return res.json({ assistantId: "asst_vip_handler" });
    }

    // Default -- return inline assistant config
    return res.json({
      assistant: {
        model: {
          provider: "openai",
          model: "gpt-4o",
          messages: [
            {
              role: "system",
              content: "You are a helpful receptionist for Acme Corp.",
            },
          ],
        },
        voice: {
          provider: "11labs",
          voiceId: "paula",
        },
        firstMessage: "Hello! Thank you for calling. How can I help you?",
      },
    });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "assistant-request":
        caller_number = message.get("customer", {}).get("number")

        # Dynamic routing based on caller
        if caller_number == "+14085559876":
            return jsonify({"assistantId": "asst_vip_handler"})

        # Default -- return inline assistant config
        return jsonify({
            "assistant": {
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful receptionist for Acme Corp.",
                        }
                    ],
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "paula",
                },
                "firstMessage": "Hello! Thank you for calling. How can I help you?",
            }
        })

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/webhooks/server-message](https://docs.vapi.ai/api-reference/webhooks/server-message)
- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### tool-calls

Sent when the assistant invokes a function tool during a call. Your server must execute the function and return the result. This is how you integrate custom business logic into voice AI conversations.

**Direction:** Vapi --> Your Server
**Response Required:** YES

#### Request Body

```json
{
  "message": {
    "type": "tool-calls",
    "call": {
      "id": "call_abc123",
      "orgId": "org_xyz789",
      "type": "inboundPhoneCall",
      "status": "in-progress"
    },
    "toolWithToolCallList": [
      {
        "type": "function",
        "function": {
          "name": "lookupOrder",
          "description": "Look up an order by order ID"
        },
        "toolCall": {
          "id": "tc_abc123",
          "type": "function",
          "function": {
            "name": "lookupOrder",
            "arguments": "{\"orderId\": \"ORD-12345\"}"
          }
        }
      }
    ],
    "timestamp": "2025-01-15T10:31:00.000Z"
  }
}
```

**Key fields:**
- `toolWithToolCallList` -- Array of tool/toolCall pairs. Typically one item, but can be multiple for parallel tool calls.
- `toolCall.function.name` -- The function name the assistant wants to call.
- `toolCall.function.arguments` -- JSON string of the function arguments.
- `toolCall.id` -- Unique ID for this specific tool call invocation. You must return this in the response.

#### Response

```json
{
  "results": [
    {
      "name": "lookupOrder",
      "toolCallId": "tc_abc123",
      "result": "Order ORD-12345: 2 widgets, shipped on Jan 10, expected delivery Jan 15. Tracking: 1Z999AA10123456784."
    }
  ]
}
```

**Response fields:**
- `results` -- Array matching the tool calls in the request.
- `results[].name` -- Must match the function name from the request.
- `results[].toolCallId` -- Must match the `toolCall.id` from the request.
- `results[].result` -- String result that will be read back to the caller by the assistant.

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "tool-calls",
      "call": { "id": "call_test123" },
      "toolWithToolCallList": [
        {
          "type": "function",
          "function": { "name": "lookupOrder" },
          "toolCall": {
            "id": "tc_test123",
            "type": "function",
            "function": {
              "name": "lookupOrder",
              "arguments": "{\"orderId\": \"ORD-12345\"}"
            }
          }
        }
      ],
      "timestamp": "2025-01-15T10:31:00.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

// Simulated order database
const orders: Record<string, any> = {
  "ORD-12345": {
    items: "2 widgets",
    shippedDate: "Jan 10",
    expectedDelivery: "Jan 15",
    tracking: "1Z999AA10123456784",
  },
};

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "tool-calls") {
    const results = message.toolWithToolCallList.map(
      (toolWithCall: any) => {
        const functionName = toolWithCall.toolCall.function.name;
        const toolCallId = toolWithCall.toolCall.id;
        const args = JSON.parse(toolWithCall.toolCall.function.arguments);

        let result: string;

        switch (functionName) {
          case "lookupOrder": {
            const order = orders[args.orderId];
            if (order) {
              result = `Order ${args.orderId}: ${order.items}, shipped on ${order.shippedDate}, expected delivery ${order.expectedDelivery}. Tracking: ${order.tracking}.`;
            } else {
              result = `Order ${args.orderId} not found.`;
            }
            break;
          }
          case "scheduleCallback": {
            result = `Callback scheduled for ${args.dateTime} at ${args.phoneNumber}.`;
            break;
          }
          default:
            result = `Unknown function: ${functionName}`;
        }

        return { name: functionName, toolCallId, result };
      }
    );

    return res.json({ results });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated order database
ORDERS = {
    "ORD-12345": {
        "items": "2 widgets",
        "shipped_date": "Jan 10",
        "expected_delivery": "Jan 15",
        "tracking": "1Z999AA10123456784",
    }
}

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "tool-calls":
        results = []
        for tool_with_call in message.get("toolWithToolCallList", []):
            tool_call = tool_with_call["toolCall"]
            function_name = tool_call["function"]["name"]
            tool_call_id = tool_call["id"]
            args = json.loads(tool_call["function"]["arguments"])

            if function_name == "lookupOrder":
                order = ORDERS.get(args.get("orderId"))
                if order:
                    result = (
                        f"Order {args['orderId']}: {order['items']}, "
                        f"shipped on {order['shipped_date']}, "
                        f"expected delivery {order['expected_delivery']}. "
                        f"Tracking: {order['tracking']}."
                    )
                else:
                    result = f"Order {args.get('orderId')} not found."
            elif function_name == "scheduleCallback":
                result = (
                    f"Callback scheduled for {args.get('dateTime')} "
                    f"at {args.get('phoneNumber')}."
                )
            else:
                result = f"Unknown function: {function_name}"

            results.append({
                "name": function_name,
                "toolCallId": tool_call_id,
                "result": result,
            })

        return jsonify({"results": results})

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/api-reference/webhooks/server-message](https://docs.vapi.ai/api-reference/webhooks/server-message)
- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### status-update

Sent when the call status changes. Provides real-time visibility into call lifecycle transitions.

**Direction:** Vapi --> Your Server
**Response Required:** NO

#### Request Body

```json
{
  "message": {
    "type": "status-update",
    "call": {
      "id": "call_abc123",
      "orgId": "org_xyz789",
      "type": "inboundPhoneCall",
      "status": "in-progress"
    },
    "status": "in-progress",
    "messages": [],
    "timestamp": "2025-01-15T10:30:05.000Z"
  }
}
```

#### Status Values

| Status         | Description                                                               |
|----------------|---------------------------------------------------------------------------|
| `scheduled`    | Call is scheduled for a future time.                                      |
| `queued`       | Call is in the queue waiting to be processed.                             |
| `ringing`      | The phone is ringing on the recipient's end.                              |
| `in-progress`  | Call has been answered and is actively ongoing.                            |
| `forwarding`   | Call is being transferred to another destination.                         |
| `ended`        | Call has ended. See `endedReason` in the end-of-call-report for details.  |

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "status-update",
      "call": { "id": "call_test123", "status": "in-progress" },
      "status": "in-progress",
      "timestamp": "2025-01-15T10:30:05.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "status-update") {
    const callId = message.call?.id;
    const status = message.status;
    const timestamp = message.timestamp;

    console.log(`[${timestamp}] Call ${callId}: status changed to "${status}"`);

    // Example: Update your CRM or database
    // await db.calls.update(callId, { status, updatedAt: timestamp });

    // Example: Trigger alerts on specific statuses
    if (status === "ended") {
      console.log(`Call ${callId} has ended.`);
    }
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "status-update":
        call_id = message.get("call", {}).get("id")
        status = message.get("status")
        timestamp = message.get("timestamp")

        print(f"[{timestamp}] Call {call_id}: status changed to '{status}'")

        # Example: Update your CRM or database
        # db.calls.update(call_id, status=status, updated_at=timestamp)

        if status == "ended":
            print(f"Call {call_id} has ended.")

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### end-of-call-report

Sent when a call completes. Contains the full call summary including recording URL, transcript, messages, cost breakdown, and the reason the call ended. This is the most important webhook for analytics, logging, and post-call processing.

**Direction:** Vapi --> Your Server
**Response Required:** NO

#### Request Body

```json
{
  "message": {
    "type": "end-of-call-report",
    "call": {
      "id": "call_abc123",
      "orgId": "org_xyz789",
      "type": "inboundPhoneCall",
      "phoneNumberId": "phn_abc123",
      "assistantId": "asst_abc123",
      "status": "ended",
      "startedAt": "2025-01-15T10:30:00.000Z",
      "endedAt": "2025-01-15T10:33:45.000Z",
      "endedReason": "customer-ended-call",
      "createdAt": "2025-01-15T10:29:55.000Z",
      "updatedAt": "2025-01-15T10:33:45.000Z"
    },
    "endedReason": "customer-ended-call",
    "artifact": {
      "recordingUrl": "https://storage.vapi.ai/recordings/call_abc123.wav",
      "stereoRecordingUrl": "https://storage.vapi.ai/recordings/call_abc123-stereo.wav",
      "transcript": "Hello! Thank you for calling Acme Corp. How can I help you? ... (full transcript)",
      "messages": [
        {
          "role": "assistant",
          "content": "Hello! Thank you for calling Acme Corp. How can I help you?"
        },
        {
          "role": "user",
          "content": "I'd like to check the status of my order."
        },
        {
          "role": "assistant",
          "content": "I'd be happy to help! Could you please provide your order number?"
        },
        {
          "role": "user",
          "content": "It's ORD-12345."
        },
        {
          "role": "tool_call",
          "content": "{\"name\": \"lookupOrder\", \"arguments\": {\"orderId\": \"ORD-12345\"}}"
        },
        {
          "role": "tool_result",
          "content": "Order ORD-12345: 2 widgets, shipped on Jan 10..."
        },
        {
          "role": "assistant",
          "content": "Your order ORD-12345 containing 2 widgets was shipped on January 10th..."
        }
      ]
    },
    "cost": 0.15,
    "costBreakdown": {
      "stt": 0.02,
      "llm": 0.08,
      "tts": 0.03,
      "transport": 0.02
    },
    "timestamp": "2025-01-15T10:33:45.000Z"
  }
}
```

#### Key Fields

| Field                       | Type   | Description                                                     |
|-----------------------------|--------|-----------------------------------------------------------------|
| `endedReason`               | string | Why the call ended (see table below).                           |
| `artifact.recordingUrl`     | string | URL to the mono recording file (WAV).                           |
| `artifact.stereoRecordingUrl`| string | URL to the stereo recording file (WAV). Left=assistant, Right=caller. |
| `artifact.transcript`       | string | Full text transcript of the entire call.                        |
| `artifact.messages`         | array  | Structured array of all messages exchanged during the call.     |
| `cost`                      | number | Total cost of the call in USD.                                  |
| `costBreakdown.stt`         | number | Speech-to-text cost in USD.                                     |
| `costBreakdown.llm`         | number | LLM inference cost in USD.                                      |
| `costBreakdown.tts`         | number | Text-to-speech cost in USD.                                     |
| `costBreakdown.transport`   | number | Telephony transport cost in USD.                                |

#### Ended Reason Values

| Reason                        | Description                                               |
|-------------------------------|-----------------------------------------------------------|
| `customer-ended-call`         | The customer (caller) hung up.                            |
| `assistant-ended-call`        | The assistant ended the call (via endCallFunction tool).   |
| `assistant-forwarded-call`    | The assistant transferred the call.                       |
| `silence-timed-out`           | No speech detected for the configured timeout period.     |
| `customer-did-not-answer`     | Outbound call was not answered.                           |
| `voicemail`                   | Outbound call went to voicemail.                          |
| `max-duration-reached`        | Call hit the maximum allowed duration.                    |
| `pipeline-error-*`           | Various pipeline errors (STT, LLM, TTS, etc.).            |

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "end-of-call-report",
      "call": {
        "id": "call_test123",
        "status": "ended",
        "endedReason": "customer-ended-call"
      },
      "endedReason": "customer-ended-call",
      "artifact": {
        "transcript": "Hello! How can I help? ... Goodbye!",
        "messages": []
      },
      "cost": 0.15,
      "costBreakdown": { "stt": 0.02, "llm": 0.08, "tts": 0.03, "transport": 0.02 },
      "timestamp": "2025-01-15T10:33:45.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "end-of-call-report") {
    const callId = message.call?.id;
    const endedReason = message.endedReason;
    const transcript = message.artifact?.transcript;
    const recordingUrl = message.artifact?.recordingUrl;
    const messages = message.artifact?.messages || [];
    const cost = message.cost;
    const costBreakdown = message.costBreakdown;

    console.log(`Call ${callId} ended: ${endedReason}`);
    console.log(`Cost: $${cost?.toFixed(2)}`);
    if (costBreakdown) {
      console.log(`  STT: $${costBreakdown.stt?.toFixed(3)}`);
      console.log(`  LLM: $${costBreakdown.llm?.toFixed(3)}`);
      console.log(`  TTS: $${costBreakdown.tts?.toFixed(3)}`);
      console.log(`  Transport: $${costBreakdown.transport?.toFixed(3)}`);
    }
    console.log(`Transcript: ${transcript?.substring(0, 200)}...`);
    console.log(`Messages: ${messages.length} total`);
    console.log(`Recording: ${recordingUrl}`);

    // Example: Store in your database
    // await db.callReports.create({
    //   callId,
    //   endedReason,
    //   transcript,
    //   recordingUrl,
    //   messages,
    //   cost,
    //   costBreakdown,
    // });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "end-of-call-report":
        call_id = message.get("call", {}).get("id")
        ended_reason = message.get("endedReason")
        artifact = message.get("artifact", {})
        transcript = artifact.get("transcript", "")
        recording_url = artifact.get("recordingUrl")
        messages = artifact.get("messages", [])
        cost = message.get("cost", 0)
        cost_breakdown = message.get("costBreakdown", {})

        print(f"Call {call_id} ended: {ended_reason}")
        print(f"Cost: ${cost:.2f}")
        if cost_breakdown:
            print(f"  STT: ${cost_breakdown.get('stt', 0):.3f}")
            print(f"  LLM: ${cost_breakdown.get('llm', 0):.3f}")
            print(f"  TTS: ${cost_breakdown.get('tts', 0):.3f}")
            print(f"  Transport: ${cost_breakdown.get('transport', 0):.3f}")
        print(f"Transcript: {transcript[:200]}...")
        print(f"Messages: {len(messages)} total")
        print(f"Recording: {recording_url}")

        # Example: Store in your database
        # db.call_reports.create(
        #     call_id=call_id,
        #     ended_reason=ended_reason,
        #     transcript=transcript,
        #     recording_url=recording_url,
        #     messages=messages,
        #     cost=cost,
        #     cost_breakdown=cost_breakdown,
        # )

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### transcript

Sent in real-time as speech is transcribed during a call. Provides both partial (in-progress) and final (complete) transcriptions. Useful for live dashboards, real-time analytics, or logging.

**Direction:** Vapi --> Your Server
**Response Required:** NO

#### Request Body

```json
{
  "message": {
    "type": "transcript",
    "call": {
      "id": "call_abc123"
    },
    "role": "user",
    "transcriptType": "final",
    "transcript": "I'd like to check the status of my order.",
    "timestamp": "2025-01-15T10:30:15.000Z"
  }
}
```

#### Key Fields

| Field             | Type   | Values                | Description                                             |
|-------------------|--------|-----------------------|---------------------------------------------------------|
| `role`            | string | `"user"`, `"assistant"` | Who is speaking.                                      |
| `transcriptType`  | string | `"partial"`, `"final"` | `partial` = still being spoken. `final` = complete utterance. |
| `transcript`      | string |                       | The transcribed text.                                   |

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "transcript",
      "call": { "id": "call_test123" },
      "role": "user",
      "transcriptType": "final",
      "transcript": "I would like to check the status of my order.",
      "timestamp": "2025-01-15T10:30:15.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "transcript") {
    const callId = message.call?.id;
    const role = message.role;
    const type = message.transcriptType;
    const text = message.transcript;

    if (type === "final") {
      console.log(`[${callId}] ${role}: ${text}`);

      // Example: Stream to a live dashboard via WebSocket
      // wss.broadcast({ callId, role, text });
    }
    // Optionally log partial transcripts for real-time display
    // if (type === "partial") {
    //   console.log(`[${callId}] ${role} (partial): ${text}`);
    // }
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "transcript":
        call_id = message.get("call", {}).get("id")
        role = message.get("role")
        transcript_type = message.get("transcriptType")
        text = message.get("transcript")

        if transcript_type == "final":
            print(f"[{call_id}] {role}: {text}")

            # Example: Stream to a live dashboard via WebSocket
            # wss.broadcast({"callId": call_id, "role": role, "text": text})

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### speech-update

Sent when speech activity is detected or stops during a call. Useful for building real-time UI indicators (e.g., "User is speaking...") or understanding turn-taking dynamics.

**Direction:** Vapi --> Your Server
**Response Required:** NO

#### Request Body

```json
{
  "message": {
    "type": "speech-update",
    "call": {
      "id": "call_abc123"
    },
    "status": "started",
    "role": "user",
    "turnNumber": 3,
    "timestamp": "2025-01-15T10:30:12.000Z"
  }
}
```

#### Key Fields

| Field        | Type   | Values                    | Description                                          |
|--------------|--------|---------------------------|------------------------------------------------------|
| `status`     | string | `"started"`, `"stopped"`  | Whether speech started or stopped.                   |
| `role`       | string | `"user"`, `"assistant"`   | Who started/stopped speaking.                        |
| `turnNumber` | number |                           | The conversational turn number (increments each turn).|

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "speech-update",
      "call": { "id": "call_test123" },
      "status": "started",
      "role": "user",
      "turnNumber": 3,
      "timestamp": "2025-01-15T10:30:12.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "speech-update") {
    const callId = message.call?.id;
    const status = message.status;  // "started" or "stopped"
    const role = message.role;      // "user" or "assistant"
    const turn = message.turnNumber;

    console.log(`[${callId}] Speech ${status}: ${role} (turn ${turn})`);

    // Example: Update live UI indicator
    // io.emit("speech-update", { callId, status, role, turn });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "speech-update":
        call_id = message.get("call", {}).get("id")
        status = message.get("status")      # "started" or "stopped"
        role = message.get("role")          # "user" or "assistant"
        turn = message.get("turnNumber")

        print(f"[{call_id}] Speech {status}: {role} (turn {turn})")

        # Example: Update live UI indicator
        # socketio.emit("speech-update", {"callId": call_id, "status": status, "role": role, "turn": turn})

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### conversation-update

Sent when the conversation messages array is updated. Provides the full message history in both Vapi's format and OpenAI-compatible format. Useful for maintaining a synchronized copy of the conversation state.

**Direction:** Vapi --> Your Server
**Response Required:** NO

#### Request Body

```json
{
  "message": {
    "type": "conversation-update",
    "call": {
      "id": "call_abc123"
    },
    "messages": [
      {
        "role": "assistant",
        "content": "Hello! Thank you for calling Acme Corp. How can I help you?"
      },
      {
        "role": "user",
        "content": "I'd like to check the status of my order."
      }
    ],
    "messagesOpenAIFormatted": [
      {
        "role": "system",
        "content": "You are a helpful receptionist..."
      },
      {
        "role": "assistant",
        "content": "Hello! Thank you for calling Acme Corp. How can I help you?"
      },
      {
        "role": "user",
        "content": "I'd like to check the status of my order."
      }
    ],
    "timestamp": "2025-01-15T10:30:20.000Z"
  }
}
```

#### Key Fields

| Field                       | Type  | Description                                                       |
|-----------------------------|-------|-------------------------------------------------------------------|
| `messages`                  | array | Conversation messages in Vapi's native format.                    |
| `messagesOpenAIFormatted`   | array | Conversation messages in OpenAI Chat Completions format (includes system prompt). |

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "conversation-update",
      "call": { "id": "call_test123" },
      "messages": [
        { "role": "assistant", "content": "Hello!" },
        { "role": "user", "content": "Hi there." }
      ],
      "messagesOpenAIFormatted": [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "assistant", "content": "Hello!" },
        { "role": "user", "content": "Hi there." }
      ],
      "timestamp": "2025-01-15T10:30:20.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "conversation-update") {
    const callId = message.call?.id;
    const messages = message.messages || [];
    const openAIMessages = message.messagesOpenAIFormatted || [];

    console.log(`[${callId}] Conversation updated: ${messages.length} messages`);

    // Example: Sync conversation state to your database
    // await db.conversations.upsert(callId, {
    //   messages,
    //   openAIMessages,
    //   updatedAt: message.timestamp,
    // });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "conversation-update":
        call_id = message.get("call", {}).get("id")
        messages = message.get("messages", [])
        openai_messages = message.get("messagesOpenAIFormatted", [])

        print(f"[{call_id}] Conversation updated: {len(messages)} messages")

        # Example: Sync conversation state to your database
        # db.conversations.upsert(call_id, messages=messages, openai_messages=openai_messages)

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### transfer-destination-request

Sent when the assistant needs to transfer a call but requires dynamic destination routing. Your server determines where to transfer the call based on the current conversation context.

**Direction:** Vapi --> Your Server
**Response Required:** YES

#### Request Body

```json
{
  "message": {
    "type": "transfer-destination-request",
    "call": {
      "id": "call_abc123",
      "orgId": "org_xyz789",
      "type": "inboundPhoneCall"
    },
    "timestamp": "2025-01-15T10:32:00.000Z"
  }
}
```

#### Response

Return a destination configuration object:

**Transfer to a phone number:**

```json
{
  "destination": {
    "type": "number",
    "number": "+14085559876",
    "message": "I'm transferring you to our billing department now. Please hold."
  }
}
```

**Transfer to a SIP endpoint:**

```json
{
  "destination": {
    "type": "sip",
    "sipUri": "sip:billing@pbx.example.com",
    "message": "Transferring you now."
  }
}
```

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "transfer-destination-request",
      "call": { "id": "call_test123", "type": "inboundPhoneCall" },
      "timestamp": "2025-01-15T10:32:00.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

const DEPARTMENT_NUMBERS: Record<string, string> = {
  billing: "+14085551001",
  support: "+14085551002",
  sales: "+14085551003",
};

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "transfer-destination-request") {
    // Determine department from conversation context
    // In practice, you'd analyze message.call or additional context
    const department = "billing"; // Simplified for example

    const targetNumber = DEPARTMENT_NUMBERS[department] || DEPARTMENT_NUMBERS.support;

    return res.json({
      destination: {
        type: "number",
        number: targetNumber,
        message: `I'm transferring you to our ${department} department now. Please hold.`,
      },
    });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

DEPARTMENT_NUMBERS = {
    "billing": "+14085551001",
    "support": "+14085551002",
    "sales": "+14085551003",
}

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "transfer-destination-request":
        # Determine department from conversation context
        department = "billing"  # Simplified for example

        target_number = DEPARTMENT_NUMBERS.get(department, DEPARTMENT_NUMBERS["support"])

        return jsonify({
            "destination": {
                "type": "number",
                "number": target_number,
                "message": f"I'm transferring you to our {department} department now. Please hold.",
            }
        })

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

### knowledge-base-request

Sent when the assistant needs to query a custom knowledge base. Your server performs the search and returns relevant content that the assistant uses to answer the caller's question.

**Direction:** Vapi --> Your Server
**Response Required:** YES

#### Request Body

```json
{
  "message": {
    "type": "knowledge-base-request",
    "call": {
      "id": "call_abc123"
    },
    "query": "What is your return policy for electronics?",
    "messages": [
      {
        "role": "user",
        "content": "What's your return policy for electronics?"
      }
    ],
    "timestamp": "2025-01-15T10:31:30.000Z"
  }
}
```

#### Response

Return relevant content from your knowledge base:

```json
{
  "results": [
    {
      "content": "Electronics can be returned within 30 days of purchase with original receipt. Items must be in original packaging and unused condition. Opened software, games, and digital downloads are non-refundable.",
      "source": "return-policy.md",
      "score": 0.95
    },
    {
      "content": "For defective electronics, we offer a 1-year warranty with free replacement or repair. Contact our support team at 1-800-ACME for warranty claims.",
      "source": "warranty-policy.md",
      "score": 0.82
    }
  ]
}
```

#### cURL Example (Simulating the Webhook)

```bash
curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "type": "knowledge-base-request",
      "call": { "id": "call_test123" },
      "query": "What is your return policy for electronics?",
      "messages": [
        { "role": "user", "content": "What is your return policy for electronics?" }
      ],
      "timestamp": "2025-01-15T10:31:30.000Z"
    }
  }'
```

#### TypeScript SDK Example (Express Handler)

```typescript
import express from "express";

const app = express();
app.use(express.json());

// Simulated knowledge base (in practice, use a vector database)
const knowledgeBase = [
  {
    content:
      "Electronics can be returned within 30 days of purchase with original receipt. Items must be in original packaging and unused condition.",
    source: "return-policy.md",
    keywords: ["return", "refund", "electronics", "policy"],
  },
  {
    content:
      "For defective electronics, we offer a 1-year warranty with free replacement or repair.",
    source: "warranty-policy.md",
    keywords: ["warranty", "defective", "repair", "replacement"],
  },
];

app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;

  if (message.type === "knowledge-base-request") {
    const query = message.query?.toLowerCase() || "";

    // Simple keyword search (use vector search in production)
    const results = knowledgeBase
      .map((doc) => {
        const score = doc.keywords.filter((kw) => query.includes(kw)).length / doc.keywords.length;
        return { content: doc.content, source: doc.source, score };
      })
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score);

    return res.json({ results });
  }

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example (Flask Handler)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated knowledge base (in practice, use a vector database)
KNOWLEDGE_BASE = [
    {
        "content": "Electronics can be returned within 30 days of purchase with original receipt. Items must be in original packaging and unused condition.",
        "source": "return-policy.md",
        "keywords": ["return", "refund", "electronics", "policy"],
    },
    {
        "content": "For defective electronics, we offer a 1-year warranty with free replacement or repair.",
        "source": "warranty-policy.md",
        "keywords": ["warranty", "defective", "repair", "replacement"],
    },
]

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    data = request.get_json()
    message = data.get("message", {})

    if message.get("type") == "knowledge-base-request":
        query = (message.get("query") or "").lower()

        # Simple keyword search (use vector search in production)
        results = []
        for doc in KNOWLEDGE_BASE:
            score = sum(1 for kw in doc["keywords"] if kw in query) / len(doc["keywords"])
            if score > 0:
                results.append({
                    "content": doc["content"],
                    "source": doc["source"],
                    "score": score,
                })

        results.sort(key=lambda r: r["score"], reverse=True)
        return jsonify({"results": results})

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### Doc Reference

- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)

---

## 2. Client Message

Client messages are events sent from Vapi to client-side SDKs (Web, iOS, Android) via WebSocket during an active call. They provide real-time updates to the frontend without requiring a server.

**Direction:** Vapi --> Client SDK (via WebSocket)
**No server needed.** These are configured on the assistant via the `clientMessages` array and handled by the Vapi Web/Mobile SDK.

### Configuration

Client messages are configured in the assistant's `clientMessages` array:

```json
{
  "assistant": {
    "clientMessages": [
      "transcript",
      "status-update",
      "speech-update",
      "conversation-update",
      "metadata",
      "transfer-update"
    ]
  }
}
```

### Available Client Message Types

| Message Type          | Description                                                    |
|-----------------------|----------------------------------------------------------------|
| `transcript`          | Real-time transcript updates (partial and final).              |
| `status-update`       | Call status changes (ringing, in-progress, ended, etc.).       |
| `speech-update`       | Speech activity detection (started/stopped for user/assistant).|
| `conversation-update` | Full conversation messages array updated.                      |
| `metadata`            | Custom metadata sent by the assistant.                         |
| `transfer-update`     | Call transfer status updates.                                  |

### TypeScript SDK Example (Web Client)

```typescript
import Vapi from "@vapi-ai/web";

const vapi = new Vapi("your-public-api-key");

// Listen for real-time transcript updates
vapi.on("message", (message) => {
  if (message.type === "transcript") {
    console.log(`${message.role}: ${message.transcript}`);
    if (message.transcriptType === "final") {
      // Update UI with final transcript
      appendToTranscript(message.role, message.transcript);
    }
  }

  if (message.type === "status-update") {
    console.log(`Call status: ${message.status}`);
    updateCallStatusUI(message.status);
  }

  if (message.type === "speech-update") {
    if (message.role === "user" && message.status === "started") {
      showSpeakingIndicator("user");
    } else if (message.role === "assistant" && message.status === "started") {
      showSpeakingIndicator("assistant");
    }
  }

  if (message.type === "conversation-update") {
    // Full conversation history available
    const messages = message.messagesOpenAIFormatted;
    updateConversationPanel(messages);
  }
});

// Start a call
await vapi.start({
  assistantId: "asst_abc123def456",
});
```

### cURL Example

Not applicable. Client messages are delivered via WebSocket to client-side SDKs. There is no HTTP endpoint to call.

### Python Example

Not applicable for client messages. Client messages are designed for browser/mobile SDKs. For server-side event handling, use [Server Messages](#1-server-message-webhook) instead.

### Doc Reference

- [https://docs.vapi.ai/api-reference/webhooks/client-message](https://docs.vapi.ai/api-reference/webhooks/client-message)

---

## Webhook Authentication

Vapi signs every webhook request with an HMAC-SHA256 signature so you can verify that the request genuinely came from Vapi and was not tampered with.

### How It Works

1. You configure a **Server URL Secret** in your Vapi dashboard (Organization Settings > Server URL Secret).
2. Vapi computes an HMAC-SHA256 signature of the request body using your secret.
3. Vapi sends the signature in the `x-vapi-signature` header.
4. Your server recomputes the signature and compares it.

### Verification

#### TypeScript Example

```typescript
import express from "express";
import crypto from "crypto";

const app = express();

// IMPORTANT: Use raw body for signature verification
app.use(
  express.json({
    verify: (req: any, _res, buf) => {
      req.rawBody = buf.toString();
    },
  })
);

const VAPI_SERVER_URL_SECRET = process.env.VAPI_SERVER_URL_SECRET!;

function verifyVapiSignature(req: any): boolean {
  const signature = req.headers["x-vapi-signature"];
  if (!signature) return false;

  const expectedSignature = crypto
    .createHmac("sha256", VAPI_SERVER_URL_SECRET)
    .update(req.rawBody)
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

app.post("/api/vapi-webhook", (req, res) => {
  // Verify signature
  if (!verifyVapiSignature(req)) {
    console.error("Invalid Vapi signature -- rejecting request");
    return res.status(401).json({ error: "Invalid signature" });
  }

  // Signature verified -- process the webhook
  const { message } = req.body;
  console.log(`Verified webhook: ${message.type}`);

  // ... handle message types ...

  res.status(200).json({});
});

app.listen(3000, () => console.log("Webhook server running on port 3000"));
```

#### Python Example

```python
import hmac
import hashlib
import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

VAPI_SERVER_URL_SECRET = os.environ["VAPI_SERVER_URL_SECRET"]

def verify_vapi_signature(req):
    signature = req.headers.get("x-vapi-signature")
    if not signature:
        return False

    expected_signature = hmac.new(
        VAPI_SERVER_URL_SECRET.encode(),
        req.get_data(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)

@app.route("/api/vapi-webhook", methods=["POST"])
def vapi_webhook():
    # Verify signature
    if not verify_vapi_signature(request):
        print("Invalid Vapi signature -- rejecting request")
        abort(401, description="Invalid signature")

    # Signature verified -- process the webhook
    data = request.get_json()
    message = data.get("message", {})
    print(f"Verified webhook: {message.get('type')}")

    # ... handle message types ...

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(port=3000)
```

#### cURL Example (Computing Signature for Testing)

```bash
# Compute HMAC-SHA256 signature for testing
PAYLOAD='{"message":{"type":"status-update","status":"in-progress"}}'
SECRET="your-server-url-secret"
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')

curl -X POST http://localhost:3000/api/vapi-webhook \
  -H "Content-Type: application/json" \
  -H "x-vapi-signature: $SIGNATURE" \
  -d "$PAYLOAD"
```

### Doc Reference

- [https://docs.vapi.ai/server-url/server-authentication](https://docs.vapi.ai/server-url/server-authentication)

---

## Server URL Priority

When Vapi needs to send a server message, it determines the target URL using the following priority chain (highest to lowest):

```
1. Tool-level server URL     (highest priority)
   Configured on the specific tool definition.
   Only applies to tool-calls messages for that tool.
        |
        v
2. Assistant-level server URL
   Configured on the assistant (assistant.serverUrl).
   Applies to all messages during calls using this assistant.
        |
        v
3. Phone Number-level server URL
   Configured on the phone number (phoneNumber.serverUrl).
   Applies to all calls on this phone number.
        |
        v
4. Organization-level server URL  (lowest priority)
   Configured in your Vapi dashboard (Organization Settings).
   Default fallback for all calls.
```

### Key Points

- **Tool-level** overrides ONLY apply to `tool-calls` messages for that specific tool. All other message types fall through to the next level.
- **Assistant-level** overrides apply to ALL message types during a call with that assistant.
- **Phone Number-level** is useful when you want different numbers to route to different servers.
- **Organization-level** is the catch-all default. Every org should have this configured.

### Example Scenario

```
Organization server URL: https://api.mycompany.com/vapi-default
Phone Number server URL: https://api.mycompany.com/vapi-sales
Assistant server URL:    https://api.mycompany.com/vapi-assistant-v2
Tool "lookupOrder" URL:  https://api.mycompany.com/vapi-orders

When a call comes in on the sales phone number with assistant-v2:
  - tool-calls for "lookupOrder" --> https://api.mycompany.com/vapi-orders
  - tool-calls for other tools   --> https://api.mycompany.com/vapi-assistant-v2
  - status-update                --> https://api.mycompany.com/vapi-assistant-v2
  - end-of-call-report           --> https://api.mycompany.com/vapi-assistant-v2
  - transcript                   --> https://api.mycompany.com/vapi-assistant-v2
```

---

## Best Practices

### Response Times

| Message Type                  | Timeout    | Recommendation                                                         |
|-------------------------------|------------|------------------------------------------------------------------------|
| `assistant-request`           | 7.5 seconds| Keep logic simple. Pre-load assistant configs. Use caching.            |
| `tool-calls`                  | Varies     | Optimize external API calls. Use connection pooling. Consider async patterns. |
| `transfer-destination-request`| ~5 seconds | Pre-compute routing rules. Minimize database lookups.                  |
| `knowledge-base-request`      | ~5 seconds | Use fast vector search. Pre-index content. Cache frequent queries.     |
| `status-update`               | N/A        | Fire-and-forget. Process asynchronously.                               |
| `end-of-call-report`          | N/A        | Fire-and-forget. Queue for background processing.                      |
| `transcript`                  | N/A        | Fire-and-forget. Stream to real-time systems.                          |
| `speech-update`               | N/A        | Fire-and-forget. Update UI indicators.                                 |
| `conversation-update`         | N/A        | Fire-and-forget. Sync to database asynchronously.                      |

### Error Handling

1. **Always return 200 for fire-and-forget messages.** Even if you encounter an error processing the message, return 200 to acknowledge receipt. Log the error internally.

2. **Return meaningful errors for synchronous messages.** For `assistant-request`, `tool-calls`, `transfer-destination-request`, and `knowledge-base-request`, return structured error responses so the assistant can communicate the issue to the caller.

3. **Implement idempotency.** Vapi may retry webhook deliveries. Use the `call.id` + `message.type` + `timestamp` as an idempotency key to avoid processing the same event twice.

```typescript
// Example: idempotency check
const idempotencyKey = `${message.call.id}:${message.type}:${message.timestamp}`;
if (await cache.has(idempotencyKey)) {
  return res.status(200).json({}); // Already processed
}
await cache.set(idempotencyKey, true, { ttl: 3600 });
```

### HTTPS

- **Always use HTTPS** for your server URL in production. Vapi sends sensitive call data (transcripts, phone numbers, recordings) in webhook payloads.
- For local development, use a tunneling service (e.g., ngrok) to expose your local server to the internet.
- Self-signed certificates are NOT supported. Use a valid TLS certificate (Let's Encrypt is free).

### Retry Handling

- Vapi may retry failed webhook deliveries (non-2xx responses or timeouts).
- Implement idempotency to handle duplicate deliveries gracefully.
- For fire-and-forget messages, always return 200 even if internal processing fails. Handle errors asynchronously.
- For synchronous messages (assistant-request, tool-calls), if you cannot process the request, return a structured error response rather than timing out.

### Logging

- Log every incoming webhook with the `call.id`, `message.type`, and `timestamp` for debugging.
- Store `end-of-call-report` payloads permanently for analytics and compliance.
- Log `tool-calls` requests and responses for debugging function call issues.

```typescript
// Recommended logging middleware
app.post("/api/vapi-webhook", (req, res) => {
  const { message } = req.body;
  const callId = message?.call?.id || "unknown";
  const messageType = message?.type || "unknown";
  const timestamp = message?.timestamp || new Date().toISOString();

  console.log(`[VAPI] ${timestamp} | call=${callId} | type=${messageType}`);

  // ... handle message ...
});
```

### Architecture Recommendations

1. **Use a message queue** for fire-and-forget messages. Accept the webhook immediately (return 200), then push the payload to a queue (SQS, RabbitMQ, Redis) for background processing.

2. **Separate synchronous and asynchronous handlers.** Synchronous messages (assistant-request, tool-calls) need fast, direct responses. Asynchronous messages (status-update, end-of-call-report) can be queued.

3. **Single webhook endpoint, router pattern.** Use one URL for all message types and route internally based on `message.type`:

```typescript
app.post("/api/vapi-webhook", async (req, res) => {
  const { message } = req.body;

  switch (message.type) {
    case "assistant-request":
      return handleAssistantRequest(message, res);
    case "tool-calls":
      return handleToolCalls(message, res);
    case "status-update":
      return handleStatusUpdate(message, res);
    case "end-of-call-report":
      return handleEndOfCallReport(message, res);
    case "transcript":
      return handleTranscript(message, res);
    case "speech-update":
      return handleSpeechUpdate(message, res);
    case "conversation-update":
      return handleConversationUpdate(message, res);
    case "transfer-destination-request":
      return handleTransferRequest(message, res);
    case "knowledge-base-request":
      return handleKnowledgeBaseRequest(message, res);
    default:
      console.warn(`Unhandled message type: ${message.type}`);
      return res.status(200).json({});
  }
});
```

### Doc References

- [https://docs.vapi.ai/api-reference/webhooks/server-message](https://docs.vapi.ai/api-reference/webhooks/server-message)
- [https://docs.vapi.ai/api-reference/webhooks/client-message](https://docs.vapi.ai/api-reference/webhooks/client-message)
- [https://docs.vapi.ai/server-url/events](https://docs.vapi.ai/server-url/events)
- [https://docs.vapi.ai/server-url/server-authentication](https://docs.vapi.ai/server-url/server-authentication)
