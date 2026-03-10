---
name: airtable-comments
description: List, create, update, and delete comments on Airtable records. Use when user wants to read record comments, add comments, edit existing comments, or remove comments. Triggers on "airtable comment", "record comment", "list comments", "add comment", "create comment", "delete comment".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Comments API

Manage comments on individual Airtable records. List existing comments, add new ones (with @mention support), update comment text, and delete comments.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base

## Quick Start

### cURL — List Comments on a Record

```bash
curl "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — List Comments on a Record

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
comments = response.json()["comments"]
for comment in comments:
    print(f"{comment['author']['name']}: {comment['text']}")
```

## Endpoints

### 1. List Comments

**`GET /v0/{baseId}/{tableId}/{recordId}/comments`**

Returns a paginated list of comments on a specific record, sorted by creation time (newest first).

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | Base ID (appXXX) |
| `tableId` | string | Table ID or name |
| `recordId` | string | Record ID (recXXX) |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `offset` | string | — | Pagination cursor from previous response |
| `pageSize` | integer | 10 | Number of comments per page |

**Response:**

```json
{
  "comments": [
    {
      "id": "comABC123",
      "text": "This task needs review before we proceed.",
      "author": {
        "id": "usrXYZ789",
        "email": "alice@example.com",
        "name": "Alice Johnson"
      },
      "createdTime": "2024-06-15T14:30:00.000Z"
    },
    {
      "id": "comDEF456",
      "text": "Looks good to me! @[usrXYZ789] please merge.",
      "author": {
        "id": "usrABC123",
        "email": "bob@example.com",
        "name": "Bob Smith"
      },
      "createdTime": "2024-06-15T10:15:00.000Z"
    }
  ],
  "offset": "itrXXXXXX/comXXXXXX"
}
```

**Comment properties:**

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Comment ID (comXXX) |
| `text` | string | Comment body text (may contain @mentions) |
| `author` | object | Author info: `id`, `email`, `name` |
| `createdTime` | string | ISO 8601 timestamp of when the comment was created |

- If `offset` is present in the response, more comments exist. Pass it as a query param in the next request.
- Comments are sorted by creation time, newest first.

**cURL with pagination:**

```bash
curl "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments?pageSize=5" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python with pagination:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    params={"pageSize": 5},
)
```

### 2. Create Comment

**`POST /v0/{baseId}/{tableId}/{recordId}/comments`**

Add a new comment to a record.

**Request Body:**

```json
{
  "text": "This task needs review before we proceed."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Comment text. Supports @mentions using `@[usrXXX]` syntax |

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "This task needs review before we proceed."}'
```

**Python:**

```python
response = requests.post(
    f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={"text": "This task needs review before we proceed."},
)
new_comment = response.json()
print(f"Created comment: {new_comment['id']}")
```

**Response:**

```json
{
  "id": "comNEW789",
  "text": "This task needs review before we proceed.",
  "author": {
    "id": "usrXYZ789",
    "email": "alice@example.com",
    "name": "Alice Johnson"
  },
  "createdTime": "2024-06-16T09:00:00.000Z"
}
```

**@mention syntax:**

To mention a user in a comment, use the format `@[usrXXX]` where `usrXXX` is the user's Airtable user ID:

```bash
curl -X POST "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hey @[usrABC123] can you take a look at this?"}'
```

The mentioned user will receive a notification in Airtable.

### 3. Update Comment

**`PATCH /v0/{baseId}/{tableId}/{recordId}/comments/{commentId}`**

Update the text of an existing comment. Only the original comment author can update it.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | Base ID (appXXX) |
| `tableId` | string | Table ID or name |
| `recordId` | string | Record ID (recXXX) |
| `commentId` | string | Comment ID (comXXX) |

**Request Body:**

```json
{
  "text": "Updated: This task has been reviewed and approved."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | New comment text |

**cURL:**

```bash
curl -X PATCH "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments/{commentId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated: This task has been reviewed and approved."}'
```

**Python:**

```python
response = requests.patch(
    f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments/{comment_id}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={"text": "Updated: This task has been reviewed and approved."},
)
updated_comment = response.json()
```

**Response:**

```json
{
  "id": "comABC123",
  "text": "Updated: This task has been reviewed and approved.",
  "author": {
    "id": "usrXYZ789",
    "email": "alice@example.com",
    "name": "Alice Johnson"
  },
  "createdTime": "2024-06-15T14:30:00.000Z"
}
```

> **Important:** Only the comment author can update their own comment. Attempting to update another user's comment returns a 403 error.

### 4. Delete Comment

**`DELETE /v0/{baseId}/{tableId}/{recordId}/comments/{commentId}`**

Delete a comment from a record. Only the original comment author can delete it.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | Base ID (appXXX) |
| `tableId` | string | Table ID or name |
| `recordId` | string | Record ID (recXXX) |
| `commentId` | string | Comment ID (comXXX) |

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}/comments/{commentId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.delete(
    f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments/{comment_id}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
result = response.json()
print(f"Deleted: {result['deleted']}")
```

**Response:**

```json
{
  "id": "comABC123",
  "deleted": true
}
```

> **Important:** Only the comment author can delete their own comment. Attempting to delete another user's comment returns a 403 error.

## Common Patterns

### Add a comment to a record

```python
import requests, os

def add_comment(base_id, table_id, record_id, text, token):
    response = requests.post(
        f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"text": text},
    )
    response.raise_for_status()
    return response.json()

comment = add_comment(
    base_id, table_id, record_id,
    "Processing complete. Results attached.",
    os.environ["AIRTABLE_ACCESS_TOKEN"],
)
print(f"Comment ID: {comment['id']}")
```

### List all comments with pagination

```python
def list_all_comments(base_id, table_id, record_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    all_comments = []
    offset = None

    while True:
        params = {"pageSize": 10}
        if offset:
            params["offset"] = offset

        response = requests.get(
            f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}/comments",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        all_comments.extend(data["comments"])

        offset = data.get("offset")
        if not offset:
            break

    return all_comments

comments = list_all_comments(base_id, table_id, record_id, os.environ["AIRTABLE_ACCESS_TOKEN"])
print(f"Total comments: {len(comments)}")
for c in comments:
    print(f"  [{c['createdTime']}] {c['author']['name']}: {c['text']}")
```

### Add a comment with @mention

```python
# Mention a user by their user ID
comment = add_comment(
    base_id, table_id, record_id,
    "Hey @[usrABC123], this record needs your attention.",
    os.environ["AIRTABLE_ACCESS_TOKEN"],
)
```

### Comment on multiple records

```python
import time

def comment_on_records(base_id, table_id, record_ids, text, token):
    results = []
    for record_id in record_ids:
        comment = add_comment(base_id, table_id, record_id, text, token)
        results.append(comment)
        time.sleep(0.2)  # respect rate limit
    return results

record_ids = ["recABC123", "recDEF456", "recGHI789"]
results = comment_on_records(
    base_id, table_id, record_ids,
    "Batch review complete.",
    os.environ["AIRTABLE_ACCESS_TOKEN"],
)
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| List comments | `data.records:read` |
| Create comment | `data.records:write` |
| Update comment | `data.records:write` |
| Delete comment | `data.records:write` |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks required scope, or attempting to update/delete another user's comment |
| 404 | `NOT_FOUND` | Invalid base, table, record, or comment ID |
| 422 | `INVALID_REQUEST` | Missing or invalid `text` field in request body |
| 429 | `TOO_MANY_REQUESTS` | Rate limited, retry after 30s |

## References

For complete API schemas and detailed response formats, see [references/comments-api.md](references/comments-api.md).
