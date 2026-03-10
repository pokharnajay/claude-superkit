---
name: airtable-records
description: List, get, create, update, and delete records in Airtable tables. Use when user wants to read data from Airtable, add new records, modify existing records, or remove records. Triggers on "airtable record", "list records", "create record", "update record", "delete record", "airtable data", "query airtable".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Records API

Perform CRUD operations on records in Airtable tables. All endpoints use the base URL `https://api.airtable.com/v0`.

> **Auth:** All requests require `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN` header.
> **Rate limit:** 5 requests/second per base.

## Quick Start

### cURL — List Records

```bash
curl "https://api.airtable.com/v0/{baseId}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — List Records

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/{base_id}/{table_id_or_name}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
records = response.json()
```

## Endpoints

### 1. List Records

**`GET /v0/{baseId}/{tableIdOrName}`**

Returns a paginated list of records in a table.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `fields[]` | array of strings | Only return specific fields (by name or ID) |
| `filterByFormula` | string | Airtable formula to filter records (e.g., `{Status}='Active'`) |
| `maxRecords` | integer | Maximum total records to return |
| `pageSize` | integer | Records per page (max 100, default 100) |
| `sort[0][field]` | string | Field name to sort by |
| `sort[0][direction]` | string | `asc` or `desc` |
| `view` | string | View name or ID to filter/sort by |
| `cellFormat` | string | `json` (default) or `string` |
| `timeZone` | string | Timezone for date formatting (e.g., `America/New_York`) |
| `userLocale` | string | Locale for formatting (e.g., `en-us`) |
| `returnFieldsByFieldId` | boolean | Use field IDs as keys instead of names |
| `recordMetadata[]` | string | Include `commentCount` to get comment counts |
| `offset` | string | Pagination cursor from previous response |

**Response:**

```json
{
  "records": [
    {
      "id": "recABC123",
      "createdTime": "2024-01-15T10:30:00.000Z",
      "fields": {
        "Name": "Example Record",
        "Status": "Active",
        "Count": 42
      }
    }
  ],
  "offset": "itrXXXXXX/recXXXXXX"
}
```

- If `offset` is present, more records exist. Pass it as a query param in the next request.
- Empty fields are omitted from the response.

**cURL with filtering and sorting:**

```bash
curl "https://api.airtable.com/v0/{baseId}/{tableIdOrName}?filterByFormula=%7BStatus%7D%3D'Active'&sort%5B0%5D%5Bfield%5D=Name&sort%5B0%5D%5Bdirection%5D=asc&pageSize=10" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python with filtering and sorting:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/{base_id}/{table_id_or_name}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    params={
        "filterByFormula": "{Status}='Active'",
        "sort[0][field]": "Name",
        "sort[0][direction]": "asc",
        "pageSize": 10,
    },
)
```

**Paginating through all records:**

```python
all_records = []
offset = None

while True:
    params = {"pageSize": 100}
    if offset:
        params["offset"] = offset

    response = requests.get(
        f"https://api.airtable.com/v0/{base_id}/{table_id_or_name}",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
        params=params,
    )
    data = response.json()
    all_records.extend(data["records"])

    offset = data.get("offset")
    if not offset:
        break
```

#### POST Alternative for List Records

When GET URL exceeds 16,000 characters (complex formulas), use POST instead:

**`POST /v0/{baseId}/{tableIdOrName}/listRecords`**

```bash
curl -X POST "https://api.airtable.com/v0/{baseId}/{tableIdOrName}/listRecords" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filterByFormula": "{Status}=\"Active\"",
    "sort": [{"field": "Name", "direction": "asc"}],
    "fields": ["Name", "Status"],
    "pageSize": 10
  }'
```

Note: `timeZone` and `userLocale` must remain as query parameters even with POST.

### 2. Get Record

**`GET /v0/{baseId}/{tableIdOrName}/{recordId}`**

Retrieve a single record by ID.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `cellFormat` | string | `json` (default) or `string` |
| `returnFieldsByFieldId` | boolean | Use field IDs as keys |
| `timeZone` | string | Timezone for date formatting |
| `userLocale` | string | Locale for formatting |

**cURL:**

```bash
curl "https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Response:**

```json
{
  "id": "recABC123",
  "createdTime": "2024-01-15T10:30:00.000Z",
  "fields": {
    "Name": "Example Record",
    "Status": "Active"
  }
}
```

### 3. Create Records

**`POST /v0/{baseId}/{tableIdOrName}`**

Create up to 10 records in a single request.

**Request Body:**

```json
{
  "records": [
    {
      "fields": {
        "Name": "New Record",
        "Status": "Active",
        "Count": 1
      }
    },
    {
      "fields": {
        "Name": "Another Record",
        "Status": "Pending"
      }
    }
  ],
  "returnFieldsByFieldId": false,
  "typecast": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `records` | array | Array of record objects (max 10) |
| `records[].fields` | object | Field name/ID → value mapping |
| `typecast` | boolean | If `true`, auto-convert string values to appropriate types and create new select options |
| `returnFieldsByFieldId` | boolean | Use field IDs in response |

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/{baseId}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"fields": {"Name": "New Record", "Status": "Active"}},
      {"fields": {"Name": "Another Record", "Status": "Pending"}}
    ]
  }'
```

**Python:**

```python
response = requests.post(
    f"https://api.airtable.com/v0/{base_id}/{table_id_or_name}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "records": [
            {"fields": {"Name": "New Record", "Status": "Active"}},
            {"fields": {"Name": "Another Record", "Status": "Pending"}},
        ]
    },
)
```

**Response:** Same as input but with `id` and `createdTime` added to each record.

### 4. Replace Record (PUT)

**`PUT /v0/{baseId}/{tableIdOrName}/{recordId}`**

Replace all fields of a record. Fields not included in the request body will be **cleared**.

**Request Body:**

```json
{
  "fields": {
    "Name": "Replaced Record",
    "Status": "Active"
  }
}
```

**cURL:**

```bash
curl -X PUT "https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Name": "Replaced Record", "Status": "Active"}}'
```

- `PUT` = full replacement (unspecified fields are **cleared to empty**)
- `PATCH` = partial update (unspecified fields are **left unchanged**)

### 4b. Replace Multiple Records (PUT)

**`PUT /v0/{baseId}/{tableIdOrName}`**

Replace up to 10 records in a single request. Supports upsert via `performUpsert`.

```json
{
  "records": [
    {
      "id": "recABC123",
      "fields": {"Name": "Full Replace", "Status": "Active"}
    }
  ]
}
```

### 5. Update Record

**`PATCH /v0/{baseId}/{tableIdOrName}/{recordId}`**

Update specific fields of a single record (partial update).

**Request Body:**

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

**cURL:**

```bash
curl -X PATCH "https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Status": "Completed"}}'
```

- `PATCH` = partial update (only specified fields change)
- `PUT` = full replacement (unspecified fields are cleared)

### 5. Update Multiple Records

**`PATCH /v0/{baseId}/{tableIdOrName}`**

Update up to 10 records in a single request.

**Request Body:**

```json
{
  "records": [
    {
      "id": "recABC123",
      "fields": {"Status": "Completed"}
    },
    {
      "id": "recDEF456",
      "fields": {"Status": "Archived"}
    }
  ],
  "returnFieldsByFieldId": false,
  "typecast": false
}
```

**Upsert mode** — match by fields instead of ID:

```json
{
  "performUpsert": {
    "fieldsToMergeOn": ["Email"]
  },
  "records": [
    {
      "fields": {
        "Email": "alice@example.com",
        "Name": "Alice Updated"
      }
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `performUpsert.fieldsToMergeOn` | array | Fields to match existing records on (must be unique or primary field) |

- If a matching record exists → updates it
- If no match → creates a new record
- Response includes `createdRecords` and `updatedRecords` arrays of IDs

**cURL (upsert):**

```bash
curl -X PATCH "https://api.airtable.com/v0/{baseId}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "performUpsert": {"fieldsToMergeOn": ["Email"]},
    "records": [
      {"fields": {"Email": "alice@example.com", "Name": "Alice Updated"}}
    ]
  }'
```

### 6. Delete Record

**`DELETE /v0/{baseId}/{tableIdOrName}/{recordId}`**

Delete a single record.

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Response:**

```json
{
  "id": "recABC123",
  "deleted": true
}
```

### 7. Delete Multiple Records

**`DELETE /v0/{baseId}/{tableIdOrName}?records[]={id1}&records[]={id2}`**

Delete up to 10 records in a single request.

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/{baseId}/{tableIdOrName}?records[]=recABC123&records[]=recDEF456" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.delete(
    f"https://api.airtable.com/v0/{base_id}/{table_id_or_name}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    params={"records[]": ["recABC123", "recDEF456"]},
)
```

**Response:**

```json
{
  "records": [
    {"id": "recABC123", "deleted": true},
    {"id": "recDEF456", "deleted": true}
  ]
}
```

## Common Patterns

### Batch operations for more than 10 records

```python
import time

def batch_create(base_id, table_name, records, token):
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    created = []
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        resp = requests.post(url, headers=headers, json={"records": batch})
        resp.raise_for_status()
        created.extend(resp.json()["records"])
        if i + 10 < len(records):
            time.sleep(0.2)  # respect rate limit
    return created
```

### filterByFormula examples

| Formula | Matches |
|---------|---------|
| `{Status}='Active'` | Status equals "Active" |
| `AND({Status}='Active', {Priority}='High')` | Both conditions |
| `OR({Status}='Active', {Status}='Pending')` | Either condition |
| `SEARCH('test', {Name})` | Name contains "test" |
| `IS_AFTER({Date}, '2024-01-01')` | Date after Jan 1, 2024 |
| `{Count} > 10` | Count greater than 10 |
| `NOT({Email} = '')` | Email is not empty |
| `RECORD_ID() = 'recABC123'` | Specific record |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks required scope |
| 404 | `NOT_FOUND` | Invalid base, table, or record ID |
| 422 | `INVALID_REQUEST` | Invalid field values or formula |
| 422 | `CANNOT_UPDATE_COMPUTED_FIELD` | Attempted to write to a computed field |
| 422 | `INVALID_MULTIPLE_CHOICE_OPTIONS` | Select option doesn't exist (use `typecast: true`) |
| 429 | `TOO_MANY_REQUESTS` | Rate limited, retry after 30s |

## References

For complete API parameter details, see [references/records-api.md](references/records-api.md).
