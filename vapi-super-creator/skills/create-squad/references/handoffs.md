# Handoff Tool Complete Reference

> Source: https://docs.vapi.ai/squads/handoff, https://docs.vapi.ai/squads/handoff#multiple-destinations

---

## Overview

The **handoff tool** is the primary mechanism for transferring calls between assistants within a Vapi squad. It enables sophisticated multi-agent conversation flows where specialized assistants handle different aspects of a customer interaction. The handoff tool replaces the legacy `assistantDestinations` approach and provides enhanced capabilities including context engineering, variable extraction, and dynamic routing.

When a handoff is triggered, the current assistant transfers the call to a destination assistant. The handoff tool controls:
- **Which assistant** receives the call (by ID or name)
- **What context** is transferred (full history, recent messages, or none)
- **What variables** are extracted and passed along
- **What messages** the caller hears during the transfer

---

## Handoff Tool Structure

Every handoff tool has this base structure:

```json
{
  "type": "handoff",
  "function": {
    "name": "handoff_to_<AgentName>",
    "description": "Description of when to trigger this handoff",
    "parameters": {
      "type": "object",
      "properties": {},
      "required": []
    }
  },
  "destinations": [
    {
      "type": "assistant",
      "assistantId": "<uuid>",
      "description": "When to route to this destination",
      "contextEngineeringPlan": {
        "type": "all"
      }
    }
  ],
  "messages": []
}
```

---

## Two Patterns for Multiple Destinations

When an assistant needs to hand off to more than one possible destination, there are two architectural patterns. The choice depends on which LLM provider you are using.

### Pattern 1: Multiple Tools Pattern (OpenAI Recommended)

Create **separate handoff tool definitions** for each destination, each with a **single destination** in its `destinations` array. This pattern works best with **OpenAI models** (gpt-4o, gpt-4o-mini, etc.) because OpenAI models perform better when each tool has a clear, singular purpose.

```json
{
  "tools": [
    {
      "type": "handoff",
      "function": {
        "name": "handoff_to_Sales",
        "description": "Use this tool when the customer wants to learn about pricing, product features, or make a purchase.",
        "parameters": {
          "type": "object",
          "properties": {
            "destination": {
              "type": "string",
              "enum": ["sales-assistant-123"]
            }
          },
          "required": ["destination"]
        }
      },
      "destinations": [
        {
          "type": "assistant",
          "assistantId": "sales-assistant-123",
          "description": "customer wants to learn about pricing or make a purchase",
          "contextEngineeringPlan": {
            "type": "all"
          }
        }
      ]
    },
    {
      "type": "handoff",
      "function": {
        "name": "handoff_to_Support",
        "description": "Use this tool when the customer needs help with an existing product or service, troubleshooting, or technical issues.",
        "parameters": {
          "type": "object",
          "properties": {
            "destination": {
              "type": "string",
              "enum": ["support-assistant-456"]
            }
          },
          "required": ["destination"]
        }
      },
      "destinations": [
        {
          "type": "assistant",
          "assistantId": "support-assistant-456",
          "description": "customer needs help with an existing product or service",
          "contextEngineeringPlan": {
            "type": "all"
          }
        }
      ]
    },
    {
      "type": "handoff",
      "function": {
        "name": "handoff_to_Billing",
        "description": "Use this tool when the customer has questions about invoices, payments, or refunds.",
        "parameters": {
          "type": "object",
          "properties": {
            "destination": {
              "type": "string",
              "enum": ["billing-assistant-789"]
            }
          },
          "required": ["destination"]
        }
      },
      "destinations": [
        {
          "type": "assistant",
          "assistantId": "billing-assistant-789",
          "description": "customer has questions about invoices, payments, or refunds",
          "contextEngineeringPlan": {
            "type": "lastNMessages",
            "maxMessages": 5
          }
        }
      ]
    }
  ]
}
```

**Why this works well with OpenAI**: OpenAI models excel at selecting the right tool from a list of distinct tools, each with its own name and description. The model can clearly reason: "The customer asked about pricing, so I should call `handoff_to_Sales`."

### Pattern 2: Single Tool Pattern (Anthropic Recommended)

Use **one handoff tool** with **multiple destinations** in the `destinations` array. This pattern works best with **Anthropic models** (Claude) because Anthropic models handle multiple options within a single tool call more effectively.

```json
{
  "tools": [
    {
      "type": "handoff",
      "destinations": [
        {
          "type": "assistant",
          "assistantId": "03e11cfe-4528-4243-a43d-6aded66ab7ba",
          "description": "customer wants to learn about pricing or make a purchase",
          "contextEngineeringPlan": {
            "type": "all"
          }
        },
        {
          "type": "assistant",
          "assistantName": "support-assistant",
          "description": "customer needs help with an existing product or service",
          "contextEngineeringPlan": {
            "type": "all"
          }
        },
        {
          "type": "assistant",
          "assistantName": "billing-assistant",
          "description": "customer has questions about invoices, payments, or refunds",
          "contextEngineeringPlan": {
            "type": "lastNMessages",
            "maxMessages": 5
          }
        }
      ]
    }
  ]
}
```

**Why this works well with Anthropic**: Claude models are better at reasoning about which destination to select from a list within a single tool, using the `description` fields to make routing decisions.

---

## Destination Types

### Using `assistantId` (Saved Assistants)

Reference a previously created assistant by its unique UUID. Use this when the destination assistant already exists in your Vapi account.

```json
{
  "type": "assistant",
  "assistantId": "03e11cfe-4528-4243-a43d-6aded66ab7ba",
  "description": "customer wants to speak with technical support",
  "contextEngineeringPlan": {
    "type": "all"
  }
}
```

### Using `assistantName` (Squad Members)

Reference another assistant within the same squad by its `name` field. Use this when both source and destination assistants are members of the same squad.

```json
{
  "type": "assistant",
  "assistantName": "TechnicalSupportAgent",
  "description": "customer needs technical assistance",
  "contextEngineeringPlan": {
    "type": "all"
  }
}
```

**Important**: When using `assistantName`, the name must exactly match the `name` property of another squad member's assistant definition.

### Using Squad Destination (Squad-to-Squad Transfer)

Transfer the call to an entirely different squad:

```json
{
  "type": "squad",
  "squadId": "your-squad-id",
  "description": "customer needs specialized support from the enterprise team",
  "entryAssistantName": "EnterpriseGreeter",
  "contextEngineeringPlan": {
    "type": "userAndAssistantMessages"
  }
}
```

### Using Transient Squad (Inline Squad Definition)

Define a squad inline without saving it first:

```json
{
  "type": "squad",
  "squad": {
    "members": [
      {
        "assistantId": "greeter-assistant-id",
        "assistantDestinations": [
          {
            "type": "assistant",
            "assistantName": "SalesSpecialist",
            "description": "customer is interested in purchasing"
          }
        ]
      },
      {
        "assistantId": "sales-assistant-id"
      }
    ]
  },
  "entryAssistantName": "GreeterAssistant",
  "description": "route customer to the sales squad"
}
```

---

## Key Properties Reference Table

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | `"handoff"` | Yes | Identifies this as a handoff tool |
| `function.name` | string | No | Custom function name (e.g., `handoff_to_Sales`). Auto-generated if not specified. |
| `function.description` | string | No | Description of when to trigger this handoff. Used by the LLM for tool selection. |
| `function.parameters` | object | No | JSON Schema for parameters extracted during handoff (e.g., `patientName`) |
| `destinations` | array | Yes | Array of destination objects |
| `destinations[].type` | `"assistant"` or `"squad"` | Yes | Type of destination |
| `destinations[].assistantId` | string (UUID) | Conditional | UUID of a saved assistant. Use this OR `assistantName`. |
| `destinations[].assistantName` | string | Conditional | Name of a squad member assistant. Use this OR `assistantId`. |
| `destinations[].description` | string | Yes | Description of when to route to this destination. Critical for LLM routing decisions. |
| `destinations[].contextEngineeringPlan` | object | No | Controls what conversation history transfers. Defaults to `"all"`. |
| `destinations[].variableExtractionPlan` | object | No | Defines variables to extract from conversation during handoff. |
| `messages` | array or null | No | Messages spoken during transfer. Set to `[]` or `null` for silent handoffs. |

---

## contextEngineeringPlan Types

The `contextEngineeringPlan` controls what conversation history the receiving assistant gets.

### `"all"` (Default) -- Transfer Full History

Transfers the entire conversation history including system messages, user messages, assistant messages, and tool calls.

```json
{
  "contextEngineeringPlan": {
    "type": "all"
  }
}
```

**Use when**: The receiving assistant needs full context of everything discussed.

### `"lastNMessages"` -- Transfer Recent Messages Only

Transfers only the most recent N messages from the conversation.

```json
{
  "contextEngineeringPlan": {
    "type": "lastNMessages",
    "maxMessages": 10
  }
}
```

**Use when**: The conversation is long and only recent context matters, or to reduce token usage.

### `"userAndAssistantMessages"` -- Filter System/Tool Messages

Transfers only user and assistant messages, filtering out system messages and tool calls for cleaner context.

```json
{
  "contextEngineeringPlan": {
    "type": "userAndAssistantMessages"
  }
}
```

**Use when**: The receiving assistant needs conversation flow but not internal system details.

### `"none"` -- No Context Transfer

Starts the receiving assistant with a completely blank conversation. No history is transferred.

```json
{
  "contextEngineeringPlan": {
    "type": "none"
  }
}
```

**Use when**: The receiving assistant should start fresh, or when context is passed via variables instead.

---

## Variable Extraction During Handoffs

Extract structured data from the conversation during transfers to pass specific context between assistants:

```json
{
  "type": "handoff",
  "function": {
    "name": "handoff_to_OrderProcessing",
    "description": "customer is ready to place an order",
    "parameters": {
      "type": "object",
      "properties": {
        "destination": {
          "type": "string",
          "enum": ["order-processing-assistant-id"]
        },
        "customerName": {
          "type": "string",
          "description": "Full name of the customer"
        },
        "email": {
          "type": "string",
          "format": "email",
          "description": "Customer's email address"
        },
        "productIds": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of product IDs customer wants to order"
        }
      },
      "required": ["destination", "customerName", "productIds"]
    }
  },
  "destinations": [
    {
      "type": "assistant",
      "assistantName": "order-processing-assistant",
      "description": "customer is ready to place an order",
      "contextEngineeringPlan": {
        "type": "all"
      },
      "variableExtractionPlan": {
        "customerName": {
          "type": "conversation",
          "description": "Extract the customer's full name from the conversation"
        },
        "email": {
          "type": "conversation",
          "description": "Extract the customer's email address from the conversation"
        }
      }
    }
  ]
}
```

### Variable Extraction Types

| Type | Description |
|------|-------------|
| `"conversation"` | Extracts information from the conversation history using the LLM |
| `"parameter"` | Uses parameters passed in the handoff function call directly |

### Using Extracted Variables in Receiving Assistant

The receiving assistant can reference extracted variables using double curly braces in its `firstMessage` and system prompt:

```json
{
  "name": "OrderProcessing",
  "firstMessage": "Hello {{customerName}}, I'll help you complete your order.",
  "model": {
    "messages": [
      {
        "role": "system",
        "content": "You are an order processing assistant.\n\n[Customer Info]\n- Name: {{customerName}}\n- Email: {{email}}\n\nAddress the customer by name throughout the conversation."
      }
    ]
  }
}
```

---

## Step-by-Step Handoff Process

The handoff follows this 6-step process:

### Step 1: Trigger Evaluation
The LLM evaluates the conversation and determines that a handoff is needed based on the tool descriptions. The `function.description` and `destinations[].description` fields are critical for accurate routing.

### Step 2: Destination Selection
If there are multiple destinations, the LLM selects the most appropriate one by comparing the user's request against each destination's `description` field.

### Step 3: Variable Extraction
If `variableExtractionPlan` is configured, the system extracts specified variables from the conversation. If `function.parameters` are defined, the LLM fills those parameters as part of the tool call.

### Step 4: Context Transfer
Based on the `contextEngineeringPlan`, the system prepares the conversation history to transfer:
- `"all"`: Full conversation history
- `"lastNMessages"`: Only the last N messages
- `"userAndAssistantMessages"`: Filtered to user/assistant only
- `"none"`: No history transferred

### Step 5: Assistant Switch
The system switches from the current assistant to the destination assistant. If `messages` are configured on the handoff tool, those are spoken to the caller during the transition. If `messages` is `[]` or `null`, the switch is silent.

### Step 6: Continuation
The receiving assistant begins its interaction using:
- Its own system prompt
- The transferred context (per contextEngineeringPlan)
- Any extracted variables (available as `{{variableName}}` in prompts)
- Its `firstMessage` (if configured)

---

## Transfer Modes (Legacy: assistantDestinations)

These transfer modes apply to the older `assistantDestinations` approach on squad members. They control how the conversation history is handled when switching assistants.

### `rolling-history` (Default)

Keeps the entire conversation history and appends the new assistant's system message. The receiving assistant sees everything that happened before.

```json
{
  "members": [
    {
      "assistant": { "name": "Router" },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Support",
          "description": "customer needs help",
          "transferMode": "rolling-history"
        }
      ]
    }
  ]
}
```

### `swap-system-message-in-history`

Replaces the previous assistant's system message with the new assistant's system message while keeping all conversation history intact.

```json
{
  "transferMode": "swap-system-message-in-history"
}
```

### `delete-history`

Starts the new assistant with a completely fresh conversation. No previous messages are carried over.

```json
{
  "transferMode": "delete-history"
}
```

### `swap-system-message-in-history-and-remove-transfer-tool-messages`

Replaces the system message AND removes any transfer tool call messages from the history. This creates the cleanest handoff where the receiving assistant does not see evidence of the transfer.

```json
{
  "transferMode": "swap-system-message-in-history-and-remove-transfer-tool-messages"
}
```

**Note**: For new implementations, use the handoff tool with `contextEngineeringPlan` instead of these legacy transfer modes. The handoff tool provides more granular control.

---

## Best Practices

### 1. Write Clear, Specific Descriptions
The `description` field on each destination is the primary mechanism the LLM uses to decide routing. Make descriptions:
- **Mutually exclusive**: Avoid overlapping conditions
- **Specific**: Include exact trigger conditions
- **Action-oriented**: Describe what the customer wants/needs

**Good**:
```json
"description": "customer is experiencing a billing issue such as incorrect charges, failed payments, or needs a refund"
```

**Bad**:
```json
"description": "customer has a problem"
```

### 2. Use Appropriate Patterns Per Model Provider
- **OpenAI models** (gpt-4o, gpt-4o-mini): Use the **Multiple Tools Pattern** with separate handoff tools per destination
- **Anthropic models** (Claude): Use the **Single Tool Pattern** with multiple destinations in one tool

### 3. Configure Context Engineering Per Destination
Not every destination needs the full conversation history:
- **Sales/Support handoffs**: Use `"all"` for full context
- **Billing/Payment**: Use `"lastNMessages"` with 5-10 messages for recent context only
- **Fresh-start scenarios**: Use `"none"` when the receiving assistant should start clean
- **Clean transfers**: Use `"userAndAssistantMessages"` to filter out internal system details

### 4. Keep Descriptions Mutually Exclusive
When multiple destinations exist, ensure descriptions do not overlap:

```json
"destinations": [
  {
    "description": "customer wants to SCHEDULE, MODIFY, or CANCEL an appointment"
  },
  {
    "description": "customer is experiencing an EMERGENCY or URGENT medical situation"
  },
  {
    "description": "customer has a question about BILLING, INSURANCE, or PAYMENT"
  }
]
```

### 5. Use Variable Extraction for Personalization
Extract key information like names, account numbers, or issue summaries to provide the receiving assistant with structured data it can use immediately.

### 6. Combine with Silent Handoffs
For seamless experiences, pair handoff tools with silent handoff configuration (see silent-handoffs.md).

---

## Legacy: assistantDestinations vs. Handoff Tool

| Feature | `assistantDestinations` (Legacy) | Handoff Tool (Recommended) |
|---------|----------------------------------|---------------------------|
| Context control | Limited transfer modes | Full contextEngineeringPlan |
| Variable extraction | Not supported | variableExtractionPlan |
| Squad-to-squad | Not supported | Supported via squad destinations |
| Custom function names | Not supported | Fully customizable |
| Dynamic routing | Not supported | Supported |
| Configuration level | Squad member level only | Assistant level or via overrides |

**Migration**: Replace `assistantDestinations` arrays on squad members with handoff tools in the assistant's `model.tools` array or use `assistantOverrides` with `tools:append`.

---

Doc ref: https://docs.vapi.ai/squads/handoff
