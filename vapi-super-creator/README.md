# Vapi Super Creator

Complete voice AI development toolkit for [Vapi](https://vapi.ai). Build, configure, test, and manage voice assistants, tools, squads, workflows, phone numbers, webhooks, and more.

## Structure

```
vapi-super-creator/
├── .claude-plugin/          # Plugin metadata
│   └── plugin.json
├── hooks/                   # Session lifecycle hooks
│   ├── hooks.json           # SessionStart hook config
│   └── session-start        # Auto-injects Vapi context + API key check
├── commands/                # CLI shortcuts (7 commands)
│   ├── create-assistant.md
│   ├── create-tool.md
│   ├── create-squad.md
│   ├── create-call.md
│   ├── create-workflow.md
│   ├── setup-webhook.md
│   └── verify-setup.md
├── agents/                  # Specialized sub-agents (5 agents)
│   ├── vapi-creator.md          # Main orchestrator + verifier
│   ├── vapi-assistant-builder.md # Full assistant lifecycle
│   ├── vapi-tool-builder.md     # Tool creation + server setup
│   ├── vapi-call-manager.md     # Calls, campaigns, analytics
│   └── vapi-infrastructure.md   # API keys, webhooks, phone numbers
├── skills/                  # Core skills library (18 skills)
│   ├── create-assistant/    # Voice assistant creation (+ 5 reference files)
│   ├── create-tool/         # Custom tools & integrations (+ 10 reference files)
│   ├── create-call/         # Outbound & batch calls
│   ├── create-squad/        # Multi-assistant handoffs (+ 4 reference files)
│   ├── create-phone-number/ # Phone number provisioning
│   ├── create-workflow/     # Visual conversation flows
│   ├── setup-api-key/       # API key & environment setup
│   ├── setup-webhook/       # Server URLs & event handling
│   ├── manage-analytics/    # Call & subscription analytics
│   ├── manage-campaigns/    # Outbound calling campaigns
│   ├── manage-chats/        # Text-based chat conversations
│   ├── manage-evals/        # Assistant performance testing
│   ├── manage-files/        # Knowledge base file management
│   ├── manage-insights/     # Reporting & dashboards
│   ├── manage-provider-resources/ # Voice pronunciation, etc.
│   ├── manage-scorecards/   # Call quality scoring
│   ├── manage-sessions/     # Persistent conversation sessions
│   └── manage-structured-outputs/ # Post-call data extraction
├── docs/                    # Documentation
│   └── IMPROVEMENTS.md      # Prioritized improvement roadmap
└── README.md                # This file
```

## Quick Start

1. Ensure your Vapi API key is configured (use `setup-api-key` skill)
2. Create an assistant: `/create-assistant`
3. Add tools: `/create-tool`
4. Test with a call: `/create-call`
5. Verify everything: `/verify-setup`

## Workflow

```
setup-api-key → create-assistant → create-tool → setup-webhook → create-phone-number → create-call
```

## Design Principles

- **Discipline Enforcement** — Red Flags tables prevent common mistakes
- **Composition** — Skills cross-reference each other with REQUIRED markers
- **Verification** — Never declare done without a clean verification pass
- **Progressive Disclosure** — SKILL.md overview + references/ for deep details

## Version

1.0.0
