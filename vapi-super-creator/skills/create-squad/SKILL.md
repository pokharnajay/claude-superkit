---
name: create-squad
description: Create multi-assistant squads in Vapi with handoffs between specialized voice agents. Use when building complex voice workflows that need multiple assistants with different roles, like triage-to-booking or sales-to-support handoffs.
---

# Create Squad

Create multi-assistant squads in Vapi where specialized voice agents hand off calls between each other. Squads enable complex voice workflows such as triage-to-booking, sales-to-support, and multi-department routing.

## Why Squads

Squads split a complex conversation across focused assistants rather than one monolithic agent. Benefits:

- **Reduced hallucination** -- each assistant has a narrow system prompt scoped to its role.
- **Lower costs** -- shorter context windows per assistant mean fewer tokens per turn.
- **Lower latency** -- smaller prompts produce faster responses.
- **Modularity** -- swap, update, or test individual assistants without touching the rest of the workflow.

## Quick Start

### cURL

```bash
curl -X POST https://api.vapi.ai/squad \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Squad",
    "members": [
      {
        "assistant": {
          "name": "Receptionist",
          "firstMessage": "Hello! How can I direct your call today?",
          "model": {
            "provider": "openai",
            "model": "gpt-4.1",
            "messages": [
              {
                "role": "system",
                "content": "You are a receptionist. Determine if the caller needs sales or support, then transfer them to the right department."
              }
            ],
            "tools": [
              {
                "type": "handoff",
                "destinations": [
                  {
                    "type": "assistant",
                    "assistantId": "sales-assistant-id",
                    "description": "Transfer when the caller asks about pricing, plans, or wants to purchase"
                  },
                  {
                    "type": "assistant",
                    "assistantId": "support-assistant-id",
                    "description": "Transfer when the caller has a technical issue or needs help"
                  }
                ]
              }
            ]
          },
          "voice": { "provider": "vapi", "voiceId": "Lily" },
          "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" }
        }
      },
      { "assistantId": "sales-assistant-id" },
      { "assistantId": "support-assistant-id" }
    ]
  }'
```

### TypeScript Server SDK

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const squad = await vapi.squads.create({
  name: "Support Squad",
  members: [
    {
      assistant: {
        name: "Receptionist",
        firstMessage: "Hello! How can I direct your call today?",
        model: {
          provider: "openai",
          model: "gpt-4.1",
          messages: [
            {
              role: "system",
              content:
                "You are a receptionist. Determine if the caller needs sales or support, then transfer them.",
            },
          ],
          tools: [
            {
              type: "handoff",
              destinations: [
                {
                  type: "assistant",
                  assistantId: "sales-assistant-id",
                  description: "Transfer for pricing and purchasing questions",
                },
                {
                  type: "assistant",
                  assistantId: "support-assistant-id",
                  description: "Transfer for technical issues",
                },
              ],
            },
          ],
        },
        voice: { provider: "vapi", voiceId: "Lily" },
        transcriber: { provider: "deepgram", model: "nova-3", language: "en" },
      },
    },
    { assistantId: "sales-assistant-id" },
    { assistantId: "support-assistant-id" },
  ],
});
```

## Squad Structure

### Members

Each squad has an array of `members`. The **first member** in the array is always the one that answers the call.

Members come in two forms:

| Form | Description | Use When |
|------|-------------|----------|
| **Transient** (inline `assistant`) | Assistant config defined directly inside the member object. | Quick prototyping or one-off squads. |
| **Persistent** (reference `assistantId`) | Points to a saved assistant by ID. | Reusable assistants shared across squads. |

**Transient member** -- full config inline:

```json
{
  "assistant": {
    "name": "Receptionist",
    "firstMessage": "Hello! How can I direct your call?",
    "model": { "provider": "openai", "model": "gpt-4.1", "messages": [...] },
    "voice": { "provider": "vapi", "voiceId": "Lily" }
  }
}
```

**Persistent member** -- reference by ID:

```json
{
  "assistantId": "saved-assistant-id"
}
```

> **Important:** For transferring between assistants in a squad, the `name` field on each assistant is **required**. The name is how handoff destinations identify their targets.

### Full Squad JSON Example (from our original config)

```json
{
  "name": "Customer Service Squad",
  "members": [
    {
      "assistantId": "greeting-assistant-id",
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Sales Agent",
          "message": "Let me transfer you to our sales team."
        },
        {
          "type": "assistant",
          "assistantName": "Support Agent",
          "message": "Connecting you with support now."
        }
      ]
    },
    { "assistantId": "sales-assistant-id" },
    { "assistantId": "support-assistant-id" }
  ]
}
```

## Handoff Tools

Handoffs are how one assistant transfers control to another. Add a tool of `type: "handoff"` to the assistant's model tools.

```json
{
  "type": "handoff",
  "destinations": [
    {
      "type": "assistant",
      "assistantId": "target-assistant-id",
      "description": "Clear description of WHEN to transfer. Be specific about trigger conditions."
    }
  ],
  "function": {
    "name": "handoff_to_sales"
  }
}
```

Key points:

- The `description` field is critical -- the LLM uses it to decide **when** to invoke the handoff. Write explicit trigger conditions.
- You can list multiple destinations in a single handoff tool, or use separate handoff tools for each destination.
- The optional `function.name` gives the handoff a human-readable name in logs and analytics.

## Assistant Overrides

When referencing a saved assistant by `assistantId`, you can override any of its properties for this specific squad without modifying the original:

```json
{
  "assistantId": "saved-assistant-id",
  "assistantOverrides": {
    "voice": { "provider": "vapi", "voiceId": "Elliot" },
    "firstMessage": "Overridden greeting for this squad"
  }
}
```

This is useful when the same assistant participates in multiple squads with slightly different behavior.

### Appending Tools via Overrides

To **add** tools (such as handoff tools) to a saved assistant without replacing its existing tools, use the special `tools:append` key:

```json
{
  "assistantId": "saved-assistant-id",
  "assistantOverrides": {
    "tools:append": [
      {
        "type": "handoff",
        "destinations": [
          {
            "type": "assistant",
            "assistantId": "another-assistant-id",
            "description": "Transfer when customer needs billing help"
          }
        ],
        "function": { "name": "handoff_to_billing" }
      }
    ]
  }
}
```

> Without `tools:append`, setting `tools` in overrides would **replace** the assistant's entire tool list. Use `tools:append` to safely add handoff capabilities.

## Member Overrides

`memberOverrides` apply configuration to **all** members in the squad at once. This is useful for enforcing consistent voice, transcriber, or other settings across the entire squad:

```json
{
  "name": "Consistent Voice Squad",
  "members": [
    { "assistantId": "receptionist-id" },
    { "assistantId": "sales-id" },
    { "assistantId": "support-id" }
  ],
  "memberOverrides": {
    "voice": { "provider": "vapi", "voiceId": "Elliot" },
    "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" }
  }
}
```

Member overrides are applied to every member. Per-member `assistantOverrides` take precedence over `memberOverrides` when both are set.

## Using Squads in Calls

### Outbound Call with a Squad

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "squadId": "your-squad-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": { "number": "+11234567890" }
  }'
```

### Transient Squad in a Call

You can also define the entire squad inline when creating a call, without saving it first:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "squad": {
      "members": [
        {
          "assistant": {
            "name": "Greeter",
            "firstMessage": "Hi there!",
            "model": { "provider": "openai", "model": "gpt-4.1", "messages": [...] }
          }
        }
      ]
    },
    "phoneNumberId": "your-phone-number-id",
    "customer": { "number": "+11234567890" }
  }'
```

## Common Patterns

### Clinic Triage to Scheduling

A medical clinic routes callers through a triage assistant that collects symptoms, then hands off to a scheduling assistant that books the appropriate appointment type.

1. **Triage Assistant** -- asks about symptoms, urgency, insurance. When enough info is gathered, hands off.
2. **Scheduling Assistant** -- receives context from triage, books appointment via external tool call to the clinic's EHR system.

### E-commerce: Sales to Support to Returns

An online store routes callers through three specialized departments:

1. **Sales Assistant** -- handles product questions, pricing, upsells. Hands off to Support for existing orders or Returns for return requests.
2. **Support Assistant** -- troubleshoots order issues, tracks shipments. Hands off to Returns if needed.
3. **Returns Assistant** -- processes return requests, generates return labels, handles refund inquiries.

## Best Practices

1. **Keep assistants focused** -- each assistant should handle 1-3 goals maximum. A narrowly scoped system prompt produces better results than a broad one.
2. **Minimize squad size** -- use the fewest members necessary. Every additional member increases complexity and potential failure points.
3. **Write specific handoff descriptions** -- vague descriptions like "transfer when appropriate" lead to incorrect handoffs. Be explicit: "Transfer when the caller asks about pricing, plans, or wants to purchase a subscription."
4. **Mention handoffs in system prompts** -- tell the assistant it can transfer calls. Example: "If the customer needs technical support, use the handoff tool to transfer them."
5. **Use member overrides for consistent settings** -- enforce the same voice, transcriber, or other config across all members with `memberOverrides` instead of repeating config in each member.

## Managing Squads (API)

### List All Squads

```bash
curl https://api.vapi.ai/squad \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get a Squad

```bash
curl https://api.vapi.ai/squad/{squad-id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update a Squad

```bash
curl -X PATCH https://api.vapi.ai/squad/{squad-id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Squad Name",
    "members": [...]
  }'
```

### Delete a Squad

```bash
curl -X DELETE https://api.vapi.ai/squad/{squad-id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Handoff Tool Patterns

The handoff tool configuration differs depending on the model provider.

### Multiple Tools Pattern (OpenAI)

OpenAI models work best with **separate handoff tools per destination**, each with its own `function.name`:

```json
{
  "tools": [
    {
      "type": "handoff",
      "destinations": [{ "type": "assistant", "assistantId": "sales-id", "description": "Transfer for pricing questions" }],
      "function": { "name": "transfer_to_sales" }
    },
    {
      "type": "handoff",
      "destinations": [{ "type": "assistant", "assistantId": "support-id", "description": "Transfer for technical issues" }],
      "function": { "name": "transfer_to_support" }
    }
  ]
}
```

### Single Tool Pattern (Anthropic)

Anthropic models work best with **one handoff tool listing multiple destinations**:

```json
{
  "tools": [
    {
      "type": "handoff",
      "destinations": [
        { "type": "assistant", "assistantId": "sales-id", "description": "Transfer for pricing questions" },
        { "type": "assistant", "assistantId": "support-id", "description": "Transfer for technical issues" }
      ]
    }
  ]
}
```

> See [Handoffs Reference](references/handoffs.md) for complete configuration details including transfer modes and message customization.

## Context Engineering

Control how much conversation history is passed to the receiving assistant during a handoff using `contextEngineeringPlan` on each destination.

| Type | Behavior | Use When |
|------|----------|----------|
| `"all"` | Passes full conversation history | Destination needs complete context (default) |
| `"lastNMessages"` | Passes only the last N messages (set `maxMessages`) | Reduce token usage for long conversations |
| `"none"` | Passes no prior conversation history | Destination starts fresh, no prior context needed |

```json
{
  "type": "assistant",
  "assistantId": "billing-id",
  "description": "Transfer for billing inquiries",
  "contextEngineeringPlan": {
    "type": "lastNMessages",
    "maxMessages": 10
  }
}
```

Use `"all"` when downstream assistants need full caller context (e.g., triage details). Use `"lastNMessages"` for cost optimization in lengthy calls. Use `"none"` when the destination assistant collects its own information from scratch.

## Silent Handoffs

Silent handoffs transfer a call between assistants **without the customer hearing any transfer announcements**, creating a seamless experience where it sounds like one continuous conversation.

To implement silent handoffs, apply these four configuration steps:

1. **Empty first message on the receiving assistant** -- set `"firstMessage": ""` with `firstMessageMode: "assistant-speaks-first-with-model-generated-message"` so the receiving assistant generates a contextual opening instead of a canned greeting.
2. **Empty messages on handoff tools** -- set `"messages": []` on the handoff tool to suppress the default "Transferring you now" announcement.
3. **Suppress transfer language in source prompts** -- add instructions like "Never say you are transferring the caller" to the source assistant's system prompt.
4. **Direct task entry in destination prompts** -- add "Proceed directly to your task without introducing yourself or acknowledging a transfer" to the destination assistant's system prompt.

> See [Silent Handoffs Guide](references/silent-handoffs.md) for complete implementation with full JSON examples.

## Real-World Examples

These patterns demonstrate common squad architectures. Each links to a full reference with complete JSON configurations.

- **Clinic Triage to Scheduling** -- Triage assistant collects symptoms and insurance, then hands off to a scheduling assistant that books the right appointment type via EHR integration.
- **E-commerce Order Management** -- Four-member squad: Sales, Support, Returns, and Billing assistants with cross-department handoffs based on caller intent.
- **Property Management Routing** -- Router assistant directs callers to Maintenance (work orders), Leasing (tours/applications), or Billing (rent payments) specialists.
- **Multilingual Support** -- Language detection router identifies the caller's preferred language, then hands off to a language-specific specialist assistant with the appropriate voice and system prompt.

> See [Squad Examples](references/examples.md) for complete configurations with full JSON.

## References

- [API Reference](references/api-reference.md) — REST API docs for Squads (5 endpoints) with handoff examples
- [Handoffs Guide](references/handoffs.md) — Multiple destinations, transfer modes, context engineering
- [Silent Handoffs](references/silent-handoffs.md) — Seamless transfers without announcements
- [Squad Examples](references/examples.md) — 5 complete real-world patterns (Clinic, E-commerce, Property, Multilingual)
- [Vapi Squads Docs](https://docs.vapi.ai/squads) — Official documentation

## Related Skills

- **create-assistant** -- create the individual assistants that make up squad members.
- **create-tool** -- build custom tools (including handoff tools) for assistants.
- **create-call** -- initiate outbound calls using a squad.
- **setup-webhook** -- receive real-time events (status updates, end-of-call reports) from squad calls.
- **create-workflow** -- for step-based flows; use squads when you need parallel multi-agent routing instead.

## Red Flags — Common Mistakes

| Temptation | Why It Fails |
|------------|-------------|
| "I'll use one assistant for everything" | If you need handoffs, you need a squad. One assistant can't transfer to itself. |
| "Transfer conditions are obvious to the AI" | Without explicit `transferDestinations`, the AI doesn't know WHERE to hand off. Define every path. |
| "The destination assistant will figure out context" | Without `assistantOverrides.firstMessage` or context passing, the destination starts cold. |
| "I'll test the whole squad at once" | Test each assistant individually FIRST, then test the squad. Debugging multi-agent is hard. |
| "Order of members doesn't matter" | The FIRST member is the entry point. Wrong order = wrong greeting. |

## Required Sub-Skills

- **REQUIRED:** `vapi-voice-ai:create-assistant` — Each squad member needs a fully configured assistant
- **REQUIRED:** `vapi-voice-ai:create-tool` — Handoff tools and member-specific tools must be created first
- **RECOMMENDED:** `vapi-voice-ai:setup-webhook` — For event handling across the squad
- **RECOMMENDED:** `vapi-voice-ai:create-call` — Test the squad with a real call
