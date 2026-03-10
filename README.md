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

## CLI Reference

### Marketplace Management

```bash
# Add a marketplace (one-time registration)
claude plugin marketplace add owner/repo

# List all registered marketplaces
claude plugin marketplace list

# Update all marketplaces (fetch latest from GitHub)
claude plugin marketplace update

# Update a specific marketplace
claude plugin marketplace update claude-superkit

# Remove a marketplace
claude plugin marketplace remove claude-superkit
```

### Plugin Management

```bash
# Install a plugin from a marketplace
claude plugin install plugin-name@marketplace-name

# Install with a specific scope (user, project, or local)
claude plugin install plugin-name@marketplace-name --scope project

# List all installed plugins
claude plugin list

# Update a plugin to the latest version (restart required)
claude plugin update plugin-name@marketplace-name

# Uninstall a plugin
claude plugin uninstall plugin-name@marketplace-name
```

### Enable / Disable Plugins

```bash
# Temporarily disable a plugin (without uninstalling)
claude plugin disable plugin-name@marketplace-name

# Disable all plugins at once
claude plugin disable --all

# Re-enable a disabled plugin
claude plugin enable plugin-name@marketplace-name
```

### Validate

```bash
# Validate a plugin or marketplace structure
claude plugin validate ./path-to-plugin-or-marketplace
```

### Load Plugins for a Single Session

```bash
# Use a local plugin directory without installing
claude --plugin-dir ./path-to-plugin
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
