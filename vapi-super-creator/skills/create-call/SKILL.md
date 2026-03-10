---
name: create-call
description: Create outbound phone calls, web calls, and batch calls using the Vapi API. Use when making automated calls, testing voice assistants, scheduling call campaigns, or initiating conversations programmatically.
---

# Create Calls

This skill covers creating outbound phone calls, web calls, batch calls, and scheduled calls using the Vapi API. Calls connect your voice assistants to real users over the phone or browser.

## Prerequisites

- Vapi account with API key configured (see the `setup-api-key` skill)
- A configured assistant (see the `create-assistant` skill)
- For phone calls: a provisioned phone number (see the `create-phone-number` skill)

## Quick Start — Outbound Phone Call

### cURL

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+14155551234"
    }
  }'
```

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({
    token: process.env.VAPI_API_KEY!
});

const call = await vapi.calls.create({
    assistantId: "your-assistant-id",
    phoneNumberId: "your-phone-number-id",
    customer: {
        number: "+14155551234"
    }
});

console.log("Call ID:", call.id);
console.log("Status:", call.status);
```

### Python (Server SDK)

```python
import os
from vapi import VapiClient

client = VapiClient(token=os.environ["VAPI_API_KEY"])

call = client.calls.create(
    assistant_id="your-assistant-id",
    phone_number_id="your-phone-number-id",
    customer={"number": "+14155551234"}
)

print(f"Call ID: {call.id}")
print(f"Status: {call.status}")
```

## Call Types

### Outbound Phone Call

The standard call type — your assistant calls a phone number.

**Required parameters:**
- `assistantId` or inline `assistant` — The voice assistant to use.
- `phoneNumberId` — The Vapi phone number to call from.
- `customer.number` — The destination phone number in E.164 format (e.g., `+14155551234`).

```json
{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
        "number": "+14155551234"
    }
}
```

### Web Call

For browser-based voice interactions using the Vapi Web SDK. No phone number required.

**Client-side setup:**

```javascript
import Vapi from '@vapi-ai/web';

const vapi = new Vapi('YOUR_PUBLIC_API_KEY');

// Start a web call with a saved assistant
vapi.start('your-assistant-id');

// Or start with a transient assistant configuration
vapi.start({
    model: {
        provider: "openai",
        model: "gpt-4o",
        messages: [
            { role: "system", content: "You are a helpful assistant." }
        ]
    },
    voice: { provider: "cartesia", voiceId: "your-voice-id" },
    firstMessage: "Hello! How can I help you?"
});

// Listen for events
vapi.on('call-start', () => console.log('Call started'));
vapi.on('call-end', () => console.log('Call ended'));
vapi.on('message', (msg) => console.log('Message:', msg));
vapi.on('error', (err) => console.error('Error:', err));

// End the call
vapi.stop();
```

> **Note:** Web calls use the **Public API Key**, not the private key. Get it from Dashboard > Organization Settings > API Keys.

### Transient Assistant Call

Instead of referencing a saved assistant by ID, provide the full assistant configuration inline. Useful for testing or one-off calls:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistant": {
      "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "You are a friendly sales assistant for Acme Corp."
          }
        ]
      },
      "voice": {
        "provider": "cartesia",
        "voiceId": "your-voice-id"
      },
      "firstMessage": "Hi! Thanks for your interest in Acme Corp. How can I help?",
      "endCallMessage": "Thanks for calling! Goodbye."
    },
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+14155551234"
    }
  }'
```

## Scheduled Calls

Schedule calls for future execution using `schedulePlan`:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+14155551234"
    },
    "schedulePlan": {
      "earliestAt": "2026-03-10T09:00:00Z",
      "latestAt": "2026-03-10T17:00:00Z"
    }
  }'
```

**Schedule parameters:**
- `earliestAt` (required) — ISO 8601 datetime string for the earliest call attempt.
- `latestAt` (optional) — Latest time Vapi will attempt the call. If omitted, Vapi calls as close to `earliestAt` as possible.

The call will be placed at any point within the `earliestAt` to `latestAt` window, depending on system availability and concurrency.

## Batch Calls

Call multiple customers with the same assistant using the `customers` array:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customers": [
      { "number": "+14155551234", "name": "Alice Johnson" },
      { "number": "+14155555678", "name": "Bob Smith" },
      { "number": "+14155559012", "name": "Carol Davis" }
    ]
  }'
```

**Important considerations:**
- Each customer receives the same assistant configuration.
- For customer-specific assistant overrides, make separate API calls.
- Batch calls are subject to your account's concurrency limits (default: 10 concurrent calls).
- For large batches, break into chunks of 50-100 numbers and run sequentially.
- You can combine `customers` with `schedulePlan` for scheduled batch calls.

### Batch + Scheduled

```json
{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customers": [
        { "number": "+14155551234" },
        { "number": "+14155555678" }
    ],
    "schedulePlan": {
        "earliestAt": "2026-03-10T09:00:00Z",
        "latestAt": "2026-03-10T17:00:00Z"
    }
}
```

## Call with Metadata

Attach custom metadata to calls for tracking, analytics, or passing context to your webhook:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistantId": "your-assistant-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+14155551234",
      "name": "Alice Johnson"
    },
    "metadata": {
      "campaignId": "spring-2026",
      "leadSource": "website",
      "priority": "high"
    }
  }'
```

Metadata is included in all webhook events for this call, allowing your server to correlate calls with your internal systems.

## Managing Calls

### List Calls

```bash
curl https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get a Specific Call

```bash
curl https://api.vapi.ai/call/<call-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Delete a Call Record

```bash
curl -X DELETE https://api.vapi.ai/call/<call-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Call Response Format

When you create a call, the API returns a call object:

```json
{
    "id": "call-id-uuid",
    "orgId": "org-id",
    "type": "outboundPhoneCall",
    "status": "queued",
    "assistantId": "assistant-id",
    "phoneNumberId": "phone-number-id",
    "customer": {
        "number": "+14155551234"
    },
    "createdAt": "2026-03-02T10:00:00.000Z",
    "updatedAt": "2026-03-02T10:00:00.000Z"
}
```

### Call Status Lifecycle

```
queued --> ringing --> in-progress --> ended
```

| Status | Description |
|--------|-------------|
| `queued` | Call is created and waiting to be placed |
| `ringing` | Call is dialing the customer's phone |
| `in-progress` | Customer answered, conversation is active |
| `ended` | Call has completed (check `endedReason` for details) |

### Common `endedReason` Values

| Reason | Description |
|--------|-------------|
| `customer-ended-call` | Customer hung up |
| `assistant-ended-call` | Assistant triggered endCall tool |
| `max-duration-reached` | Hit `maxDurationSeconds` limit |
| `silence-timed-out` | No speech detected for too long |
| `pipeline-error` | Internal processing error |
| `customer-did-not-answer` | No answer after ringing |
| `voicemail` | Call went to voicemail |

## TCPA Compliance Warning

> **Important:** When making automated outbound calls, you are responsible for compliance with the Telephone Consumer Protection Act (TCPA) and any applicable local regulations. This includes:
> - Obtaining prior express consent before making automated calls.
> - Maintaining an internal Do Not Call list.
> - Honoring the National Do Not Call Registry.
> - Identifying yourself and the purpose of the call.
> - Providing an opt-out mechanism.
>
> Vapi provides the technology platform but does not ensure regulatory compliance on your behalf. Consult legal counsel for your specific use case.

## Concurrency Limits

Each Vapi account includes **10 concurrent call slots** by default. Monitor usage via the API response's `subscriptionLimits` object. To increase limits, contact Vapi support or upgrade your plan.

Tips for managing concurrency:
- Break large batch lists into chunks of 50-100 numbers.
- Run batches sequentially rather than all at once.
- Use `schedulePlan` to spread calls over time windows.
- Monitor active calls before starting new batches.

## References

- [API Reference](references/api-reference.md) — Complete REST API docs for Calls, Campaigns, and Analytics (11 endpoints)

## Related Skills

- See the `setup-api-key` skill if you need to configure your API key first.
- See the `create-assistant` skill to build the assistant that handles the call.
- See the `create-phone-number` skill to provision a phone number for outbound calls.
- See the `create-squad` skill for calls that use multi-assistant squads.
- See the `create-workflow` skill for calls that use workflow-based conversation flows.
- See the `setup-webhook` skill to receive call events and end-of-call reports.
