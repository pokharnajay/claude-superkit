# Claude Superkit

A monorepo of Claude Code plugin bundles — installable skill packs that extend Claude Code with domain-specific superpowers.

## Bundles

| Bundle | Description | Skills | Agents | Commands |
|--------|-------------|--------|--------|----------|
| [airtable-super-creator](airtable-super-creator/) | Complete Airtable development toolkit — manage bases, tables, fields, records, views, webhooks, and more via the Airtable Web API | 16 | 8 | 10 |
| [vapi-super-creator](vapi-super-creator/) | Complete voice AI toolkit for Vapi — build assistants, tools, squads, workflows, phone numbers, and webhooks | 18 | 5 | 7 |

## Installation

Install a bundle directly from GitHub:

```bash
claude install-plugin github:pokharnajay/claude-superkit/airtable-super-creator
claude install-plugin github:pokharnajay/claude-superkit/vapi-super-creator
```

## Repository Structure

```
claude-superkit/
├── airtable-super-creator/   # Airtable plugin bundle
│   ├── .claude-plugin/
│   ├── skills/
│   ├── agents/
│   ├── commands/
│   ├── hooks/
│   └── docs/
├── vapi-super-creator/       # Vapi voice AI plugin bundle
│   ├── .claude-plugin/
│   ├── skills/
│   ├── agents/
│   ├── commands/
│   ├── hooks/
│   └── docs/
├── LICENSE
└── README.md
```

## License

MIT — see [LICENSE](LICENSE) for details.
