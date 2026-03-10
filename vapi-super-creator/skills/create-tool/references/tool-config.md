# Tool Configuration Reference

> Sources: https://docs.vapi.ai/tools/tool-rejection-plan

> **Doc reference:** https://docs.vapi.ai/tools/tool-rejection-plan

The tool rejection plan prevents unintended tool calls by evaluating conversation state using conditions. Uses AND logic by default -- if all conditions match, the tool call is rejected.

### Condition Types

#### Regex Conditions

Match message content patterns to prevent inappropriate tool calls:

```json
{
  "conditions": [
    {
      "type": "regex",
      "regex": "\\?",
      "target": { "position": -1, "role": "user" }
    }
  ]
}
```

This rejects transfer calls when the user is asking a question (contains "?") rather than requesting a transfer.

#### Liquid Conditions

Complex logic using Liquid templates to evaluate conversation state:

```json
{
  "conditions": [
    {
      "type": "liquid",
      "liquid": "{% assign recentMessages = messages | last: 5 %}{% assign userMessages = recentMessages | where: 'role', 'user' %}{% assign mentioned = false %}{% for msg in userMessages %}{% if msg.content contains 'transfer' or msg.content contains 'connect' or msg.content contains 'representative' %}{% assign mentioned = true %}{% endif %}{% endfor %}{% if mentioned %}false{% else %}true{% endif %}"
    }
  ]
}
```

This prevents transfers unless the user has recently mentioned transfer-related keywords.

### Group Conditions with OR Logic

```json
{
  "conditions": [
    {
      "type": "group",
      "operator": "OR",
      "conditions": [
        { "type": "regex", "regex": "(?i)\\bcancel\\b", "target": { "role": "user" } },
        { "type": "regex", "regex": "(?i)\\bstop\\b", "target": { "role": "user" } }
      ]
    }
  ]
}
```

### Negation for Positive Confirmation

Require specific words before allowing tool execution:

```json
{
  "conditions": [
    {
      "type": "regex",
      "regex": "(?i)\\b(bye|goodbye|farewell|see you later|take care)\\b",
      "target": { "position": -1, "role": "user" },
      "negate": true
    }
  ]
}
```

This prevents ending the call unless the user has said goodbye.

### Position-Based Targeting

Use `position: -1` to target the most recent message:

```json
{
  "target": { "position": -1, "role": "user" }
}
```

### Best Practices
- Structure prompts with clear fallback options
- Never mention technical aspects of tool rejection to users
- Guide users naturally through alternative flows or ask clarifying questions

---

## 11. Tool Messages Configuration

Tool messages provide spoken feedback to users during different phases of tool execution. These apply to ALL tool types (built-in, custom, integration).

### Message Types

| Type | When Spoken | Description |
|------|------------|-------------|
| `request-start` | When tool execution begins | "Let me look that up for you." |
| `request-complete` | When tool succeeds | "I found your information." |
| `request-failed` | When tool fails | "I'm sorry, I couldn't complete that request." |
| `request-response-delayed` | When tool takes longer than expected | "This is taking a bit longer. Please hold." |

### Basic Configuration

```json
{
  "tools": [
    {
      "type": "transferCall",
      "destinations": [...],
      "messages": [
        {
          "type": "request-start",
          "content": "I'm transferring you to our technical support specialist now."
        },
        {
          "type": "request-response-delayed",
          "content": "Please hold on, I'm still connecting you to technical support.",
          "timingMilliseconds": 5000
        },
        {
          "type": "request-complete",
          "content": "You're now connected with our technical support team."
        },
        {
          "type": "request-failed",
          "content": "I apologize, but I'm unable to transfer you to technical support at the moment. Let me see how I can help you directly."
        }
      ]
    }
  ]
}
```

### timingMilliseconds

For `request-response-delayed` messages, specifies when to trigger (in milliseconds):

```json
{
  "type": "request-response-delayed",
  "content": "Please hold while I transfer your call.",
  "timingMilliseconds": 3000
}
```

This speaks the delayed message if the tool takes longer than 3 seconds to complete.

### Conditional Messages

Messages can be conditional based on parameter values:

```json
{
  "messages": [
    {
      "type": "request-start",
      "content": "Transferring you to our premium support team.",
      "conditions": [
        {
          "param": "{{customerTier}}",
          "operator": "eq",
          "value": "premium"
        }
      ]
    },
    {
      "type": "request-start",
      "content": "Let me connect you with our support team.",
      "conditions": [
        {
          "param": "{{customerTier}}",
          "operator": "neq",
          "value": "premium"
        }
      ]
    }
  ]
}
```

### Message Properties Table

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Message type (`request-start`, `request-complete`, `request-failed`, `request-response-delayed`) |
| `content` | string | Message content to be spoken (or audio URL) |
| `timingMilliseconds` | number | For delayed messages, when to trigger (ms) |
| `conditions` | array | Optional conditions for conditional messages |
| `blocking` | boolean | Whether the message blocks further processing |

### Complete Example with All Message Types

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "lookupOrder",
        "description": "Look up an order by order number",
        "parameters": {
          "type": "object",
          "properties": {
            "orderNumber": { "type": "string", "description": "The order number" }
          },
          "required": ["orderNumber"]
        }
      },
      "server": { "url": "https://your-api.com/lookup" },
      "messages": [
        {
          "type": "request-start",
          "content": "Let me look up that order for you."
        },
        {
          "type": "request-response-delayed",
          "content": "I'm still searching for your order. Just a moment.",
          "timingMilliseconds": 4000
        },
        {
          "type": "request-complete",
          "content": "I found your order details."
        },
        {
          "type": "request-failed",
          "content": "I'm sorry, I was unable to find that order. Could you double-check the order number?"
        }
      ]
    }
  ]
}
```

---

## Quick Reference: Tool Configuration Patterns

### Minimal Tool (Built-in)
```json
{ "type": "endCall" }
```

### Webhook Tool (Custom Function)
```json
{
  "type": "function",
  "function": {
    "name": "myTool",
    "description": "Description for the LLM",
    "parameters": {
      "type": "object",
      "properties": { ... },
      "required": [...]
    }
  },
  "server": { "url": "https://your-server.com/webhook" },
  "async": false,
  "maxTokens": 500
}
```

### Code Tool (Serverless)
```json
{
  "type": "code",
  "name": "myCodeTool",
  "description": "Description",
  "code": "const result = args.param;\nreturn { data: result };",
  "parameters": { ... },
  "environmentVariables": [{ "name": "API_KEY", "value": "..." }]
}
```

### Integration Tool (Google Calendar)
```json
{
  "type": "google.calendar.event.create",
  "name": "scheduleEvent",
  "description": "Schedule a calendar event"
}
```

### Client-Side Tool (No Server)
```json
{
  "type": "function",
  "async": true,
  "function": {
    "name": "updateUI",
    "description": "Update the UI",
    "parameters": { ... }
  }
}
```

---

*This reference was compiled from the official Vapi documentation. For the latest updates, always refer to https://docs.vapi.ai/tools*
