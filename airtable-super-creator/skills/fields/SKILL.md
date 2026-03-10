---
name: airtable-fields
description: List, create, and update fields in Airtable tables, with a complete field type reference. Use when user wants to inspect table columns, add new fields, modify field options, or understand field types and their schemas. Triggers on "airtable field", "list fields", "create field", "update field", "field type", "field model", "add column".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Fields API

List, create, and update fields (columns) in Airtable tables. Includes a comprehensive reference for every field type and its options.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base

## Quick Start

### cURL — List All Fields in a Table

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — List All Fields in a Table

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
fields = response.json()["fields"]
for field in fields:
    print(f"{field['id']}: {field['name']} ({field['type']})")
```

### cURL — Create a Single Select Field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priority",
    "type": "singleSelect",
    "description": "Task priority level",
    "options": {
      "choices": [
        {"name": "Low", "color": "blueLight2"},
        {"name": "Medium", "color": "yellowLight2"},
        {"name": "High", "color": "redLight2"}
      ]
    }
  }'
```

## Endpoints

### 1. List Fields

**`GET /v0/meta/bases/{baseId}/tables/{tableId}/fields`**

Returns all fields in a table with their IDs, names, types, descriptions, and options.

**Response:**

```json
{
  "fields": [
    {
      "id": "fldABC123",
      "name": "Task Name",
      "type": "singleLineText",
      "description": "Primary task identifier"
    },
    {
      "id": "fldDEF456",
      "name": "Status",
      "type": "singleSelect",
      "options": {
        "choices": [
          {"id": "selABC", "name": "Todo", "color": "blueLight2"},
          {"id": "selDEF", "name": "Done", "color": "greenLight2"}
        ]
      }
    },
    {
      "id": "fldGHI789",
      "name": "Due Date",
      "type": "date",
      "options": {
        "dateFormat": {"name": "local", "format": "M/D/YYYY"}
      }
    }
  ]
}
```

**Field object properties:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Field ID (`fldXXX`) |
| `name` | string | Display name of the field |
| `type` | string | Field type identifier (see field-types reference) |
| `description` | string | Optional human-readable description |
| `options` | object | Type-specific configuration (choices, format, etc.) |

### 2. Create Field

**`POST /v0/meta/bases/{baseId}/tables/{tableId}/fields`**

Creates a new field in a table.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display name of the field |
| `type` | string | Yes | Field type (e.g., `singleLineText`, `number`, `singleSelect`) |
| `description` | string | No | Human-readable description |
| `options` | object | Depends on type | Type-specific configuration |

**Example — Create a text field:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Notes", "type": "multilineText", "description": "Additional notes"}'
```

**Example — Create a number field:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Price",
    "type": "currency",
    "options": {
      "precision": 2,
      "symbol": "$"
    }
  }'
```

**Example — Create a date field:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Start Date",
    "type": "date",
    "options": {
      "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"}
    }
  }'
```

**Example — Create a linked record field:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Related Tasks",
    "type": "multipleRecordLinks",
    "options": {
      "linkedTableId": "tblTARGET123"
    }
  }'
```

**Example — Create an attachments field:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Files", "type": "multipleAttachments"}'
```

**Response:** Returns the created field object with its generated `id`.

```json
{
  "id": "fldNEW123",
  "name": "Priority",
  "type": "singleSelect",
  "description": "Task priority level",
  "options": {
    "choices": [
      {"id": "selABC", "name": "Low", "color": "blueLight2"},
      {"id": "selDEF", "name": "Medium", "color": "yellowLight2"},
      {"id": "selGHI", "name": "High", "color": "redLight2"}
    ]
  }
}
```

### 3. Update Field

**`PATCH /v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}`**

Update an existing field's name, description, or type-specific options.

**Important constraints:**
- You **can** update: `name`, `description`
- Some types allow updating `options` (e.g., adding new select choices)
- You **cannot** change a field's `type` after creation
- You **cannot** delete fields via the API

**Request Body:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | New display name |
| `description` | string | New description |
| `options` | object | Updated type-specific options (varies by type) |

**cURL — Rename a field:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Task Priority", "description": "Updated priority field"}'
```

**cURL — Add new choices to a select field:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "options": {
      "choices": [
        {"id": "selABC", "name": "Low", "color": "blueLight2"},
        {"id": "selDEF", "name": "Medium", "color": "yellowLight2"},
        {"id": "selGHI", "name": "High", "color": "redLight2"},
        {"name": "Critical", "color": "redDark1"}
      ]
    }
  }'
```

**Note:** When updating select choices, you must include **all existing choices** (with their `id`s) plus any new ones. Omitting an existing choice does not delete it.

**Python — Update a field:**

```python
response = requests.patch(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields/{field_id}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Task Priority",
        "description": "Updated description",
    },
)
updated_field = response.json()
```

## Common Patterns

### Add a select field with choices

```python
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Status",
        "type": "singleSelect",
        "options": {
            "choices": [
                {"name": "Backlog", "color": "blueLight2"},
                {"name": "In Progress", "color": "yellowLight2"},
                {"name": "Review", "color": "purpleLight2"},
                {"name": "Done", "color": "greenLight2"},
            ]
        },
    },
)
```

### Add a linked record field

```python
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Assigned Projects",
        "type": "multipleRecordLinks",
        "options": {
            "linkedTableId": target_table_id,
            "prefersSingleRecordLink": False,
        },
    },
)
```

### Add a formula field

```python
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Full Name",
        "type": "formula",
        "options": {
            "expression": "CONCATENATE({First Name}, ' ', {Last Name})",
        },
    },
)
```

### List all fields and group by type

```python
from collections import defaultdict

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
fields = response.json()["fields"]

by_type = defaultdict(list)
for f in fields:
    by_type[f["type"]].append(f["name"])

for ftype, names in sorted(by_type.items()):
    print(f"{ftype}: {', '.join(names)}")
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| List fields | `schema.bases:read` |
| Create field | `schema.bases:write` |
| Update field | `schema.bases:write` |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:read` or `schema.bases:write` scope |
| 404 | `NOT_FOUND` | Invalid base ID, table ID, or field ID |
| 422 | `INVALID_REQUEST` | Invalid field definition, unsupported type, or bad options |
| 422 | `CANNOT_CHANGE_FIELD_TYPE` | Attempted to change a field's type |
| 422 | `FIELD_NAME_ALREADY_EXISTS` | A field with that name already exists in the table |
| 422 | `CANNOT_DELETE_FIELD` | Field deletion is not supported via API |

## References

- For complete API parameter details, see [references/fields-api.md](references/fields-api.md).
- For the full field type reference (all 32 types), see [references/field-types.md](references/field-types.md).
