---
name: workspaces
description: Create, manage, and delete Airtable workspaces. Move bases between workspaces, manage workspace collaborators, and organize your Airtable organization structure. Use when the user wants to create workspaces, move bases, or manage workspace-level access.
---

# Airtable Workspaces

Manage Airtable workspaces — the organizational containers that hold bases.

## Endpoints

### Create Workspace

```
POST https://api.airtable.com/v0/meta/workspaces
```

**Request Body:**
```json
{
  "name": "Marketing Team"
}
```

**Response:**
```json
{
  "id": "wspXXXXXXXXXXXXXX",
  "name": "Marketing Team"
}
```

**cURL:**
```bash
curl -X POST "https://api.airtable.com/v0/meta/workspaces" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Marketing Team"}'
```

### Delete Workspace (Enterprise Only)

```
DELETE https://api.airtable.com/v0/meta/workspaces/{workspaceId}
```

**cURL:**
```bash
curl -X DELETE "https://api.airtable.com/v0/meta/workspaces/{workspaceId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Note:** Only available for enterprise accounts. Workspace must be empty (no bases) before deletion.

### List Workspace Collaborators (Enterprise Only)

```
GET https://api.airtable.com/v0/meta/workspaces/{workspaceId}/collaborators
```

**Response:**
```json
{
  "collaborators": [
    {
      "userId": "usrXXXXXXXXXXXXXX",
      "email": "user@example.com",
      "permissionLevel": "owner"
    },
    {
      "userId": "usrYYYYYYYYYYYYYY",
      "email": "teammate@example.com",
      "permissionLevel": "create"
    }
  ]
}
```

### Add Workspace Collaborator

```
POST https://api.airtable.com/v0/meta/workspaces/{workspaceId}/collaborators
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "permissionLevel": "create"
}
```

### Move Base to Workspace

```
POST https://api.airtable.com/v0/meta/workspaces/{targetWorkspaceId}/moveBase
```

**Request Body:**
```json
{
  "baseId": "appXXXXXXXXXXXXXX"
}
```

## Permission Levels

| Level | Can Do |
|-------|--------|
| `owner` | Full control, manage collaborators, delete workspace |
| `create` | Create bases, edit, comment, read |
| `edit` | Edit records in existing bases, comment, read |
| `comment` | Comment on records, read |
| `read` | View only |

## Workspace Best Practices

1. **One workspace per team/department** — keeps access management clean
2. **Name workspaces descriptively** — "Engineering", "Marketing", "Sales Ops"
3. **Use workspace-level permissions** — instead of per-base permissions when possible
4. **Move bases** instead of recreating — preserves data and automations
5. **Audit collaborators regularly** — remove departed team members

## Common Patterns

### Organize by Department

```
Company Workspace (owner: admin@company.com)
├── Engineering Workspace
│   ├── Bug Tracker Base
│   ├── Sprint Planning Base
│   └── Architecture Docs Base
├── Marketing Workspace
│   ├── Content Calendar Base
│   ├── Campaign Tracker Base
│   └── Brand Assets Base
└── Sales Workspace
    ├── CRM Base
    ├── Pipeline Base
    └── Contracts Base
```

### Migrate Base Between Workspaces

```bash
# 1. Find the base ID
curl -s -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  https://api.airtable.com/v0/meta/bases | python3 -c "
import sys, json
for b in json.load(sys.stdin)['bases']:
    print(f\"{b['id']}: {b['name']}\")
"

# 2. Move to target workspace
curl -X POST "https://api.airtable.com/v0/meta/workspaces/{targetWorkspaceId}/moveBase" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"baseId": "appXXXXXXXXXXXXXX"}'
```
