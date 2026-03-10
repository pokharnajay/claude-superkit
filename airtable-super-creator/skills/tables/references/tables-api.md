# Airtable Tables API — Complete Reference

Comprehensive reference for all table management endpoints, field types, field options schemas, color values, and error codes.

**Base URL:** `https://api.airtable.com/v0`

---

## Endpoints

### 1. List Tables (Get Base Schema)

**`GET /v0/meta/bases/{baseId}/tables`**

**Required scope:** `schema.bases:read`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (e.g., `appABC123`) |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include` | array | No | Additional data to include. Currently supports `visibleFieldIds`. |

#### Response Schema

```json
{
  "tables": [
    {
      "id": "tblXXXXXX",
      "name": "string",
      "description": "string",
      "primaryFieldId": "fldXXXXXX",
      "fields": [
        {
          "id": "fldXXXXXX",
          "name": "string",
          "type": "string",
          "description": "string",
          "options": {}
        }
      ],
      "views": [
        {
          "id": "viwXXXXXX",
          "name": "string",
          "type": "grid | form | calendar | gallery | kanban | timeline | gantt",
          "personalForOwner": "usrXXXXXX | null",
          "visibleFieldIds": ["fldXXXXXX"]
        }
      ]
    }
  ]
}
```

**Notes:**
- `visibleFieldIds` is only populated when `include=visibleFieldIds` is passed.
- `personalForOwner` is `null` for shared views, or a user ID for personal views.
- `options` is omitted for field types that have no configurable options.
- `description` may be an empty string or omitted.

---

### 2. Create Table

**`POST /v0/meta/bases/{baseId}/tables`**

**Required scope:** `schema.bases:write`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (e.g., `appABC123`) |

#### Request Body Schema

```json
{
  "name": "string (required, 1-255 chars)",
  "description": "string (optional)",
  "fields": [
    {
      "name": "string (required, 1-255 chars)",
      "type": "string (required)",
      "description": "string (optional)",
      "options": {}
    }
  ]
}
```

**Constraints:**
- `name` is required and must be unique within the base.
- `fields` array must contain at least one field.
- Field names must be unique within the table.
- The first field becomes the primary field if its type is eligible (see Primary Field Types below).
- If the first field type is not eligible as a primary field, a `singleLineText` field named "Name" is auto-created as the primary field.

#### Primary Field Eligible Types

The following types are allowed as the primary field (first field):

- `singleLineText`
- `email`
- `url`
- `singleSelect`
- `number`
- `currency`
- `percent`
- `autoNumber`
- `barcode`
- `phoneNumber`

#### Response Schema

Same structure as List Tables response, but for a single table:

```json
{
  "id": "tblXXXXXX",
  "name": "string",
  "description": "string",
  "primaryFieldId": "fldXXXXXX",
  "fields": [
    {
      "id": "fldXXXXXX",
      "name": "string",
      "type": "string",
      "description": "string",
      "options": {}
    }
  ],
  "views": [
    {
      "id": "viwXXXXXX",
      "name": "Grid view",
      "type": "grid"
    }
  ]
}
```

---

### 3. Update Table

**`PATCH /v0/meta/bases/{baseId}/tables/{tableId}`**

**Required scope:** `schema.bases:write`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (e.g., `appABC123`) |
| `tableId` | string | Yes | Table ID (e.g., `tblABC123`) |

#### Request Body Schema

```json
{
  "name": "string (optional, 1-255 chars)",
  "description": "string | null (optional)"
}
```

At least one field must be provided. Pass `null` as the description value to clear it.

#### Response Schema

Full table object (same as Create Table response), reflecting the updated state.

#### Limitations

- Cannot delete a table through the API.
- Cannot add, remove, or reorder fields (use the Fields API).
- Cannot change the primary field or its type.

---

## Supported Field Types

The following field types can be used when creating tables (in the `fields[].type` property).

### Text Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `singleLineText` | Single-line text input | No |
| `multilineText` | Multi-line text area | No |
| `richText` | Rich text with formatting | No |
| `email` | Email address | No |
| `url` | URL/web address | No |
| `phoneNumber` | Phone number | No |

### Numeric Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `number` | Numeric value | Yes (`precision`) |
| `percent` | Percentage value | Yes (`precision`) |
| `currency` | Currency value | Yes (`precision`, `symbol`) |
| `rating` | Star/icon rating | Yes (`max`, `icon`, `color`) |
| `duration` | Time duration | Yes (`durationFormat`) |
| `autoNumber` | Auto-incrementing number | No |

### Selection Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `singleSelect` | Single choice dropdown | Yes (`choices`) |
| `multipleSelects` | Multi-choice tags | Yes (`choices`) |
| `checkbox` | Boolean toggle | Yes (`icon`, `color`) |

### Date/Time Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `date` | Date only | Yes (`dateFormat`) |
| `dateTime` | Date and time | Yes (`dateFormat`, `timeFormat`, `timeZone`) |
| `createdTime` | Auto-set creation timestamp | Yes (`result` with format config) |
| `lastModifiedTime` | Auto-set modification timestamp | Yes (`result` with format config, optional `fieldIdsThatCanSetTimestamp`) |

### Relationship Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `multipleRecordLinks` | Link to records in another table | Yes (`linkedTableId`, optionally `prefersSingleRecordLink`, `inverseLinkFieldId`) |
| `lookup` | Lookup values from linked records | Yes (`fieldIdInLinkedTable`, `recordLinkFieldId`) |
| `count` | Count linked records | Yes (`recordLinkFieldId`) |

### Collaborator Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `singleCollaborator` | Single user/collaborator | No |
| `multipleCollaborators` | Multiple users/collaborators | No |
| `createdBy` | Auto-set record creator | No |
| `lastModifiedBy` | Auto-set last modifier | Yes (optional `fieldIdsThatCanSetTimestamp`) |

### Computed Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `formula` | Computed formula result | Yes (`expression`, `result`) |
| `rollup` | Aggregate linked record values | Yes (`fieldIdInLinkedTable`, `recordLinkFieldId`, `result`) |

### Other Fields

| Type | Description | Options Required |
|------|-------------|------------------|
| `multipleAttachments` | File attachments | Yes (`isReversed`) |
| `barcode` | Barcode/QR code value | No |
| `button` | Clickable button | No (configured in UI) |
| `externalSyncSource` | External sync source indicator | No (read-only, auto-managed) |

---

## Field Options Schemas

### `number`

```json
{
  "precision": 0
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `precision` | integer | `0` - `8` | Number of decimal places |

### `percent`

```json
{
  "precision": 0
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `precision` | integer | `0` - `8` | Number of decimal places |

### `currency`

```json
{
  "precision": 2,
  "symbol": "$"
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `precision` | integer | `0` - `7` | Number of decimal places |
| `symbol` | string | Any string | Currency symbol (e.g., `$`, `EUR`, `GBP`) |

### `singleSelect`

```json
{
  "choices": [
    {
      "name": "Option A",
      "color": "blueLight2"
    },
    {
      "name": "Option B",
      "color": "greenLight2"
    }
  ]
}
```

| Option | Type | Description |
|--------|------|-------------|
| `choices` | array | Array of choice objects |
| `choices[].name` | string | Choice display name (required) |
| `choices[].color` | string | Color name (optional, see Color Options) |
| `choices[].id` | string | Choice ID (read-only, assigned by API) |

### `multipleSelects`

Same schema as `singleSelect`:

```json
{
  "choices": [
    {"name": "Tag A", "color": "redLight2"},
    {"name": "Tag B", "color": "blueLight2"}
  ]
}
```

### `checkbox`

```json
{
  "icon": "check",
  "color": "greenBright"
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `icon` | string | `"check"`, `"xCheckbox"`, `"star"`, `"heart"`, `"thumbsUp"`, `"flag"`, `"dot"` | Icon to display |
| `color` | string | `"greenBright"`, `"tealBright"`, `"cyanBright"`, `"blueBright"`, `"purpleBright"`, `"pinkBright"`, `"redBright"`, `"orangeBright"`, `"yellowBright"`, `"grayBright"` | Icon color |

### `rating`

```json
{
  "max": 5,
  "icon": "star",
  "color": "yellowBright"
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `max` | integer | `1` - `10` | Maximum rating value |
| `icon` | string | `"star"`, `"heart"`, `"thumbsUp"`, `"flag"`, `"dot"` | Icon to display |
| `color` | string | Same as checkbox colors | Icon color |

### `date`

```json
{
  "dateFormat": {
    "name": "iso"
  }
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `dateFormat.name` | string | `"local"`, `"friendly"`, `"us"`, `"european"`, `"iso"` | Date display format |

Format examples:
- `"local"` — uses browser locale
- `"friendly"` — January 15, 2025
- `"us"` — 1/15/2025
- `"european"` — 15/1/2025
- `"iso"` — 2025-01-15

### `dateTime`

```json
{
  "dateFormat": {
    "name": "iso"
  },
  "timeFormat": {
    "name": "24hour"
  },
  "timeZone": "America/New_York"
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `dateFormat.name` | string | Same as `date` | Date display format |
| `timeFormat.name` | string | `"12hour"`, `"24hour"` | Time display format |
| `timeZone` | string | IANA timezone | Timezone (e.g., `"America/New_York"`, `"UTC"`, `"Europe/London"`) |

### `duration`

```json
{
  "durationFormat": "h:mm"
}
```

| Option | Type | Values | Description |
|--------|------|--------|-------------|
| `durationFormat` | string | `"h:mm"`, `"h:mm:ss"`, `"h:mm:ss.S"`, `"h:mm:ss.SS"`, `"h:mm:ss.SSS"` | Duration display format |

### `multipleRecordLinks`

```json
{
  "linkedTableId": "tblABC123",
  "prefersSingleRecordLink": false,
  "inverseLinkFieldId": "fldDEF456"
}
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `linkedTableId` | string | Yes | ID of the table to link to |
| `prefersSingleRecordLink` | boolean | No | If `true`, UI limits selection to one record (default `false`) |
| `inverseLinkFieldId` | string | No | Field ID of the corresponding link field in the linked table (read-only on create; auto-generated) |

### `lookup`

```json
{
  "fieldIdInLinkedTable": "fldABC123",
  "recordLinkFieldId": "fldDEF456",
  "result": {
    "type": "singleLineText"
  }
}
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `fieldIdInLinkedTable` | string | Yes | Field ID in the linked table to look up |
| `recordLinkFieldId` | string | Yes | ID of the `multipleRecordLinks` field in this table |
| `result` | object | No | Describes the result type; read-only, populated by API |

### `rollup`

```json
{
  "fieldIdInLinkedTable": "fldABC123",
  "recordLinkFieldId": "fldDEF456",
  "referencedFieldIds": ["fldABC123"],
  "result": {
    "type": "number",
    "options": {
      "precision": 0
    }
  }
}
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `fieldIdInLinkedTable` | string | Yes | Field ID in the linked table to aggregate |
| `recordLinkFieldId` | string | Yes | ID of the `multipleRecordLinks` field in this table |
| `referencedFieldIds` | array | No | Read-only; field IDs referenced by the rollup |
| `result` | object | No | Describes the result type and its options |

### `count`

```json
{
  "isValid": true,
  "recordLinkFieldId": "fldABC123"
}
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `recordLinkFieldId` | string | Yes | ID of the `multipleRecordLinks` field to count |
| `isValid` | boolean | No | Read-only; indicates if the count field is properly configured |

### `formula`

```json
{
  "expression": "IF({Status}='Done', 1, 0)",
  "referencedFieldIds": ["fldABC123"],
  "result": {
    "type": "number",
    "options": {
      "precision": 0
    }
  }
}
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `expression` | string | Yes | Airtable formula expression |
| `referencedFieldIds` | array | No | Read-only; field IDs referenced in the formula |
| `result` | object | No | Describes the computed result type |

### `multipleAttachments`

```json
{
  "isReversed": false
}
```

| Option | Type | Description |
|--------|------|-------------|
| `isReversed` | boolean | Whether attachments display in reverse order |

### `createdTime`

```json
{
  "result": {
    "type": "dateTime",
    "options": {
      "dateFormat": {"name": "iso"},
      "timeFormat": {"name": "24hour"},
      "timeZone": "UTC"
    }
  }
}
```

### `lastModifiedTime`

```json
{
  "isValid": true,
  "referencedFieldIds": [],
  "fieldIdsThatCanSetTimestamp": ["fldABC123", "fldDEF456"],
  "result": {
    "type": "dateTime",
    "options": {
      "dateFormat": {"name": "iso"},
      "timeFormat": {"name": "24hour"},
      "timeZone": "UTC"
    }
  }
}
```

| Option | Type | Description |
|--------|------|-------------|
| `fieldIdsThatCanSetTimestamp` | array or null | Field IDs that trigger timestamp update. `null` or empty means all fields trigger it. |
| `result` | object | Date/time format configuration |

### `lastModifiedBy`

```json
{
  "fieldIdsThatCanSetTimestamp": null
}
```

| Option | Type | Description |
|--------|------|-------------|
| `fieldIdsThatCanSetTimestamp` | array or null | Field IDs that trigger collaborator update. `null` means all fields trigger it. |

### `singleCollaborator` / `multipleCollaborators`

No options required. Values are collaborator objects:

```json
{
  "id": "usrABC123",
  "email": "user@example.com",
  "name": "User Name"
}
```

### `barcode`

No options required. Values are barcode objects:

```json
{
  "text": "1234567890",
  "type": "upce"
}
```

### `button`

Button fields cannot be fully configured via the API. They are configured in the Airtable UI. The API returns:

```json
{
  "label": "Open URL",
  "style": "default"
}
```

### `externalSyncSource`

This field type is read-only and auto-managed by Airtable sync features. It cannot be created or modified via the API.

---

## Color Options

### Select Field Colors

Available colors for `singleSelect` and `multipleSelects` choices:

#### Light Colors (Light2 series)

| Color Name | Description |
|------------|-------------|
| `blueLight2` | Light blue |
| `cyanLight2` | Light cyan |
| `tealLight2` | Light teal |
| `greenLight2` | Light green |
| `yellowLight2` | Light yellow |
| `orangeLight2` | Light orange |
| `redLight2` | Light red |
| `pinkLight2` | Light pink |
| `purpleLight2` | Light purple |
| `grayLight2` | Light gray |

#### Dark Colors (Dark1 series)

| Color Name | Description |
|------------|-------------|
| `blueDark1` | Dark blue |
| `cyanDark1` | Dark cyan |
| `tealDark1` | Dark teal |
| `greenDark1` | Dark green |
| `yellowDark1` | Dark yellow |
| `orangeDark1` | Dark orange |
| `redDark1` | Dark red |
| `pinkDark1` | Dark pink |
| `purpleDark1` | Dark purple |
| `grayDark1` | Dark gray |

#### Bright Colors (Bright series — for checkbox, rating icons)

| Color Name | Description |
|------------|-------------|
| `greenBright` | Bright green |
| `tealBright` | Bright teal |
| `cyanBright` | Bright cyan |
| `blueBright` | Bright blue |
| `purpleBright` | Bright purple |
| `pinkBright` | Bright pink |
| `redBright` | Bright red |
| `orangeBright` | Bright orange |
| `yellowBright` | Bright yellow |
| `grayBright` | Bright gray |

**Note:** If no color is specified for a select choice, Airtable assigns one automatically. Bright colors are used for checkbox and rating icon colors, not for select choices.

---

## Error Codes

### HTTP Status Codes

| Status | Error Type | Description |
|--------|-----------|-------------|
| 400 | `BAD_REQUEST` | Malformed JSON or missing required fields in the request body |
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid `Authorization` header or token |
| 403 | `NOT_AUTHORIZED` | Token does not have the required scope (`schema.bases:read` or `schema.bases:write`) |
| 404 | `NOT_FOUND` | The specified `baseId` or `tableId` does not exist or is not accessible |
| 409 | `CONFLICT` | Concurrent modification conflict (retry the request) |
| 422 | `INVALID_REQUEST` | Semantically invalid request (see detailed 422 errors below) |
| 429 | `TOO_MANY_REQUESTS` | Rate limit exceeded (5 req/sec per base). Retry after `Retry-After` header value. |
| 500 | `SERVER_ERROR` | Internal server error. Retry with exponential backoff. |
| 502 | `BAD_GATEWAY` | Upstream service unavailable. Retry with exponential backoff. |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily unavailable. Retry with exponential backoff. |

### Detailed 422 Errors

| Error Type | Cause | Resolution |
|-----------|-------|------------|
| `INVALID_REQUEST` | Generic validation failure | Check the `message` field for details |
| `DUPLICATE_TABLE_NAME` | Table name already exists in this base | Choose a different name |
| `INVALID_TABLE_NAME` | Name is empty, too long (>255 chars), or contains invalid characters | Use a valid name |
| `CANNOT_CREATE_FIELD_TYPE` | The field type cannot be created via API (e.g., `externalSyncSource`) | Use a supported field type |
| `INVALID_FIELD_TYPE` | Unrecognized field type string | Check spelling and use a supported type |
| `INVALID_FIELD_OPTIONS` | Options do not match the schema for the specified field type | See field options schemas above |
| `DUPLICATE_FIELD_NAME` | Two or more fields have the same name | Use unique field names |
| `INVALID_FIELD_NAME` | Field name is empty, too long (>255 chars), or contains invalid characters | Use a valid field name |
| `MISSING_FIELD_OPTIONS` | Required options missing for the field type (e.g., `singleSelect` without `choices`) | Provide required options |
| `TABLE_NOT_FOUND` | The `tableId` in the URL path does not exist | Verify the table ID |
| `BASE_NOT_FOUND` | The `baseId` in the URL path does not exist | Verify the base ID |
| `INVALID_LINKED_TABLE_ID` | The `linkedTableId` in `multipleRecordLinks` options does not exist | Verify the linked table ID |
| `CANNOT_MODIFY_PRIMARY_FIELD` | Attempted to change the primary field type via update | Primary field type is immutable |
| `FIELD_COUNT_LIMIT_EXCEEDED` | Too many fields in the table (limit varies by plan) | Remove unused fields or upgrade plan |

### Error Response Format

All error responses follow this structure:

```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "A human-readable description of what went wrong"
  }
}
```

---

## Full cURL Examples

### List all tables in a base

```bash
curl "https://api.airtable.com/v0/meta/bases/appABC123/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### List tables with visible field IDs

```bash
curl "https://api.airtable.com/v0/meta/bases/appABC123/tables?include=visibleFieldIds" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Create a simple table

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/appABC123/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Contacts",
    "fields": [
      {"name": "Full Name", "type": "singleLineText"},
      {"name": "Email", "type": "email"},
      {"name": "Phone", "type": "phoneNumber"}
    ]
  }'
```

### Create a table with linked records

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/appABC123/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tasks",
    "description": "Task management linked to Projects",
    "fields": [
      {"name": "Task", "type": "singleLineText"},
      {"name": "Project", "type": "multipleRecordLinks", "options": {
        "linkedTableId": "tblPROJECTS"
      }},
      {"name": "Status", "type": "singleSelect", "options": {
        "choices": [
          {"name": "Backlog", "color": "grayLight2"},
          {"name": "To Do", "color": "blueLight2"},
          {"name": "In Progress", "color": "yellowLight2"},
          {"name": "Done", "color": "greenLight2"}
        ]
      }},
      {"name": "Due", "type": "date", "options": {"dateFormat": {"name": "iso"}}}
    ]
  }'
```

### Create a table with formula and computed fields

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/appABC123/tables" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invoices",
    "fields": [
      {"name": "Invoice #", "type": "autoNumber"},
      {"name": "Amount", "type": "currency", "options": {"precision": 2, "symbol": "$"}},
      {"name": "Tax Rate", "type": "percent", "options": {"precision": 1}},
      {"name": "Paid", "type": "checkbox", "options": {"icon": "check", "color": "greenBright"}},
      {"name": "Created", "type": "createdTime", "options": {
        "result": {
          "type": "dateTime",
          "options": {
            "dateFormat": {"name": "iso"},
            "timeFormat": {"name": "24hour"},
            "timeZone": "UTC"
          }
        }
      }}
    ]
  }'
```

### Rename a table

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/appABC123/tables/tblDEF456" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Archived Projects"}'
```

### Update table description

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/appABC123/tables/tblDEF456" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Projects that are no longer active"}'
```

### Clear table description

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/appABC123/tables/tblDEF456" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": null}'
```

---

## Full Python Examples

### List all tables and print schema summary

```python
import requests, os

def list_tables(base_id):
    response = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    )
    response.raise_for_status()
    tables = response.json()["tables"]
    for table in tables:
        print(f"\nTable: {table['name']} (ID: {table['id']})")
        print(f"  Primary field: {table['primaryFieldId']}")
        print(f"  Description: {table.get('description', '(none)')}")
        print(f"  Fields ({len(table['fields'])}):")
        for field in table["fields"]:
            opts = f" | options: {field['options']}" if "options" in field else ""
            print(f"    - {field['name']} ({field['type']}){opts}")
        print(f"  Views ({len(table['views'])}):")
        for view in table["views"]:
            print(f"    - {view['name']} ({view['type']})")
    return tables
```

### Create a CRM table

```python
import requests, os

def create_crm_table(base_id):
    response = requests.post(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
        headers={
            "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        },
        json={
            "name": "CRM Contacts",
            "description": "Customer relationship management",
            "fields": [
                {"name": "Contact Name", "type": "singleLineText"},
                {"name": "Company", "type": "singleLineText"},
                {"name": "Email", "type": "email"},
                {"name": "Phone", "type": "phoneNumber"},
                {"name": "Website", "type": "url"},
                {"name": "Stage", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Lead", "color": "blueLight2"},
                        {"name": "Qualified", "color": "cyanLight2"},
                        {"name": "Proposal", "color": "yellowLight2"},
                        {"name": "Negotiation", "color": "orangeLight2"},
                        {"name": "Closed Won", "color": "greenLight2"},
                        {"name": "Closed Lost", "color": "redLight2"},
                    ]
                }},
                {"name": "Tags", "type": "multipleSelects", "options": {
                    "choices": [
                        {"name": "Enterprise", "color": "purpleLight2"},
                        {"name": "SMB", "color": "tealLight2"},
                        {"name": "Startup", "color": "pinkLight2"},
                    ]
                }},
                {"name": "Deal Value", "type": "currency", "options": {
                    "precision": 2, "symbol": "$"
                }},
                {"name": "Confidence", "type": "rating", "options": {
                    "max": 5, "icon": "star", "color": "yellowBright"
                }},
                {"name": "First Contact", "type": "date", "options": {
                    "dateFormat": {"name": "iso"}
                }},
                {"name": "Notes", "type": "richText"},
                {"name": "Active", "type": "checkbox", "options": {
                    "icon": "check", "color": "greenBright"
                }},
            ],
        },
    )
    response.raise_for_status()
    return response.json()
```

### Rename a table with error handling

```python
import requests, os

def rename_table(base_id, table_id, new_name):
    response = requests.patch(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}",
        headers={
            "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        },
        json={"name": new_name},
    )
    if response.status_code == 422:
        error = response.json().get("error", {})
        if error.get("type") == "DUPLICATE_TABLE_NAME":
            print(f"Error: A table named '{new_name}' already exists.")
        else:
            print(f"Error: {error.get('message', 'Unknown error')}")
        return None
    response.raise_for_status()
    return response.json()
```

### Find a table by name

```python
import requests, os

def find_table_by_name(base_id, table_name):
    response = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    )
    response.raise_for_status()
    for table in response.json()["tables"]:
        if table["name"].lower() == table_name.lower():
            return table
    return None
```
