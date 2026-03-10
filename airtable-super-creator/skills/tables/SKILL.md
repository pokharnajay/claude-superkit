---
name: airtable-tables
description: List, create, and update tables within an Airtable base. Use when user wants to view base schema, create new tables, rename tables, or update table metadata. Triggers on "airtable table", "list tables", "create table", "update table", "rename table", "base schema", "table schema".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Tables API

Manage tables within an Airtable base — list all tables (get base schema), create new tables with typed fields, and update table metadata. All endpoints use the base URL `https://api.airtable.com/v0`.

> **Auth:** All requests require `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN` header.
> **Rate limit:** 5 requests/second per base.

## Quick Start

### cURL — List Tables (Get Base Schema)

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — List Tables

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
tables = response.json()["tables"]
```

### cURL — Create Table

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Projects",
    "description": "Track all active projects",
    "fields": [
      {"name": "Name", "type": "singleLineText"},
      {"name": "Status", "type": "singleSelect", "options": {
        "choices": [
          {"name": "To Do", "color": "redLight2"},
          {"name": "In Progress", "color": "yellowLight2"},
          {"name": "Done", "color": "greenLight2"}
        ]
      }},
      {"name": "Due Date", "type": "date", "options": {"dateFormat": {"name": "iso"}}}
    ]
  }'
```

### Python — Create Table

```python
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Projects",
        "description": "Track all active projects",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect", "options": {
                "choices": [
                    {"name": "To Do", "color": "redLight2"},
                    {"name": "In Progress", "color": "yellowLight2"},
                    {"name": "Done", "color": "greenLight2"},
                ]
            }},
            {"name": "Due Date", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
        ],
    },
)
new_table = response.json()
```

## Endpoints

### 1. List Tables (Get Base Schema)

**`GET /v0/meta/bases/{baseId}/tables`**

Returns all tables in a base with their fields and views. This is the same as the "Get base schema" endpoint.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | The ID of the base (e.g., `appABC123`) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `include` | array of strings | Optional. Include additional information. Currently supports `visibleFieldIds` to include field visibility per view. |

**Response:**

```json
{
  "tables": [
    {
      "id": "tblABC123",
      "name": "Projects",
      "description": "Track all active projects",
      "primaryFieldId": "fldXYZ789",
      "fields": [
        {
          "id": "fldXYZ789",
          "name": "Name",
          "type": "singleLineText",
          "description": ""
        },
        {
          "id": "fldDEF456",
          "name": "Status",
          "type": "singleSelect",
          "description": "",
          "options": {
            "choices": [
              {"id": "selABC1", "name": "To Do", "color": "redLight2"},
              {"id": "selABC2", "name": "In Progress", "color": "yellowLight2"},
              {"id": "selABC3", "name": "Done", "color": "greenLight2"}
            ]
          }
        }
      ],
      "views": [
        {
          "id": "viwABC123",
          "name": "Grid view",
          "type": "grid",
          "personalForOwner": null,
          "visibleFieldIds": null
        }
      ]
    }
  ]
}
```

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `tables` | array | Array of table objects |
| `tables[].id` | string | Table ID (e.g., `tblXXX`) |
| `tables[].name` | string | Table name |
| `tables[].description` | string | Table description (may be empty) |
| `tables[].primaryFieldId` | string | Field ID of the primary field |
| `tables[].fields` | array | Array of field objects |
| `tables[].fields[].id` | string | Field ID (e.g., `fldXXX`) |
| `tables[].fields[].name` | string | Field name |
| `tables[].fields[].type` | string | Field type |
| `tables[].fields[].description` | string | Field description |
| `tables[].fields[].options` | object | Type-specific field configuration |
| `tables[].views` | array | Array of view objects |
| `tables[].views[].id` | string | View ID (e.g., `viwXXX`) |
| `tables[].views[].name` | string | View name |
| `tables[].views[].type` | string | View type (`grid`, `form`, `calendar`, `gallery`, `kanban`, `timeline`, `gantt`) |
| `tables[].views[].personalForOwner` | string or null | User ID if view is personal, null otherwise |
| `tables[].views[].visibleFieldIds` | array or null | Visible field IDs (only if `include=visibleFieldIds`) |

**Python — List tables with visible field IDs:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    params={"include": ["visibleFieldIds"]},
)
for table in response.json()["tables"]:
    print(f"Table: {table['name']} ({table['id']})")
    for field in table["fields"]:
        print(f"  Field: {field['name']} ({field['type']})")
```

### 2. Create Table

**`POST /v0/meta/bases/{baseId}/tables`**

Create a new table in a base. You must provide at least one field. If the first field in the array is not a valid primary field type, Airtable automatically creates a `singleLineText` primary field named "Name".

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | The ID of the base (e.g., `appABC123`) |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Table name (1-255 characters) |
| `description` | string | No | Table description |
| `fields` | array | Yes | Array of field objects (at least one required) |
| `fields[].name` | string | Yes | Field name (1-255 characters, unique within table) |
| `fields[].type` | string | Yes | Field type (see references for all types) |
| `fields[].description` | string | No | Field description |
| `fields[].options` | object | Varies | Type-specific configuration (required for some types like `singleSelect`) |

**cURL — Create table with multiple field types:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Team Tasks",
    "description": "Task tracker for the engineering team",
    "fields": [
      {"name": "Task Name", "type": "singleLineText"},
      {"name": "Description", "type": "multilineText"},
      {"name": "Priority", "type": "singleSelect", "options": {
        "choices": [
          {"name": "Critical", "color": "redLight2"},
          {"name": "High", "color": "orangeLight2"},
          {"name": "Medium", "color": "yellowLight2"},
          {"name": "Low", "color": "greenLight2"}
        ]
      }},
      {"name": "Story Points", "type": "number", "options": {"precision": 0}},
      {"name": "Due Date", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
      {"name": "Completed", "type": "checkbox", "options": {"icon": "check", "color": "greenBright"}},
      {"name": "Assignee Email", "type": "email"},
      {"name": "Notes", "type": "richText"}
    ]
  }'
```

**Python — Create table:**

```python
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Team Tasks",
        "description": "Task tracker for the engineering team",
        "fields": [
            {"name": "Task Name", "type": "singleLineText"},
            {"name": "Description", "type": "multilineText"},
            {"name": "Priority", "type": "singleSelect", "options": {
                "choices": [
                    {"name": "Critical", "color": "redLight2"},
                    {"name": "High", "color": "orangeLight2"},
                    {"name": "Medium", "color": "yellowLight2"},
                    {"name": "Low", "color": "greenLight2"},
                ]
            }},
            {"name": "Story Points", "type": "number", "options": {"precision": 0}},
            {"name": "Due Date", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
            {"name": "Completed", "type": "checkbox", "options": {"icon": "check", "color": "greenBright"}},
            {"name": "Assignee Email", "type": "email"},
            {"name": "Notes", "type": "richText"},
        ],
    },
)
new_table = response.json()
print(f"Created table: {new_table['id']}")
```

**Response:**

```json
{
  "id": "tblNEW123",
  "name": "Team Tasks",
  "description": "Task tracker for the engineering team",
  "primaryFieldId": "fldPRI001",
  "fields": [
    {
      "id": "fldPRI001",
      "name": "Task Name",
      "type": "singleLineText"
    },
    {
      "id": "fldFLD002",
      "name": "Description",
      "type": "multilineText"
    },
    {
      "id": "fldFLD003",
      "name": "Priority",
      "type": "singleSelect",
      "options": {
        "choices": [
          {"id": "selOPT1", "name": "Critical", "color": "redLight2"},
          {"id": "selOPT2", "name": "High", "color": "orangeLight2"},
          {"id": "selOPT3", "name": "Medium", "color": "yellowLight2"},
          {"id": "selOPT4", "name": "Low", "color": "greenLight2"}
        ]
      }
    }
  ],
  "views": [
    {
      "id": "viwDEF456",
      "name": "Grid view",
      "type": "grid"
    }
  ]
}
```

**Notes:**
- The first field in the array becomes the primary field if its type is valid as a primary field (`singleLineText`, `email`, `url`, `singleSelect`, `number`, `currency`, `percent`, `autoNumber`, `barcode`, `phoneNumber`).
- If the first field type is not valid as a primary field, a `singleLineText` primary field named "Name" is auto-created.
- A default "Grid view" is automatically created.
- Each field in the response includes an assigned `id`.
- Select field choices in the response include assigned `id` values.

### 3. Update Table

**`PATCH /v0/meta/bases/{baseId}/tables/{tableId}`**

Update a table's name and/or description. You cannot delete a table, add/remove fields, or reorder fields through this endpoint. Use the Fields API to manage fields.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | The ID of the base (e.g., `appABC123`) |
| `tableId` | string | The ID of the table (e.g., `tblABC123`) |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | New table name (1-255 characters) |
| `description` | string | No | New table description (use `null` to clear) |

**cURL — Rename a table:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Active Projects"}'
```

**cURL — Update description:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "All currently active projects for Q1 2025"}'
```

**cURL — Clear description:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": null}'
```

**Python — Rename a table:**

```python
response = requests.patch(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={"name": "Active Projects"},
)
updated_table = response.json()
print(f"Renamed to: {updated_table['name']}")
```

**Python — Update name and description:**

```python
response = requests.patch(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Active Projects",
        "description": "Tracks all active engineering projects",
    },
)
```

**Response:**

```json
{
  "id": "tblABC123",
  "name": "Active Projects",
  "description": "Tracks all active engineering projects",
  "primaryFieldId": "fldXYZ789",
  "fields": [
    {
      "id": "fldXYZ789",
      "name": "Name",
      "type": "singleLineText"
    }
  ],
  "views": [
    {
      "id": "viwABC123",
      "name": "Grid view",
      "type": "grid"
    }
  ]
}
```

**Limitations:**
- Cannot delete a table via the API.
- Cannot add or remove fields — use the Fields API (`POST /v0/meta/bases/{baseId}/tables/{tableId}/fields`).
- Cannot reorder fields via this endpoint.
- Cannot change the primary field type.

## Common Patterns

### Create a table with multiple field types

```python
import requests, os

def create_project_table(base_id):
    """Create a fully configured project tracking table."""
    return requests.post(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
        headers={
            "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        },
        json={
            "name": "Project Tracker",
            "description": "Central project management table",
            "fields": [
                {"name": "Project Name", "type": "singleLineText"},
                {"name": "Description", "type": "multilineText"},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Planning", "color": "blueLight2"},
                        {"name": "In Progress", "color": "yellowLight2"},
                        {"name": "Review", "color": "orangeLight2"},
                        {"name": "Complete", "color": "greenLight2"},
                    ]
                }},
                {"name": "Priority", "type": "rating", "options": {"max": 5, "icon": "star", "color": "yellowBright"}},
                {"name": "Budget", "type": "currency", "options": {"precision": 2, "symbol": "$"}},
                {"name": "Start Date", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
                {"name": "Website", "type": "url"},
                {"name": "Contact Email", "type": "email"},
                {"name": "Active", "type": "checkbox", "options": {"icon": "check", "color": "greenBright"}},
            ],
        },
    ).json()
```

### Rename a table

```python
def rename_table(base_id, table_id, new_name):
    """Rename a table."""
    return requests.patch(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}",
        headers={
            "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        },
        json={"name": new_name},
    ).json()
```

### List all tables and their field counts

```python
def list_tables_summary(base_id):
    """Print a summary of all tables in a base."""
    response = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    )
    for table in response.json()["tables"]:
        print(f"{table['name']} ({table['id']}): {len(table['fields'])} fields, {len(table['views'])} views")
```

## Required Scopes

| Scope | Operations |
|-------|-----------|
| `schema.bases:read` | List tables (get base schema) |
| `schema.bases:write` | Create table, update table |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:read` or `schema.bases:write` scope |
| 404 | `NOT_FOUND` | Invalid base ID or table ID |
| 422 | `INVALID_REQUEST` | Invalid table name, duplicate field names, or invalid field options |
| 422 | `CANNOT_CREATE_FIELD_TYPE` | The specified field type cannot be created via the API |
| 422 | `DUPLICATE_TABLE_NAME` | A table with that name already exists in the base |
| 422 | `INVALID_FIELD_TYPE` | Unrecognized or unsupported field type |
| 422 | `INVALID_FIELD_OPTIONS` | Field options do not match the expected schema for the field type |
| 429 | `TOO_MANY_REQUESTS` | Rate limited, retry after 30s |
| 500 | `SERVER_ERROR` | Internal server error, retry with exponential backoff |

## References

For complete field type options, color values, and detailed request/response schemas, see [references/tables-api.md](references/tables-api.md).
