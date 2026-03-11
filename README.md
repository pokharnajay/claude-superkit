# Claude Superkit

A marketplace of Claude Code plugin bundles — installable skill packs that extend Claude Code with domain-specific superpowers.

## Bundles

| Bundle | Description | Skills | Agents | Commands |
|--------|-------------|--------|--------|----------|
| [airtable-super-creator](airtable-super-creator/) | Complete Airtable development toolkit — manage bases, tables, fields, records, views, webhooks, and more via the Airtable Web API | 16 | 8 | 10 |
| [vapi-super-creator](vapi-super-creator/) | Complete voice AI toolkit for Vapi — build assistants, tools, squads, workflows, phone numbers, and webhooks | 18 | 5 | 7 |
| [canvas-design](canvas-design/) | Museum-quality visual art — 20+ formats, 80+ fonts, procedural noise/textures, curated palettes, composition frameworks | 1 | — | — |

## Installation

**Step 1:** Register the marketplace (one-time):

```bash
claude plugin marketplace add pokharnajay/claude-superkit
```

**Step 2:** Install the plugins you want:

```bash
# Install for all projects (user scope — default)
claude plugin install airtable-super-creator@claude-superkit
claude plugin install vapi-super-creator@claude-superkit
claude plugin install canvas-design@claude-superkit

# Install for the current project only (shared via git)
claude plugin install airtable-super-creator@claude-superkit --scope project
claude plugin install vapi-super-creator@claude-superkit --scope project
claude plugin install canvas-design@claude-superkit --scope project

# Install locally (not shared with team)
claude plugin install airtable-super-creator@claude-superkit --scope local
claude plugin install vapi-super-creator@claude-superkit --scope local
claude plugin install canvas-design@claude-superkit --scope local
```

### Installation Scopes

| Scope | Stored in | Shared via git? | Use case |
|-------|-----------|-----------------|----------|
| `user` (default) | `~/.claude/plugins/` | No | Personal — available in all your projects |
| `project` | `.claude/plugins/` in project root | Yes | Team — everyone who clones the repo gets it |
| `local` | `.claude/plugins/` (gitignored) | No | Personal per-project — only you, only this project |

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
# Install a plugin (default: user scope)
claude plugin install plugin-name@marketplace-name

# Install with a specific scope
claude plugin install plugin-name@marketplace-name --scope user      # all projects (default)
claude plugin install plugin-name@marketplace-name --scope project   # current project, shared via git
claude plugin install plugin-name@marketplace-name --scope local     # current project, not shared

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

# Disable with a specific scope
claude plugin disable plugin-name@marketplace-name --scope project

# Disable all plugins at once
claude plugin disable --all

# Re-enable a disabled plugin
claude plugin enable plugin-name@marketplace-name

# Re-enable with a specific scope
claude plugin enable plugin-name@marketplace-name --scope project
```

### Validate

```bash
# Validate a plugin or marketplace structure
claude plugin validate ./path-to-plugin-or-marketplace
```

### Load Plugins for a Single Session

```bash
# Use a local plugin directory without installing (great for development/testing)
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
├── canvas-design/            # Visual art & design plugin
│   ├── .claude-plugin/
│   ├── skills/               # 1 skill + 80+ fonts
│   └── docs/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace manifest
├── LICENSE
└── README.md
```

## Links

- **GitHub:** [pokharnajay/claude-superkit](https://github.com/pokharnajay/claude-superkit)
- **Notion:** [Claude Skills - SuperKit](https://www.notion.so/Claude-Skills-SuperKit-32011c9d2b3981129409d244cf2e5475)

<!-- Notion Page ID: 32011c9d-2b39-8112-9409-d244cf2e5475 -->

## License

MIT — see [LICENSE](LICENSE) for details.
