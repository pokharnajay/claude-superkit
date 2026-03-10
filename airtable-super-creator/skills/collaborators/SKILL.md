---
name: airtable-collaborators
description: Get base collaborators, add collaborators, and list share links for Airtable bases. Use when user wants to manage base access, invite users, check permissions, or view share links. Triggers on "airtable collaborator", "base collaborator", "add collaborator", "share base", "list shares", "base permissions", "invite user".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Collaborators & Shares API

Manage collaborator access and share links for Airtable bases. List who has access, invite new collaborators by user ID or email, and retrieve share links.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base

## Quick Start

### cURL -- List Base Collaborators

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python -- List Base Collaborators

```python
import requests, os

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
collaborators = response.json()["collaborators"]
for c in collaborators:
    print(f"{c['email']} - {c['permissionLevel']}")
```

## Endpoints

### 1. Get Base Collaborators

**`GET /v0/meta/bases/{baseId}/collaborators`**

Returns a paginated list of all collaborators on a base, including their user ID, email, and permission level.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | The ID of the base (appXXX) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `offset` | string | Pagination cursor from previous response |

**Response:**

```json
{
  "collaborators": [
    {
      "userId": "usrABC123",
      "email": "alice@example.com",
      "permissionLevel": "owner"
    },
    {
      "userId": "usrDEF456",
      "email": "bob@example.com",
      "permissionLevel": "edit"
    },
    {
      "userId": "usrGHI789",
      "email": "carol@example.com",
      "permissionLevel": "read"
    }
  ],
  "offset": "itrXXXXXX/usrXXXXXX"
}
```

**Permission Levels:**

| Level | Description |
|-------|-------------|
| `none` | No access (collaborator record exists but access revoked) |
| `read` | Can view records and comments |
| `comment` | Can view and add comments |
| `edit` | Can edit records |
| `create` | Can edit records and configure base (create tables, fields, views) |
| `owner` | Full access including managing collaborators and deleting the base |

- If `offset` is present in the response, more collaborators exist. Pass it as a query param in the next request.

**Paginating through all collaborators:**

```python
all_collaborators = []
offset = None

while True:
    params = {}
    if offset:
        params["offset"] = offset
    response = requests.get(
        f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
        params=params,
    )
    data = response.json()
    all_collaborators.extend(data["collaborators"])
    offset = data.get("offset")
    if not offset:
        break

print(f"Total collaborators: {len(all_collaborators)}")
```

### 2. Add Base Collaborator

**`POST /v0/meta/bases/{baseId}/collaborators`**

Add one or more collaborators to a base. You can invite by user ID or by email address.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | The ID of the base (appXXX) |

**Request Body:**

```json
{
  "collaborators": [
    {
      "userId": "usrXXX123",
      "permissionLevel": "edit"
    }
  ]
}
```

Or invite by email:

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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `collaborators` | array | Yes | Array of collaborator objects to add |
| `collaborators[].userId` | string | Either userId or email | Airtable user ID (usrXXX) |
| `collaborators[].email` | string | Either userId or email | Email address to invite |
| `collaborators[].permissionLevel` | string | Yes | One of: `read`, `comment`, `edit`, `create` |

**cURL -- Invite by email:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "collaborators": [
      {"email": "newuser@example.com", "permissionLevel": "edit"}
    ]
  }'
```

**cURL -- Invite by user ID:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/bases/{baseId}/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "collaborators": [
      {"userId": "usrXXX123", "permissionLevel": "comment"}
    ]
  }'
```

**Python -- Invite multiple collaborators:**

```python
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "collaborators": [
            {"email": "alice@example.com", "permissionLevel": "edit"},
            {"email": "bob@example.com", "permissionLevel": "read"},
        ]
    },
)
result = response.json()
```

**Notes:**
- The maximum number of collaborators per request varies by plan.
- You cannot assign the `owner` permission level via the API.
- Inviting by email will send an invitation if the user does not already have an Airtable account.
- Adding a collaborator who already exists on the base will update their permission level.

### 3. List Shares

**`GET /v0/meta/bases/{baseId}/shares`**

Returns all share links associated with a base, including view shares, base shares, and form shares.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `baseId` | string | The ID of the base (appXXX) |

**Response:**

```json
{
  "shares": [
    {
      "shareId": "shrABC123",
      "type": "view",
      "state": "enabled",
      "viewId": "viwDEF456"
    },
    {
      "shareId": "shrGHI789",
      "type": "base",
      "state": "disabled"
    },
    {
      "shareId": "shrJKL012",
      "type": "form",
      "state": "enabled",
      "viewId": "viwMNO345"
    }
  ]
}
```

**Share object properties:**

| Property | Type | Description |
|----------|------|-------------|
| `shareId` | string | Unique share ID (shrXXX) |
| `type` | string | Share type: `view`, `base`, or `form` |
| `state` | string | `enabled` or `disabled` |
| `viewId` | string | The associated view ID (for `view` and `form` types) |

**cURL:**

```bash
curl "https://api.airtable.com/v0/meta/bases/{baseId}/shares" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/shares",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
shares = response.json()["shares"]
for share in shares:
    print(f"{share['shareId']} ({share['type']}) - {share['state']}")
```

### 4. Update Base Collaborator

**`PATCH /v0/meta/bases/{baseId}/collaborators/{userId}`**

Change a collaborator's permission level on a base.

**Request Body:**

```json
{
  "permissionLevel": "create"
}
```

**cURL:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/bases/{baseId}/collaborators/{userId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"permissionLevel": "create"}'
```

### 5. Remove Base Collaborator

**`DELETE /v0/meta/bases/{baseId}/collaborators/{userId}`**

Remove a collaborator from a base.

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/meta/bases/{baseId}/collaborators/{userId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Note:** Cannot remove the owner of a base.

### 6. Add Workspace Collaborator

**`POST /v0/meta/workspaces/{workspaceId}/collaborators`**

Add a collaborator at the workspace level (grants access to all bases in the workspace).

**Request Body:**

```json
{
  "email": "user@example.com",
  "permissionLevel": "create"
}
```

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/workspaces/{workspaceId}/collaborators" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "permissionLevel": "create"}'
```

## Common Patterns

### List all collaborators and their roles

```python
import requests, os

base_id = "appXXXXXXXXXXXXXX"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
)
for c in response.json()["collaborators"]:
    print(f"{c['email']:40s} {c['permissionLevel']}")
```

### Invite a new user to a base

```python
import requests, os

base_id = "appXXXXXXXXXXXXXX"
response = requests.post(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "collaborators": [
            {"email": "newteammember@example.com", "permissionLevel": "edit"}
        ]
    },
)
if response.status_code == 200:
    print("Collaborator added successfully")
else:
    print(f"Error: {response.status_code} - {response.json()}")
```

### Check a specific user's permissions

```python
import requests, os

base_id = "appXXXXXXXXXXXXXX"
target_email = "alice@example.com"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/collaborators",
    headers=headers,
)
collaborators = response.json()["collaborators"]
user = next((c for c in collaborators if c["email"] == target_email), None)

if user:
    print(f"{target_email} has '{user['permissionLevel']}' access")
else:
    print(f"{target_email} is not a collaborator on this base")
```

### List all enabled share links

```python
import requests, os

base_id = "appXXXXXXXXXXXXXX"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/bases/{base_id}/shares",
    headers=headers,
)
enabled_shares = [s for s in response.json()["shares"] if s["state"] == "enabled"]
for share in enabled_shares:
    view_info = f" (view: {share['viewId']})" if "viewId" in share else ""
    print(f"{share['shareId']} - {share['type']}{view_info}")
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| Get base collaborators | `schema.bases:read` |
| Add base collaborator | `schema.bases:write` |
| List shares | `schema.bases:read` |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks required scope or insufficient permissions on base |
| 404 | `NOT_FOUND` | Invalid base ID |
| 422 | `INVALID_REQUEST` | Invalid permission level, missing required fields, or invalid email/userId |
| 422 | `INVALID_PERMISSIONS` | Cannot assign `owner` permission via API |
| 429 | `TOO_MANY_REQUESTS` | Rate limited, retry after 30s |

## References

For complete API parameter details, see [references/collaborators-api.md](references/collaborators-api.md).
