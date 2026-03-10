# Airtable Comments API Reference

Complete reference for all Airtable Comments API endpoints, request/response schemas, mention format, pagination, and author object details.

> **Base URL:** `https://api.airtable.com/v0`
> **Auth:** All requests require `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`

---

## Endpoints Overview

| Method | Endpoint | Description | Scope Required |
|--------|----------|-------------|----------------|
| GET | `/v0/{baseId}/{tableId}/{recordId}/comments` | List comments on a record | `data.records:read` |
| POST | `/v0/{baseId}/{tableId}/{recordId}/comments` | Create a comment on a record | `data.records:write` |
| PATCH | `/v0/{baseId}/{tableId}/{recordId}/comments/{commentId}` | Update a comment | `data.records:write` |
| DELETE | `/v0/{baseId}/{tableId}/{recordId}/comments/{commentId}` | Delete a comment | `data.records:write` |

---

## Common Path Parameters

All comment endpoints share these path parameters:

| Parameter | Type | Required | Format | Description |
|-----------|------|----------|--------|-------------|
| `baseId` | string | Yes | `appXXXXXXXXXXXXXX` | The ID of the Airtable base |
| `tableId` | string | Yes | `tblXXXXXXXXXXXXXX` or name | The ID or name of the table containing the record |
| `recordId` | string | Yes | `recXXXXXXXXXXXXXX` | The ID of the record to interact with |
| `commentId` | string | For PATCH/DELETE | `comXXXXXXXXXXXXXX` | The ID of the specific comment |

---

## Data Models

### Comment Object

The comment object is returned in list, create, and update responses.

```json
{
  "id": "comXXXXXXXXXXXXXX",
  "text": "string",
  "author": {
    "id": "usrXXXXXXXXXXXXXX",
    "email": "string",
    "name": "string"
  },
  "createdTime": "2024-06-15T14:30:00.000Z"
}
```

#### Comment Fields

| Field | Type | Always Present | Description |
|-------|------|----------------|-------------|
| `id` | string | Yes | Unique comment identifier (format: `comXXXXXXXXXXXXXX`) |
| `text` | string | Yes | The comment body text. May contain @mention references in the format `@[usrXXX]` |
| `author` | object | Yes | The user who created the comment (see Author Object below) |
| `createdTime` | string | Yes | ISO 8601 timestamp in UTC when the comment was created |

### Author Object

The author object identifies the Airtable user who wrote the comment.

```json
{
  "id": "usrXXXXXXXXXXXXXX",
  "email": "alice@example.com",
  "name": "Alice Johnson"
}
```

#### Author Fields

| Field | Type | Always Present | Description |
|-------|------|----------------|-------------|
| `id` | string | Yes | Unique user identifier (format: `usrXXXXXXXXXXXXXX`). This is the ID used in @mentions |
| `email` | string | Yes | The user's email address |
| `name` | string | Yes | The user's display name |

### Deleted Comment Object

Returned by the DELETE endpoint upon successful deletion.

```json
{
  "id": "comXXXXXXXXXXXXXX",
  "deleted": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The ID of the deleted comment |
| `deleted` | boolean | Always `true` when deletion succeeds |

---

## 1. List Comments

**`GET /v0/{baseId}/{tableId}/{recordId}/comments`**

Retrieves a paginated list of comments on a specific record. Comments are sorted by creation time in descending order (newest first).

### Query Parameters

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `offset` | string | — | No | Pagination cursor returned from a previous response. Pass this value to retrieve the next page of results |
| `pageSize` | integer | 10 | No | Number of comments to return per page. Minimum: 1 |

### Request

```bash
curl "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments?pageSize=10" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Response Schema

```json
{
  "comments": [
    {
      "id": "comXXXXXXXXXXXXXX",
      "text": "string",
      "author": {
        "id": "usrXXXXXXXXXXXXXX",
        "email": "string",
        "name": "string"
      },
      "createdTime": "string (ISO 8601)"
    }
  ],
  "offset": "string (optional)"
}
```

### Response Fields

| Field | Type | Always Present | Description |
|-------|------|----------------|-------------|
| `comments` | array | Yes | Array of comment objects. Empty array if record has no comments |
| `offset` | string | No | Pagination cursor. Present only if there are more comments to retrieve. Pass this value as a query parameter in the next request |

### Full Response Example

```json
{
  "comments": [
    {
      "id": "comRst901uvw234",
      "text": "Final review complete. Shipping to production.",
      "author": {
        "id": "usrJKL345mno678",
        "email": "carol@example.com",
        "name": "Carol Williams"
      },
      "createdTime": "2024-06-16T16:45:00.000Z"
    },
    {
      "id": "comGhi567jkl890",
      "text": "Hey @[usrABC123def456] can you verify the numbers in this record?",
      "author": {
        "id": "usrJKL345mno678",
        "email": "carol@example.com",
        "name": "Carol Williams"
      },
      "createdTime": "2024-06-16T11:30:00.000Z"
    },
    {
      "id": "comAbc123def456",
      "text": "I've updated the status to reflect the latest changes.",
      "author": {
        "id": "usrABC123def456",
        "email": "alice@example.com",
        "name": "Alice Johnson"
      },
      "createdTime": "2024-06-15T14:30:00.000Z"
    }
  ],
  "offset": "itrXyz789abc012/comAbc123def456"
}
```

### Pagination

To retrieve all comments on a record:

1. Make an initial request without `offset`
2. If the response contains an `offset` field, pass it as a query parameter in the next request
3. Continue until no `offset` is returned

```python
all_comments = []
offset = None

while True:
    params = {"pageSize": 10}
    if offset:
        params["offset"] = offset

    response = requests.get(
        f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    data = response.json()
    all_comments.extend(data["comments"])

    offset = data.get("offset")
    if not offset:
        break
```

### Sorting

Comments are always returned in **descending order by `createdTime`** (newest first). This sort order is fixed and cannot be changed via the API.

---

## 2. Create Comment

**`POST /v0/{baseId}/{tableId}/{recordId}/comments`**

Creates a new comment on a specific record. The comment is attributed to the owner of the access token used for authentication.

### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer {token}` | Yes |
| `Content-Type` | `application/json` | Yes |

### Request Body Schema

```json
{
  "text": "string"
}
```

### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | The comment text. Must be a non-empty string. Supports @mentions using `@[usrXXX]` syntax |

### Request Example

```bash
curl -X POST "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Reviewed and approved. @[usrABC123def456] please proceed with next steps."
  }'
```

### Response Schema

Returns the created comment object:

```json
{
  "id": "comXXXXXXXXXXXXXX",
  "text": "string",
  "author": {
    "id": "usrXXXXXXXXXXXXXX",
    "email": "string",
    "name": "string"
  },
  "createdTime": "string (ISO 8601)"
}
```

### Full Response Example

```json
{
  "id": "comNew789xyz012",
  "text": "Reviewed and approved. @[usrABC123def456] please proceed with next steps.",
  "author": {
    "id": "usrJKL345mno678",
    "email": "carol@example.com",
    "name": "Carol Williams"
  },
  "createdTime": "2024-06-17T09:15:00.000Z"
}
```

---

## 3. Update Comment

**`PATCH /v0/{baseId}/{tableId}/{recordId}/comments/{commentId}`**

Updates the text of an existing comment. **Only the original author** of the comment can update it. The `author` and `createdTime` fields remain unchanged.

### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer {token}` | Yes |
| `Content-Type` | `application/json` | Yes |

### Request Body Schema

```json
{
  "text": "string"
}
```

### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | The new comment text. Must be a non-empty string. Replaces the entire previous text |

### Request Example

```bash
curl -X PATCH "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments/{commentId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated: Reviewed and approved with minor changes noted in the attached document."
  }'
```

### Response Schema

Returns the updated comment object:

```json
{
  "id": "comXXXXXXXXXXXXXX",
  "text": "string",
  "author": {
    "id": "usrXXXXXXXXXXXXXX",
    "email": "string",
    "name": "string"
  },
  "createdTime": "string (ISO 8601)"
}
```

### Full Response Example

```json
{
  "id": "comAbc123def456",
  "text": "Updated: Reviewed and approved with minor changes noted in the attached document.",
  "author": {
    "id": "usrABC123def456",
    "email": "alice@example.com",
    "name": "Alice Johnson"
  },
  "createdTime": "2024-06-15T14:30:00.000Z"
}
```

### Author Restriction

If a token attempts to update a comment authored by a different user, the API returns:

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You are not permitted to perform this operation"
  }
}
```

HTTP status: **403 Forbidden**

---

## 4. Delete Comment

**`DELETE /v0/{baseId}/{tableId}/{recordId}/comments/{commentId}`**

Permanently deletes a comment from a record. **Only the original author** of the comment can delete it. This action cannot be undone.

### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer {token}` | Yes |

### Request Example

```bash
curl -X DELETE "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments/{commentId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Response Schema

```json
{
  "id": "comXXXXXXXXXXXXXX",
  "deleted": true
}
```

### Full Response Example

```json
{
  "id": "comAbc123def456",
  "deleted": true
}
```

### Author Restriction

If a token attempts to delete a comment authored by a different user, the API returns:

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You are not permitted to perform this operation"
  }
}
```

HTTP status: **403 Forbidden**

---

## @Mention Format

Comments support mentioning Airtable users using a special syntax. Mentioned users receive an in-app notification.

### Syntax

```
@[usrXXXXXXXXXXXXXX]
```

Where `usrXXXXXXXXXXXXXX` is the Airtable user ID of the person to mention.

### Examples

| Text | Description |
|------|-------------|
| `"Hello @[usrABC123def456]"` | Mention a single user at the end |
| `"@[usrABC123def456] please review this"` | Mention at the beginning |
| `"@[usrABC123def456] and @[usrDEF456ghi789] need to coordinate"` | Multiple mentions |
| `"Task assigned to @[usrABC123def456]. CC @[usrDEF456ghi789]"` | Multiple mentions in context |

### Finding User IDs

User IDs can be obtained from:
- The `author.id` field in comment responses
- The collaborator endpoints (see the collaborators skill)
- The `singleCollaborator` or `multipleCollaborators` field values in record responses

### Mention Behavior

- Mentioned users receive a notification in Airtable
- The mention is stored as the raw `@[usrXXX]` syntax in the API
- In the Airtable UI, mentions are rendered as the user's display name with a highlight
- Invalid user IDs (users not in the base) are stored as-is but do not trigger notifications

---

## ID Formats

| Entity | Prefix | Format | Example |
|--------|--------|--------|---------|
| Base | `app` | 14 alphanumeric chars | `appABC123def456gh` |
| Table | `tbl` | 14 alphanumeric chars | `tblABC123def456gh` |
| Record | `rec` | 14 alphanumeric chars | `recABC123def456gh` |
| Comment | `com` | 14 alphanumeric chars | `comABC123def456gh` |
| User | `usr` | 14 alphanumeric chars | `usrABC123def456gh` |

---

## Required Scopes

| Endpoint | Method | Required Scope | Description |
|----------|--------|----------------|-------------|
| List Comments | GET | `data.records:read` | Read access to record data |
| Create Comment | POST | `data.records:write` | Write access to record data |
| Update Comment | PATCH | `data.records:write` | Write access; must be comment author |
| Delete Comment | DELETE | `data.records:write` | Write access; must be comment author |

**Important:** Even with `data.records:write` scope, update and delete operations are restricted to comments authored by the token owner. This is an ownership check, not a scope check.

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

The `Authorization` header is missing or contains an invalid token.

### 403 Forbidden — Insufficient Scope

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You are not permitted to perform this operation"
  }
}
```

The token does not have the required scope (`data.records:read` or `data.records:write`), or the token does not have access to the specified base.

### 403 Forbidden — Not Comment Author

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You are not permitted to perform this operation"
  }
}
```

The token owner is not the author of the comment being updated or deleted. Only the original author can modify or remove their comments.

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
- The `recordId` does not exist in the specified table
- The `commentId` does not exist on the specified record

### 422 Unprocessable Entity

```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "Could not parse the request body"
  }
}
```

The request body is missing, malformed, or the `text` field is empty or not a string.

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

Each API call (list, create, update, delete) counts as one request toward the rate limit.

---

## Usage Notes

1. **Comment ordering:** List responses always return comments newest-first. There is no parameter to change the sort order. To display comments oldest-first, reverse the array client-side.

2. **Pagination default:** The default `pageSize` is 10 comments. Adjust based on your needs, but be aware that very large page sizes may increase response time.

3. **Author ownership:** The comment API enforces strict author ownership for update and delete operations. The token used for authentication must belong to the same user who created the comment. There is no admin override for this restriction.

4. **Table ID vs name:** The `tableId` path parameter accepts either the table ID (e.g., `tblABC123`) or the table name (e.g., `Tasks`). Using table IDs is recommended for stability, as table names can change.

5. **Comment count on records:** To include comment counts when listing records, pass `recordMetadata[]=commentCount` as a query parameter to the List Records endpoint. This returns a `commentCount` field in each record's metadata without needing to call the comments endpoint.

6. **Rich text:** Comments are plain text only. Markdown, HTML, and other formatting are not supported. The only special syntax is the @mention format (`@[usrXXX]`).

7. **Character limit:** Comment text has a maximum length. Extremely long comments may be rejected with a 422 error.

8. **Timestamps:** All `createdTime` values are in ISO 8601 format with UTC timezone (ending in `Z`). The `createdTime` is immutable and does not change when a comment is updated.

9. **Deleted comments:** Once deleted, a comment cannot be recovered. The delete response only contains the `id` and `deleted: true` confirmation. The comment text and author information are not returned.

10. **Concurrent access:** If two users attempt to update the same comment simultaneously (which would require both to be the author, i.e., the same user with two tokens), the last write wins. There is no optimistic locking or conflict detection for comments.
