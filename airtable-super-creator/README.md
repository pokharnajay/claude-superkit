# Airtable Super Creator

Complete Airtable development toolkit for Claude Code — 16 skills, 8 agents, 10 commands covering every Airtable Web API endpoint.

## Installation

```bash
claude install-marketplace github:pokharnajay/claude-superkit
claude install-plugin airtable-super-creator
```

## Skills (16)

| Skill | Description |
|-------|-------------|
| `setup-api-key` | Configure Airtable personal access token |
| `user-info` | Check authenticated user, token scopes (whoami) |
| `bases` | List, create, update, delete bases |
| `tables` | Create, list, update tables |
| `fields` | Create, update 32+ field types |
| `records` | Full CRUD + upsert + batch (10/request) |
| `views` | Create, list, update, delete views |
| `comments` | Record comments with @mention support |
| `webhooks` | Real-time change notifications (7-day expiry) |
| `collaborators` | Base and workspace access management |
| `workspaces` | Workspace creation, deletion, base moves |
| `interfaces` | Interface listing and sharing |
| `attachments` | File upload to records |
| `automations` | Triggers, actions, and scripting |
| `sync` | Data sync pipelines and upsert patterns |
| `enterprise` | Enterprise user/audit management |

## Agents (8)

| Agent | Description |
|-------|-------------|
| `airtable-creator` | **Main orchestrator** — routes to sub-agents, runs verify loop |
| `airtable-base-architect` | Schema design, base creation, data modeling |
| `airtable-record-ops` | Bulk imports, migrations, batch CRUD, deduplication |
| `airtable-field-manager` | Field types, formula writing, rollups, lookups |
| `airtable-interface-builder` | Interface sharing and access management |
| `airtable-admin` | Enterprise, workspaces, webhooks, security audits |
| `airtable-schema-designer` | Quick schema design from requirements |
| `airtable-data-manager` | Data operations (alias for record-ops) |

## Commands (10)

| Command | Description |
|---------|-------------|
| `/create-base` | Create a new Airtable base with tables, fields, and initial schema |
| `/manage-records` | Create, read, update, or delete records |
| `/manage-tables` | Create, list, or update tables |
| `/manage-fields` | Create, list, or update fields |
| `/setup-webhook` | Create and manage webhooks for real-time notifications |
| `/design-schema` | Design an optimal database schema from requirements |
| `/import-data` | Bulk import from CSV, JSON, or external sources |
| `/manage-workspaces` | Create, manage, and organize workspaces |
| `/manage-collaborators` | Add, update, or remove collaborators |
| `/check-token` | Verify token validity, user info, and scopes |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `session-start` | `startup`, `resume`, `clear`, `compact` | Auto-injects Airtable context and checks API key |

## Quick Start

1. Set up your token: `/check-token`
2. Create a base: `/create-base`
3. Add tables and fields: `/manage-tables` → `/manage-fields`
4. Import data: `/import-data`
5. Create views: use the `views` skill
6. Set up webhooks: `/setup-webhook`

## API Coverage

| API Category | Endpoints Covered |
|-------------|-------------------|
| Records | GET, POST (list + create), PATCH, PUT, DELETE (single + batch + upsert) |
| Bases | GET (list + schema), POST, PATCH, DELETE |
| Tables | GET, POST, PATCH |
| Fields | GET, POST, PATCH |
| Views | GET (list + metadata), POST, PATCH, DELETE |
| Comments | GET, POST, PATCH, DELETE |
| Webhooks | GET (list + payloads), POST (create + refresh + enable), DELETE |
| Collaborators | GET, POST, PATCH, DELETE (base + workspace level) |
| Workspaces | POST (create + move base), DELETE, GET (collaborators) |
| Interfaces | GET (list + detail), POST/PATCH/DELETE (collaborators + invite links) |
| Attachments | POST upload (content.airtable.com) |
| Enterprise | GET/PATCH users, grant/revoke admin, claim users, audit logs, export |
| User Info | GET /meta/whoami |

## Requirements

- Airtable personal access token (starts with `pat`)
- Required scopes depend on operation (see `setup-api-key` skill)
- Enterprise endpoints require Enterprise Scale plan
