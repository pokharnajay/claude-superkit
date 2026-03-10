# Airtable Field Types — Complete Reference

This is the master reference for every Airtable field type. For each type, this document covers:
- Type name and `type` value used in the API
- Options schema (every configurable property)
- Cell value format (what the API returns and accepts as JSON)
- Example create request
- Notes and limitations

> **API Base URL:** `https://api.airtable.com/v0`
> **Create field endpoint:** `POST /v0/meta/bases/{baseId}/tables/{tableId}/fields`

---

## Table of Contents

1. [singleLineText](#1-singlelinetext)
2. [email](#2-email)
3. [url](#3-url)
4. [multilineText](#4-multilinetext)
5. [number](#5-number)
6. [percent](#6-percent)
7. [currency](#7-currency)
8. [singleSelect](#8-singleselect)
9. [multipleSelects](#9-multipleselects)
10. [singleCollaborator](#10-singlecollaborator)
11. [multipleCollaborators](#11-multiplecollaborators)
12. [multipleRecordLinks](#12-multiplerecordlinks)
13. [date](#13-date)
14. [dateTime](#14-datetime)
15. [phoneNumber](#15-phonenumber)
16. [multipleAttachments](#16-multipleattachments)
17. [checkbox](#17-checkbox)
18. [rating](#18-rating)
19. [duration](#19-duration)
20. [richText](#20-richtext)
21. [autoNumber](#21-autonumber)
22. [barcode](#22-barcode)
23. [button](#23-button)
24. [lastModifiedBy](#24-lastmodifiedby)
25. [createdBy](#25-createdby)
26. [lastModifiedTime](#26-lastmodifiedtime)
27. [createdTime](#27-createdtime)
28. [formula](#28-formula)
29. [lookup](#29-lookup)
30. [rollup](#30-rollup)
31. [count](#31-count)
32. [externalSyncSource](#32-externalsyncsource)

---

## 1. singleLineText

Plain single-line text field.

**Type value:** `"singleLineText"`

### Options Schema

No options. This type does not accept or return an `options` object.

### Cell Value Format

- **Read:** `string` or `null`
- **Write:** `string`

```json
"Hello world"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Title",
    "type": "singleLineText",
    "description": "A short text title"
  }'
```

### Notes

- Maximum length: approximately 100,000 characters.
- The primary field of a table is often a `singleLineText` field.
- No formatting is applied; newlines are stripped.

---

## 2. email

Email address field. Validated as an email format in the UI but stored as a string in the API.

**Type value:** `"email"`

### Options Schema

No options.

### Cell Value Format

- **Read:** `string` or `null`
- **Write:** `string`

```json
"user@example.com"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Email Address",
    "type": "email"
  }'
```

### Notes

- The API does not enforce email format validation on writes; the UI does.
- Clickable as a mailto link in the Airtable UI.

---

## 3. url

URL field. Validated as a URL in the UI but stored as a string in the API.

**Type value:** `"url"`

### Options Schema

No options.

### Cell Value Format

- **Read:** `string` or `null`
- **Write:** `string`

```json
"https://example.com/page"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website",
    "type": "url"
  }'
```

### Notes

- The API does not enforce URL format validation on writes.
- Clickable as a hyperlink in the Airtable UI.

---

## 4. multilineText

Multi-line plain text field. Supports newlines but no formatting.

**Type value:** `"multilineText"`

### Options Schema

No options.

### Cell Value Format

- **Read:** `string` or `null`
- **Write:** `string`

```json
"Line one\nLine two\nLine three"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Description",
    "type": "multilineText",
    "description": "Detailed description with line breaks"
  }'
```

### Notes

- Newlines are preserved as `\n` in the JSON response.
- No rich formatting (bold, italic, etc.). Use `richText` for that.
- Maximum length: approximately 100,000 characters.

---

## 5. number

Numeric field with configurable decimal precision.

**Type value:** `"number"`

### Options Schema

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `precision` | integer | Yes | `1` | Number of decimal places. Range: `0` to `8`. `0` = integer. |

### Cell Value Format

- **Read:** `number` or `null`
- **Write:** `number`

```json
42
```

```json
3.14159265
```

### Example Create Request

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

**Decimal number:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Score",
    "type": "number",
    "options": {"precision": 2}
  }'
```

### Notes

- `precision: 0` stores integers only.
- `precision: 1` through `precision: 8` stores decimals with that many decimal places.
- Values are stored as IEEE 754 double-precision floating point.
- The UI rounds display to the configured precision; the API may return more decimal places.

---

## 6. percent

Percentage field. Stored as a decimal (0.5 = 50%) with configurable display precision.

**Type value:** `"percent"`

### Options Schema

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `precision` | integer | Yes | `0` | Number of decimal places displayed. Range: `0` to `8`. |

### Cell Value Format

- **Read:** `number` or `null` (stored as decimal, e.g., `0.5` = 50%)
- **Write:** `number` (decimal format)

```json
0.75
```

This represents 75%.

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Completion Rate",
    "type": "percent",
    "options": {"precision": 1}
  }'
```

### Notes

- The API uses decimal representation: `0.5` = 50%, `1.0` = 100%, `1.5` = 150%.
- The UI displays the value with a `%` symbol.
- When writing, pass the decimal value, not the percentage number.

---

## 7. currency

Currency field with a symbol and decimal precision.

**Type value:** `"currency"`

### Options Schema

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `precision` | integer | Yes | `2` | Number of decimal places. Range: `0` to `8`. |
| `symbol` | string | Yes | `"$"` | Currency symbol displayed before the value. |

### Cell Value Format

- **Read:** `number` or `null`
- **Write:** `number`

```json
29.99
```

### Example Create Request

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

**Euro currency:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cost (EUR)",
    "type": "currency",
    "options": {
      "precision": 2,
      "symbol": "\u20ac"
    }
  }'
```

### Notes

- The symbol is for display only; the API value is a raw number.
- Common symbols: `$`, `€`, `£`, `¥`, `₹`, `CHF`, `kr`, `R$`.
- The symbol can be any string, not just single characters.

---

## 8. singleSelect

Single choice from a predefined list of options.

**Type value:** `"singleSelect"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `choices` | array | Yes | Array of choice objects |

**Choice object:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Read-only | Choice ID (`selXXX`). Auto-generated on create. Required when updating existing choices. |
| `name` | string | Yes | Display name of the choice |
| `color` | string | No | Color identifier (see color list below) |

**Available colors:**
`blueLight1`, `blueLight2`, `blueBright`, `blueDark1`,
`cyanLight1`, `cyanLight2`, `cyanBright`, `cyanDark1`,
`tealLight1`, `tealLight2`, `tealBright`, `tealDark1`,
`greenLight1`, `greenLight2`, `greenBright`, `greenDark1`,
`yellowLight1`, `yellowLight2`, `yellowBright`, `yellowDark1`,
`orangeLight1`, `orangeLight2`, `orangeBright`, `orangeDark1`,
`redLight1`, `redLight2`, `redBright`, `redDark1`,
`pinkLight1`, `pinkLight2`, `pinkBright`, `pinkDark1`,
`purpleLight1`, `purpleLight2`, `purpleBright`, `purpleDark1`,
`grayLight1`, `grayLight2`, `grayBright`, `grayDark1`

### Cell Value Format

- **Read:** `string` (the choice name) or `null`
- **Write:** `string` (must match an existing choice name exactly, unless `typecast: true`)

```json
"In Progress"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Status",
    "type": "singleSelect",
    "options": {
      "choices": [
        {"name": "Backlog", "color": "blueLight2"},
        {"name": "In Progress", "color": "yellowLight2"},
        {"name": "Review", "color": "purpleLight2"},
        {"name": "Done", "color": "greenLight2"},
        {"name": "Cancelled", "color": "grayLight2"}
      ]
    }
  }'
```

### Notes

- Writing a value that does not match an existing choice returns an error unless `typecast: true` is set on the record write, which auto-creates the choice.
- Choices cannot be deleted via the API; they can only be added or renamed.
- When updating choices, include all existing choices with their `id` plus new choices without an `id`.
- Choice names must be unique within the field.

---

## 9. multipleSelects

Multiple choices from a predefined list of options.

**Type value:** `"multipleSelects"`

### Options Schema

Same as `singleSelect`:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `choices` | array | Yes | Array of choice objects (same schema as singleSelect) |

### Cell Value Format

- **Read:** `array of strings` (choice names) or `null` / empty array
- **Write:** `array of strings`

```json
["Bug", "High Priority", "Frontend"]
```

### Example Create Request

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
        {"name": "Enhancement", "color": "blueLight2"},
        {"name": "Documentation", "color": "purpleLight2"},
        {"name": "High Priority", "color": "orangeLight2"}
      ]
    }
  }'
```

### Notes

- Same color and choice management rules as `singleSelect`.
- Order of selected values is preserved.
- Writing replaces the entire array; to add a tag, read existing values first, append, and write back.

---

## 10. singleCollaborator

A single Airtable user (collaborator) on the base.

**Type value:** `"singleCollaborator"`

### Options Schema

No options.

### Cell Value Format

- **Read:** collaborator object or `null`
- **Write:** `{"id": "usrXXX"}` (only the `id` is required)

**Read format:**

```json
{
  "id": "usrABC123",
  "email": "alice@example.com",
  "name": "Alice Johnson"
}
```

**Write format:**

```json
{"id": "usrABC123"}
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assignee",
    "type": "singleCollaborator"
  }'
```

### Notes

- Only users who are collaborators on the base can be assigned.
- The `email` and `name` fields are read-only; only `id` is used for writes.
- Set to `null` to clear the collaborator.

---

## 11. multipleCollaborators

Multiple Airtable users (collaborators) on the base.

**Type value:** `"multipleCollaborators"`

### Options Schema

No options.

### Cell Value Format

- **Read:** array of collaborator objects or `null` / empty array
- **Write:** array of `{"id": "usrXXX"}` objects

**Read format:**

```json
[
  {"id": "usrABC123", "email": "alice@example.com", "name": "Alice Johnson"},
  {"id": "usrDEF456", "email": "bob@example.com", "name": "Bob Smith"}
]
```

**Write format:**

```json
[{"id": "usrABC123"}, {"id": "usrDEF456"}]
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Reviewers",
    "type": "multipleCollaborators"
  }'
```

### Notes

- Same collaborator rules as `singleCollaborator`.
- Writing replaces the entire array of collaborators.

---

## 12. multipleRecordLinks

Links to records in another table (or the same table for self-links).

**Type value:** `"multipleRecordLinks"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `linkedTableId` | string | Yes (create) | Table ID of the linked table (`tblXXX`) |
| `prefersSingleRecordLink` | boolean | No | If `true`, the UI shows this as a single link field (but the API still returns an array). Default: `false`. |
| `inverseLinkFieldId` | string | Read-only | Field ID of the automatically created inverse link field in the linked table |
| `isReversed` | boolean | Read-only | Whether this is the inverse (auto-created) side of a link |
| `viewIdForRecordSelection` | string | No | View ID to restrict which records can be linked |

### Cell Value Format

- **Read:** array of record link objects or `null` / empty array
- **Write:** array of `{"id": "recXXX"}` objects

**Read format:**

```json
[
  {"id": "recABC123"},
  {"id": "recDEF456"}
]
```

**Write format (same):**

```json
[{"id": "recABC123"}, {"id": "recDEF456"}]
```

### Example Create Request

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

**Single-link preference:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Primary Contact",
    "type": "multipleRecordLinks",
    "options": {
      "linkedTableId": "tblCONTACTS",
      "prefersSingleRecordLink": true
    }
  }'
```

### Notes

- Creating a link field automatically creates an inverse link field in the target table.
- Even with `prefersSingleRecordLink: true`, the API still returns/accepts an array.
- Self-linking (linking to the same table) is supported.
- You cannot change `linkedTableId` after creation.
- Writing replaces all linked records; to add a link, read existing links first, append, and write back.

---

## 13. date

Date-only field (no time component).

**Type value:** `"date"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `dateFormat` | object | Yes | Date display format |

**dateFormat object:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Format name: `"local"`, `"friendly"`, `"us"`, `"european"`, `"iso"` |
| `format` | string | The date format pattern string |

**Available date formats:**

| `name` | `format` | Example |
|--------|----------|---------|
| `"local"` | `"M/D/YYYY"` | 3/15/2024 |
| `"friendly"` | `"MMMM D, YYYY"` | March 15, 2024 |
| `"us"` | `"M/D/YYYY"` | 3/15/2024 |
| `"european"` | `"D/M/YYYY"` | 15/3/2024 |
| `"iso"` | `"YYYY-MM-DD"` | 2024-03-15 |

### Cell Value Format

- **Read:** `string` (ISO 8601 date) or `null`
- **Write:** `string` (ISO 8601 date)

```json
"2024-03-15"
```

### Example Create Request

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

### Notes

- The API always returns dates in ISO 8601 format (`YYYY-MM-DD`) regardless of the display format.
- The `dateFormat` only affects display in the Airtable UI.
- No time zone considerations for date-only fields.

---

## 14. dateTime

Date and time field with time zone support.

**Type value:** `"dateTime"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `dateFormat` | object | Yes | Date display format (same as `date` type) |
| `timeFormat` | object | Yes | Time display format |
| `timeZone` | string | Yes | IANA time zone identifier |

**timeFormat object:**

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Format name: `"12hour"` or `"24hour"` |
| `format` | string | The time format pattern string |

**Available time formats:**

| `name` | `format` | Example |
|--------|----------|---------|
| `"12hour"` | `"h:mma"` | 3:30pm |
| `"24hour"` | `"HH:mm"` | 15:30 |

**Common time zones:** `"America/New_York"`, `"America/Chicago"`, `"America/Denver"`, `"America/Los_Angeles"`, `"Europe/London"`, `"Europe/Paris"`, `"Europe/Berlin"`, `"Asia/Tokyo"`, `"Asia/Shanghai"`, `"Asia/Kolkata"`, `"Australia/Sydney"`, `"UTC"`, `"client"` (uses the viewer's local time zone)

### Cell Value Format

- **Read:** `string` (ISO 8601 datetime in UTC) or `null`
- **Write:** `string` (ISO 8601 datetime)

```json
"2024-03-15T15:30:00.000Z"
```

### Example Create Request

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

**12-hour format with friendly date:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Event Start",
    "type": "dateTime",
    "options": {
      "dateFormat": {"name": "friendly", "format": "MMMM D, YYYY"},
      "timeFormat": {"name": "12hour", "format": "h:mma"},
      "timeZone": "America/Los_Angeles"
    }
  }'
```

### Notes

- The API always returns datetimes in UTC (with `Z` suffix).
- The `timeZone` setting affects display in the Airtable UI and how input without timezone info is interpreted.
- Use `"client"` as the timeZone to use the viewer's local time zone.

---

## 15. phoneNumber

Phone number stored as a string.

**Type value:** `"phoneNumber"`

### Options Schema

No options.

### Cell Value Format

- **Read:** `string` or `null`
- **Write:** `string`

```json
"+1 (555) 123-4567"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phone",
    "type": "phoneNumber"
  }'
```

### Notes

- No format validation is enforced by the API. Any string is accepted.
- Clickable as a tel link in the Airtable UI.
- Store in international format (e.g., `+14155551234`) for consistency.

---

## 16. multipleAttachments

File attachments field. Stores an array of attachment objects.

**Type value:** `"multipleAttachments"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `isReversed` | boolean | Read-only | Whether attachment order is reversed |

### Cell Value Format

- **Read:** array of attachment objects or `null` / empty array
- **Write:** array of `{"url": "..."}` objects (for creating via URL)

**Read format (full attachment object):**

```json
[
  {
    "id": "attABC123",
    "url": "https://dl.airtable.com/.attachments/...",
    "filename": "document.pdf",
    "size": 245678,
    "type": "application/pdf",
    "width": null,
    "height": null,
    "thumbnails": {
      "small": {"url": "https://...", "width": 36, "height": 36},
      "large": {"url": "https://...", "width": 256, "height": 256},
      "full": {"url": "https://...", "width": 1000, "height": 1000}
    }
  },
  {
    "id": "attDEF456",
    "url": "https://dl.airtable.com/.attachments/...",
    "filename": "photo.jpg",
    "size": 1048576,
    "type": "image/jpeg",
    "width": 1920,
    "height": 1080,
    "thumbnails": {
      "small": {"url": "https://...", "width": 64, "height": 36},
      "large": {"url": "https://...", "width": 256, "height": 144},
      "full": {"url": "https://...", "width": 1920, "height": 1080}
    }
  }
]
```

**Attachment object properties:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Attachment ID (`attXXX`) |
| `url` | string | Temporary download URL (expires after a few hours) |
| `filename` | string | Original filename |
| `size` | integer | File size in bytes |
| `type` | string | MIME type (e.g., `image/jpeg`, `application/pdf`) |
| `width` | integer or null | Width in pixels (images only) |
| `height` | integer or null | Height in pixels (images only) |
| `thumbnails` | object or null | Thumbnail URLs (images only) with `small`, `large`, `full` variants |

**Write format (upload via URL):**

```json
[
  {"url": "https://example.com/file.pdf", "filename": "document.pdf"},
  {"url": "https://example.com/image.jpg"}
]
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Attachments",
    "type": "multipleAttachments"
  }'
```

### Notes

- Attachment URLs are **temporary** and expire after a few hours. Do not cache them permanently.
- To add attachments to a record, provide an array of `{"url": "..."}` objects. Airtable downloads the file from the URL.
- Writing replaces all attachments. To add new attachments, include existing attachment objects (with their `id`) plus new `{"url": "..."}` objects.
- Maximum file size: 5 MB on free plan, up to 100 MB on paid plans.
- Thumbnails are only generated for image files.

---

## 17. checkbox

Boolean checkbox field.

**Type value:** `"checkbox"`

### Options Schema

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `icon` | string | No | `"check"` | Icon style |
| `color` | string | No | `"greenBright"` | Icon color |

**Available icons:** `"check"`, `"xCheckbox"`, `"star"`, `"heart"`, `"thumbsUp"`, `"flag"`, `"dot"`

**Available colors:** `"greenBright"`, `"tealBright"`, `"cyanBright"`, `"blueBright"`, `"purpleBright"`, `"pinkBright"`, `"redBright"`, `"orangeBright"`, `"yellowBright"`, `"grayBright"`

### Cell Value Format

- **Read:** `true` or `null` (unchecked values are `null`, not `false`)
- **Write:** `true` or `false`

```json
true
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Approved",
    "type": "checkbox",
    "options": {
      "icon": "check",
      "color": "greenBright"
    }
  }'
```

**Star checkbox:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Starred",
    "type": "checkbox",
    "options": {
      "icon": "star",
      "color": "yellowBright"
    }
  }'
```

### Notes

- Unchecked values are returned as `null` (field omitted), not `false`.
- Writing `false` unchecks the checkbox.
- In `filterByFormula`, unchecked = `FALSE()` or `0`, checked = `TRUE()` or `1`.

---

## 18. rating

Star rating field with configurable maximum and icon.

**Type value:** `"rating"`

### Options Schema

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `max` | integer | Yes | `5` | Maximum rating value. Range: `1` to `10`. |
| `icon` | string | No | `"star"` | Icon style |
| `color` | string | No | `"yellowBright"` | Icon color |

**Available icons:** `"star"`, `"heart"`, `"thumbsUp"`, `"flag"`, `"dot"`

**Available colors:** Same as checkbox colors: `"greenBright"`, `"tealBright"`, `"cyanBright"`, `"blueBright"`, `"purpleBright"`, `"pinkBright"`, `"redBright"`, `"orangeBright"`, `"yellowBright"`, `"grayBright"`

### Cell Value Format

- **Read:** `integer` (1 to max) or `null` (no rating)
- **Write:** `integer` (1 to max) or `null` to clear

```json
4
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priority",
    "type": "rating",
    "options": {
      "max": 5,
      "icon": "star",
      "color": "yellowBright"
    }
  }'
```

**10-point heart rating:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Satisfaction",
    "type": "rating",
    "options": {
      "max": 10,
      "icon": "heart",
      "color": "redBright"
    }
  }'
```

### Notes

- A value of `0` is treated as no rating (same as `null`).
- Minimum meaningful value is `1`.
- The `max` value can be updated after field creation.

---

## 19. duration

Duration field stored in seconds with configurable display format.

**Type value:** `"duration"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `durationFormat` | string | Yes | Display format for the duration |

**Available duration formats:**

| `durationFormat` | Display Example | Description |
|-----------------|-----------------|-------------|
| `"h:mm"` | `1:30` | Hours and minutes |
| `"h:mm:ss"` | `1:30:45` | Hours, minutes, and seconds |
| `"h:mm:ss.S"` | `1:30:45.5` | With tenths of a second |
| `"h:mm:ss.SS"` | `1:30:45.50` | With hundredths of a second |
| `"h:mm:ss.SSS"` | `1:30:45.500` | With milliseconds |

### Cell Value Format

- **Read:** `number` (total seconds) or `null`
- **Write:** `number` (total seconds)

```json
5445
```

This represents 1 hour, 30 minutes, 45 seconds (1*3600 + 30*60 + 45).

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Time Spent",
    "type": "duration",
    "options": {
      "durationFormat": "h:mm:ss"
    }
  }'
```

### Notes

- The API always reads/writes in seconds as a number.
- Fractional seconds are supported for high-precision formats.
- To convert: `total_seconds = hours * 3600 + minutes * 60 + seconds`.

---

## 20. richText

Rich text field supporting Markdown-formatted content.

**Type value:** `"richText"`

### Options Schema

No options.

### Cell Value Format

- **Read:** `string` (Markdown-formatted) or `null`
- **Write:** `string` (Markdown-formatted)

```json
"# Heading\n\nThis is **bold** and *italic* text.\n\n- Item 1\n- Item 2\n\n[Link](https://example.com)"
```

### Supported Markdown Syntax

- Headings: `# H1`, `## H2`, `### H3`
- Bold: `**text**`
- Italic: `*text*`
- Strikethrough: `~~text~~`
- Code: `` `inline` `` and ` ```block``` `
- Links: `[text](url)`
- Lists: `- item` or `1. item`
- Blockquotes: `> text`
- Horizontal rules: `---`
- Mentions: `@[user name](usrXXX)`

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Notes",
    "type": "richText"
  }'
```

### Notes

- Rich text is stored and returned as Markdown.
- The Airtable UI renders the Markdown with formatting.
- User mentions use a special syntax: `@[Display Name](usrXXX)`.
- Not all Markdown features may be supported (e.g., tables, images).

---

## 21. autoNumber

Auto-incrementing integer assigned to each record. Read-only.

**Type value:** `"autoNumber"`

### Options Schema

No options. This field is fully automatic.

### Cell Value Format

- **Read:** `integer` or `null`
- **Write:** Not writable. This is a computed field.

```json
42
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Record Number",
    "type": "autoNumber"
  }'
```

### Notes

- Values are assigned sequentially starting from 1.
- Values are never reused, even if a record is deleted.
- Cannot be written to or modified via the API.
- Only one autoNumber field per table.

---

## 22. barcode

Barcode field storing a text value and optional type.

**Type value:** `"barcode"`

### Options Schema

No options.

### Cell Value Format

- **Read:** barcode object or `null`
- **Write:** barcode object

```json
{
  "text": "1234567890128",
  "type": "upce"
}
```

**Barcode object properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `text` | string | Yes | The barcode value |
| `type` | string | No | Barcode type (e.g., `"upce"`, `"code39"`, `"code128"`, `"ean13"`, `"qr"`) |

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Barcode",
    "type": "barcode"
  }'
```

### Notes

- The `type` field is optional and may not always be present.
- Barcodes can be scanned via the Airtable mobile app.
- The `text` property is the decoded barcode content.

---

## 23. button

Button field that triggers an action (open URL or run automation). Configuration is read-only via API.

**Type value:** `"button"`

### Options Schema (Read-Only)

| Property | Type | Description |
|----------|------|-------------|
| `label` | string | Button label text |
| `url` | string | URL to open when clicked (for URL buttons) |

### Cell Value Format

- **Read:** button object or `null`
- **Write:** Not writable. Button configuration is set in the Airtable UI.

**Read format:**

```json
{
  "label": "Open Link",
  "url": "https://example.com/record/123"
}
```

### Example Create Request

Button fields cannot be fully configured via the API. You can create the field, but the button action must be configured in the Airtable UI.

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Open Link",
    "type": "button"
  }'
```

### Notes

- Button actions (URL formula or automation trigger) must be configured in the Airtable UI.
- The cell value is read-only via the API.
- Two button action types: "Open URL" (opens a URL formula) and "Run automation" (triggers an automation).

---

## 24. lastModifiedBy

Automatically tracks which collaborator last modified the record. Computed, read-only.

**Type value:** `"lastModifiedBy"`

### Options Schema (Read-Only)

| Property | Type | Description |
|----------|------|-------------|
| `referencedFieldIds` | array | If specified, only tracks modifications to these field IDs. If `null`, tracks all fields. |

### Cell Value Format

- **Read:** collaborator object or `null`
- **Write:** Not writable. This is a computed field.

```json
{
  "id": "usrABC123",
  "email": "alice@example.com",
  "name": "Alice Johnson"
}
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Last Modified By",
    "type": "lastModifiedBy"
  }'
```

### Notes

- Automatically updates when any tracked field changes.
- API modifications (via access token) may show a system user or the token owner.
- Cannot be written to or cleared.

---

## 25. createdBy

Automatically records which collaborator created the record. Computed, read-only.

**Type value:** `"createdBy"`

### Options Schema

No configurable options. This field is fully automatic.

### Cell Value Format

- **Read:** collaborator object or `null`
- **Write:** Not writable. This is a computed field.

```json
{
  "id": "usrDEF456",
  "email": "bob@example.com",
  "name": "Bob Smith"
}
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Created By",
    "type": "createdBy"
  }'
```

### Notes

- Set once when the record is created and never changes.
- Records created via API will show the token owner as the creator.
- Cannot be written to or modified.

---

## 26. lastModifiedTime

Automatically tracks when the record was last modified. Computed, read-only.

**Type value:** `"lastModifiedTime"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `isValid` | boolean | Read-only | Whether the field configuration is valid |
| `referencedFieldIds` | array | No | If specified, only tracks modifications to these field IDs. If `null`, tracks all fields. |
| `result` | object | No | Display format configuration |

**result object:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"dateTime"` or `"date"` |
| `options` | object | Format options (same as `dateTime` or `date` type options) |

### Cell Value Format

- **Read:** `string` (ISO 8601 datetime in UTC) or `null`
- **Write:** Not writable. This is a computed field.

```json
"2024-03-15T15:30:00.000Z"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Last Modified",
    "type": "lastModifiedTime",
    "options": {
      "result": {
        "type": "dateTime",
        "options": {
          "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"},
          "timeFormat": {"name": "24hour", "format": "HH:mm"},
          "timeZone": "America/New_York"
        }
      }
    }
  }'
```

### Notes

- Always returns UTC timestamps via the API regardless of configured time zone.
- The `result` options only affect display in the Airtable UI.
- If `referencedFieldIds` is set, the timestamp only updates when those specific fields change.

---

## 27. createdTime

Automatically records when the record was created. Computed, read-only.

**Type value:** `"createdTime"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `result` | object | No | Display format configuration |

**result object:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Always `"dateTime"` or `"date"` |
| `options` | object | Format options (same as `dateTime` or `date` type options) |

### Cell Value Format

- **Read:** `string` (ISO 8601 datetime in UTC) or `null`
- **Write:** Not writable. This is a computed field.

```json
"2024-01-10T09:15:00.000Z"
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Created At",
    "type": "createdTime",
    "options": {
      "result": {
        "type": "dateTime",
        "options": {
          "dateFormat": {"name": "friendly", "format": "MMMM D, YYYY"},
          "timeFormat": {"name": "12hour", "format": "h:mma"},
          "timeZone": "UTC"
        }
      }
    }
  }'
```

### Notes

- Set once when the record is created and never changes.
- Always returns UTC timestamps via the API.
- Note: the record object itself always includes a `createdTime` property, even without this field type.

---

## 28. formula

Computed field that evaluates an Airtable formula expression.

**Type value:** `"formula"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `expression` | string | Yes | The Airtable formula expression |
| `referencedFieldIds` | array | Read-only | Field IDs referenced in the formula |
| `result` | object | Read-only | The computed result type and its options |

**result object:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Result type: `"singleLineText"`, `"number"`, `"date"`, `"dateTime"`, `"checkbox"`, etc. |
| `options` | object | Type-specific options for the result type |

### Cell Value Format

- **Read:** varies depending on formula result type (string, number, boolean, date, array, etc.) or `null`
- **Write:** Not writable. This is a computed field.

**String result:**
```json
"Alice Johnson"
```

**Number result:**
```json
150.5
```

**Boolean result:**
```json
true
```

**Error result:**
```json
{"error": {"type": "ERROR_TYPE"}}
```

### Example Create Request

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

**Numeric formula:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Total Cost",
    "type": "formula",
    "options": {
      "expression": "{Quantity} * {Unit Price}"
    }
  }'
```

**Conditional formula:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Status Label",
    "type": "formula",
    "options": {
      "expression": "IF({Complete}, \"Done\", \"Pending\")"
    }
  }'
```

### Notes

- The `result` type is determined automatically from the formula and cannot be set manually.
- Reference other fields using `{Field Name}` syntax.
- Supports many functions: `CONCATENATE`, `IF`, `SUM`, `AVERAGE`, `LEN`, `SEARCH`, `DATETIME_FORMAT`, `CREATED_TIME`, `LAST_MODIFIED_TIME`, etc.
- Formula errors are returned as objects with an `error` property.
- The formula expression can be updated via the Update Field endpoint.

---

## 29. lookup

Looks up field values from linked records.

**Type value:** `"lookup"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `recordLinkFieldId` | string | Yes | Field ID of the `multipleRecordLinks` field to look through (`fldXXX`) |
| `fieldIdInLinkedTable` | string | Yes | Field ID in the linked table to pull values from (`fldXXX`) |
| `result` | object | Read-only | The result type based on the looked-up field |

**result object:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Result type matching the looked-up field's type |
| `options` | object | Type-specific options for the result type |

### Cell Value Format

- **Read:** array of looked-up values (type depends on the source field) or `null`
- **Write:** Not writable. This is a computed field.

**Lookup of text values:**
```json
["Project Alpha", "Project Beta"]
```

**Lookup of number values:**
```json
[100, 250, 50]
```

**Lookup of select values:**
```json
["Active", "Pending"]
```

### Example Create Request

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Names",
    "type": "lookup",
    "options": {
      "recordLinkFieldId": "fldLINK123",
      "fieldIdInLinkedTable": "fldNAME456"
    }
  }'
```

### Notes

- Requires an existing `multipleRecordLinks` field in the same table.
- The `recordLinkFieldId` must point to a link field in the current table.
- The `fieldIdInLinkedTable` must be a valid field ID in the target table.
- Returns an array even if only one linked record exists.
- Lookup values update automatically when the source data changes.
- Cannot look up computed fields in some cases (formula of formula, etc.).

---

## 30. rollup

Aggregates values from linked records using an aggregation function.

**Type value:** `"rollup"`

### Options Schema

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `recordLinkFieldId` | string | Yes | Field ID of the `multipleRecordLinks` field (`fldXXX`) |
| `fieldIdInLinkedTable` | string | Yes | Field ID in the linked table to aggregate (`fldXXX`) |
| `referencedFieldIds` | array | Yes | Array containing the `fieldIdInLinkedTable` value |
| `result` | object | Read-only | The computed result type |

**result object:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | string | Result type determined by the rollup function |
| `options` | object | Type-specific options for the result |

### Cell Value Format

- **Read:** varies by aggregation function (number, string, date, etc.) or `null`
- **Write:** Not writable. This is a computed field.

**Numeric rollup (SUM, AVERAGE, etc.):**
```json
450.5
```

**Array rollup (ARRAYUNIQUE, ARRAYJOIN, etc.):**
```json
"Alpha, Beta, Gamma"
```

### Common Aggregation Functions

These are set as part of the rollup configuration (though the API uses `referencedFieldIds` to identify the source field and Airtable determines the function from the UI configuration):

- `SUM(values)` — sum of all values
- `AVERAGE(values)` — average of all values
- `MIN(values)` — minimum value
- `MAX(values)` — maximum value
- `COUNT(values)` — count of non-empty values
- `COUNTA(values)` — count of non-empty values (including text)
- `COUNTALL(values)` — count of all values including empty
- `ARRAYJOIN(values, ", ")` — join values into a string
- `ARRAYUNIQUE(values)` — unique values only
- `ARRAYCOMPACT(values)` — remove empty values
- `AND(values)` — logical AND of boolean values
- `OR(values)` — logical OR of boolean values
- `XOR(values)` — logical XOR of boolean values
- `CONCATENATE(values)` — concatenate all values

### Example Create Request

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

### Notes

- Requires an existing `multipleRecordLinks` field in the same table.
- The aggregation function is configured in the Airtable UI or inferred from the formula.
- `referencedFieldIds` must include at least the `fieldIdInLinkedTable`.
- The result type depends on the aggregation function and the source field type.
- Rollup values update automatically when linked records change.

---

## 31. count

Counts the number of linked records. Computed, read-only.

**Type value:** `"count"`

### Options Schema

| Property | Type | Description |
|----------|------|-------------|
| `isValid` | boolean | Read-only. Whether the count field configuration is valid. |
| `recordLinkFieldId` | string | Read-only. The link field being counted. |

### Cell Value Format

- **Read:** `integer` or `null` (0 if no linked records)
- **Write:** Not writable. This is a computed field.

```json
5
```

### Example Create Request

Count fields are typically created in the Airtable UI because they reference a specific link field. If creating via API:

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/tables/{tableId}/fields" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Number of Tasks",
    "type": "count",
    "options": {
      "recordLinkFieldId": "fldLINK123"
    }
  }'
```

### Notes

- Counts the total number of records linked through a specific `multipleRecordLinks` field.
- Updates automatically when linked records are added or removed.
- Returns `null` for records with no linked records, or `0` depending on context.
- Cannot be written to or modified.

---

## 32. externalSyncSource

Represents data synced from an external source (e.g., Google Calendar, Jira, Salesforce). Fully read-only and managed by Airtable's sync feature.

**Type value:** `"externalSyncSource"`

### Options Schema

No user-configurable options. This field type is managed by Airtable's sync infrastructure.

### Cell Value Format

- **Read:** `string` or `null`
- **Write:** Not writable. This is a system-managed field.

```json
"Salesforce"
```

### Example Create Request

This field type **cannot** be created via the API. It is automatically created when you set up an external data sync in the Airtable UI.

### Notes

- Created automatically when configuring a sync from an external source.
- Cannot be created, modified, or deleted via the API.
- Indicates the origin of synced data.
- The field value identifies the external source type or name.

---

## Field Type Categories Summary

### Editable Text Fields
| Type | Cell Value | Options |
|------|-----------|---------|
| `singleLineText` | `string` | None |
| `multilineText` | `string` | None |
| `richText` | `string` (Markdown) | None |
| `email` | `string` | None |
| `url` | `string` | None |
| `phoneNumber` | `string` | None |

### Editable Numeric Fields
| Type | Cell Value | Key Options |
|------|-----------|-------------|
| `number` | `number` | `precision` (0-8) |
| `percent` | `number` (decimal) | `precision` (0-8) |
| `currency` | `number` | `precision` (0-8), `symbol` |
| `rating` | `integer` (1-max) | `max` (1-10), `icon`, `color` |
| `duration` | `number` (seconds) | `durationFormat` |

### Editable Choice Fields
| Type | Cell Value | Key Options |
|------|-----------|-------------|
| `singleSelect` | `string` | `choices` array |
| `multipleSelects` | `array of strings` | `choices` array |
| `checkbox` | `true` or `null` | `icon`, `color` |

### Editable Date Fields
| Type | Cell Value | Key Options |
|------|-----------|-------------|
| `date` | `string` (YYYY-MM-DD) | `dateFormat` |
| `dateTime` | `string` (ISO 8601 UTC) | `dateFormat`, `timeFormat`, `timeZone` |

### Editable Relationship Fields
| Type | Cell Value | Key Options |
|------|-----------|-------------|
| `multipleRecordLinks` | `array of {id}` | `linkedTableId`, `prefersSingleRecordLink` |
| `singleCollaborator` | `{id, email, name}` | None |
| `multipleCollaborators` | `array of {id, email, name}` | None |

### Editable Other Fields
| Type | Cell Value | Key Options |
|------|-----------|-------------|
| `multipleAttachments` | `array of attachment objects` | None |
| `barcode` | `{text, type}` | None |

### Computed / Read-Only Fields
| Type | Cell Value | Writable |
|------|-----------|----------|
| `formula` | varies | No |
| `lookup` | array of values | No |
| `rollup` | varies | No |
| `count` | `integer` | No |
| `autoNumber` | `integer` | No |
| `createdTime` | `string` (ISO datetime) | No |
| `lastModifiedTime` | `string` (ISO datetime) | No |
| `createdBy` | collaborator object | No |
| `lastModifiedBy` | collaborator object | No |
| `button` | `{label, url}` | No |
| `externalSyncSource` | `string` | No |
