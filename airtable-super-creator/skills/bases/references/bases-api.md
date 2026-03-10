# Airtable Bases API — Complete Reference

> **Base URL:** `https://api.airtable.com/v0`
> **Authentication:** `Authorization: Bearer <token>`
> **Rate Limit:** 5 requests per second per base
> **Content-Type:** `application/json` (for POST/PUT/PATCH requests)

---

## Table of Contents

1. [List Bases](#1-list-bases)
2. [Get Base Schema](#2-get-base-schema)
3. [Create Base](#3-create-base)
4. [Permission Levels](#4-permission-levels)
5. [Field Types Reference](#5-field-types-reference)
6. [View Types Reference](#6-view-types-reference)
7. [Error Codes](#7-error-codes)
8. [Required OAuth Scopes](#8-required-oauth-scopes)
9. [Rate Limiting](#9-rate-limiting)
10. [ID Format Reference](#10-id-format-reference)

---

## 1. List Bases

**`GET /v0/meta/bases`**

Returns a list of all bases that the authenticated user or token has access to. Results are paginated and returned in no guaranteed order.

### Request

**Headers:**

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | Yes |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `offset` | string | No | Pagination cursor returned from a previous request. Pass this value to retrieve the next page of results. |

### Response Schema

**Top-level object:**

| Property | Type | Description |
|----------|------|-------------|
| `bases` | array of Base objects | List of bases the token can access |
| `offset` | string or null | Pagination cursor. Present only if there are more results. Pass to next request to get the next page. |

**Base object:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique base identifier. Always starts with `app` (e.g., `appABC123def456`). |
| `name` | string | Human-readable name of the base as displayed in Airtable. |
| `permissionLevel` | string | The highest permission level the token has on this base. One of: `none`, `read`, `comment`, `edit`, `create`, `owner`. |

### Response Example

```json
{
  "bases": [
    {
      "id": "appABC123def456",
      "name": "Project Tracker",
      "permissionLevel": "create"
    },
    {
      "id": "appDEF789ghi012",
      "name": "Customer CRM",
      "permissionLevel": "edit"
    },
    {
      "id": "appGHI345jkl678",
      "name": "Content Calendar",
      "permissionLevel": "read"
    }
  ],
  "offset": "itrABCDEF123456/appGHI345jkl678"
}
```

### Pagination

- The API returns bases in pages. If there are more bases than can be returned in a single response, the response includes an `offset` string.
- To fetch the next page, include `offset` as a query parameter in the subsequent request.
- When `offset` is absent from the response, you have retrieved all bases.
- The page size is determined by the server and is not configurable by the client.
- The `offset` value is opaque and should not be parsed or constructed manually.

### Pagination Example (Python)

```python
import requests, os

headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}
all_bases = []
offset = None

while True:
    params = {}
    if offset:
        params["offset"] = offset

    response = requests.get(
        "https://api.airtable.com/v0/meta/bases",
        headers=headers,
        params=params,
    )
    response.raise_for_status()
    data = response.json()

    all_bases.extend(data["bases"])
    offset = data.get("offset")

    if not offset:
        break

print(f"Total bases: {len(all_bases)}")
for base in all_bases:
    print(f"  {base['id']}: {base['name']} (permission: {base['permissionLevel']})")
```

### Notes

- Bases where the token has `none` permission level may still appear in the list but cannot be read or modified.
- The list includes bases across all workspaces the token has access to.
- Deleted bases are not returned.
- The name reflects the current name; if a base is renamed, subsequent calls return the updated name.

---

## 2. Get Base Schema

**`GET /v0/meta/bases/{baseId}/tables`**

Returns the complete schema of a base, including all tables, their fields (with full type configuration), and all views.

### Request

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (starts with `app`). |

**Headers:**

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | Yes |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `include` | array of strings | No | Additional data to include. Currently supports `visibleFieldIds` which adds the list of visible field IDs to each view object. Pass as `include[]=visibleFieldIds`. |

### Response Schema

**Top-level object:**

| Property | Type | Description |
|----------|------|-------------|
| `tables` | array of Table objects | All tables in the base. |

**Table object:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique table identifier. Always starts with `tbl`. |
| `name` | string | Display name of the table. |
| `description` | string or null | Optional description set by the user. |
| `primaryFieldId` | string | The field ID of the primary field (first column). This field cannot be deleted and is always present. |
| `fields` | array of Field objects | All fields (columns) in the table, in order. |
| `views` | array of View objects | All views defined on the table, in order. |

**Field object:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique field identifier. Always starts with `fld`. |
| `name` | string | Display name of the field. |
| `type` | string | The field type identifier. See Field Types Reference below. |
| `description` | string or null | Optional user-provided description of the field. |
| `options` | object or null | Type-specific configuration. Structure varies by field type. Not all field types have options. |

**View object:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique view identifier. Always starts with `viw`. |
| `name` | string | Display name of the view. |
| `type` | string | The view type. One of: `grid`, `form`, `calendar`, `gallery`, `kanban`, `timeline`, `block`. |
| `personalForUserId` | string or null | If set, indicates this is a personal/locked view only visible to the specified user. |
| `visibleFieldIds` | array of strings or null | Only present when `include[]=visibleFieldIds` is passed. Lists the field IDs visible in this view, in display order. |

### Response Example

```json
{
  "tables": [
    {
      "id": "tblABC123",
      "name": "Tasks",
      "description": "All project tasks and their assignments",
      "primaryFieldId": "fldPRI001",
      "fields": [
        {
          "id": "fldPRI001",
          "name": "Task Name",
          "type": "singleLineText",
          "description": "The name of the task"
        },
        {
          "id": "fldSTS002",
          "name": "Status",
          "type": "singleSelect",
          "options": {
            "choices": [
              {
                "id": "selOPT001",
                "name": "Todo",
                "color": "blueLight2"
              },
              {
                "id": "selOPT002",
                "name": "In Progress",
                "color": "yellowLight2"
              },
              {
                "id": "selOPT003",
                "name": "Done",
                "color": "greenLight2"
              }
            ]
          }
        },
        {
          "id": "fldASG003",
          "name": "Assignee",
          "type": "singleCollaborator",
          "description": "Person responsible for this task"
        },
        {
          "id": "fldDUE004",
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
          "id": "fldATT005",
          "name": "Attachments",
          "type": "multipleAttachments",
          "options": {
            "isReversed": false
          }
        },
        {
          "id": "fldLNK006",
          "name": "Related Projects",
          "type": "multipleRecordLinks",
          "options": {
            "linkedTableId": "tblDEF456",
            "isReversed": false,
            "prefersSingleRecordLink": false,
            "inverseLinkFieldId": "fldINV007"
          }
        },
        {
          "id": "fldFRM007",
          "name": "Total Hours",
          "type": "formula",
          "options": {
            "expression": "SUM(values)",
            "referencedFieldIds": ["fldHRS008"],
            "result": {
              "type": "number",
              "options": {
                "precision": 1
              }
            }
          }
        }
      ],
      "views": [
        {
          "id": "viwGRD001",
          "name": "Grid view",
          "type": "grid"
        },
        {
          "id": "viwKBN002",
          "name": "Kanban Board",
          "type": "kanban"
        },
        {
          "id": "viwCAL003",
          "name": "Schedule",
          "type": "calendar"
        },
        {
          "id": "viwFRM004",
          "name": "Task Submission",
          "type": "form"
        }
      ]
    },
    {
      "id": "tblDEF456",
      "name": "Projects",
      "description": "Master list of projects",
      "primaryFieldId": "fldPRJ001",
      "fields": [
        {
          "id": "fldPRJ001",
          "name": "Project Name",
          "type": "singleLineText"
        },
        {
          "id": "fldINV007",
          "name": "Tasks",
          "type": "multipleRecordLinks",
          "options": {
            "linkedTableId": "tblABC123",
            "isReversed": true,
            "prefersSingleRecordLink": false,
            "inverseLinkFieldId": "fldLNK006"
          }
        }
      ],
      "views": [
        {
          "id": "viwGRD005",
          "name": "Grid view",
          "type": "grid"
        }
      ]
    }
  ]
}
```

### Using the `include` Parameter

To retrieve visible field IDs for each view:

```bash
curl "https://api.airtable.com/v0/meta/bases/appABC123/tables?include[]=visibleFieldIds" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

When included, each view object gains the `visibleFieldIds` array:

```json
{
  "id": "viwGRD001",
  "name": "Grid view",
  "type": "grid",
  "visibleFieldIds": ["fldPRI001", "fldSTS002", "fldASG003", "fldDUE004"]
}
```

### Notes

- The schema reflects the current state of the base. Any structural changes (adding/removing tables, fields, or views) are immediately reflected.
- Computed field types (formula, rollup, lookup, count) include a `result` property in their options describing the output type.
- The primary field is always the first field in the `fields` array and is identified by `primaryFieldId`.
- Field order in the array matches the default field order, but individual views may reorder or hide fields.

---

## 3. Create Base

**`POST /v0/meta/bases`**

Creates a new base in a specified workspace with one or more tables and their field definitions.

### Request

**Headers:**

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | Yes |
| `Content-Type` | `application/json` | Yes |

### Request Body Schema

**Top-level object:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | The name for the new base. Maximum 255 characters. |
| `workspaceId` | string | Yes | The ID of the workspace to create the base in. Always starts with `wsp`. |
| `tables` | array of Table Definition objects | Yes | At least one table must be provided. |

**Table Definition object:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Table name. Maximum 255 characters. Must be unique within the base. |
| `description` | string | No | Optional description for the table. |
| `fields` | array of Field Definition objects | Yes | At least one field must be provided. The first field becomes the primary field. |

**Field Definition object:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Field name. Maximum 255 characters. Must be unique within the table. |
| `type` | string | Yes | The field type. See supported types below. |
| `description` | string | No | Optional description for the field. |
| `options` | object | Depends | Type-specific configuration. Required for some field types (e.g., `singleSelect`, `number`), optional for others. |

### Supported Field Types for Base Creation

The following field types can be used when creating a base:

| Type | Options Required | Description |
|------|-----------------|-------------|
| `singleLineText` | No | Single line of text. |
| `multilineText` | No | Multi-line long text. Supports rich text formatting. |
| `email` | No | Email address field. |
| `url` | No | URL field. |
| `phoneNumber` | No | Phone number field. |
| `number` | No (optional) | Numeric field. Options: `precision` (0-8, decimal places). |
| `currency` | No (optional) | Currency field. Options: `precision` (0-7), `symbol` (e.g., `"$"`). |
| `percent` | No (optional) | Percentage field. Options: `precision` (0-8). |
| `duration` | No (optional) | Duration field. Options: `durationFormat` (`h:mm`, `h:mm:ss`, `h:mm:ss.S`, `h:mm:ss.SS`, `h:mm:ss.SSS`). |
| `singleSelect` | Yes | Single select dropdown. Options: `choices` array. |
| `multipleSelects` | Yes | Multiple select tags. Options: `choices` array. |
| `checkbox` | No (optional) | Boolean checkbox. Options: `color`, `icon`. |
| `date` | No (optional) | Date field. Options: `dateFormat` object. |
| `dateTime` | No (optional) | Date and time field. Options: `dateFormat`, `timeFormat`, `timeZone`. |
| `rating` | No (optional) | Star rating (1-10). Options: `max` (1-10), `color`, `icon`. |
| `richText` | No | Rich text with formatting support. |
| `multipleAttachments` | No | File attachment field. Options: `isReversed`. |
| `singleCollaborator` | No | Single user/collaborator. |
| `multipleCollaborators` | No | Multiple users/collaborators. |
| `multipleRecordLinks` | Yes | Link to records in another table. Options: `linkedTableId`, `prefersSingleRecordLink`. |
| `barcode` | No | Barcode field. |
| `autoNumber` | No | Auto-incrementing number. Cannot be the primary field. |
| `externalSyncSource` | No | Synced from external source (read-only after creation). |

**Field types NOT supported for base creation:**

- `formula` — Must be added after base creation via the fields API.
- `rollup` — Must be added after base creation via the fields API.
- `lookup` — Must be added after base creation via the fields API.
- `count` — Must be added after base creation via the fields API.
- `createdTime` — Must be added after base creation via the fields API.
- `lastModifiedTime` — Must be added after base creation via the fields API.
- `createdBy` — Must be added after base creation via the fields API.
- `lastModifiedBy` — Must be added after base creation via the fields API.
- `button` — Must be added after base creation via the fields API.
- `aiText` — Must be added after base creation via the fields API.

### Select Field Choice Options

For `singleSelect` and `multipleSelects` fields, each choice object has:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Display name of the choice. Must be unique within the field. |
| `color` | string | No | Color name. See available colors below. |

**Available colors for select choices:**

`blueLight2`, `cyanLight2`, `tealLight2`, `greenLight2`, `yellowLight2`, `orangeLight2`, `redLight2`, `pinkLight2`, `purpleLight2`, `grayLight2`, `blueDark1`, `cyanDark1`, `tealDark1`, `greenDark1`, `yellowDark1`, `orangeDark1`, `redDark1`, `pinkDark1`, `purpleDark1`, `grayDark1`

### Date Format Options

For `date` and `dateTime` fields:

**`dateFormat` object:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | One of: `local`, `friendly`, `us`, `european`, `iso` |
| `format` | string | The date format string corresponding to the name |

**Date format values:**

| Name | Format |
|------|--------|
| `local` | `M/D/YYYY` |
| `friendly` | `MMMM D, YYYY` |
| `us` | `M/D/YYYY` |
| `european` | `D/M/YYYY` |
| `iso` | `YYYY-MM-DD` |

**`timeFormat` object (for `dateTime` only):**

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | One of: `12hour`, `24hour` |
| `format` | string | `h:mma` for 12-hour, `HH:mm` for 24-hour |

**`timeZone` (for `dateTime` only):**

A valid IANA timezone string, e.g., `"America/New_York"`, `"Europe/London"`, `"UTC"`, `"Asia/Tokyo"`.

### Number/Currency/Percent Precision

| Type | `precision` Range | Default | Description |
|------|-------------------|---------|-------------|
| `number` | 0-8 | 1 | Number of decimal places |
| `currency` | 0-7 | 2 | Number of decimal places |
| `percent` | 0-8 | 0 | Number of decimal places |

### Request Example — Full

```json
{
  "name": "Project Management Suite",
  "workspaceId": "wspABC123",
  "tables": [
    {
      "name": "Projects",
      "description": "Master list of all projects",
      "fields": [
        {
          "name": "Project Name",
          "type": "singleLineText",
          "description": "Official name of the project"
        },
        {
          "name": "Status",
          "type": "singleSelect",
          "options": {
            "choices": [
              {"name": "Planning", "color": "blueLight2"},
              {"name": "Active", "color": "greenLight2"},
              {"name": "On Hold", "color": "yellowLight2"},
              {"name": "Completed", "color": "grayLight2"},
              {"name": "Cancelled", "color": "redLight2"}
            ]
          }
        },
        {
          "name": "Start Date",
          "type": "date",
          "options": {
            "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"}
          }
        },
        {
          "name": "Budget",
          "type": "currency",
          "options": {
            "precision": 2,
            "symbol": "$"
          }
        },
        {
          "name": "Description",
          "type": "multilineText"
        },
        {
          "name": "Priority",
          "type": "rating",
          "options": {
            "max": 5,
            "color": "yellowBright",
            "icon": "star"
          }
        }
      ]
    },
    {
      "name": "Team Members",
      "description": "All team members across projects",
      "fields": [
        {
          "name": "Full Name",
          "type": "singleLineText"
        },
        {
          "name": "Email",
          "type": "email"
        },
        {
          "name": "Role",
          "type": "singleSelect",
          "options": {
            "choices": [
              {"name": "Developer", "color": "blueLight2"},
              {"name": "Designer", "color": "purpleLight2"},
              {"name": "Manager", "color": "greenLight2"},
              {"name": "QA", "color": "orangeLight2"}
            ]
          }
        },
        {
          "name": "Phone",
          "type": "phoneNumber"
        }
      ]
    }
  ]
}
```

### Response Schema

**Top-level object:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | The ID of the newly created base (starts with `app`). |
| `name` | string | The name of the base. |
| `tables` | array of Table objects | The created tables with their server-assigned IDs. |

Each table in the response includes:
- `id` — Server-assigned table ID (starts with `tbl`).
- `name` — The table name as provided.
- `fields` — Array of fields, each with a server-assigned `id` (starts with `fld`), along with `name`, `type`, and `options`.
- `views` — Array of automatically created views. A default `Grid view` of type `grid` is always created for each table.

### Response Example

```json
{
  "id": "appNEW789xyz",
  "name": "Project Management Suite",
  "tables": [
    {
      "id": "tblPRJ001",
      "name": "Projects",
      "fields": [
        {"id": "fldPRN001", "name": "Project Name", "type": "singleLineText"},
        {
          "id": "fldSTS001",
          "name": "Status",
          "type": "singleSelect",
          "options": {
            "choices": [
              {"id": "selPLN", "name": "Planning", "color": "blueLight2"},
              {"id": "selACT", "name": "Active", "color": "greenLight2"},
              {"id": "selHLD", "name": "On Hold", "color": "yellowLight2"},
              {"id": "selCMP", "name": "Completed", "color": "grayLight2"},
              {"id": "selCNC", "name": "Cancelled", "color": "redLight2"}
            ]
          }
        },
        {
          "id": "fldSTD001",
          "name": "Start Date",
          "type": "date",
          "options": {"dateFormat": {"name": "iso", "format": "YYYY-MM-DD"}}
        },
        {
          "id": "fldBDG001",
          "name": "Budget",
          "type": "currency",
          "options": {"precision": 2, "symbol": "$"}
        },
        {"id": "fldDSC001", "name": "Description", "type": "multilineText"},
        {
          "id": "fldPRT001",
          "name": "Priority",
          "type": "rating",
          "options": {"max": 5, "color": "yellowBright", "icon": "star"}
        }
      ],
      "views": [
        {"id": "viwDEF001", "name": "Grid view", "type": "grid"}
      ]
    },
    {
      "id": "tblTMM001",
      "name": "Team Members",
      "fields": [
        {"id": "fldFLN001", "name": "Full Name", "type": "singleLineText"},
        {"id": "fldEML001", "name": "Email", "type": "email"},
        {
          "id": "fldRLE001",
          "name": "Role",
          "type": "singleSelect",
          "options": {
            "choices": [
              {"id": "selDEV", "name": "Developer", "color": "blueLight2"},
              {"id": "selDES", "name": "Designer", "color": "purpleLight2"},
              {"id": "selMGR", "name": "Manager", "color": "greenLight2"},
              {"id": "selQAE", "name": "QA", "color": "orangeLight2"}
            ]
          }
        },
        {"id": "fldPHN001", "name": "Phone", "type": "phoneNumber"}
      ],
      "views": [
        {"id": "viwDEF002", "name": "Grid view", "type": "grid"}
      ]
    }
  ]
}
```

### Workspace Requirements and Limitations

- The `workspaceId` must refer to a workspace where the token has `create` permission or higher.
- A workspace ID always starts with the prefix `wsp`.
- You must provide at least one table, and each table must have at least one field.
- The first field defined in each table becomes the primary field. The primary field must be one of these types: `singleLineText`, `number`, `autoNumber`, `barcode`, `email`, `url`, `phoneNumber`, `formula`, `rollup`, or `singleSelect`. If you use an unsupported type as the first field, the request will fail.
- Table names must be unique within the base.
- Field names must be unique within each table.
- Maximum number of tables per base creation request is not officially documented, but extremely large requests may time out.
- The created base always gets a default `Grid view` for each table, even if no views are specified.
- You cannot define views during base creation; views are created automatically and can be modified afterward via the API.
- Linked record fields (`multipleRecordLinks`) can only link to tables defined within the same base creation request, referencing them by `linkedTableId`. Since the table IDs are not yet assigned, you must use a different approach: define the tables first without link fields, then add link fields via the fields API after creation.

---

## 4. Permission Levels

Permission levels indicate what operations a user or token can perform on a base. They are hierarchical — each level includes all capabilities of lower levels.

| Level | Value | Description |
|-------|-------|-------------|
| **None** | `none` | No access to the base. The base may appear in listings but cannot be read or modified. This typically occurs when a token has workspace-level access but has been explicitly denied base access. |
| **Read** | `read` | Can view the base schema and read records. Cannot modify any data, add comments, or change the structure. Suitable for reporting and data consumption integrations. |
| **Comment** | `comment` | Includes all `read` capabilities. Additionally can add comments to records. Cannot modify record data or base structure. |
| **Edit** | `edit` | Includes all `comment` capabilities. Can create, update, and delete records. Can modify record data within existing fields. Cannot modify the base schema (add/remove/rename tables, fields, or views). |
| **Create** | `create` | Includes all `edit` capabilities. Can modify the base schema — create, update, and delete tables, fields, and views. Can manage automations and other base-level configurations. This is the most common level for full API integrations. |
| **Owner** | `owner` | Includes all `create` capabilities. Has full administrative control over the base including managing permissions, transferring ownership, and deleting the base entirely. Typically only granted to the base creator or workspace administrators. |

### Permission Level Hierarchy

```
owner > create > edit > comment > read > none
```

### How Permission Levels Are Determined

- For personal access tokens: the permission level is determined by the token's scopes and the user's access level to the base.
- For OAuth tokens: the permission level is the intersection of the OAuth app's requested scopes, the user's base access, and any restrictions applied during authorization.
- The `permissionLevel` returned in the List Bases response reflects the effective permission level after all restrictions are applied.

---

## 5. Field Types Reference

Complete list of all Airtable field types that may appear in base schema responses. Note that not all of these can be used when creating a base (see the Create Base section for the supported subset).

| Type Identifier | Display Name | Has Options | Editable via API |
|-----------------|-------------|-------------|------------------|
| `singleLineText` | Single line text | No | Yes |
| `multilineText` | Long text | No | Yes |
| `richText` | Rich text | No | Yes |
| `email` | Email | No | Yes |
| `url` | URL | No | Yes |
| `phoneNumber` | Phone number | No | Yes |
| `number` | Number | Yes (`precision`) | Yes |
| `currency` | Currency | Yes (`precision`, `symbol`) | Yes |
| `percent` | Percent | Yes (`precision`) | Yes |
| `duration` | Duration | Yes (`durationFormat`) | Yes |
| `singleSelect` | Single select | Yes (`choices`) | Yes |
| `multipleSelects` | Multiple select | Yes (`choices`) | Yes |
| `checkbox` | Checkbox | Yes (`color`, `icon`) | Yes |
| `date` | Date | Yes (`dateFormat`) | Yes |
| `dateTime` | Date and time | Yes (`dateFormat`, `timeFormat`, `timeZone`) | Yes |
| `rating` | Rating | Yes (`max`, `color`, `icon`) | Yes |
| `multipleAttachments` | Attachment | Yes (`isReversed`) | Yes |
| `singleCollaborator` | Collaborator | No | Yes |
| `multipleCollaborators` | Collaborators | No | Yes |
| `multipleRecordLinks` | Link to another record | Yes (`linkedTableId`, etc.) | Yes |
| `barcode` | Barcode | No | Yes |
| `autoNumber` | Auto number | No | No (auto-generated) |
| `formula` | Formula | Yes (`expression`, `referencedFieldIds`, `result`) | No (computed) |
| `rollup` | Rollup | Yes (`fieldIdInLinkedTable`, `recordLinkFieldId`, `referencedFieldIds`, `result`) | No (computed) |
| `lookup` | Lookup | Yes (`fieldIdInLinkedTable`, `recordLinkFieldId`, `result`) | No (computed) |
| `count` | Count | Yes (`isValid`, `recordLinkFieldId`) | No (computed) |
| `createdTime` | Created time | Yes (`result`) | No (auto-generated) |
| `lastModifiedTime` | Last modified time | Yes (`fieldIdsToWatch`, `result`) | No (auto-generated) |
| `createdBy` | Created by | Yes (`result`) | No (auto-generated) |
| `lastModifiedBy` | Last modified by | Yes (`fieldIdsToWatch`, `result`) | No (auto-generated) |
| `button` | Button | Yes (`label`, `url` or `formula`) | No (interactive only) |
| `externalSyncSource` | Sync source | No | No (sync-managed) |
| `aiText` | AI-generated text | Yes (`prompt`, `referencedFieldIds`) | No (AI-generated) |

---

## 6. View Types Reference

All view types that may appear in a base schema. Views cannot be created or modified during base creation, but appear in schema responses.

| Type | Display Name | Description |
|------|-------------|-------------|
| `grid` | Grid view | Spreadsheet-like table view. The default view type created for every table. Displays records as rows with fields as columns. Supports sorting, filtering, grouping, and field reordering. |
| `form` | Form view | A data entry form. Allows external or internal users to submit new records through a form interface. Each visible field becomes a form input. |
| `calendar` | Calendar view | Displays records on a calendar. Requires at least one date or dateTime field to position records on the calendar. Supports day, week, month, and multi-month views. |
| `gallery` | Gallery view | Card-based view displaying records as visual cards. Ideal for image-heavy tables or when a visual overview is preferred over a tabular layout. |
| `kanban` | Kanban view | Board view with columns based on a single select, collaborator, or linked record field. Records appear as cards that can be dragged between columns. |
| `timeline` | Timeline view | Gantt chart-like view showing records along a timeline. Requires at least one date field for start dates, optionally a second for end dates. |
| `block` | Interface/Block | An interface designer block or dashboard. May contain multiple visual components and custom layouts. |

---

## 7. Error Codes

### Common Errors (All Endpoints)

| HTTP Status | Error Type | Description | Resolution |
|-------------|-----------|-------------|------------|
| 400 | `BAD_REQUEST` | Malformed request body or invalid JSON syntax. | Check that your JSON is valid and all required fields are present. |
| 401 | `AUTHENTICATION_REQUIRED` | No authorization header provided, or the token is malformed. | Ensure you include `Authorization: Bearer <token>` header with a valid token. |
| 403 | `NOT_AUTHORIZED` | The token is valid but does not have the required scope or permission level to perform this operation. | Check that your token has the necessary scopes (`schema.bases:read` or `schema.bases:write`) and that the user has adequate permissions on the target base or workspace. |
| 404 | `NOT_FOUND` | The specified resource (base ID, workspace ID) does not exist or the token does not have access to it. | Verify that the ID is correct and that the token has at least `read` access to the resource. |
| 422 | `INVALID_REQUEST` | The request body is syntactically valid JSON but contains semantic errors (e.g., invalid field type, duplicate names, missing required properties). | Review the error message for specific details about which field or property is invalid. |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests. The API enforces a rate limit of 5 requests per second per base. | Implement exponential backoff. Wait at least 30 seconds before retrying. Use the `Retry-After` header if present. |
| 500 | `SERVER_ERROR` | An unexpected internal error occurred on Airtable's servers. | Retry the request after a brief delay. If the error persists, contact Airtable support. |
| 503 | `SERVICE_UNAVAILABLE` | The Airtable service is temporarily unavailable, likely due to maintenance or high load. | Retry after a brief delay. Check Airtable's status page for ongoing incidents. |

### List Bases Specific Errors

| HTTP Status | Error Type | Description |
|-------------|-----------|-------------|
| 401 | `AUTHENTICATION_REQUIRED` | Token is missing or invalid. |
| 403 | `NOT_AUTHORIZED` | Token lacks the `schema.bases:read` scope. |
| 400 | `BAD_REQUEST` | Invalid `offset` parameter value. |

### Get Base Schema Specific Errors

| HTTP Status | Error Type | Description |
|-------------|-----------|-------------|
| 401 | `AUTHENTICATION_REQUIRED` | Token is missing or invalid. |
| 403 | `NOT_AUTHORIZED` | Token lacks the `schema.bases:read` scope, or user lacks `read` permission on the base. |
| 404 | `NOT_FOUND` | The base ID does not exist or the token cannot access it. |
| 422 | `INVALID_REQUEST` | Invalid value for the `include` parameter. |

### Create Base Specific Errors

| HTTP Status | Error Type | Description |
|-------------|-----------|-------------|
| 401 | `AUTHENTICATION_REQUIRED` | Token is missing or invalid. |
| 403 | `NOT_AUTHORIZED` | Token lacks the `schema.bases:write` scope, or user lacks permission to create bases in the specified workspace. |
| 404 | `NOT_FOUND` | The workspace ID does not exist or the token cannot access it. |
| 422 | `INVALID_REQUEST` | Various semantic errors in the request body. Common sub-errors include: |
| | | - `"name" is required` — Base name is missing. |
| | | - `"workspaceId" is required` — Workspace ID is missing. |
| | | - `"tables" must have at least one entry` — No tables provided. |
| | | - `"fields" must have at least one entry` — A table has no fields. |
| | | - `Duplicate table name` — Two tables share the same name. |
| | | - `Duplicate field name` — Two fields in the same table share the same name. |
| | | - `Invalid field type` — An unsupported field type was used. |
| | | - `Invalid options for field type` — The options object does not match the field type's schema. |
| | | - `Primary field type not supported` — The first field uses a type that cannot be a primary field. |

### Error Response Format

All errors follow this structure:

```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "Could not find table \"tblXXXXXX\" in the base. Please verify that the table exists."
  }
}
```

| Property | Type | Description |
|----------|------|-------------|
| `error.type` | string | Machine-readable error type identifier. |
| `error.message` | string | Human-readable description of what went wrong. May include specific details about which field or property caused the error. |

---

## 8. Required OAuth Scopes

To use the Bases API endpoints, your personal access token or OAuth integration must have the following scopes:

| Scope | Endpoints Enabled | Description |
|-------|-------------------|-------------|
| `schema.bases:read` | List Bases, Get Base Schema | Allows reading the list of bases and their full schema (tables, fields, views). This is a read-only scope. |
| `schema.bases:write` | Create Base | Allows creating new bases in workspaces where the user has permission. This scope implicitly includes `schema.bases:read` capabilities. |

### Scope Hierarchy

- `schema.bases:write` includes all permissions of `schema.bases:read`.
- If you only need to list bases or inspect schemas, use `schema.bases:read` to follow the principle of least privilege.
- Creating a base requires `schema.bases:write` even if you have `owner` permission on the workspace.

### Additional Related Scopes

While not directly part of the Bases API, these scopes are commonly used alongside base operations:

| Scope | Description |
|-------|-------------|
| `data.records:read` | Read record data from tables in accessible bases. |
| `data.records:write` | Create, update, and delete records in accessible bases. |
| `data.recordComments:read` | Read comments on records. |
| `data.recordComments:write` | Create, update, and delete comments on records. |
| `schema.bases:write` | Also enables table/field/view creation and modification via separate API endpoints (not just base creation). |
| `webhook:manage` | Create and manage webhooks for bases. |

---

## 9. Rate Limiting

The Airtable API enforces rate limits to ensure fair usage and service stability.

### Rate Limit Details

| Metric | Limit |
|--------|-------|
| Requests per second per base | 5 |
| Concurrent requests per base | Not officially documented, but requests exceeding 5/sec are throttled |

### Rate Limit Response

When you exceed the rate limit, the API returns:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

```json
{
  "error": {
    "type": "RATE_LIMIT_EXCEEDED",
    "message": "You have made too many requests in a short period of time. Please retry your request later."
  }
}
```

### Best Practices

- **Implement exponential backoff:** When you receive a 429 response, wait for the duration specified in the `Retry-After` header before retrying. If no header is present, wait at least 30 seconds.
- **Batch where possible:** For record operations, use batch endpoints to reduce the number of requests.
- **Cache schema data:** Base schemas change infrequently. Cache the results of Get Base Schema and only refresh when needed or when you detect schema changes.
- **Use pagination efficiently:** When listing bases, process each page fully before requesting the next one.

### Rate Limit Scope

- Rate limits are applied per base, not per token or per user. Different tokens accessing the same base share the same rate limit pool.
- The List Bases endpoint is not associated with any specific base, so it has its own rate limit pool.
- The Create Base endpoint's rate limit is associated with the workspace, not a specific base.

---

## 10. ID Format Reference

Airtable uses prefixed IDs to identify different resource types. These prefixes help you identify what type of resource an ID refers to.

| Prefix | Resource Type | Example | Description |
|--------|--------------|---------|-------------|
| `app` | Base | `appABC123def456` | Identifies a base (also called an "app" in the API). |
| `tbl` | Table | `tblXYZ789ghi012` | Identifies a table within a base. |
| `fld` | Field | `fldDEF456jkl789` | Identifies a field (column) within a table. |
| `viw` | View | `viwGHI012mno345` | Identifies a view on a table. |
| `rec` | Record | `recJKL345pqr678` | Identifies a record (row) within a table. |
| `sel` | Select choice | `selMNO678stu901` | Identifies a choice option within a select field. |
| `wsp` | Workspace | `wspPQR901vwx234` | Identifies a workspace (organization unit containing bases). |
| `usr` | User | `usrSTU234yza567` | Identifies a user/collaborator. |
| `itr` | Iterator/cursor | `itrVWX567bcd890` | Identifies a pagination cursor (used in offsets). |

### ID Characteristics

- All IDs are strings of alphanumeric characters following the prefix.
- IDs are globally unique across all Airtable resources.
- IDs are immutable once assigned and never change, even if the resource is renamed.
- IDs are case-sensitive.
- IDs should be treated as opaque strings; do not attempt to parse or construct them.
