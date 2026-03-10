# Airtable Records API — Complete Reference

Base URL: `https://api.airtable.com/v0`

All requests require the header `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`.

Rate limit: 5 requests per second per base. Exceeding this returns HTTP 429.

---

## Table of Contents

1. [List Records](#1-list-records)
2. [Get Record](#2-get-record)
3. [Create Records](#3-create-records)
4. [Update Record (Single)](#4-update-record-single)
5. [Update Multiple Records](#5-update-multiple-records)
6. [Delete Record (Single)](#6-delete-record-single)
7. [Delete Multiple Records](#7-delete-multiple-records)
8. [filterByFormula Reference](#8-filterbyformula-reference)
9. [Cell Value Formats](#9-cell-value-formats)
10. [Pagination Details](#10-pagination-details)
11. [Error Codes](#11-error-codes)

---

## 1. List Records

### GET Method

**`GET /v0/{baseId}/{tableIdOrName}`**

Returns a paginated list of records from a table. Records are returned in an unspecified order unless a `sort` or `view` parameter is provided.

### Query Parameters (Complete Reference)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fields[]` | array of strings | No | all fields | Only return data for the specified fields. Specify multiple by repeating: `fields[]=Name&fields[]=Email`. Accepts field names or field IDs. Unknown field names are ignored. |
| `filterByFormula` | string | No | none | An Airtable formula used to filter records. The formula is evaluated for each record, and if the result is falsy (0, empty string, `NaN`, `false`, or blank), the record is omitted. See [filterByFormula Reference](#8-filterbyformula-reference). |
| `maxRecords` | integer | No | unlimited | The maximum total number of records to return across all pages. Must be a positive integer. |
| `pageSize` | integer | No | 100 | The number of records returned in each request. Must be between 1 and 100 (inclusive). |
| `sort[N][field]` | string | No | none | The name or ID of the field to sort by. N is a zero-based index (0, 1, 2...) for multi-field sorting. |
| `sort[N][direction]` | string | No | `asc` | Sort direction: `asc` (ascending) or `desc` (descending). |
| `view` | string | No | none | The name or ID of a view in the table. When specified, only records visible in that view are returned, using the view's filters, sort, and field visibility settings. |
| `cellFormat` | string | No | `json` | The format for cell values. `json` returns typed JSON values. `string` returns all values as human-readable strings. When `string` is used, `timeZone` and `userLocale` should also be specified. |
| `timeZone` | string | No | `UTC` | The timezone to use for date formatting when `cellFormat` is `string`. Uses IANA timezone identifiers (e.g., `America/New_York`, `Europe/London`, `Asia/Tokyo`). |
| `userLocale` | string | No | `en-us` | The locale to use for formatting numbers and dates when `cellFormat` is `string`. Examples: `en-us`, `fr-fr`, `de-de`, `ja-jp`, `zh-cn`. |
| `returnFieldsByFieldId` | boolean | No | `false` | When `true`, the `fields` object in each record uses field IDs (e.g., `fldXXXXXX`) as keys instead of field names. Useful for resilience against field renames. |
| `recordMetadata[]` | array of strings | No | none | Additional metadata to include. Currently only supports `commentCount`. Usage: `recordMetadata[]=commentCount`. |
| `offset` | string | No | none | A pagination cursor returned by a previous List Records response. Pass this to retrieve the next page of results. |

### Response Schema

```json
{
  "records": [
    {
      "id": "recXXXXXXXXXXXXXX",
      "createdTime": "2024-01-15T10:30:00.000Z",
      "fields": {
        "FieldName": "value",
        "AnotherField": 42
      }
    }
  ],
  "offset": "itrXXXXXX/recXXXXXX"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `records` | array | Array of record objects. |
| `records[].id` | string | The unique record ID (starts with `rec`). |
| `records[].createdTime` | string | ISO 8601 timestamp of when the record was created. |
| `records[].fields` | object | Key-value map of field name (or field ID) to cell value. Empty/null fields are omitted entirely. |
| `records[].commentCount` | integer | Number of comments on the record. Only present when `recordMetadata[]=commentCount` is specified. |
| `offset` | string | Pagination cursor. Present only when more records are available. Absent on the last page. |

### POST Alternative for List Records

**`POST /v0/{baseId}/{tableIdOrName}/listRecords`**

Use when the GET URL would exceed 16,000 characters (common with complex `filterByFormula` values).

**Request Body:**

```json
{
  "fields": ["Name", "Status", "Email"],
  "filterByFormula": "{Status}='Active'",
  "maxRecords": 50,
  "pageSize": 10,
  "sort": [
    {"field": "Name", "direction": "asc"},
    {"field": "CreatedDate", "direction": "desc"}
  ],
  "view": "Grid view",
  "cellFormat": "json",
  "returnFieldsByFieldId": false,
  "recordMetadata": ["commentCount"],
  "offset": "itrXXXXXX/recXXXXXX"
}
```

| Body Parameter | Type | Description |
|----------------|------|-------------|
| `fields` | array of strings | Field names or IDs to return. |
| `filterByFormula` | string | Formula filter. |
| `maxRecords` | integer | Maximum total records. |
| `pageSize` | integer | Records per page (1-100). |
| `sort` | array of objects | Each object has `field` (string) and `direction` (`asc` or `desc`). |
| `view` | string | View name or ID. |
| `cellFormat` | string | `json` or `string`. |
| `returnFieldsByFieldId` | boolean | Use field IDs as keys. |
| `recordMetadata` | array of strings | Metadata to include (e.g., `["commentCount"]`). |
| `offset` | string | Pagination cursor. |

**Important:** `timeZone` and `userLocale` must still be passed as query parameters, not in the request body, even when using the POST method.

The response schema is identical to the GET method.

---

## 2. Get Record

**`GET /v0/{baseId}/{tableIdOrName}/{recordId}`**

Retrieve a single record by its record ID.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (starts with `app`). |
| `tableIdOrName` | string | Yes | The table ID (starts with `tbl`) or URL-encoded table name. |
| `recordId` | string | Yes | The record ID (starts with `rec`). |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cellFormat` | string | No | `json` | `json` or `string`. |
| `returnFieldsByFieldId` | boolean | No | `false` | Use field IDs as keys instead of names. |
| `timeZone` | string | No | `UTC` | Timezone for date formatting (when `cellFormat=string`). |
| `userLocale` | string | No | `en-us` | Locale for number/date formatting (when `cellFormat=string`). |

### Response Schema

```json
{
  "id": "recXXXXXXXXXXXXXX",
  "createdTime": "2024-01-15T10:30:00.000Z",
  "fields": {
    "Name": "Example Record",
    "Status": "Active",
    "Count": 42,
    "Tags": ["urgent", "review"]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The unique record ID. |
| `createdTime` | string | ISO 8601 creation timestamp. |
| `fields` | object | Key-value map of field name/ID to cell value. Empty fields are omitted. |

---

## 3. Create Records

**`POST /v0/{baseId}/{tableIdOrName}`**

Create one or more records. Maximum 10 records per request.

### Request Body Schema

```json
{
  "records": [
    {
      "fields": {
        "Name": "New Record",
        "Status": "Active",
        "Count": 1,
        "Attachments": [
          {
            "url": "https://example.com/image.jpg",
            "filename": "image.jpg"
          }
        ]
      }
    }
  ],
  "returnFieldsByFieldId": false,
  "typecast": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `records` | array | Yes | — | Array of record objects. Minimum 1, maximum 10. |
| `records[].fields` | object | Yes | — | Map of field name (or field ID) to the value to set. |
| `returnFieldsByFieldId` | boolean | No | `false` | When `true`, response uses field IDs as keys. |
| `typecast` | boolean | No | `false` | When `true`, the API will attempt to convert string values to the appropriate cell value type. For example, a string `"42"` would be converted to the integer `42` for a number field. For single/multiple select fields, new options will be created automatically if they don't already exist. Without `typecast`, providing an unknown select option returns a 422 error. |

### Attachment Upload Format

When creating or updating attachment fields, each attachment object supports the following properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `url` | string | Yes | The URL of the file to attach. Airtable will download and host the file. The URL must be publicly accessible. |
| `filename` | string | No | Override the filename. If not provided, the filename is inferred from the URL. |

Example:

```json
{
  "fields": {
    "Photos": [
      {
        "url": "https://example.com/photo1.jpg",
        "filename": "my-photo.jpg"
      },
      {
        "url": "https://example.com/photo2.png"
      }
    ]
  }
}
```

**Important:** When updating an attachment field, you must include all existing attachments plus any new ones. Providing only new attachments will replace (remove) the existing ones. To add to existing attachments, first GET the record, then include the existing attachment objects (with their `id`) alongside the new ones.

### Response Schema

```json
{
  "records": [
    {
      "id": "recXXXXXXXXXXXXXX",
      "createdTime": "2024-01-15T10:30:00.000Z",
      "fields": {
        "Name": "New Record",
        "Status": "Active",
        "Count": 1
      }
    }
  ]
}
```

The response mirrors the created records with `id` and `createdTime` added.

---

## 4. Update Record (Single)

### PATCH — Partial Update

**`PATCH /v0/{baseId}/{tableIdOrName}/{recordId}`**

Updates only the specified fields. All other fields remain unchanged.

### PUT — Full Replacement

**`PUT /v0/{baseId}/{tableIdOrName}/{recordId}`**

Replaces all writable fields. Any field not included in the request body is cleared (set to empty/null).

### Request Body Schema

```json
{
  "fields": {
    "Status": "Completed",
    "Count": 99
  },
  "returnFieldsByFieldId": false,
  "typecast": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `fields` | object | Yes | — | Map of field name/ID to new value. |
| `returnFieldsByFieldId` | boolean | No | `false` | Use field IDs in response. |
| `typecast` | boolean | No | `false` | Auto-convert string values and create select options. |

### PATCH vs PUT Behavior

| Behavior | PATCH | PUT |
|----------|-------|-----|
| Specified fields | Updated to new values | Updated to new values |
| Omitted fields | Left unchanged | Cleared (set to null/empty) |
| Computed fields (formula, rollup, etc.) | Ignored if included | Ignored if included |
| Read-only fields (createdTime, autoNumber) | Cannot be set | Cannot be set |

### Response Schema

```json
{
  "id": "recXXXXXXXXXXXXXX",
  "createdTime": "2024-01-15T10:30:00.000Z",
  "fields": {
    "Name": "Example Record",
    "Status": "Completed",
    "Count": 99
  }
}
```

---

## 5. Update Multiple Records

### PATCH — Partial Update (Multiple)

**`PATCH /v0/{baseId}/{tableIdOrName}`**

Update up to 10 records in one request. Only specified fields are changed.

### PUT — Full Replacement (Multiple)

**`PUT /v0/{baseId}/{tableIdOrName}`**

Replace all writable fields for up to 10 records. Omitted fields are cleared.

### Request Body Schema

```json
{
  "records": [
    {
      "id": "recABC123",
      "fields": {
        "Status": "Completed"
      }
    },
    {
      "id": "recDEF456",
      "fields": {
        "Status": "Archived",
        "Count": 0
      }
    }
  ],
  "returnFieldsByFieldId": false,
  "typecast": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `records` | array | Yes | — | Array of record update objects (max 10). |
| `records[].id` | string | Yes (unless upsert) | — | The record ID to update. |
| `records[].fields` | object | Yes | — | Map of field name/ID to new value. |
| `returnFieldsByFieldId` | boolean | No | `false` | Use field IDs in response. |
| `typecast` | boolean | No | `false` | Auto-convert and create select options. |

### Upsert Mode (performUpsert)

Add the `performUpsert` property to enable upsert behavior. When enabled, records are matched by the specified fields rather than by record ID.

```json
{
  "performUpsert": {
    "fieldsToMergeOn": ["Email"]
  },
  "records": [
    {
      "fields": {
        "Email": "alice@example.com",
        "Name": "Alice Updated",
        "Status": "Active"
      }
    },
    {
      "fields": {
        "Email": "bob@example.com",
        "Name": "Bob New",
        "Status": "Pending"
      }
    }
  ],
  "typecast": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `performUpsert` | object | No | Enables upsert mode. |
| `performUpsert.fieldsToMergeOn` | array of strings | Yes (if upsert) | One or more field names or IDs to match on. These fields must have unique values or be the primary field. At least one field is required. You can specify up to 3 fields. |

**Upsert behavior:**

- If a record with matching values exists in the specified fields, the existing record is updated.
- If no matching record exists, a new record is created.
- If multiple records match, the first match is updated (others are ignored).
- The `records[].id` field is not required and is ignored when `performUpsert` is present.

**Upsert response:**

```json
{
  "records": [
    {
      "id": "recABC123",
      "createdTime": "2024-01-15T10:30:00.000Z",
      "fields": { ... }
    }
  ],
  "createdRecords": ["recDEF456"],
  "updatedRecords": ["recABC123"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `records` | array | All records that were created or updated. |
| `createdRecords` | array of strings | Record IDs of newly created records. |
| `updatedRecords` | array of strings | Record IDs of updated (existing) records. |

---

## 6. Delete Record (Single)

**`DELETE /v0/{baseId}/{tableIdOrName}/{recordId}`**

Permanently delete a single record. This action cannot be undone via the API.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | Base ID (starts with `app`). |
| `tableIdOrName` | string | Yes | Table ID (starts with `tbl`) or URL-encoded table name. |
| `recordId` | string | Yes | Record ID (starts with `rec`). |

### Response Schema

```json
{
  "id": "recXXXXXXXXXXXXXX",
  "deleted": true
}
```

---

## 7. Delete Multiple Records

**`DELETE /v0/{baseId}/{tableIdOrName}?records[]={id1}&records[]={id2}`**

Delete up to 10 records in a single request. Record IDs are passed as repeated query parameters.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `records[]` | array of strings | Yes | Record IDs to delete. Specify multiple by repeating: `records[]=recABC&records[]=recDEF`. Maximum 10. |

### URL Format Examples

Delete 1 record:
```
DELETE /v0/{baseId}/{tableIdOrName}?records[]=recABC123
```

Delete 3 records:
```
DELETE /v0/{baseId}/{tableIdOrName}?records[]=recABC123&records[]=recDEF456&records[]=recGHI789
```

### Response Schema

```json
{
  "records": [
    {
      "id": "recABC123",
      "deleted": true
    },
    {
      "id": "recDEF456",
      "deleted": true
    }
  ]
}
```

Each entry in the `records` array contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The deleted record's ID. |
| `deleted` | boolean | Always `true` on success. |

---

## 8. filterByFormula Reference

The `filterByFormula` parameter accepts an Airtable formula expression. The formula is evaluated for each record. Records where the formula returns a truthy value (non-zero number, non-empty string, `true`) are included in the results.

### Field References

- Reference fields by wrapping the field name in curly braces: `{Field Name}`
- Field names are case-sensitive.
- For field names with special characters, use the exact name: `{Field With Spaces}`
- You can also use field IDs: `{fldXXXXXXXXXXXXXX}`

### String Literals

- Use single quotes for strings: `'Active'`
- Escape single quotes within strings by doubling them: `'it''s'`
- Use double quotes as an alternative: `"Active"`

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal | `{Status}='Active'` |
| `!=` | Not equal | `{Status}!='Archived'` |
| `<` | Less than | `{Count}<10` |
| `>` | Greater than | `{Count}>10` |
| `<=` | Less than or equal | `{Count}<=10` |
| `>=` | Greater than or equal | `{Count}>=10` |
| `&` | String concatenation | `{First}&' '&{Last}` |
| `+` | Addition | `{A}+{B}` |
| `-` | Subtraction | `{A}-{B}` |
| `*` | Multiplication | `{A}*{B}` |
| `/` | Division | `{A}/{B}` |

### Logical Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `AND` | `AND(expr1, expr2, ...)` | Returns `true` if all arguments are truthy. |
| `OR` | `OR(expr1, expr2, ...)` | Returns `true` if any argument is truthy. |
| `NOT` | `NOT(expr)` | Returns `true` if the argument is falsy. |
| `IF` | `IF(expr, value1, value2)` | Returns `value1` if `expr` is truthy, otherwise `value2`. |
| `SWITCH` | `SWITCH(expr, pattern1, value1, [pattern2, value2, ...], [default])` | Evaluates `expr` and returns the value corresponding to the first matching pattern. Returns `default` if no match. |
| `XOR` | `XOR(expr1, expr2, ...)` | Returns `true` if an odd number of arguments are truthy. |
| `TRUE` | `TRUE()` | Returns the boolean `true`. |
| `FALSE` | `FALSE()` | Returns the boolean `false`. |

### Text Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `SEARCH` | `SEARCH(query, text, [start])` | Returns the 0-based position of `query` in `text`. Returns blank if not found. Case-insensitive. `start` is an optional starting position. |
| `FIND` | `FIND(query, text, [start])` | Same as SEARCH but case-sensitive. |
| `LEN` | `LEN(text)` | Returns the number of characters in `text`. |
| `LEFT` | `LEFT(text, count)` | Returns the first `count` characters of `text`. |
| `RIGHT` | `RIGHT(text, count)` | Returns the last `count` characters of `text`. |
| `MID` | `MID(text, start, count)` | Returns `count` characters starting at position `start` (1-based). |
| `TRIM` | `TRIM(text)` | Removes leading and trailing whitespace from `text`. |
| `LOWER` | `LOWER(text)` | Converts `text` to lowercase. |
| `UPPER` | `UPPER(text)` | Converts `text` to uppercase. |
| `SUBSTITUTE` | `SUBSTITUTE(text, old, new, [index])` | Replaces occurrences of `old` with `new` in `text`. If `index` is specified, only replaces the Nth occurrence. |
| `CONCATENATE` | `CONCATENATE(str1, str2, ...)` | Joins multiple strings together. Equivalent to `str1 & str2 & ...`. |
| `REPT` | `REPT(text, count)` | Repeats `text` the specified number of times. |
| `REPLACE` | `REPLACE(text, start, count, replacement)` | Replaces `count` characters in `text` starting at `start` (1-based) with `replacement`. |
| `T` | `T(value)` | Returns `value` if it is text, otherwise returns an empty string. |
| `ENCODE_URL_COMPONENT` | `ENCODE_URL_COMPONENT(text)` | URL-encodes the given text. |

### Numeric Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `VALUE` | `VALUE(text)` | Converts a string to a number. |
| `INT` | `INT(number)` | Rounds a number down to the nearest integer. |
| `ROUND` | `ROUND(number, precision)` | Rounds a number to the specified number of decimal places. |
| `ROUNDUP` | `ROUNDUP(number, precision)` | Rounds a number up (away from zero). |
| `ROUNDDOWN` | `ROUNDDOWN(number, precision)` | Rounds a number down (toward zero). |
| `MOD` | `MOD(number, divisor)` | Returns the remainder after dividing `number` by `divisor`. |
| `ABS` | `ABS(number)` | Returns the absolute value. |
| `MAX` | `MAX(num1, num2, ...)` | Returns the largest value. |
| `MIN` | `MIN(num1, num2, ...)` | Returns the smallest value. |
| `SUM` | `SUM(num1, num2, ...)` | Returns the sum of all arguments. |
| `AVERAGE` | `AVERAGE(num1, num2, ...)` | Returns the arithmetic mean. |
| `COUNT` | `COUNT(val1, val2, ...)` | Counts the number of numeric values (ignores non-numeric). |
| `COUNTA` | `COUNTA(val1, val2, ...)` | Counts the number of non-empty values. |
| `COUNTALL` | `COUNTALL(val1, val2, ...)` | Counts all values, including empty ones. |
| `CEILING` | `CEILING(number, [significance])` | Rounds up to the nearest multiple of `significance`. |
| `FLOOR` | `FLOOR(number, [significance])` | Rounds down to the nearest multiple of `significance`. |
| `EVEN` | `EVEN(number)` | Rounds up to the nearest even integer. |
| `ODD` | `ODD(number)` | Rounds up to the nearest odd integer. |
| `SQRT` | `SQRT(number)` | Returns the square root. |
| `POWER` | `POWER(base, exponent)` | Returns `base` raised to `exponent`. |
| `EXP` | `EXP(number)` | Returns `e` raised to the given power. |
| `LOG` | `LOG(number, [base])` | Returns the logarithm. Default base is 10. |
| `BLANK` | `BLANK()` | Returns a blank value (empty/null). |
| `ERROR` | `ERROR(message)` | Returns an error value with the given message. |

### Date and Time Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `DATETIME_FORMAT` | `DATETIME_FORMAT(date, format)` | Formats a date/datetime value. Uses Moment.js format tokens (e.g., `'YYYY-MM-DD'`, `'M/D/YYYY h:mm A'`). |
| `DATETIME_PARSE` | `DATETIME_PARSE(text, [format], [locale])` | Parses a text string into a date. If `format` is omitted, tries ISO 8601. |
| `IS_BEFORE` | `IS_BEFORE(date1, date2)` | Returns `true` if `date1` is before `date2`. |
| `IS_AFTER` | `IS_AFTER(date1, date2)` | Returns `true` if `date1` is after `date2`. |
| `IS_SAME` | `IS_SAME(date1, date2, [unit])` | Returns `true` if `date1` and `date2` are the same. Optional `unit`: `'year'`, `'month'`, `'day'`, `'hour'`, `'minute'`, `'second'`. |
| `DATEADD` | `DATEADD(date, count, unit)` | Adds `count` units to a date. Units: `'years'`, `'months'`, `'weeks'`, `'days'`, `'hours'`, `'minutes'`, `'seconds'`. |
| `DATESTR` | `DATESTR(date)` | Formats a date as `YYYY-MM-DD` string. |
| `TIMESTR` | `TIMESTR(datetime)` | Formats a datetime as `HH:mm:ss.SSS` string. |
| `NOW` | `NOW()` | Returns the current date and time. |
| `TODAY` | `TODAY()` | Returns the current date (without time). |
| `TONOW` | `TONOW(date)` | Returns the number of days between `date` and now. |
| `FROMNOW` | `FROMNOW(date)` | Returns the number of days from now to `date`. |
| `YEAR` | `YEAR(date)` | Returns the 4-digit year of the date. |
| `MONTH` | `MONTH(date)` | Returns the month (1-12). |
| `DAY` | `DAY(date)` | Returns the day of the month (1-31). |
| `HOUR` | `HOUR(datetime)` | Returns the hour (0-23). |
| `MINUTE` | `MINUTE(datetime)` | Returns the minute (0-59). |
| `SECOND` | `SECOND(datetime)` | Returns the second (0-59). |
| `WEEKDAY` | `WEEKDAY(date, [startDayOfWeek])` | Returns the day of the week as a number. `startDayOfWeek`: `'Sunday'` (default) or `'Monday'`. |
| `WEEKNUM` | `WEEKNUM(date, [startDayOfWeek])` | Returns the week number of the year. |
| `SET_LOCALE` | `SET_LOCALE(date, locale)` | Sets the locale for date formatting. |
| `SET_TIMEZONE` | `SET_TIMEZONE(date, timezone)` | Converts a date to the specified timezone. |
| `WORKDAY` | `WORKDAY(date, numDays, [holidays])` | Returns a date that is `numDays` working days after `date`, optionally excluding holidays. |
| `WORKDAY_DIFF` | `WORKDAY_DIFF(date1, date2, [holidays])` | Returns the number of working days between two dates. |

### Record Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `RECORD_ID` | `RECORD_ID()` | Returns the ID of the current record (`recXXXXXX`). |
| `CREATED_TIME` | `CREATED_TIME()` | Returns the creation timestamp of the current record. |
| `LAST_MODIFIED_TIME` | `LAST_MODIFIED_TIME()` | Returns the last modified timestamp of the current record. Can optionally specify fields: `LAST_MODIFIED_TIME({Field1}, {Field2})`. |

### Array Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `ARRAYJOIN` | `ARRAYJOIN(array, separator)` | Joins array elements with the separator. |
| `ARRAYCOMPACT` | `ARRAYCOMPACT(array)` | Removes empty items from an array. |
| `ARRAYUNIQUE` | `ARRAYUNIQUE(array)` | Returns unique items from an array. |
| `ARRAYFLATTEN` | `ARRAYFLATTEN(array)` | Flattens nested arrays into a single flat array. |
| `ARRAYSLICE` | `ARRAYSLICE(array, start, [end])` | Returns a subset of the array from `start` to `end`. |

### Regex Functions

| Function | Syntax | Description |
|----------|--------|-------------|
| `REGEX_MATCH` | `REGEX_MATCH(text, regex)` | Returns the first match of the regex in text. |
| `REGEX_EXTRACT` | `REGEX_EXTRACT(text, regex)` | Returns the first match of the regex. |
| `REGEX_REPLACE` | `REGEX_REPLACE(text, regex, replacement)` | Replaces regex matches with the replacement. |

### Common Formula Examples

```
# Exact match
{Status}='Active'

# Multiple conditions (AND)
AND({Status}='Active', {Priority}='High')

# Multiple conditions (OR)
OR({Status}='Active', {Status}='Pending')

# Contains text (case-insensitive)
SEARCH('test', {Name})

# Does NOT contain text
NOT(SEARCH('test', {Name}))

# Field is not empty
NOT({Email} = '')
{Email} != ''
LEN({Email}) > 0

# Field is empty
{Email} = ''
{Email} = BLANK()

# Date comparisons
IS_AFTER({Due Date}, '2024-01-01')
IS_BEFORE({Due Date}, NOW())
IS_SAME({Created}, TODAY(), 'day')

# Numeric comparisons
{Count} > 10
AND({Count} >= 5, {Count} <= 20)

# Specific record by ID
RECORD_ID() = 'recABC123'

# Multiple record IDs
OR(RECORD_ID()='recABC', RECORD_ID()='recDEF', RECORD_ID()='recGHI')

# Linked records contain a value
FIND('Alice', ARRAYJOIN({Assignees}, ','))

# Date within last 7 days
IS_AFTER({Created}, DATEADD(NOW(), -7, 'days'))

# Checkbox is checked
{Completed} = TRUE()
{Completed} = 1

# Checkbox is not checked
{Completed} = FALSE()
{Completed} = 0
NOT({Completed})
```

---

## 9. Cell Value Formats

Each Airtable field type returns and accepts values in a specific JSON format. When `cellFormat` is `json` (default), the following formats apply.

### singleLineText

- **Read:** `string`
- **Write:** `string`
- **Example:** `"Hello World"`

### multilineText

- **Read:** `string` (with `\n` for newlines)
- **Write:** `string`
- **Example:** `"Line 1\nLine 2\nLine 3"`

### richText

- **Read:** `string` (Markdown-formatted)
- **Write:** `string` (Markdown-formatted)
- **Example:** `"**Bold** and *italic* text\n- Bullet 1\n- Bullet 2"`
- **Supported Markdown:** bold (`**text**`), italic (`*text*`), strikethrough (`~~text~~`), inline code, links, headings, bulleted lists, numbered lists, blockquotes.

### number

- **Read:** `number`
- **Write:** `number`
- **Example:** `42`, `3.14`, `-10`
- **Note:** Integers and floating point are both valid.

### currency

- **Read:** `number`
- **Write:** `number`
- **Example:** `19.99`, `1000`
- **Note:** Stored as a plain number. Currency symbol and formatting are applied by the field configuration.

### percent

- **Read:** `number` (where 1 = 100%)
- **Write:** `number`
- **Example:** `0.5` for 50%, `1.0` for 100%, `0.01` for 1%

### checkbox

- **Read:** `boolean` or absent
- **Write:** `boolean`
- **Example:** `true` (checked) or field is omitted (unchecked)
- **Note:** Unchecked checkboxes are omitted from the response (the field key is absent). To uncheck, set to `false` or `null`.

### date

- **Read:** `string` (ISO 8601 date)
- **Write:** `string` (ISO 8601)
- **Example:** `"2024-01-15"`
- **Format:** `YYYY-MM-DD`

### dateTime

- **Read:** `string` (ISO 8601 datetime with timezone)
- **Write:** `string` (ISO 8601)
- **Example:** `"2024-01-15T10:30:00.000Z"`
- **Note:** Always returned in UTC. When writing, you can include a timezone offset: `"2024-01-15T10:30:00-05:00"`.

### duration

- **Read:** `number` (seconds)
- **Write:** `number` (seconds)
- **Example:** `3661` for 1 hour, 1 minute, 1 second
- **Note:** Stored as total seconds. The display format (h:mm, h:mm:ss, etc.) is controlled by the field configuration.

### singleSelect

- **Read:** `string`
- **Write:** `string`
- **Example:** `"Option A"`
- **Note:** The value must exactly match an existing option name unless `typecast: true` is used, in which case new options are created automatically.

### multipleSelects

- **Read:** `array of strings`
- **Write:** `array of strings`
- **Example:** `["Option A", "Option B"]`
- **Note:** Same `typecast` behavior as singleSelect.

### multipleRecordLinks

- **Read:** `array of strings` (record IDs)
- **Write:** `array of strings` (record IDs)
- **Example:** `["recABC123", "recDEF456"]`
- **Note:** When updating, provide the complete list of linked record IDs. To add a link, include all existing IDs plus the new one. To remove a link, omit its ID.

### collaborator

- **Read:** `object`
- **Write:** `object`
- **Read Example:**
  ```json
  {
    "id": "usrXXXXXXXXXXXXXX",
    "email": "alice@example.com",
    "name": "Alice Smith"
  }
  ```
- **Write:** `{"id": "usrXXXXXX"}` or `{"email": "alice@example.com"}`

### attachments

- **Read:** `array of objects`
- **Write:** `array of objects`
- **Read Example:**
  ```json
  [
    {
      "id": "attXXXXXXXXXXXXXX",
      "url": "https://dl.airtable.com/.attachments/...",
      "filename": "image.jpg",
      "size": 12345,
      "type": "image/jpeg",
      "width": 800,
      "height": 600,
      "thumbnails": {
        "small": {
          "url": "https://dl.airtable.com/.attachmentThumbnails/...",
          "width": 36,
          "height": 36
        },
        "large": {
          "url": "https://dl.airtable.com/.attachmentThumbnails/...",
          "width": 256,
          "height": 256
        },
        "full": {
          "url": "https://dl.airtable.com/.attachmentThumbnails/...",
          "width": 800,
          "height": 600
        }
      }
    }
  ]
  ```
- **Write Example:**
  ```json
  [
    {
      "url": "https://example.com/file.pdf",
      "filename": "document.pdf"
    }
  ]
  ```
- **Write properties:** `url` (required), `filename` (optional).
- **Note:** Attachment URLs returned by the API expire after a few hours. Do not cache them for long-term use. To add attachments to a record that already has them, include the existing attachment objects (with their `id`) alongside new ones.

### barcode

- **Read:** `object`
- **Write:** `object`
- **Example:**
  ```json
  {
    "text": "1234567890",
    "type": "upce"
  }
  ```
- **Properties:** `text` (string, the barcode value) and optionally `type` (string, the barcode symbology).

### button

- **Read:** `object`
- **Write:** Not writable (read-only).
- **Example:**
  ```json
  {
    "label": "Open URL",
    "url": "https://example.com"
  }
  ```

### formula

- **Read:** Varies (depends on the formula result type: string, number, boolean, array, date, etc.)
- **Write:** Not writable (computed field).
- **Note:** The JSON type depends on what the formula returns. A formula that returns text yields a string, one that returns a number yields a number, etc. Formulas that return arrays (e.g., ARRAYJOIN of a lookup) return arrays.

### lookup

- **Read:** `array` (of the looked-up field's values)
- **Write:** Not writable (computed field).
- **Example:** `["Value1", "Value2"]` or `[42, 85]`
- **Note:** Always returns an array, even for single values. The element type matches the looked-up field type.

### rollup

- **Read:** Varies (depends on the rollup aggregation function)
- **Write:** Not writable (computed field).
- **Example:** `42` (for SUM), `"text1, text2"` (for ARRAYJOIN)
- **Note:** The result type depends on the aggregation function used.

### count

- **Read:** `integer`
- **Write:** Not writable (computed field).
- **Example:** `5`
- **Note:** Returns the count of linked records.

### autoNumber

- **Read:** `integer`
- **Write:** Not writable (auto-generated).
- **Example:** `1`, `2`, `42`

### rating

- **Read:** `integer`
- **Write:** `integer`
- **Example:** `3` (for 3 out of 5 stars, or whatever max is configured)
- **Note:** Value ranges from 1 to the configured maximum (default 5). An unrated field is omitted from the response.

### url

- **Read:** `string`
- **Write:** `string`
- **Example:** `"https://example.com"`

### email

- **Read:** `string`
- **Write:** `string`
- **Example:** `"alice@example.com"`

### phone

- **Read:** `string`
- **Write:** `string`
- **Example:** `"+1-555-123-4567"`

### createdTime

- **Read:** `string` (ISO 8601 datetime)
- **Write:** Not writable (auto-generated).
- **Example:** `"2024-01-15T10:30:00.000Z"`

### lastModifiedTime

- **Read:** `string` (ISO 8601 datetime)
- **Write:** Not writable (auto-generated).
- **Example:** `"2024-06-20T14:22:33.000Z"`

### createdBy / lastModifiedBy

- **Read:** `object`
- **Write:** Not writable (auto-generated).
- **Example:**
  ```json
  {
    "id": "usrXXXXXXXXXXXXXX",
    "email": "alice@example.com",
    "name": "Alice Smith"
  }
  ```

### externalSyncSource

- **Read:** `string`
- **Write:** Not writable (auto-generated by sync).
- **Note:** The value depends on the external sync configuration.

### aiText

- **Read:** `object`
- **Write:** Not writable (auto-generated by AI).
- **Example:**
  ```json
  {
    "state": "generated",
    "value": "AI-generated summary text here.",
    "isStale": false,
    "errorType": null
  }
  ```

### cellFormat=string

When `cellFormat=string` is used, all values are returned as human-readable strings regardless of their actual type:

| Field Type | String Format Example |
|------------|----------------------|
| number | `"42"`, `"3.14"` |
| currency | `"$19.99"` |
| percent | `"50%"` |
| checkbox | `"checked"` (omitted if unchecked) |
| date | `"1/15/2024"` (locale-dependent) |
| dateTime | `"1/15/2024 10:30am"` (locale/tz-dependent) |
| duration | `"1:01:01"` |
| singleSelect | `"Option A"` |
| multipleSelects | `"Option A, Option B"` |
| multipleRecordLinks | `"Record Name 1, Record Name 2"` |
| collaborator | `"Alice Smith"` |
| attachments | `"image.jpg, document.pdf"` |
| rating | `"3"` |

---

## 10. Pagination Details

### How Pagination Works

1. Make an initial request with optional `pageSize` (default 100, max 100).
2. If the response contains an `offset` field, more records exist.
3. Pass the `offset` value as a query parameter (or in POST body) in the next request.
4. Repeat until no `offset` is returned.

### Key Behaviors

| Behavior | Details |
|----------|---------|
| **Default page size** | 100 records |
| **Maximum page size** | 100 records |
| **Minimum page size** | 1 record |
| **Offset format** | Opaque string (e.g., `itrXXXXXX/recXXXXXX`). Do not parse or construct these values. |
| **Offset validity** | Each offset is tied to the specific query parameters used. Changing filters, sort, or view invalidates the offset. |
| **Offset expiration** | Offsets may expire after a period of inactivity. If expired, start pagination from the beginning. |
| **Consistency** | Pagination provides a snapshot-like view. Records created or deleted during pagination may or may not appear. |
| **maxRecords interaction** | `maxRecords` limits the total across all pages. If `maxRecords=25` and `pageSize=10`, you get 10 + 10 + 5 records. |
| **Empty results** | If no records match, the response contains an empty `records` array and no `offset`. |

### Pagination with Sorting

- Sorting is applied server-side before pagination. Each page contains the next sorted chunk.
- Multi-field sorting is supported: `sort[0][field]=Name&sort[0][direction]=asc&sort[1][field]=Date&sort[1][direction]=desc`

### Pagination with Views

- When a `view` is specified, only records visible in that view are returned. The view's sort order is used unless overridden by `sort` parameters.

### Pagination with POST listRecords

- Pass `offset` in the request body instead of as a query parameter.
- All other pagination behavior is identical.

### Rate Limiting During Pagination

- Each page request counts as one API call.
- Respect the 5 requests/second rate limit.
- For large tables, add a small delay (200ms) between page requests.

---

## 11. Error Codes

All errors return a JSON response body with the following structure:

```json
{
  "error": {
    "type": "ERROR_TYPE",
    "message": "Human-readable description of the error."
  }
}
```

### Complete Error Reference

| HTTP Status | Error Type | Description |
|-------------|-----------|-------------|
| 400 | `BAD_REQUEST` | The request body or parameters are malformed. Check JSON syntax, required fields, and parameter types. |
| 401 | `AUTHENTICATION_REQUIRED` | No Authorization header provided, or the header format is incorrect. Must be `Bearer {token}`. |
| 401 | `INVALID_ACCESS_TOKEN` | The provided access token is invalid, expired, or revoked. |
| 403 | `NOT_AUTHORIZED` | The token is valid but does not have the required scopes or permissions for the requested resource. Check that the token has `data.records:read` and/or `data.records:write` scopes. |
| 404 | `NOT_FOUND` | The specified base, table, view, or record was not found. Verify the IDs are correct and that the resource exists. |
| 404 | `TABLE_NOT_FOUND` | The specified table does not exist in the base. |
| 404 | `VIEW_NOT_FOUND` | The specified view does not exist in the table. |
| 404 | `RECORD_NOT_FOUND` | The specified record ID does not exist in the table. |
| 413 | `REQUEST_TOO_LARGE` | The request body exceeds the maximum allowed size. This can happen with large attachment URLs or many records. |
| 422 | `INVALID_REQUEST` | The request is well-formed but contains invalid data. Common causes: invalid field names, wrong value types, invalid formula syntax. The error message provides specific details. |
| 422 | `CANNOT_UPDATE_COMPUTED_FIELD` | Attempted to write to a computed field (formula, rollup, lookup, count, autoNumber, createdTime, lastModifiedTime, createdBy, lastModifiedBy). These fields are read-only. |
| 422 | `INVALID_MULTIPLE_CHOICE_OPTIONS` | A single select or multiple select value was provided that doesn't match any existing option. Either use an existing option name or set `typecast: true` to create new options automatically. |
| 422 | `INVALID_FILTER_BY_FORMULA` | The `filterByFormula` value contains a syntax error or references a non-existent field. |
| 422 | `INVALID_SORT` | The `sort` parameter references a field that does not exist or has an invalid direction value. |
| 422 | `FIELD_NOT_FOUND` | A field name or ID in the request does not match any field in the table. |
| 422 | `INVALID_FIELD_VALUE` | A cell value does not match the expected type for the field (e.g., string provided for a number field without `typecast`). |
| 422 | `DUPLICATE_RECORD_ID` | The same record ID appears more than once in a batch update request. |
| 422 | `INVALID_RECORD_ID` | A record ID has an invalid format (must start with `rec` and be 17 characters). |
| 422 | `TOO_MANY_RECORDS` | More than 10 records were provided in a single create, update, or delete request. |
| 422 | `INVALID_CELL_FORMAT` | The `cellFormat` parameter has an invalid value. Must be `json` or `string`. |
| 422 | `INVALID_TYPECAST` | The `typecast` parameter could not convert the provided value to the expected type. |
| 422 | `INVALID_ATTACHMENT_OBJECT` | An attachment object is missing the required `url` property or has an invalid format. |
| 429 | `TOO_MANY_REQUESTS` | Rate limit exceeded. The API allows 5 requests per second per base. Retry after 30 seconds. The response may include a `Retry-After` header. |
| 500 | `SERVER_ERROR` | An unexpected error occurred on Airtable's servers. Retry the request after a brief delay. |
| 502 | `BAD_GATEWAY` | A temporary connectivity issue. Retry the request after a brief delay. |
| 503 | `SERVICE_UNAVAILABLE` | The Airtable service is temporarily unavailable (e.g., during maintenance). Retry after a delay. |

### Error Handling Best Practices

1. **Always check the HTTP status code** before parsing the response body.
2. **Handle 429 gracefully** by implementing exponential backoff or waiting at least 30 seconds before retrying.
3. **Log the full error response** including `error.type` and `error.message` for debugging.
4. **Validate before sending** to avoid 422 errors:
   - Ensure field names match exactly (case-sensitive).
   - Ensure cell values match the expected type.
   - Ensure batch sizes do not exceed 10 records.
5. **Retry on 5xx errors** with exponential backoff (e.g., 1s, 2s, 4s, 8s).

### Required Token Scopes for Records Operations

| Operation | Required Scope |
|-----------|---------------|
| List records | `data.records:read` |
| Get record | `data.records:read` |
| Create records | `data.records:write` |
| Update records | `data.records:write` |
| Delete records | `data.records:write` |
| With comment count | `data.records:read` + `data.recordComments:read` |

---

## Appendix: URL Encoding for Query Parameters

When using query parameters in GET requests, special characters must be URL-encoded:

| Character | Encoded | Context |
|-----------|---------|---------|
| `{` | `%7B` | Field references in formulas |
| `}` | `%7D` | Field references in formulas |
| `=` | `%3D` | Equality in formulas |
| `'` | `%27` | String literals in formulas |
| ` ` (space) | `%20` or `+` | Any parameter value |
| `[` | `%5B` | Array parameter syntax |
| `]` | `%5D` | Array parameter syntax |
| `&` | `%26` | String concatenation in formulas (not parameter separator) |
| `+` | `%2B` | Addition in formulas |

Example: `filterByFormula={Status}='Active'` becomes:
```
filterByFormula=%7BStatus%7D%3D'Active'
```

Full URL:
```
https://api.airtable.com/v0/{baseId}/{tableIdOrName}?filterByFormula=%7BStatus%7D%3D%27Active%27
```
