# Claude Superkit

A marketplace of Claude Code plugin bundles — installable skill packs that extend Claude Code with domain-specific superpowers.

## Bundles

| Bundle | Description | Skills | Agents | Commands |
|--------|-------------|--------|--------|----------|
| [airtable-super-creator](airtable-super-creator/) | Complete Airtable development toolkit — manage bases, tables, fields, records, views, webhooks, and more via the Airtable Web API | 16 | 8 | 10 |
| [vapi-super-creator](vapi-super-creator/) | Complete voice AI toolkit for Vapi — build assistants, tools, squads, workflows, phone numbers, and webhooks | 18 | 5 | 7 |

## Installation

**Step 1:** Register the marketplace (one-time):

```bash
claude plugin marketplace add pokharnajay/claude-superkit
```

**Step 2:** Install the plugins you want:

```bash
claude plugin install airtable-super-creator@claude-superkit
claude plugin install vapi-super-creator@claude-superkit
```

## Repository Structure

```
claude-superkit/
├── airtable-super-creator/   # Airtable plugin bundle
│   ├── .claude-plugin/
│   ├── skills/               # 16 skills
│   ├── agents/               # 8 agents
│   ├── commands/             # 10 commands
│   ├── hooks/
│   └── docs/
├── vapi-super-creator/       # Vapi voice AI plugin bundle
│   ├── .claude-plugin/
│   ├── skills/               # 18 skills
│   ├── agents/               # 5 agents
│   ├── commands/             # 7 commands
│   ├── hooks/
│   └── docs/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace manifest
├── LICENSE
└── README.md
```

## License

MIT — see [LICENSE](LICENSE) for details.
