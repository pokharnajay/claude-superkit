# Airtable Collaborators & Shares API Reference

Complete reference for the Airtable Collaborators and Shares endpoints. Covers listing collaborators, adding collaborators, and listing share links for bases.

> **Base URL:** `https://api.airtable.com/v0`
> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`

---

## Table of Contents

1. [Get Base Collaborators](#get-base-collaborators)
2. [Add Base Collaborator](#add-base-collaborator)
3. [List Shares](#list-shares)
4. [Permission Levels](#permission-levels)
5. [Share Types](#share-types)
6. [Pagination](#pagination)
7. [Error Reference](#error-reference)
8. [Examples](#examples)

---

## Get Base Collaborators

### Endpoint

```
GET /v0/meta/bases/{baseId}/collaborators
```

### Description

Returns a paginated list of all collaborators who have access to the specified base. Each collaborator entry includes their user ID, email address, and current permission level.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The Airtable base ID (format: `appXXXXXXXXXXXXXX`) |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `offset` | string | No | Pagination cursor returned from a previous request. Pass this to retrieve the next page of results. |

### Response Schema

```json
{
  "collaborators": [
    {
      "userId": "usrABC123DEF456",
      "email": "user@example.com",
      "permissionLevel": "edit"
    }
  ],
  "offset": "itrXXXXXXXXXXXXXX/usrXXXXXXXXXXXXXX"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `collaborators` | array | Array of collaborator objects |
| `collaborators[].userId` | string | Unique Airtable user ID (format: `usrXXXXXXXXXXXXXX`) |
| `collaborators[].email` | string | Email address of the collaborator |
| `collaborators[].permissionLevel` | string | Current permission level on the base. One of: `none`, `read`, `comment`, `edit`, `create`, `owner` |
| `offset` | string or null | If present, pass as query parameter to get the next page. Absent when no more results. |

### cURL Example

```bash
# List collaborators for a base
curl "https://api.airtable.com/v0/meta/bases/appABC123DEF456/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# With pagination
curl "https://api.airtable.com/v0/meta/bases/appABC123DEF456/collaborators?offset=itrXXX/usrXXX" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python Example

```python
import requests, os

base_id = "appABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
)
response.raise_for_status()
data = response.json()

for collaborator in data["collaborators"]:
    print(f"User: {collaborator['userId']}")
    print(f"  Email: {collaborator['email']}")
    print(f"  Permission: {collaborator['permissionLevel']}")
```

### Required Scope

`schema.bases:read`

---

## Add Base Collaborator

### Endpoint

```
POST /v0/meta/bases/{baseId}/collaborators
```

### Description

Adds one or more collaborators to a base. Collaborators can be specified by their Airtable user ID or by email address. If a collaborator already exists on the base, their permission level will be updated to the new value.

When inviting by email, if the user does not have an existing Airtable account, an invitation email will be sent.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The Airtable base ID (format: `appXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |
| `Content-Type` | `application/json` |

### Request Body Schema

```json
{
  "collaborators": [
    {
      "userId": "usrXXXXXXXXXXXXXX",
      "permissionLevel": "edit"
    }
  ]
}
```

Or with email:

```json
{
  "collaborators": [
    {
      "email": "user@example.com",
      "permissionLevel": "edit"
    }
  ]
}
```

### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `collaborators` | array | Yes | Array of collaborator objects to add or update |
| `collaborators[].userId` | string | Conditional | Airtable user ID. Required if `email` is not provided. |
| `collaborators[].email` | string | Conditional | Email address. Required if `userId` is not provided. |
| `collaborators[].permissionLevel` | string | Yes | Permission level to grant. One of: `read`, `comment`, `edit`, `create`. Cannot be `owner`. |

### Constraints

- You must provide either `userId` or `email` for each collaborator, not both.
- The `owner` permission level cannot be assigned via the API.
- The maximum number of collaborators per request depends on your Airtable plan.
- The calling token must have `create` or `owner` permission on the base.

### Response Schema

On success, returns the list of collaborators that were added or updated:

```json
{
  "collaborators": [
    {
      "userId": "usrABC123DEF456",
      "email": "user@example.com",
      "permissionLevel": "edit"
    }
  ]
}
```

### cURL Examples

```bash
# Add collaborator by email
curl -X POST "https://api.airtable.com/v0/meta/bases/appABC123DEF456/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "collaborators": [
      {"email": "alice@example.com", "permissionLevel": "edit"}
    ]
  }'

# Add collaborator by user ID
curl -X POST "https://api.airtable.com/v0/meta/bases/appABC123DEF456/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "collaborators": [
      {"userId": "usrXXX123YYY456", "permissionLevel": "comment"}
    ]
  }'

# Add multiple collaborators at once
curl -X POST "https://api.airtable.com/v0/meta/bases/appABC123DEF456/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "collaborators": [
      {"email": "alice@example.com", "permissionLevel": "edit"},
      {"email": "bob@example.com", "permissionLevel": "read"},
      {"email": "carol@example.com", "permissionLevel": "comment"}
    ]
  }'
```

### Python Examples

```python
import requests, os

base_id = "appABC123DEF456"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

# Add a single collaborator by email
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
    json={
        "collaborators": [
            {"email": "newuser@example.com", "permissionLevel": "edit"}
        ]
    },
)
response.raise_for_status()
print("Collaborator added:", response.json())

# Add a single collaborator by user ID
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
    json={
        "collaborators": [
            {"userId": "usrXXX123YYY456", "permissionLevel": "read"}
        ]
    },
)
response.raise_for_status()

# Update an existing collaborator's permission level
# (same endpoint -- if user already exists, their level is updated)
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
    json={
        "collaborators": [
            {"email": "existinguser@example.com", "permissionLevel": "create"}
        ]
    },
)
response.raise_for_status()
```

### Required Scope

`schema.bases:write`

---

## List Shares

### Endpoint

```
GET /v0/meta/bases/{baseId}/shares
```

### Description

Returns all share links associated with a base. Share links allow external access to views, the full base, or form views without requiring collaborator-level access.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The Airtable base ID (format: `appXXXXXXXXXXXXXX`) |

### Response Schema

```json
{
  "shares": [
    {
      "shareId": "shrABC123DEF456",
      "type": "view",
      "state": "enabled",
      "viewId": "viwXYZ789ABC012"
    },
    {
      "shareId": "shrGHI789JKL012",
      "type": "base",
      "state": "disabled"
    },
    {
      "shareId": "shrMNO345PQR678",
      "type": "form",
      "state": "enabled",
      "viewId": "viwSTU901VWX234"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `shares` | array | Array of share objects |
| `shares[].shareId` | string | Unique share ID (format: `shrXXXXXXXXXXXXXX`) |
| `shares[].type` | string | Type of share. One of: `view`, `base`, `form` |
| `shares[].state` | string | Current state of the share link. One of: `enabled`, `disabled` |
| `shares[].viewId` | string | The associated view ID. Present for `view` and `form` share types. |

### cURL Example

```bash
curl "https://api.airtable.com/v0/meta/bases/appABC123DEF456/shares" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python Example

```python
import requests, os

base_id = "appABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/shares",
    headers=headers,
)
response.raise_for_status()
shares = response.json()["shares"]

for share in shares:
    status = "ACTIVE" if share["state"] == "enabled" else "INACTIVE"
    view_info = f" -> view {share['viewId']}" if "viewId" in share else ""
    print(f"[{status}] {share['shareId']} ({share['type']}){view_info}")
```

### Required Scope

`schema.bases:read`

---

## Permission Levels

The following permission levels are used across the Airtable platform for base-level access control:

| Level | Value | Can View | Can Comment | Can Edit Records | Can Configure Base | Can Manage Collaborators |
|-------|-------|----------|-------------|-----------------|-------------------|-------------------------|
| None | `none` | No | No | No | No | No |
| Read | `read` | Yes | No | No | No | No |
| Comment | `comment` | Yes | Yes | No | No | No |
| Edit | `edit` | Yes | Yes | Yes | No | No |
| Create | `create` | Yes | Yes | Yes | Yes | No |
| Owner | `owner` | Yes | Yes | Yes | Yes | Yes |

### Permission Level Hierarchy

Permissions are hierarchical. Each level includes all capabilities of the levels below it:

```
owner > create > edit > comment > read > none
```

### Notes on Permission Assignment

- The `owner` level cannot be assigned via the API. Use the Airtable web UI to transfer ownership.
- When updating a collaborator's permission, the new level completely replaces the old one.
- A token must have `create` or `owner` access on a base to add or modify collaborators.

---

## Share Types

| Type | Description | Has viewId |
|------|-------------|------------|
| `view` | A shared view link that gives read-only access to a specific view of the base | Yes |
| `base` | A shared base link that gives read-only access to the entire base | No |
| `form` | A shared form link that allows external users to submit records via a form view | Yes |

### Share States

| State | Description |
|-------|-------------|
| `enabled` | The share link is active and accessible |
| `disabled` | The share link exists but is not currently accessible |

---

## Pagination

The Get Base Collaborators endpoint supports cursor-based pagination.

### How Pagination Works

1. Make the initial request without an `offset` parameter.
2. If the response includes an `offset` field, more results are available.
3. Pass the `offset` value as a query parameter in your next request.
4. Repeat until the response no longer includes an `offset` field.

### Python Pagination Helper

```python
import requests, os

def get_all_collaborators(base_id):
    """Fetch all collaborators across all pages."""
    headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators"
    all_collaborators = []
    offset = None

    while True:
        params = {}
        if offset:
            params["offset"] = offset

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        all_collaborators.extend(data["collaborators"])
        offset = data.get("offset")

        if not offset:
            break

    return all_collaborators
```

---

## Error Reference

### HTTP Status Codes

| Status | Error Type | Description | Common Cause |
|--------|-----------|-------------|--------------|
| 400 | `BAD_REQUEST` | The request body is malformed | Invalid JSON, missing fields |
| 401 | `AUTHENTICATION_REQUIRED` | No valid authentication provided | Missing or expired token |
| 403 | `NOT_AUTHORIZED` | Authenticated but lacking permission | Token lacks scope, or insufficient base permission |
| 404 | `NOT_FOUND` | Resource does not exist | Invalid base ID |
| 422 | `INVALID_REQUEST` | Request is well-formed but semantically invalid | Invalid permission level, invalid email format |
| 422 | `INVALID_PERMISSIONS` | Permission level is not allowed | Attempted to set `owner` via API |
| 429 | `TOO_MANY_REQUESTS` | Rate limit exceeded | More than 5 requests/sec per base |
| 500 | `SERVER_ERROR` | Internal server error | Retry with exponential backoff |

### Error Response Format

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You do not have permission to perform this operation."
  }
}
```

### Common Error Scenarios

**Adding collaborator without sufficient permissions:**
```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You must have at least 'create' permission level on this base to add collaborators."
  }
}
```

**Attempting to set owner permission:**
```json
{
  "error": {
    "type": "INVALID_PERMISSIONS",
    "message": "The 'owner' permission level cannot be assigned via the API."
  }
}
```

**Invalid email address:**
```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "Invalid email address format."
  }
}
```

---

## Examples

### Audit Base Access

List all collaborators and group them by permission level:

```python
import requests, os
from collections import defaultdict

base_id = "appABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
)
response.raise_for_status()

by_permission = defaultdict(list)
for c in response.json()["collaborators"]:
    by_permission[c["permissionLevel"]].append(c["email"])

for level in ["owner", "create", "edit", "comment", "read", "none"]:
    users = by_permission.get(level, [])
    if users:
        print(f"\n{level.upper()} ({len(users)}):")
        for email in sorted(users):
            print(f"  - {email}")
```

### Bulk Invite from a List

Invite multiple users from a list of emails:

```python
import requests, os

base_id = "appABC123DEF456"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

emails_to_invite = [
    "alice@example.com",
    "bob@example.com",
    "carol@example.com",
    "dave@example.com",
]
permission_level = "edit"

collaborators = [
    {"email": email, "permissionLevel": permission_level}
    for email in emails_to_invite
]

response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
    json={"collaborators": collaborators},
)

if response.status_code == 200:
    print(f"Successfully invited {len(emails_to_invite)} collaborators")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### Check If a User Has Access

Determine whether a specific user is a collaborator and what level they have:

```python
import requests, os

def check_user_access(base_id, target_email):
    """Check if a user has access to a base and return their permission level."""
    headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

    all_collaborators = []
    offset = None

    while True:
        params = {}
        if offset:
            params["offset"] = offset
        response = requests.get(
            f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        all_collaborators.extend(data["collaborators"])
        offset = data.get("offset")
        if not offset:
            break

    user = next(
        (c for c in all_collaborators if c["email"].lower() == target_email.lower()),
        None,
    )

    if user:
        return user["permissionLevel"]
    return None


# Usage
level = check_user_access("appABC123DEF456", "alice@example.com")
if level:
    print(f"User has '{level}' access")
else:
    print("User does not have access to this base")
```

### Get All Active Share Links with URLs

List enabled shares and construct their public URLs:

```python
import requests, os

base_id = "appABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/shares",
    headers=headers,
)
response.raise_for_status()

shares = response.json()["shares"]
active_shares = [s for s in shares if s["state"] == "enabled"]

print(f"Found {len(active_shares)} active share link(s):\n")
for share in active_shares:
    share_url = f"https://airtable.com/{share['shareId']}"
    print(f"  Type: {share['type']}")
    print(f"  ID:   {share['shareId']}")
    print(f"  URL:  {share_url}")
    if "viewId" in share:
        print(f"  View: {share['viewId']}")
    print()
```
