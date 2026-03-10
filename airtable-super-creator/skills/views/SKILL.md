---
name: airtable-views
description: List views and get view metadata in Airtable tables. Use when user wants to see available views, inspect view configuration, or find specific view types. Triggers on "airtable view", "list views", "view metadata", "grid view", "kanban view", "gallery view".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Views API

List views in a table and retrieve detailed view metadata including field order, filters, sorts, and groupings.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base

## Quick Start

### cURL — List Views

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/views" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — List Views

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/views",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
views = response.json()["views"]
for view in views:
    print(f"{view['id']}: {view['name']} ({view['type']})")
```

## Endpoints

### 1. List Views

**`GET /v0/meta/bases/{baseId}/tables/{tableId}/views`**

Returns all views in a table with basic metadata.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | Base ID (appXXX) |
| `tableId` | string | Table ID (tblXXX) |

**Response:**

```json
{
  "views": [
    {
      "id": "viwABC123",
      "name": "Grid view",
      "type": "grid",
      "personalForNonOwner": false
    },
    {
      "id": "viwDEF456",
      "name": "Project Board",
      "type": "kanban",
      "personalForNonOwner": false
    },
    {
      "id": "viwGHI789",
      "name": "Photo Gallery",
      "type": "gallery",
      "personalForNonOwner": true
    }
  ]
}
```

**View properties:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | View ID (viwXXX) |
| `name` | string | Display name of the view |
| `type` | string | View type (see types below) |
| `personalForNonOwner` | boolean | If `true`, view is personal and only visible to the owner; other users see a default personal version |

**View types:**

| Type | Description |
|------|-------------|
| `grid` | Spreadsheet-style rows and columns (default view type) |
| `form` | Form for submitting new records |
| `calendar` | Records displayed on a calendar by date field |
| `gallery` | Card-based layout showing record thumbnails |
| `kanban` | Board with records grouped into stacked columns |
| `timeline` | Gantt-style timeline visualization |
| `block` | Interface/dashboard block view |

### 2. Get View Metadata

**`GET /v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}`**

Returns detailed metadata for a single view, including visible fields, filters, sorts, and group configuration.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | Base ID (appXXX) |
| `tableId` | string | Table ID (tblXXX) |
| `viewId` | string | View ID (viwXXX) |

**cURL:**

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/views/{view_id}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
view = response.json()
print(f"View: {view['name']} ({view['type']})")
if "visibleFieldIds" in view:
    print(f"Visible fields: {view['visibleFieldIds']}")
```

**Response (grid view example):**

```json
{
  "id": "viwABC123",
  "name": "Active Tasks",
  "type": "grid",
  "personalForNonOwner": false,
  "visibleFieldIds": [
    "fldXYZ789",
    "fldDEF456",
    "fldGHI789",
    "fldJKL012"
  ],
  "filters": {
    "conjunction": "and",
    "filterSet": [
      {
        "fieldId": "fldDEF456",
        "operator": "=",
        "value": "Active"
      }
    ]
  },
  "sorts": [
    {
      "fieldId": "fldJKL012",
      "direction": "asc"
    }
  ],
  "groupLevels": [
    {
      "fieldId": "fldDEF456",
      "direction": "asc"
    }
  ]
}
```

**Response properties:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | View ID |
| `name` | string | View display name |
| `type` | string | View type |
| `personalForNonOwner` | boolean | Whether the view is personal |
| `visibleFieldIds` | array | Ordered list of field IDs visible in this view |
| `filters` | object | Filter configuration (if any filters are applied) |
| `filters.conjunction` | string | `"and"` or `"or"` |
| `filters.filterSet` | array | Array of filter conditions |
| `sorts` | array | Sort configuration (if any sorts are applied) |
| `groupLevels` | array | Grouping configuration (if any groups are applied) |

> **Note:** The `filters`, `sorts`, and `groupLevels` properties are only present when the view has those configurations. Not all view types support all properties.

### 3. Create View

**`POST /v0/meta/bases/{baseId}/tables/{tableId}/views`**

Create a new view in a table.

**Request Body:**

```json
{
  "name": "Active Tasks",
  "type": "grid"
}
```

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/views" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Active Tasks", "type": "grid"}'
```

**View types for creation:** `grid`, `form`, `calendar`, `gallery`, `kanban`, `timeline`

### 4. Update View

**`PATCH /v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}`**

Update a view's name or other properties.

**Request Body:**

```json
{
  "name": "Renamed View"
}
```

**cURL:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Renamed View"}'
```

### 5. Delete View

**`DELETE /v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}`**

Permanently delete a view.

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Note:** Cannot delete the last remaining view in a table.

## Common Patterns

### List all views across all tables in a base

```python
import requests, os

headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

# First, get all tables in the base
tables_resp = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers=headers,
)
tables = tables_resp.json()["tables"]

# Then list views for each table
for table in tables:
    views_resp = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table['id']}/views",
        headers=headers,
    )
    views = views_resp.json()["views"]
    print(f"\nTable: {table['name']} ({table['id']})")
    for view in views:
        print(f"  {view['id']}: {view['name']} ({view['type']})")
```

### Find a view by name

```python
def find_view_by_name(base_id, table_id, view_name, token):
    response = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/views",
        headers={"Authorization": f"Bearer {token}"},
    )
    views = response.json()["views"]
    return next((v for v in views if v["name"] == view_name), None)

view = find_view_by_name(base_id, table_id, "Active Tasks", os.environ["AIRTABLE_ACCESS_TOKEN"])
if view:
    print(f"Found view: {view['id']}")
```

### Get visible fields for a view with field names

```python
# Get view metadata
view_resp = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/views/{view_id}",
    headers=headers,
)
view = view_resp.json()

# Get table schema for field name lookup
schema_resp = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
    headers=headers,
)
tables = schema_resp.json()["tables"]
table = next(t for t in tables if t["id"] == table_id)
field_map = {f["id"]: f["name"] for f in table["fields"]}

# Print visible fields in order
if "visibleFieldIds" in view:
    for fid in view["visibleFieldIds"]:
        print(f"  {fid}: {field_map.get(fid, 'Unknown')}")
```

### Find all kanban views in a base

```python
def find_views_by_type(base_id, view_type, token):
    headers = {"Authorization": f"Bearer {token}"}
    tables_resp = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
        headers=headers,
    )
    results = []
    for table in tables_resp.json()["tables"]:
        views_resp = requests.get(
            f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table['id']}/views",
            headers=headers,
        )
        for view in views_resp.json()["views"]:
            if view["type"] == view_type:
                results.append({"table": table["name"], "view": view})
    return results

kanban_views = find_views_by_type(base_id, "kanban", os.environ["AIRTABLE_ACCESS_TOKEN"])
for item in kanban_views:
    print(f"Table: {item['table']}, View: {item['view']['name']}")
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| List views | `schema.bases:read` |
| Get view metadata | `schema.bases:read` |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:read` scope |
| 404 | `NOT_FOUND` | Invalid base ID, table ID, or view ID |
| 404 | `TABLE_NOT_FOUND` | Table does not exist in the specified base |
| 404 | `VIEW_NOT_FOUND` | View does not exist in the specified table |

## References

For complete API response schemas and view type details, see [references/views-api.md](references/views-api.md).
