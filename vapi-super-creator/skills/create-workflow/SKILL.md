---
name: create-workflow
description: Build visual conversation workflows in Vapi with nodes for conversation steps, tool execution, conditional branching, and handoffs. Use when creating structured multi-step voice interactions that need deterministic flow control beyond what a single assistant prompt provides.
---

# Create Workflows

> **Note:** Vapi recommends using Assistants or Squads for most use cases. Workflows are still supported but may be deprecated in the future. Consider whether your use case truly requires deterministic node-based flow control before choosing workflows over a well-prompted assistant.

This skill covers building conversation workflows in Vapi using the visual workflow editor and API. Workflows provide deterministic, node-based control over multi-step voice interactions.

## When to Use Workflows vs Assistants

| Criteria | Assistant | Workflow |
|----------|-----------|----------|
| Conversation style | Open-ended, flexible | Structured, deterministic steps |
| Flow control | LLM decides next action via prompt | Explicit node-to-node transitions |
| Best for | Customer support, general Q&A, conversational AI | Appointment booking, lead qualification, structured surveys |
| Complexity | Single prompt + tools | Visual node graph with conditions |
| Model per step | One model for entire call | Different model/voice per node |
| Variable extraction | Via tool calls | Built-in per-node variable extraction |
| Setup effort | Lower (prompt engineering) | Higher (node design + conditions) |

**Rule of thumb:** If you can describe the conversation flow as a flowchart with clear branching, use a workflow. If the conversation needs to be flexible and adaptive, use an assistant.

## Prerequisites

- Vapi account with API key configured (see the `setup-api-key` skill)
- For API-based workflows: understanding of Vapi's node/edge JSON structure

## Quick Start via Dashboard

1. Open [Vapi Dashboard](https://dashboard.vapi.ai) > **Workflows** tab.
2. Click **Create Workflow**.
3. You will see a visual canvas with a starting **Conversation Node**.
4. Add nodes by clicking the **+** button or dragging from the node palette.
5. Connect nodes by dragging edges between them and defining conditions.
6. Configure each node's prompt, voice, model, and variables.
7. Click **Save** to publish the workflow.

## Using a Workflow in a Call

Once saved, attach a workflow to an outbound call:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "workflowId": "your-workflow-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+14155551234"
    }
  }'
```

> See the `create-call` skill for more call creation options.

## Node Types

### Conversation Node

The default and most configurable node type. Serves as the main building block for conversation flows.

**Configuration options:**
- **First Message** — The initial spoken message when entering this node.
- **Prompt** — Detailed system instructions guiding the assistant's responses within this node.
- **Model** — LLM provider and model (can differ per node).
- **Voice** — TTS provider and voice (can differ per node).
- **Transcriber** — STT provider and settings.
- **Extract Variables** — Gather variables from the conversation using liquid syntax `{{ variable_name }}`.

```
Example: A "Greeting" node with firstMessage = "Welcome! Are you calling about
a new appointment or an existing one?" and extract variable: appointment_type
(enum: ["new", "existing"])
```

### Tool Node

Integrates pre-created tools from your Tools library. Select a tool to execute at this point in the flow, then route based on the result.

**Use cases:**
- Check appointment availability
- Look up customer records
- Submit form data to your backend

### API Request Node

Make HTTP requests to external APIs or automation services directly from the workflow, without needing a pre-created tool.

### Transfer Call Node

Transfer the call to a phone number or human agent. Configure:
- Phone number destination
- Transfer plan with a message or call summary for the receiving agent

### End Call Node

Terminal node that explicitly ends the call. Configure an optional goodbye message.

### Global Node

A special node that can be reached from **any point** in the workflow. Commonly used for:
- Human escalation ("I want to talk to a person")
- Emergency routing
- Universal fallback handling

Configure with:
- **Global toggle** enabled
- **Enter Condition** defining when to route to this node (e.g., "User asked to speak with a human agent")

## Conditions & Edges

Nodes are connected via **edges** that specify conditions for conversation flow. There are three types:

### AI-Based Conditions

Written in plain language and evaluated by the LLM:

```
User wants to schedule a new appointment
```

```
User is frustrated or asking for a manager
```

### Logical Conditions

For precise control using extracted variables:

```
{{ appointment_type == "new" }}
```

```
{{ customer_tier == "VIP" }}
```

### Combined Conditions

Mix logical operators with variables:

```
{{ customer_tier == "VIP" or total_orders > 50 }}
```

**Best practices for conditions:**
- Use descriptive natural language for AI-based conditions.
- Format as: "User [verb] [rest of condition]".
- Extract variables as enums to enable reliable branching.
- Test all conditional paths thoroughly.
- Keep conditions simple and specific.

## Variable Extraction

Variables extracted in Conversation Nodes can be used throughout the workflow via liquid syntax `{{ variable_name }}`.

Configure variables by:
- Defining variable **name** and **data type** (String, Number, Boolean, Integer).
- Writing clear **extraction prompts** that tell the LLM what to extract.
- Setting **enums** for String-type variables to constrain values (e.g., `["new", "existing", "cancel"]`).

Variables persist across nodes and can be referenced in prompts, conditions, and tool parameters.

## Workflow Patterns

### Appointment Scheduling

```
[Greeting] --> (new appt?) --> [Collect Date] --> [Check Availability] --> [Confirm Booking]
     |                                                     |
     +--> (existing?) --> [Lookup Appointment] --> [Modify/Cancel]
     |
     +--> (other) --> [General FAQ] --> [End Call]
```

**Nodes:**
1. **Greeting** (Conversation) — Ask new or existing appointment. Extract: `intent` (enum: new, existing, other).
2. **Collect Date** (Conversation) — Ask preferred date/time. Extract: `preferred_date`, `preferred_time`.
3. **Check Availability** (Tool) — Call your scheduling API with extracted variables.
4. **Confirm Booking** (Conversation) — Present available slots, confirm selection.
5. **Lookup Appointment** (Tool) — Fetch existing appointment by phone number.
6. **Modify/Cancel** (Conversation) — Handle changes or cancellation.

### Lead Qualification

```
[Intro] --> [Company Size] --> [Budget] --> [Timeline] --> [Qualified?]
                                                              |
                                                   (yes) --> [Book Demo]
                                                   (no)  --> [Send Resources] --> [End]
```

**Nodes:**
1. **Intro** (Conversation) — Introduce and ask about their needs. Extract: `use_case`.
2. **Company Size** (Conversation) — Ask company size. Extract: `company_size` (enum: small, medium, enterprise).
3. **Budget** (Conversation) — Ask budget range. Extract: `budget_range`.
4. **Timeline** (Conversation) — Ask decision timeline. Extract: `timeline`.
5. **Qualified?** — Logical condition: `{{ company_size == "enterprise" or budget_range == "high" }}`.
6. **Book Demo** (Conversation + Tool) — Schedule a demo via your calendar API.
7. **Send Resources** (Tool) — Email marketing materials via API.

### Support Triage

```
[Greeting] --> [Identify Issue] --> (billing?) --> [Billing Support]
                                --> (technical?) --> [Tech Support]
                                --> (account?) --> [Account Help]
                                --> (human?) --> [Transfer to Agent]
                                                      ^
                                                      | (Global Node - reachable from anywhere)
```

**Nodes:**
1. **Greeting** (Conversation) — Identify the issue category. Extract: `issue_type` (enum: billing, technical, account, other).
2. **Billing Support** (Conversation) — Handle billing questions with billing-specific prompt.
3. **Tech Support** (Conversation) — Troubleshoot technical issues with different model/voice.
4. **Account Help** (Conversation) — Handle account changes.
5. **Transfer to Agent** (Global + Transfer Call) — Always reachable. Transfers to human support number.

## Attaching Workflows to Phone Numbers

Assign a workflow to handle all inbound calls on a phone number:

```bash
curl -X PATCH https://api.vapi.ai/phone-number/<phone-number-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "workflowId": "your-workflow-id"
  }'
```

> See the `create-phone-number` skill for phone number management.

## Attaching Workflows in Outbound Calls

Use a workflow for outbound calls by referencing it in the call creation:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "workflowId": "your-workflow-id",
    "phoneNumberId": "your-phone-number-id",
    "customer": {
      "number": "+14155551234"
    }
  }'
```

You can also combine workflows with scheduled and batch calls:

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "workflowId": "your-workflow-id",
    "phoneNumberId": "your-phone-number-id",
    "customers": [
      { "number": "+14155551234" },
      { "number": "+14155555678" }
    ],
    "schedulePlan": {
      "earliestAt": "2026-03-10T09:00:00Z"
    }
  }'
```

## Tips & Best Practices

- **Start simple** — Begin with 2-3 nodes and expand. Complex workflows are harder to debug.
- **Use enums** — Extract variables as enums whenever possible for reliable branching.
- **Test each path** — Use the Dashboard's test call feature to walk through every branch.
- **Global nodes for escalation** — Always include a global escalation node so users can reach a human from any point.
- **Keep node prompts focused** — Each node should have a clear, narrow purpose. Long prompts in workflow nodes defeat the purpose of structured flows.
- **Variable naming** — Use descriptive, snake_case variable names (e.g., `preferred_date`, `issue_type`).

## Related Skills

- See the `setup-api-key` skill if you need to configure your API key first.
- See the `create-assistant` skill for the simpler prompt-based approach (recommended for most use cases).
- See the `create-squad` skill for multi-assistant handoffs without workflow nodes.
- See the `create-tool` skill to build tools that workflow Tool Nodes can reference.
- See the `create-call` skill for making calls with workflows attached.
- See the `create-phone-number` skill to set up numbers for inbound workflow calls.
