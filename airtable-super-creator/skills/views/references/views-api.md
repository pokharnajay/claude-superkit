# Airtable Views API Reference

Complete reference for all Airtable Views API endpoints, response schemas, and view type details.

> **Base URL:** `https://api.airtable.com/v0`
> **Auth:** All requests require `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`

---

## Endpoints

### 1. List Views

**`GET /v0/meta/bases/{baseId}/tables/{tableId}/views`**

Returns all views configured for a specific table.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (format: `appXXXXXXXXXXXXXX`) |
| `tableId` | string | Yes | The ID of the table (format: `tblXXXXXXXXXXXXXX`) |

#### Response Schema

```json
{
  "views": [
    {
      "id": "viwXXXXXXXXXXXXXX",
      "name": "string",
      "type": "grid | form | calendar | gallery | kanban | timeline | block",
      "personalForNonOwner": false
    }
  ]
}
```

#### Response Fields

| Field | Type | Always Present | Description |
|-------|------|----------------|-------------|
| `views` | array | Yes | Array of view objects |
| `views[].id` | string | Yes | Unique view identifier (format: `viwXXXXXXXXXXXXXX`) |
| `views[].name` | string | Yes | Human-readable display name of the view |
| `views[].type` | string | Yes | The view type identifier (see View Types section below) |
| `views[].personalForNonOwner` | boolean | Yes | Whether this is a personal view. If `true`, the view configuration is personal to the owner; non-owner collaborators see a default personal copy |

#### Full Response Example

```json
{
  "views": [
    {
      "id": "viwABC123def456",
      "name": "Grid view",
      "type": "grid",
      "personalForNonOwner": false
    },
    {
      "id": "viwDEF456ghi789",
      "name": "Project Board",
      "type": "kanban",
      "personalForNonOwner": false
    },
    {
      "id": "viwGHI789jkl012",
      "name": "Photo Gallery",
      "type": "gallery",
      "personalForNonOwner": true
    },
    {
      "id": "viwJKL012mno345",
      "name": "Submit Request",
      "type": "form",
      "personalForNonOwner": false
    },
    {
      "id": "viwMNO345pqr678",
      "name": "Event Calendar",
      "type": "calendar",
      "personalForNonOwner": false
    },
    {
      "id": "viwPQR678stu901",
      "name": "Project Timeline",
      "type": "timeline",
      "personalForNonOwner": false
    }
  ]
}
```

---

### 2. Get View Metadata

**`GET /v0/meta/bases/{baseId}/tables/{tableId}/views/{viewId}`**

Returns detailed metadata for a single view including visible field order, filter configuration, sort configuration, and group levels.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (format: `appXXXXXXXXXXXXXX`) |
| `tableId` | string | Yes | The ID of the table (format: `tblXXXXXXXXXXXXXX`) |
| `viewId` | string | Yes | The ID of the view (format: `viwXXXXXXXXXXXXXX`) |

#### Response Schema

```json
{
  "id": "viwXXXXXXXXXXXXXX",
  "name": "string",
  "type": "grid | form | calendar | gallery | kanban | timeline | block",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXXX", "fldYYY", "fldZZZ"],
  "filters": {
    "conjunction": "and | or",
    "filterSet": [
      {
        "fieldId": "fldXXXXXXXXXXXXXX",
        "operator": "string",
        "value": "any"
      }
    ]
  },
  "sorts": [
    {
      "fieldId": "fldXXXXXXXXXXXXXX",
      "direction": "asc | desc"
    }
  ],
  "groupLevels": [
    {
      "fieldId": "fldXXXXXXXXXXXXXX",
      "direction": "asc | desc"
    }
  ]
}
```

#### Response Fields

| Field | Type | Always Present | Description |
|-------|------|----------------|-------------|
| `id` | string | Yes | Unique view identifier |
| `name` | string | Yes | Human-readable display name |
| `type` | string | Yes | View type identifier |
| `personalForNonOwner` | boolean | Yes | Whether the view is personal |
| `visibleFieldIds` | array of strings | No | Ordered list of field IDs that are visible in the view. The order matches the column order in the view. Only present for views that support column ordering |
| `filters` | object | No | Filter configuration. Only present if the view has active filters |
| `sorts` | array | No | Sort configuration. Only present if the view has active sorts |
| `groupLevels` | array | No | Group configuration. Only present if the view has active grouping |

#### Filter Object Schema

```json
{
  "conjunction": "and",
  "filterSet": [
    {
      "fieldId": "fldDEF456",
      "operator": "=",
      "value": "Active"
    },
    {
      "fieldId": "fldGHI789",
      "operator": "isNotEmpty"
    },
    {
      "conjunction": "or",
      "filterSet": [
        {
          "fieldId": "fldJKL012",
          "operator": ">",
          "value": 10
        },
        {
          "fieldId": "fldJKL012",
          "operator": "=",
          "value": 0
        }
      ]
    }
  ]
}
```

#### Filter Fields

| Field | Type | Description |
|-------|------|-------------|
| `conjunction` | string | How to combine filters: `"and"` (all must match) or `"or"` (any must match) |
| `filterSet` | array | Array of filter conditions or nested filter groups |
| `filterSet[].fieldId` | string | The field ID to filter on |
| `filterSet[].operator` | string | The comparison operator (see Filter Operators below) |
| `filterSet[].value` | any | The value to compare against. Not present for unary operators like `isEmpty` |
| `filterSet[].conjunction` | string | Present for nested filter groups, enabling complex AND/OR combinations |
| `filterSet[].filterSet` | array | Present for nested filter groups |

#### Filter Operators

| Operator | Description | Applicable Field Types |
|----------|-------------|----------------------|
| `=` | Equals | Text, number, select, date |
| `!=` | Not equals | Text, number, select, date |
| `<` | Less than | Number, date |
| `>` | Greater than | Number, date |
| `<=` | Less than or equal to | Number, date |
| `>=` | Greater than or equal to | Number, date |
| `contains` | Contains substring | Text, long text, rich text |
| `doesNotContain` | Does not contain substring | Text, long text, rich text |
| `isEmpty` | Field is empty (no value) | All field types |
| `isNotEmpty` | Field has a value | All field types |
| `isWithin` | Date is within range | Date, dateTime |
| `isBefore` | Date is before value | Date, dateTime |
| `isAfter` | Date is after value | Date, dateTime |
| `isExactly` | Date is exactly value | Date, dateTime |
| `hasAnyOf` | Has any of the values | Multiple select, linked records |
| `hasAllOf` | Has all of the values | Multiple select, linked records |
| `hasNoneOf` | Has none of the values | Multiple select, linked records |
| `isAnyOf` | Is any of the values | Single select |
| `isNoneOf` | Is none of the values | Single select |
| `filename` | Attachment filename match | Attachment |
| `filetype` | Attachment file type match | Attachment |

#### Sort Object Schema

```json
{
  "fieldId": "fldJKL012",
  "direction": "asc"
}
```

#### Sort Fields

| Field | Type | Description |
|-------|------|-------------|
| `fieldId` | string | The field ID to sort by |
| `direction` | string | Sort direction: `"asc"` (ascending A-Z, 0-9, oldest first) or `"desc"` (descending Z-A, 9-0, newest first) |

When multiple sort objects are present, they are applied in order (first sort is primary, second is secondary, etc.).

#### Group Level Object Schema

```json
{
  "fieldId": "fldDEF456",
  "direction": "asc"
}
```

#### Group Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `fieldId` | string | The field ID to group records by |
| `direction` | string | Order of groups: `"asc"` (ascending) or `"desc"` (descending) |

Groups organize records into collapsible sections based on the field value. Multiple group levels create nested groupings.

---

## View Types

### grid

The default spreadsheet-style view. Records are displayed as rows with fields as columns.

**Supports:** `visibleFieldIds`, `filters`, `sorts`, `groupLevels`

**Characteristics:**
- Most common view type; every table has at least one grid view
- Supports row height adjustment (short, medium, tall, extra tall)
- Supports frozen columns
- Supports row coloring based on conditions
- Supports field-level column width customization

**Metadata example:**

```json
{
  "id": "viwABC123",
  "name": "All Records",
  "type": "grid",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXYZ789", "fldDEF456", "fldGHI789"],
  "filters": {
    "conjunction": "and",
    "filterSet": [
      {"fieldId": "fldDEF456", "operator": "=", "value": "Active"}
    ]
  },
  "sorts": [
    {"fieldId": "fldXYZ789", "direction": "asc"}
  ],
  "groupLevels": [
    {"fieldId": "fldDEF456", "direction": "asc"}
  ]
}
```

### form

A form view for submitting new records. Each field becomes a form input.

**Supports:** `visibleFieldIds` (determines which fields appear in the form)

**Characteristics:**
- Used for data collection from collaborators or external users
- Fields can be marked as required
- Supports a cover image and description
- Shareable via public URL
- Does not support filters, sorts, or groupLevels in metadata

**Metadata example:**

```json
{
  "id": "viwFRM123",
  "name": "Submit Request",
  "type": "form",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXYZ789", "fldDEF456"]
}
```

### calendar

Displays records on a calendar based on a date or dateTime field.

**Supports:** `visibleFieldIds`, `filters`, `sorts`

**Characteristics:**
- Requires at least one date or dateTime field
- Supports month, 2-week, week, 3-day, and day views
- Records without a date value are hidden
- Can display date ranges if two date fields are configured

**Metadata example:**

```json
{
  "id": "viwCAL123",
  "name": "Event Calendar",
  "type": "calendar",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXYZ789", "fldJKL012"],
  "filters": {
    "conjunction": "and",
    "filterSet": [
      {"fieldId": "fldDEF456", "operator": "=", "value": "Confirmed"}
    ]
  }
}
```

### gallery

A card-based view showing records as visual cards with a cover image.

**Supports:** `visibleFieldIds`, `filters`, `sorts`

**Characteristics:**
- Displays records as cards in a responsive grid
- Can use an attachment field as the card cover image
- Configurable card size
- Each card shows a subset of fields
- Ideal for visual catalogs, portfolios, and media libraries

**Metadata example:**

```json
{
  "id": "viwGAL123",
  "name": "Photo Gallery",
  "type": "gallery",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXYZ789", "fldATTACH1"],
  "sorts": [
    {"fieldId": "fldXYZ789", "direction": "desc"}
  ]
}
```

### kanban

A board view with records grouped into stacked columns based on a single select, collaborator, or linked record field.

**Supports:** `visibleFieldIds`, `filters`, `sorts`, `groupLevels`

**Characteristics:**
- Records are displayed as cards in vertical columns
- Columns correspond to field values (e.g., select options)
- Drag-and-drop to move records between columns
- Supports a "hidden" stack for uncategorized records
- Configurable card fields and cover image

**Metadata example:**

```json
{
  "id": "viwKAN123",
  "name": "Project Board",
  "type": "kanban",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXYZ789", "fldGHI789", "fldJKL012"],
  "filters": {
    "conjunction": "and",
    "filterSet": [
      {"fieldId": "fldDEF456", "operator": "isNotEmpty"}
    ]
  },
  "groupLevels": [
    {"fieldId": "fldDEF456", "direction": "asc"}
  ]
}
```

### timeline

A Gantt-style view showing records across a horizontal timeline.

**Supports:** `visibleFieldIds`, `filters`, `sorts`, `groupLevels`

**Characteristics:**
- Requires at least one date field (start date); optionally a second date field (end date)
- Records appear as horizontal bars on a time axis
- Supports day, week, month, quarter, and year granularity
- Records can be grouped into swimlanes
- Drag-and-drop to change dates

**Metadata example:**

```json
{
  "id": "viwTML123",
  "name": "Project Timeline",
  "type": "timeline",
  "personalForNonOwner": false,
  "visibleFieldIds": ["fldXYZ789", "fldSTART1", "fldEND1"],
  "groupLevels": [
    {"fieldId": "fldDEF456", "direction": "asc"}
  ]
}
```

### block

An interface or dashboard block view. These are views embedded within Airtable interfaces.

**Supports:** Limited metadata; configuration is managed within the interface designer.

**Characteristics:**
- Part of Airtable's Interface Designer feature
- Can embed charts, filtered record lists, summaries, and forms
- Configuration is primarily managed through the Airtable UI
- Limited API metadata exposure compared to other view types

**Metadata example:**

```json
{
  "id": "viwBLK123",
  "name": "Dashboard Block",
  "type": "block",
  "personalForNonOwner": false
}
```

---

## View Type Feature Matrix

| Feature | grid | form | calendar | gallery | kanban | timeline | block |
|---------|------|------|----------|---------|--------|----------|-------|
| `visibleFieldIds` | Yes | Yes | Yes | Yes | Yes | Yes | No |
| `filters` | Yes | No | Yes | Yes | Yes | Yes | No |
| `sorts` | Yes | No | Yes | Yes | Yes | Yes | No |
| `groupLevels` | Yes | No | No | No | Yes | Yes | No |
| Drag-and-drop reorder | No | No | No | No | Yes | Yes | No |
| Date field required | No | No | Yes | No | No | Yes | No |
| Cover image support | No | No | No | Yes | Yes | No | No |
| Public sharing | No | Yes | No | No | No | No | No |

---

## Personal vs Shared Views

Views in Airtable can be either **shared** or **personal**:

| Property | Shared View | Personal View |
|----------|-------------|---------------|
| `personalForNonOwner` | `false` | `true` |
| Visibility | All collaborators see the same configuration | Only the owner sees their configuration |
| Non-owner access | Everyone shares filters, sorts, and column order | Non-owners see a default personal copy they can customize |
| Modifications | Changes affect all collaborators (if they have permission) | Changes only affect the individual user |

When `personalForNonOwner` is `true`:
- The view returned via the API reflects the **owner's** configuration
- Other users interacting with this view in the Airtable UI see their own personal copy
- API requests always operate on the canonical (owner's) version of the view

---

## ID Formats

| Entity | Format | Example |
|--------|--------|---------|
| Base | `app` + 14 alphanumeric chars | `appABC123def456gh` |
| Table | `tbl` + 14 alphanumeric chars | `tblABC123def456gh` |
| View | `viw` + 14 alphanumeric chars | `viwABC123def456gh` |
| Field | `fld` + 14 alphanumeric chars | `fldABC123def456gh` |

---

## Error Responses

### 401 Unauthorized

```json
{
  "error": {
    "type": "AUTHENTICATION_REQUIRED",
    "message": "You must provide a valid API key to perform this operation"
  }
}
```

### 403 Forbidden

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You are not permitted to perform this operation"
  }
}
```

Occurs when the token does not have the `schema.bases:read` scope, or the token does not have access to the specified base.

### 404 Not Found

```json
{
  "error": {
    "type": "NOT_FOUND",
    "message": "Could not find what you are looking for"
  }
}
```

Possible causes:
- The `baseId` does not exist or the token does not have access
- The `tableId` does not exist in the specified base
- The `viewId` does not exist in the specified table

### 429 Too Many Requests

```json
{
  "error": {
    "type": "TOO_MANY_REQUESTS",
    "message": "You have made too many requests in a short period of time. Please retry your request later."
  }
}
```

Back off and retry after the duration specified in the `Retry-After` response header (in seconds).

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Per-base limit | 5 requests per second |
| Cross-base limit | 50 requests per second per token |
| Retry behavior | Exponential backoff recommended; respect `Retry-After` header |

---

## Required Scopes

Both view endpoints require the `schema.bases:read` scope on the personal access token.

| Endpoint | Method | Scope |
|----------|--------|-------|
| List Views | GET | `schema.bases:read` |
| Get View Metadata | GET | `schema.bases:read` |

---

## Usage Notes

1. **View ordering:** The list endpoint returns views in the order they appear in the Airtable UI sidebar.
2. **Field ID resolution:** The `visibleFieldIds` array contains field IDs, not names. Use the Get Base Schema endpoint (`GET /v0/meta/bases/{baseId}/tables`) to resolve field IDs to names.
3. **Filter availability:** Not all views expose their filter configuration via the API. Form views and block views do not return filter metadata.
4. **Nested filters:** Filter sets can contain nested filter groups with their own `conjunction` and `filterSet`, enabling complex AND/OR logic combinations.
5. **Default view:** Every table always has at least one view (typically a grid view). This default view cannot be deleted.
6. **View-scoped record queries:** When listing records via `GET /v0/{baseId}/{tableIdOrName}`, you can pass a `view` query parameter to apply that view's filters, sorts, and field order to the record response.
