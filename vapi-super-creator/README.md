# Vapi Super Creator

Complete voice AI development toolkit for Claude Code and [Vapi](https://vapi.ai) — 18 skills, 5 agents, 7 commands to build, configure, test, and manage voice assistants.

## Installation

```bash
claude plugin marketplace add github:pokharnajay/claude-superkit
claude plugin install vapi-super-creator@claude-superkit
```

## Skills (18)

| Skill | Description |
|-------|-------------|
| `setup-api-key` | Obtain and configure Vapi API key |
| `create-assistant` | Create voice AI assistants with models, voices, transcribers, tools, and hooks |
| `create-tool` | Build function tools, API request tools, transfer/end call tools, and integrations |
| `create-call` | Create outbound phone calls, web calls, and batch calls |
| `create-squad` | Multi-assistant squads with handoffs between specialized agents |
| `create-workflow` | Visual conversation workflows with branching and tool nodes |
| `create-phone-number` | Provision and manage phone numbers (Twilio, Vonage, Telnyx, Vapi) |
| `setup-webhook` | Configure server URLs and webhooks for real-time call events |
| `manage-analytics` | Query call and subscription analytics — costs, duration, concurrency |
| `manage-campaigns` | Outbound calling campaigns at scale |
| `manage-chats` | Text-based chat conversations using assistants, squads, or workflows |
| `manage-evals` | Test assistant performance with mock conversations and scoring |
| `manage-files` | Upload and manage knowledge base files |
| `manage-insights` | Reporting dashboards with charts, metrics, and formulas |
| `manage-provider-resources` | Pronunciation dictionaries for Cartesia and ElevenLabs |
| `manage-scorecards` | Observability scorecards for call quality scoring |
| `manage-sessions` | Persistent conversation sessions across multiple calls or chats |
| `manage-structured-outputs` | Extract structured data from conversations using AI or regex |

## Agents (5)

| Agent | Description |
|-------|-------------|
| `vapi-creator` | **Main orchestrator** — verifies configurations and routes to sub-agents |
| `vapi-assistant-builder` | Full assistant lifecycle — build from scratch or modify existing |
| `vapi-tool-builder` | Tool creation, tool servers, and external API integrations |
| `vapi-call-manager` | Outbound calls, campaigns, testing, and call analytics |
| `vapi-infrastructure` | API keys, phone numbers, webhooks, file uploads, provider configs |

## Commands (7)

| Command | Description |
|---------|-------------|
| `/create-assistant` | Create a Vapi voice AI assistant with model, voice, and tools |
| `/create-tool` | Create custom tools (function, API, transfer, end call, integrations) |
| `/create-call` | Create outbound phone calls, web calls, and batch calls |
| `/create-squad` | Create multi-assistant squads with handoffs |
| `/create-workflow` | Build visual conversation workflows with branching |
| `/setup-webhook` | Configure server URLs and webhooks for call events |
| `/verify-setup` | Verify all Vapi resources are correctly configured |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `session-start` | `startup`, `resume`, `clear`, `compact` | Auto-injects Vapi context and checks API key |

## Quick Start

1. Set up your API key: use the `setup-api-key` skill
2. Create an assistant: `/create-assistant`
3. Add tools: `/create-tool`
4. Set up webhooks: `/setup-webhook`
5. Provision a phone number: use the `create-phone-number` skill
6. Test with a call: `/create-call`
7. Verify everything: `/verify-setup`

## Workflow

```
setup-api-key → create-assistant → create-tool → setup-webhook → create-phone-number → create-call → verify-setup
```

## Design Principles

- **Discipline Enforcement** — Red Flags tables prevent common mistakes
- **Composition** — Skills cross-reference each other with REQUIRED markers
- **Verification** — Never declare done without a clean verification pass
- **Progressive Disclosure** — SKILL.md overview + references/ for deep details

## Requirements

- Vapi API key (get one at [vapi.ai](https://vapi.ai))
- Phone number provider account (Twilio/Vonage/Telnyx) for inbound calls
