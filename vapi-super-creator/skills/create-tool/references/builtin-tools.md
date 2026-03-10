# Built-in (Default) Tools Reference

> Source: https://docs.vapi.ai/tools/default-tools

### 2.1 endCall Tool

Allows the assistant to terminate the current call when appropriate conditions are met.

**Configuration:**
```json
{
  "type": "endCall"
}
```

**MANDATORY**: Every assistant should include the endCall tool. Your system prompt must instruct the assistant when to use it.

**Complete example:**
```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are an assistant at a law firm. If the user is being mean, use the endCall function. When the conversation is naturally concluded, end the call."
      }
    ],
    "tools": [
      { "type": "endCall" }
    ]
  }
}
```

**Use cases:**
- Ending calls when users are abusive or inappropriate
- Completing calls after successful task completion
- Implementing call time limits
- Graceful goodbye after conversation concludes

---

### 2.2 transferCall Tool

Enables call forwarding to predefined phone numbers, SIP endpoints, or other assistants.

#### Basic Blind Transfer (Phone Number)

```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+16054440129",
      "message": "I am forwarding your call to Department A. Please stay on the line."
    }
  ]
}
```

#### SIP Transfer

```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "sip",
      "sipUri": "sip:user@domain.com",
      "message": "Transferring you now."
    }
  ]
}
```

#### Multiple Destinations with Descriptions (LLM Routing)

The assistant uses `description` fields to decide which destination to choose:

```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+15551234567",
      "description": "Transfer to sales team for pricing questions and new purchases",
      "message": "Connecting you with our sales team."
    },
    {
      "type": "number",
      "number": "+15559876543",
      "description": "Transfer to technical support for product issues and troubleshooting",
      "message": "Connecting you with technical support."
    }
  ]
}
```

#### Transfer Modes

| Mode | `transferPlan.mode` | Description |
|------|---------------------|-------------|
| **Blind** | (default, no transferPlan) | Direct transfer without context |
| **Warm with Summary** | `"warm-transfer-with-summary"` | AI-generated call summary sent via SIP header |
| **Warm with Message** | `"warm-transfer-with-message"` | Custom TTS message played to recipient |
| **Assistant-based (Experimental)** | `"warm-transfer-experimental"` | AI assistant manages the transfer conversation |

#### Warm Transfer with Summary

```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+14155551234",
      "transferPlan": {
        "mode": "warm-transfer-with-summary",
        "summaryPlan": {
          "enabled": true,
          "messages": [
            {
              "role": "system",
              "content": "Please provide a summary of the call."
            },
            {
              "role": "user",
              "content": "Here is the transcript:\n\n{{transcript}}\n\n"
            }
          ]
        }
      }
    }
  ]
}
```

#### Warm Transfer with Message

```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+14155551234",
      "transferPlan": {
        "mode": "warm-transfer-with-message",
        "message": "Hey, this call has been forwarded through Vapi."
      }
    }
  ]
}
```

#### Assistant-Based Warm Transfer

Uses a dedicated AI assistant to speak with the recipient, then decides whether to complete or cancel the transfer:

```json
{
  "type": "transferCall",
  "function": {
    "name": "salesTransferAssistant"
  },
  "destinations": [
    {
      "type": "number",
      "number": "+14155551234",
      "transferPlan": {
        "mode": "warm-transfer-experimental",
        "holdAudioUrl": "https://api.twilio.com/cowbell.mp3",
        "voicemailDetectionType": "transcript",
        "fallbackPlan": {
          "message": "Could not transfer your call, goodbye.",
          "endCallEnabled": true
        },
        "summaryPlan": {
          "enabled": true,
          "messages": [
            { "role": "system", "content": "Please provide a summary of the call." },
            { "role": "user", "content": "Here is the transcript:\n\n{{transcript}}\n\n" }
          ]
        },
        "transferAssistant": {
          "firstMessage": "Hello, I have a customer on the line. Are you available to take this call?",
          "firstMessageMode": "assistant-speaks-first",
          "maxDurationSeconds": 120,
          "silenceTimeoutSeconds": 30,
          "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "messages": [
              {
                "role": "system",
                "content": "You are a transfer assistant designed to facilitate call transfers between a customer and an operator. You have access to the previous customer conversation. Use transferSuccessful to complete or transferCancel to cancel."
              }
            ]
          }
        }
      }
    }
  ]
}
```

**Transfer Assistant Built-in Tools:**
- `transferSuccessful` - Completes the transfer, merges calls, connects parties
- `transferCancel` - Cancels the transfer, returns customer to original assistant

**Transfer Assistant Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `firstMessage` | string | Initial message when operator answers |
| `firstMessageMode` | string | Controls when first message is delivered |
| `maxDurationSeconds` | number | Maximum duration for the operator call |
| `silenceTimeoutSeconds` | number | Seconds of silence before cancelling |
| `model` | object | Assistant configuration with provider and prompts |

**Limitations:**
- Warm transfers require Twilio-based telephony
- Assistant-based transfers require `warm-transfer-experimental` mode
- Only works with Twilio, Vapi phone numbers, and SIP trunks (not Telnyx or Vonage)

---

### 2.3 SMS Tool

Sends SMS messages using a configured Twilio account.

**Configuration:**
```json
{
  "type": "sms",
  "metadata": {
    "from": "+15551234567"
  }
}
```

**Requirements:**
- Twilio phone number with SMS capability
- Currently only supports US-to-US messaging

**Complete example:**
```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are an assistant. When the user asks you to send a text message, use the sms function."
      }
    ],
    "tools": [
      {
        "type": "sms",
        "metadata": {
          "from": "+15551234567"
        }
      }
    ]
  }
}
```

**Use cases:**
- Sending appointment confirmations
- Sharing links or reference numbers
- Follow-up communications

---

### 2.4 DTMF Tool

Enables the assistant to enter keypad digits for IVR navigation and data input.

**Configuration:**
```json
{
  "type": "dtmf"
}
```

**Technical Implementation:**
- Uses **out-of-band RFC 2833 method** for reliable tone transmission
- Transmits DTMF signals separately from the audio stream within RTP packets
- More reliable than in-band DTMF in VoIP environments where audio compression might affect signal quality

**Complete example:**
```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are an assistant. When you hit a menu, use the dtmf function to enter the digits."
      }
    ],
    "tools": [
      { "type": "dtmf" }
    ]
  }
}
```

**Use cases:**
- Navigating phone menus and IVR systems
- Entering account numbers or verification codes
- Accessing automated services

---

### 2.5 API Request Tool

Makes HTTP requests to external APIs during conversations, bridging Vapi with your business logic.

**Configuration:**
```json
{
  "type": "apiRequest",
  "name": "checkOrderStatus",
  "url": "https://api.yourcompany.com/orders/{{orderNumber}}",
  "method": "GET",
  "body": {
    "type": "object",
    "properties": {
      "orderNumber": {
        "description": "The user's order number",
        "type": "string"
      }
    },
    "required": ["orderNumber"]
  }
}
```

**Supported HTTP Methods:** `GET`, `POST`, `PUT`, `DELETE`

**URL Template Variables:** Use `{{paramName}}` syntax (LiquidJS) to reference conversation data in URLs.

#### Advanced POST Example with Headers

```json
{
  "type": "apiRequest",
  "name": "bookAppointment",
  "url": "https://api.yourcompany.com/appointments",
  "method": "POST",
  "headers": {
    "type": "object",
    "properties": {
      "x-api-key": {
        "type": "string",
        "value": "123456789"
      }
    }
  },
  "body": {
    "type": "object",
    "properties": {
      "date": {
        "description": "The date of the appointment",
        "type": "string"
      },
      "customerName": {
        "description": "The name of the customer",
        "type": "string"
      }
    },
    "required": ["date", "customerName"]
  }
}
```

#### Retry Logic with backoffPlan

```json
{
  "backoffPlan": {
    "type": "exponential",
    "maxRetries": 4,
    "baseDelaySeconds": 1.5,
    "timeoutSeconds": 45
  }
}
```

**backoffPlan Parameters:**

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `type` | string | `"exponential"` or `"fixed"` | Backoff strategy type |
| `maxRetries` | number | 0-10 (default: 0) | Maximum retry attempts |
| `baseDelaySeconds` | number | 0-10 | Initial delay between retries |
| `timeoutSeconds` | number | - | Total timeout for the request |

**Exponential Backoff Timing Example (baseDelay=1s):**
- First retry: 1s
- Second retry: 2s
- Third retry: 4s
- Fourth retry: 8s

---

