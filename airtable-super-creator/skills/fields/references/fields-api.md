# Airtable Fields API Reference

Complete API reference for listing, creating, and updating fields in Airtable tables.

> **Base URL:** `https://api.airtable.com/v0`
> **Auth:** All requests require `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Rate limit:** 5 requests/second per base

---

## 1. List Fields

**`GET /v0/meta/bases/{baseId}/tables/{tableId}/fields`**

Returns all fields in a table.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (format: `appXXXXXXXXXXXXXX`) |
| `tableId` | string | Yes | Table ID (format: `tblXXXXXXXXXXXXXX`) |

### Query Parameters

None.

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

### cURL

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
data = response.json()
fields = data["fields"]
```

### Response Schema

```json
{
  "fields": [
    {
      "id": "fldXXXXXXXXXXXXXX",
      "name": "string",
      "type": "string",
      "description": "string | undefined",
      "options": "object | undefined"
    }
  ]
}
```

### Response Field Properties

| Property | Type | Always Present | Description |
|----------|------|----------------|-------------|
| `id` | string | Yes | Unique field identifier (`fldXXX`) |
| `name` | string | Yes | Display name of the field |
| `type` | string | Yes | Field type identifier (e.g., `singleLineText`, `number`, `singleSelect`) |
| `description` | string | No | Human-readable description; omitted if not set |
| `options` | object | No | Type-specific configuration; omitted for types with no options (e.g., `singleLineText`) |

### Full Response Example

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
          {"id": "selDEF", "name": "In Progress", "color": "yellowLight2"},
          {"id": "selGHI", "name": "Done", "color": "greenLight2"}
        ]
      }
    },
    {
      "id": "fldGHI789",
      "name": "Priority",
      "type": "number",
      "options": {
        "precision": 0
      }
    },
    {
      "id": "fldJKL012",
      "name": "Due Date",
      "type": "date",
      "options": {
        "dateFormat": {
          "name": "local",
          "format": "M/D/YYYY"
        }
      }
    },
    {
      "id": "fldMNO345",
      "name": "Assignee",
      "type": "singleCollaborator"
    },
    {
      "id": "fldPQR678",
      "name": "Related Projects",
      "type": "multipleRecordLinks",
      "options": {
        "linkedTableId": "tblTARGET123",
        "prefersSingleRecordLink": false,
        "inverseLinkFieldId": "fldINV456",
        "isReversed": false
      }
    },
    {
      "id": "fldSTU901",
      "name": "Total Hours",
      "type": "formula",
      "options": {
        "expression": "SUM(values)",
        "referencedFieldIds": ["fldREF1"],
        "result": {
          "type": "number",
          "options": {
            "precision": 2
          }
        }
      }
    },
    {
      "id": "fldVWX234",
      "name": "Created",
      "type": "createdTime",
      "options": {
        "result": {
          "type": "dateTime",
          "options": {
            "dateFormat": {"name": "local", "format": "M/D/YYYY"},
            "timeFormat": {"name": "12hour", "format": "h:mma"},
            "timeZone": "America/New_York"
          }
        }
      }
    }
  ]
}
```

### Required Scope

`schema.bases:read`

### Errors

| Status | Error Type | Description |
|--------|-----------|-------------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:read` scope |
| 404 | `NOT_FOUND` | Invalid base ID or table ID |

---

## 2. Create Field

**`POST /v0/meta/bases/{baseId}/tables/{tableId}/fields`**

Creates a new field in the specified table.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (format: `appXXXXXXXXXXXXXX`) |
| `tableId` | string | Yes | Table ID (format: `tblXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |
| `Content-Type` | `application/json` |

### Request Body Schema

```json
{
  "name": "string (required)",
  "type": "string (required)",
  "description": "string (optional)",
  "options": "object (optional, depends on type)"
}
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name. Must be unique within the table. Max 255 characters. |
| `type` | string | Yes | Field type identifier. See field-types reference for all valid values. |
| `description` | string | No | Human-readable description of the field's purpose |
| `options` | object | Depends on type | Type-specific configuration. Required for some types, optional for others. |

### Types That Require `options`

| Type | Required Options |
|------|-----------------|
| `number` | `precision` (0-8) |
| `percent` | `precision` (0-8) |
| `currency` | `precision` (0-8), `symbol` |
| `singleSelect` | `choices` array |
| `multipleSelects` | `choices` array |
| `date` | `dateFormat` |
| `dateTime` | `dateFormat`, `timeFormat`, `timeZone` |
| `duration` | `durationFormat` |
| `rating` | `max`, `icon`, `color` |
| `checkbox` | `icon`, `color` |
| `multipleRecordLinks` | `linkedTableId` |
| `formula` | `expression` |
| `lookup` | `recordLinkFieldId`, `fieldIdInLinkedTable` |
| `rollup` | `recordLinkFieldId`, `fieldIdInLinkedTable`, `referencedFieldIds` |

### Types That Do NOT Require `options`

| Type |
|------|
| `singleLineText` |
| `multilineText` |
| `richText` |
| `email` |
| `url` |
| `phoneNumber` |
| `multipleAttachments` |
| `singleCollaborator` |
| `multipleCollaborators` |
| `barcode` |
| `autoNumber` |

### Example Requests

#### Create a singleLineText field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Title",
    "type": "singleLineText",
    "description": "Record title"
  }'
```

#### Create a number field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quantity",
    "type": "number",
    "options": {"precision": 0}
  }'
```

#### Create a currency field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Price",
    "type": "currency",
    "options": {"precision": 2, "symbol": "$"}
  }'
```

#### Create a singleSelect field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Status",
    "type": "singleSelect",
    "options": {
      "choices": [
        {"name": "Not Started", "color": "blueLight2"},
        {"name": "In Progress", "color": "yellowLight2"},
        {"name": "Completed", "color": "greenLight2"}
      ]
    }
  }'
```

#### Create a multipleSelects field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tags",
    "type": "multipleSelects",
    "options": {
      "choices": [
        {"name": "Bug", "color": "redLight2"},
        {"name": "Feature", "color": "greenLight2"},
        {"name": "Docs", "color": "blueLight2"}
      ]
    }
  }'
```

#### Create a date field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Due Date",
    "type": "date",
    "options": {
      "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"}
    }
  }'
```

#### Create a dateTime field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Meeting Time",
    "type": "dateTime",
    "options": {
      "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"},
      "timeFormat": {"name": "24hour", "format": "HH:mm"},
      "timeZone": "America/New_York"
    }
  }'
```

#### Create a multipleRecordLinks field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Related Projects",
    "type": "multipleRecordLinks",
    "options": {
      "linkedTableId": "tblTARGET123",
      "prefersSingleRecordLink": false
    }
  }'
```

#### Create an attachments field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Documents",
    "type": "multipleAttachments"
  }'
```

#### Create a checkbox field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Approved",
    "type": "checkbox",
    "options": {"icon": "check", "color": "greenBright"}
  }'
```

#### Create a rating field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priority Rating",
    "type": "rating",
    "options": {"max": 5, "icon": "star", "color": "yellowBright"}
  }'
```

#### Create a formula field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Full Name",
    "type": "formula",
    "options": {
      "expression": "CONCATENATE({First Name}, \" \", {Last Name})"
    }
  }'
```

#### Create a lookup field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Status",
    "type": "lookup",
    "options": {
      "recordLinkFieldId": "fldLINK123",
      "fieldIdInLinkedTable": "fldSTATUS456"
    }
  }'
```

#### Create a rollup field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Total Revenue",
    "type": "rollup",
    "options": {
      "recordLinkFieldId": "fldLINK123",
      "fieldIdInLinkedTable": "fldAMOUNT456",
      "referencedFieldIds": ["fldAMOUNT456"]
    }
  }'
```

#### Create a duration field

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Time Spent",
    "type": "duration",
    "options": {"durationFormat": "h:mm:ss"}
  }'
```

### Python — Create Field

```python
import requests, os

response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Status",
        "type": "singleSelect",
        "description": "Current status of the record",
        "options": {
            "choices": [
                {"name": "Backlog", "color": "blueLight2"},
                {"name": "In Progress", "color": "yellowLight2"},
                {"name": "Done", "color": "greenLight2"},
            ]
        },
    },
)
new_field = response.json()
print(f"Created field: {new_field['id']} — {new_field['name']}")
```

### Response Schema

Returns the created field object:

```json
{
  "id": "fldNEWXXXXXXXXXX",
  "name": "string",
  "type": "string",
  "description": "string | undefined",
  "options": "object | undefined"
}
```

### Required Scope

`schema.bases:write`

### Errors

| Status | Error Type | Description |
|--------|-----------|-------------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:write` scope |
| 404 | `NOT_FOUND` | Invalid base ID or table ID |
| 422 | `INVALID_REQUEST` | Invalid field name, type, or options |
| 422 | `FIELD_NAME_ALREADY_EXISTS` | A field with that name already exists |
| 422 | `INVALID_FIELD_TYPE` | Unrecognized or unsupported field type |
| 422 | `INVALID_OPTIONS_FOR_FIELD_TYPE` | Options do not match the expected schema for the type |

---

## 3. Update Field

**`PATCH /v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}`**

Update an existing field's name, description, or type-specific options.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (format: `appXXXXXXXXXXXXXX`) |
| `tableId` | string | Yes | Table ID (format: `tblXXXXXXXXXXXXXX`) |
| `fieldId` | string | Yes | Field ID (format: `fldXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |
| `Content-Type` | `application/json` |

### Request Body Schema

```json
{
  "name": "string (optional)",
  "description": "string (optional)",
  "options": "object (optional, depends on type)"
}
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | New display name. Must be unique within the table. |
| `description` | string | No | New description. Set to `null` to clear. |
| `options` | object | No | Updated type-specific configuration. |

### Constraints

- **Cannot change `type`:** The field type is immutable after creation. Attempting to change it returns a `422` error.
- **Cannot delete fields:** The API does not provide a delete field endpoint. Fields must be deleted manually in the Airtable UI.
- **Select choices:** When updating choices on a `singleSelect` or `multipleSelects` field, you must include all existing choices (by their `id`) plus any new ones. You cannot remove choices via the API.
- **Computed fields:** Fields like `formula`, `lookup`, `rollup`, `count`, `autoNumber`, `createdTime`, `lastModifiedTime`, `createdBy`, and `lastModifiedBy` may have limited update options.

### What Can Be Updated Per Type

| Field Type | `name` | `description` | `options` |
|------------|--------|---------------|-----------|
| `singleLineText` | Yes | Yes | N/A |
| `multilineText` | Yes | Yes | N/A |
| `richText` | Yes | Yes | N/A |
| `email` | Yes | Yes | N/A |
| `url` | Yes | Yes | N/A |
| `phoneNumber` | Yes | Yes | N/A |
| `number` | Yes | Yes | Yes (precision) |
| `percent` | Yes | Yes | Yes (precision) |
| `currency` | Yes | Yes | Yes (precision, symbol) |
| `singleSelect` | Yes | Yes | Yes (add choices) |
| `multipleSelects` | Yes | Yes | Yes (add choices) |
| `date` | Yes | Yes | Yes (dateFormat) |
| `dateTime` | Yes | Yes | Yes (dateFormat, timeFormat, timeZone) |
| `duration` | Yes | Yes | Yes (durationFormat) |
| `checkbox` | Yes | Yes | Yes (icon, color) |
| `rating` | Yes | Yes | Yes (max, icon, color) |
| `multipleRecordLinks` | Yes | Yes | Limited (prefersSingleRecordLink) |
| `multipleAttachments` | Yes | Yes | N/A |
| `singleCollaborator` | Yes | Yes | N/A |
| `multipleCollaborators` | Yes | Yes | N/A |
| `formula` | Yes | Yes | Yes (expression) |
| `lookup` | Yes | Yes | Limited |
| `rollup` | Yes | Yes | Limited |
| `autoNumber` | Yes | Yes | N/A |
| `barcode` | Yes | Yes | N/A |
| `createdTime` | Yes | Yes | Limited |
| `lastModifiedTime` | Yes | Yes | Limited |
| `createdBy` | Yes | Yes | N/A |
| `lastModifiedBy` | Yes | Yes | N/A |
| `count` | Yes | Yes | N/A |

### Example Requests

#### Rename a field

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Field Name"}'
```

#### Update description

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated field description"}'
```

#### Clear description

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": null}'
```

#### Add choices to a singleSelect field

When updating choices, **include all existing choices by ID** and add new ones without an ID:

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "options": {
      "choices": [
        {"id": "selEXIST1", "name": "Todo", "color": "blueLight2"},
        {"id": "selEXIST2", "name": "In Progress", "color": "yellowLight2"},
        {"id": "selEXIST3", "name": "Done", "color": "greenLight2"},
        {"name": "Blocked", "color": "redLight2"}
      ]
    }
  }'
```

#### Update number precision

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"options": {"precision": 2}}'
```

#### Update a formula expression

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"options": {"expression": "CONCATENATE({First Name}, \" \", {Last Name})"}}'
```

### Python — Update Field

```python
import requests, os

# Rename and add select choices
response = requests.patch(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields/{field_id}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Priority Level",
        "description": "Updated priority field with new options",
        "options": {
            "choices": [
                {"id": "selEXIST1", "name": "Low", "color": "blueLight2"},
                {"id": "selEXIST2", "name": "Medium", "color": "yellowLight2"},
                {"id": "selEXIST3", "name": "High", "color": "redLight2"},
                {"name": "Critical", "color": "redDark1"},
            ]
        },
    },
)
updated = response.json()
print(f"Updated: {updated['id']} — {updated['name']}")
```

### Response Schema

Returns the updated field object:

```json
{
  "id": "fldXXXXXXXXXXXXXX",
  "name": "string",
  "type": "string",
  "description": "string | undefined",
  "options": "object | undefined"
}
```

### Required Scope

`schema.bases:write`

### Errors

| Status | Error Type | Description |
|--------|-----------|-------------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `schema.bases:write` scope |
| 404 | `NOT_FOUND` | Invalid base ID, table ID, or field ID |
| 422 | `INVALID_REQUEST` | Invalid update payload |
| 422 | `CANNOT_CHANGE_FIELD_TYPE` | Attempted to change the `type` property |
| 422 | `FIELD_NAME_ALREADY_EXISTS` | Another field already has that name |
| 422 | `INVALID_OPTIONS_FOR_FIELD_TYPE` | Options do not match the expected schema |

---

## Color Values for Select Choices

These color identifiers can be used in `singleSelect` and `multipleSelects` choice definitions:

| Color Family | Light 1 | Light 2 | Bright | Dark 1 |
|-------------|---------|---------|--------|--------|
| Blue | `blueLight1` | `blueLight2` | `blueBright` | `blueDark1` |
| Cyan | `cyanLight1` | `cyanLight2` | `cyanBright` | `cyanDark1` |
| Teal | `tealLight1` | `tealLight2` | `tealBright` | `tealDark1` |
| Green | `greenLight1` | `greenLight2` | `greenBright` | `greenDark1` |
| Yellow | `yellowLight1` | `yellowLight2` | `yellowBright` | `yellowDark1` |
| Orange | `orangeLight1` | `orangeLight2` | `orangeBright` | `orangeDark1` |
| Red | `redLight1` | `redLight2` | `redBright` | `redDark1` |
| Pink | `pinkLight1` | `pinkLight2` | `pinkBright` | `pinkDark1` |
| Purple | `purpleLight1` | `purpleLight2` | `purpleBright` | `purpleDark1` |
| Gray | `grayLight1` | `grayLight2` | `grayBright` | `grayDark1` |

---

## ID Formats

| Entity | Prefix | Example |
|--------|--------|---------|
| Base | `app` | `appABC123DEF456` |
| Table | `tbl` | `tblABC123DEF456` |
| Field | `fld` | `fldABC123DEF456` |
| View | `viw` | `viwABC123DEF456` |
| Record | `rec` | `recABC123DEF456` |
| Select choice | `sel` | `selABC123DEF456` |
