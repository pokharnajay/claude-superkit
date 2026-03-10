---
name: interfaces
description: List and manage Airtable interfaces, add interface collaborators, and create invite links. Use when the user wants to view interfaces, share interfaces with team members, or manage interface access permissions.
---

# Airtable Interfaces

Manage Airtable interfaces — custom app-like views built on top of your base data.

## Endpoints

### List Interfaces

```
GET https://api.airtable.com/v0/meta/bases/{baseId}/interfaces
```

**Response:**
```json
{
  "interfaces": [
    {
      "id": "pbdXXXXXXXXXXXXXX",
      "name": "Project Dashboard",
      "description": "Overview of all active projects",
      "createdTime": "2024-01-15T10:30:00.000Z"
    },
    {
      "id": "pbdYYYYYYYYYYYYYY",
      "name": "Employee Directory",
      "description": "Searchable team directory"
    }
  ]
}
```

**cURL:**
```bash
curl -s -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  "https://api.airtable.com/v0/meta/bases/{baseId}/interfaces" | python3 -m json.tool
```

### Get Interface

```
GET https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}
```

**Response:**
```json
{
  "id": "pbdXXXXXXXXXXXXXX",
  "name": "Project Dashboard",
  "description": "Overview of all active projects",
  "createdTime": "2024-01-15T10:30:00.000Z"
}
```

### Add Interface Collaborator

```
POST https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}/collaborators
```

**Request Body (by email):**
```json
{
  "email": "user@example.com",
  "permissionLevel": "editor"
}
```

**Request Body (by userId):**
```json
{
  "userId": "usrXXXXXXXXXXXXXX",
  "permissionLevel": "editor"
}
```

### Update Interface Collaborator

```
PATCH https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}/collaborators/{userId}
```

**Request Body:**
```json
{
  "permissionLevel": "commenter"
}
```

### Remove Interface Collaborator

```
DELETE https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}/collaborators/{userId}
```

### Create Interface Invite Link

```
POST https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}/inviteLinks
```

**Request Body:**
```json
{
  "permissionLevel": "editor"
}
```

**Response:**
```json
{
  "id": "invXXXXXXXXXXXXXX",
  "url": "https://airtable.com/invite/...",
  "permissionLevel": "editor",
  "createdTime": "2024-01-15T10:30:00.000Z"
}
```

### Delete Interface Invite Link

```
DELETE https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}/inviteLinks/{inviteLinkId}
```

## Interface Permission Levels

| Level | Can Do |
|-------|--------|
| `owner` | Full control, manage collaborators, delete interface |
| `editor` | Edit interface layout and configuration |
| `commenter` | View and comment |
| `viewer` | View only |

## Interface Types

Airtable interfaces can include these layout components:

| Component | Description |
|-----------|-------------|
| Grid | Table view of records |
| Detail | Single record detail view |
| Form | Record creation/editing form |
| Chart | Bar, line, pie, scatter charts |
| Number | Single metric/KPI display |
| Timeline | Gantt-style timeline |
| Gallery | Card-based gallery view |
| Kanban | Board with draggable cards |
| Button | Action buttons |
| Text | Rich text content blocks |

## Common Patterns

### Share Interface with External Team

```bash
# 1. List interfaces to find the right one
curl -s -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  "https://api.airtable.com/v0/meta/bases/{baseId}/interfaces" | python3 -m json.tool

# 2. Create an invite link for viewers
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/interfaces/{interfaceId}/inviteLinks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"permissionLevel": "viewer"}'

# 3. Share the returned URL with external users
```

### Audit Interface Access

```bash
# List all interfaces and their collaborators
curl -s -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  "https://api.airtable.com/v0/meta/bases/{baseId}/interfaces" | python3 -c "
import sys, json
interfaces = json.load(sys.stdin)['interfaces']
for iface in interfaces:
    print(f\"Interface: {iface['name']} ({iface['id']})\")"
```

## Important Notes

- Interfaces are created and designed through the Airtable UI (not the API)
- The API supports listing interfaces and managing their collaborators/sharing
- Interface layout and component configuration is UI-only
- Interfaces inherit base-level data access — collaborators see data based on their base permissions
