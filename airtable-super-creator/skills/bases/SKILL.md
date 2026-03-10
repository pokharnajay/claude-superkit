---
name: airtable-bases
description: List bases, get base schema, and create new bases in Airtable. Use when user wants to see their Airtable bases, inspect base structure/schema, or create a new base programmatically. Triggers on "airtable base", "list bases", "base schema", "create base", "airtable workspace".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Bases API

Manage Airtable bases — list all accessible bases, inspect their schema (tables, fields, views), and create new bases programmatically.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base

## Quick Start

### cURL — List All Bases

```bash
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — List All Bases

```python
import requests, os

response = requests.get(
    "https://api.airtable.com/v0/meta/bases",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
bases = response.json()["bases"]
for base in bases:
    print(f"{base['id']}: {base['name']}")
```

## Endpoints

### 1. List Bases

**`GET /v0/meta/bases`**

Returns all bases the token has access to.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `offset` | string | Pagination cursor from previous response |

**Response:**

```json
{
  "bases": [
    {
      "id": "appABC123",
      "name": "Project Tracker",
      "permissionLevel": "create"
    },
    {
      "id": "appDEF456",
      "name": "CRM",
      "permissionLevel": "edit"
    }
  ],
  "offset": "itrXXXXXX/appXXXXXX"
}
```

**Permission levels:** `none`, `read`, `comment`, `edit`, `create`, `owner`

**Paginating through all bases:**

```python
all_bases = []
offset = None

while True:
    params = {}
    if offset:
        params["offset"] = offset
    response = requests.get(
        "https://api.airtable.com/v0/meta/bases",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
        params=params,
    )
    data = response.json()
    all_bases.extend(data["bases"])
    offset = data.get("offset")
    if not offset:
        break
```

### 2. Get Base Schema

**`GET /v0/meta/bases/{baseId}/tables`**

Returns the full schema of a base including all tables, fields, and views.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `include` | array | Optional: `visibleFieldIds` to include visible field IDs per view |

**cURL:**

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Response:**

```json
{
  "tables": [
    {
      "id": "tblABC123",
      "name": "Tasks",
      "description": "Project tasks and assignments",
      "primaryFieldId": "fldXYZ789",
      "fields": [
        {
          "id": "fldXYZ789",
          "name": "Task Name",
          "type": "singleLineText",
          "description": "Name of the task"
        },
        {
          "id": "fldDEF456",
          "name": "Status",
          "type": "singleSelect",
          "options": {
            "choices": [
              {"id": "selABC", "name": "Todo", "color": "blueLight2"},
              {"id": "selDEF", "name": "In Progress", "color": "yellowLight2"},
              {"id": "selGHI", "name": "Done", "color": "greenLight2"}
            ]
          }
        },
        {
          "id": "fldGHI789",
          "name": "Assignee",
          "type": "singleCollaborator"
        },
        {
          "id": "fldJKL012",
          "name": "Due Date",
          "type": "date",
          "options": {
            "dateFormat": {"name": "local", "format": "M/D/YYYY"}
          }
        }
      ],
      "views": [
        {
          "id": "viwABC123",
          "name": "Grid view",
          "type": "grid"
        },
        {
          "id": "viwDEF456",
          "name": "Kanban",
          "type": "kanban"
        }
      ]
    }
  ]
}
```

**Field object properties:**

| Property | Description |
|----------|-------------|
| `id` | Field ID (fldXXX) |
| `name` | Display name |
| `type` | Field type (see fields skill for all types) |
| `description` | Optional description |
| `options` | Type-specific config (choices for select, date format, etc.) |

**View types:** `grid`, `form`, `calendar`, `gallery`, `kanban`, `timeline`, `block`

### 3. Create Base

**`POST /v0/meta/bases`**

Create a new base in a workspace.

**Request Body:**

```json
{
  "name": "New Project",
  "workspaceId": "wspABC123",
  "tables": [
    {
      "name": "Tasks",
      "description": "Project tasks",
      "fields": [
        {
          "name": "Task Name",
          "type": "singleLineText",
          "description": "Name of the task"
        },
        {
          "name": "Status",
          "type": "singleSelect",
          "options": {
            "choices": [
              {"name": "Todo", "color": "blueLight2"},
              {"name": "In Progress", "color": "yellowLight2"},
              {"name": "Done", "color": "greenLight2"}
            ]
          }
        },
        {
          "name": "Due Date",
          "type": "date",
          "options": {
            "dateFormat": {"name": "local", "format": "M/D/YYYY"}
          }
        },
        {
          "name": "Notes",
          "type": "multilineText"
        }
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Base name |
| `workspaceId` | string | Yes | Workspace to create in (wspXXX) |
| `tables` | array | Yes | At least one table definition |
| `tables[].name` | string | Yes | Table name |
| `tables[].description` | string | No | Table description |
| `tables[].fields` | array | Yes | At least one field definition |
| `tables[].fields[].name` | string | Yes | Field name |
| `tables[].fields[].type` | string | Yes | Field type |
| `tables[].fields[].description` | string | No | Field description |
| `tables[].fields[].options` | object | No | Type-specific options |

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Project",
    "workspaceId": "wspABC123",
    "tables": [
      {
        "name": "Tasks",
        "fields": [
          {"name": "Name", "type": "singleLineText"},
          {"name": "Notes", "type": "multilineText"}
        ]
      }
    ]
  }'
```

**Python:**

```python
response = requests.post(
    "https://api.airtable.com/v0/meta/bases",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "New Project",
        "workspaceId": workspace_id,
        "tables": [
            {
                "name": "Tasks",
                "fields": [
                    {"name": "Name", "type": "singleLineText"},
                    {"name": "Notes", "type": "multilineText"},
                ],
            }
        ],
    },
)
new_base = response.json()
print(f"Created base: {new_base['id']}")
```

**Response:**

```json
{
  "id": "appNEW123",
  "name": "New Project",
  "tables": [
    {
      "id": "tblNEW456",
      "name": "Tasks",
      "fields": [
        {"id": "fldNEW789", "name": "Name", "type": "singleLineText"},
        {"id": "fldNEW012", "name": "Notes", "type": "multilineText"}
      ],
      "views": [
        {"id": "viwNEW345", "name": "Grid view", "type": "grid"}
      ]
    }
  ]
}
```

### 4. Update Base

**`PATCH /v0/meta/bases/{baseId}`**

Update a base's name or other properties.

**Request Body:**

```json
{
  "name": "Renamed Project"
}
```

**cURL:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Renamed Project"}'
```

### 5. Delete Base (Enterprise Only)

**`DELETE /v0/meta/bases/{baseId}`**

Permanently delete a base. **This action cannot be undone.**

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/meta/bases/{baseId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Note:** Requires Enterprise Scale plan. Returns HTTP 200 with empty body on success.

## Common Patterns

### Get all table names and IDs from a base

```python
response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
for table in response.json()["tables"]:
    print(f"{table['id']}: {table['name']} ({len(table['fields'])} fields, {len(table['views'])} views)")
```

### Find a base by name

```python
response = requests.get(
    "https://api.airtable.com/v0/meta/bases",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
target = next((b for b in response.json()["bases"] if b["name"] == "My Base"), None)
if target:
    print(f"Found: {target['id']}")
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| List bases | `schema.bases:read` |
| Get base schema | `schema.bases:read` |
| Create base | `schema.bases:write` |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:read` or `schema.bases:write` scope |
| 404 | `NOT_FOUND` | Invalid base ID or workspace ID |
| 422 | `INVALID_REQUEST` | Invalid table/field definition |

## References

For complete API details, see [references/bases-api.md](references/bases-api.md).
