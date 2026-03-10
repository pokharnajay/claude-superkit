# Airtable Enterprise User Management API Reference

Complete reference for the Airtable Enterprise user management endpoints. Covers retrieving user information, updating user state, and managing user email addresses within an enterprise account.

> **Base URL:** `https://api.airtable.com/v0`
> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Plan:** Enterprise Scale plan required

---

## Table of Contents

1. [Get Enterprise User](#get-enterprise-user)
2. [Manage Enterprise User (PATCH)](#manage-enterprise-user)
3. [User Object Schema](#user-object-schema)
4. [User States](#user-states)
5. [Collaborations Schema](#collaborations-schema)
6. [Groups Schema](#groups-schema)
7. [Error Reference](#error-reference)
8. [Common Patterns](#common-patterns)
9. [Best Practices](#best-practices)

---

## Get Enterprise User

### Endpoint

```
GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}
```

### Description

Retrieve detailed information about a specific user within the enterprise account. Returns the user's profile, current state, collaboration details across bases, workspaces, and interfaces, and group memberships.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enterpriseAccountId` | string | Yes | The enterprise account ID (format: `entXXXXXXXXXXXXXX`) |
| `userId` | string | Yes | The Airtable user ID (format: `usrXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

### Response Schema

```json
{
  "id": "usrABC123DEF456",
  "email": "alice@company.com",
  "state": "active",
  "createdTime": "2024-01-15T10:30:00.000Z",
  "lastActivityTime": "2024-06-01T14:22:00.000Z",
  "invitedToAirtableByUserId": "usrINVITER123",
  "collaborations": {
    "bases": [
      {
        "baseId": "appXXX123",
        "permissionLevel": "edit"
      },
      {
        "baseId": "appYYY456",
        "permissionLevel": "owner"
      }
    ],
    "workspaces": [
      {
        "workspaceId": "wspXXX456",
        "permissionLevel": "owner"
      }
    ],
    "interfaces": [
      {
        "interfaceId": "intXXX789",
        "baseId": "appXXX123",
        "permissionLevel": "editor"
      }
    ]
  },
  "groups": [
    {
      "groupId": "grpXXX123",
      "name": "Engineering"
    },
    {
      "groupId": "grpYYY456",
      "name": "All Employees"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user ID (`usrXXX`) |
| `email` | string | User's email address |
| `state` | string | Current user state: `active`, `deactivated`, or `pending` |
| `createdTime` | string | ISO 8601 timestamp when the user was created |
| `lastActivityTime` | string | ISO 8601 timestamp of the user's last activity. May be `null` for `pending` users. |
| `invitedToAirtableByUserId` | string | User ID of the person who invited this user. May be `null`. |
| `collaborations` | object | All collaborations the user has across bases, workspaces, and interfaces |
| `collaborations.bases` | array | Array of base collaboration objects |
| `collaborations.bases[].baseId` | string | Base ID (`appXXX`) |
| `collaborations.bases[].permissionLevel` | string | Permission level on the base: `none`, `read`, `comment`, `edit`, `create`, `owner` |
| `collaborations.workspaces` | array | Array of workspace collaboration objects |
| `collaborations.workspaces[].workspaceId` | string | Workspace ID (`wspXXX`) |
| `collaborations.workspaces[].permissionLevel` | string | Permission level in the workspace: `read`, `comment`, `edit`, `create`, `owner` |
| `collaborations.interfaces` | array | Array of interface collaboration objects |
| `collaborations.interfaces[].interfaceId` | string | Interface ID (`intXXX`) |
| `collaborations.interfaces[].baseId` | string | Base ID the interface belongs to (`appXXX`) |
| `collaborations.interfaces[].permissionLevel` | string | Permission level on the interface: `viewer`, `editor`, `owner` |
| `groups` | array | Array of group membership objects |
| `groups[].groupId` | string | Group ID (`grpXXX`) |
| `groups[].name` | string | Group display name |

### cURL Example

```bash
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/users/usrGHI789JKL012" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python Example

```python
import requests, os

enterprise_id = "entABC123DEF456"
user_id = "usrGHI789JKL012"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers=headers,
)
response.raise_for_status()
user = response.json()

print(f"User: {user['email']}")
print(f"State: {user['state']}")
print(f"Created: {user['createdTime']}")
print(f"Last Active: {user.get('lastActivityTime', 'N/A')}")
print(f"Base Collaborations: {len(user['collaborations']['bases'])}")
print(f"Workspace Collaborations: {len(user['collaborations']['workspaces'])}")
print(f"Groups: {[g['name'] for g in user['groups']]}")
```

### Required Scope

`enterprise.user:read`

---

## Manage Enterprise User

### Endpoint

```
PATCH /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}
```

### Description

Update a user's state or email within the enterprise account. This endpoint can be used to deactivate users (offboarding), reactivate previously deactivated users, and update email addresses.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enterpriseAccountId` | string | Yes | The enterprise account ID (format: `entXXXXXXXXXXXXXX`) |
| `userId` | string | Yes | The Airtable user ID (format: `usrXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |
| `Content-Type` | `application/json` |

### Request Body Schema

```json
{
  "state": "deactivated",
  "email": "newemail@company.com"
}
```

### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `state` | string | No | New user state. Valid values: `active`, `deactivated`. Cannot set to `pending`. |
| `email` | string | No | New email address for the user. Must be a valid email format. |

At least one field (`state` or `email`) must be provided.

### State Transitions

| From State | To State | Allowed | Notes |
|------------|----------|---------|-------|
| `active` | `deactivated` | Yes | Deactivates the user immediately. User loses all access. |
| `deactivated` | `active` | Yes | Reactivates the user. Collaborations may need to be re-added. |
| `pending` | `deactivated` | Yes | Cancels the pending invitation. |
| `pending` | `active` | No | Pending users must accept their invitation to become active. |
| Any | `pending` | No | Cannot set state to pending via API. |

### Response Schema

Returns the updated user object with the same schema as the GET endpoint:

```json
{
  "id": "usrABC123DEF456",
  "email": "alice@company.com",
  "state": "deactivated",
  "createdTime": "2024-01-15T10:30:00.000Z",
  "lastActivityTime": "2024-06-01T14:22:00.000Z",
  "collaborations": {
    "bases": [],
    "workspaces": [],
    "interfaces": []
  },
  "groups": []
}
```

### cURL Examples

```bash
# Deactivate a user
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/users/usrGHI789JKL012" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "deactivated"}'

# Reactivate a user
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/users/usrGHI789JKL012" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "active"}'

# Update a user's email
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/users/usrGHI789JKL012" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice.smith@company.com"}'

# Deactivate and update email in one request
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/users/usrGHI789JKL012" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "deactivated", "email": "alice.smith@company.com"}'
```

### Python Examples

```python
import requests, os

enterprise_id = "entABC123DEF456"
user_id = "usrGHI789JKL012"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

# Deactivate a user
response = requests.patch(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers=headers,
    json={"state": "deactivated"},
)
response.raise_for_status()
print(f"User deactivated: {response.json()['email']}")

# Reactivate a user
response = requests.patch(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers=headers,
    json={"state": "active"},
)
response.raise_for_status()
print(f"User reactivated: {response.json()['email']}")

# Update email
response = requests.patch(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers=headers,
    json={"email": "new.email@company.com"},
)
response.raise_for_status()
print(f"Email updated to: {response.json()['email']}")
```

### Required Scope

`enterprise.user:write`

---

## User Object Schema

### Complete User Object

| Field | Type | Always Present | Description |
|-------|------|---------------|-------------|
| `id` | string | Yes | User ID in `usrXXXXXXXXXXXXXX` format |
| `email` | string | Yes | User's current email address |
| `state` | string | Yes | One of: `active`, `deactivated`, `pending` |
| `createdTime` | string | Yes | ISO 8601 UTC timestamp of account creation |
| `lastActivityTime` | string | No | ISO 8601 UTC timestamp. Null for `pending` users or users who have never logged in. |
| `invitedToAirtableByUserId` | string | No | The `usrXXX` ID of whoever invited this user. Null if the user self-registered. |
| `collaborations` | object | Yes | Container for all collaboration arrays |
| `groups` | array | Yes | Group memberships. May be empty array `[]`. |

### ID Formats

| Entity | Format | Example |
|--------|--------|---------|
| User | `usrXXXXXXXXXXXXXX` | `usrABC123DEF456` |
| Enterprise Account | `entXXXXXXXXXXXXXX` | `entABC123DEF456` |
| Base | `appXXXXXXXXXXXXXX` | `appABC123DEF456` |
| Workspace | `wspXXXXXXXXXXXXXX` | `wspABC123DEF456` |
| Interface | `intXXXXXXXXXXXXXX` | `intABC123DEF456` |
| Group | `grpXXXXXXXXXXXXXX` | `grpABC123DEF456` |

---

## User States

### State Definitions

| State | Description | Can Log In | Has Collaborations |
|-------|-------------|------------|-------------------|
| `active` | Account is active. User can log in and access all their collaborations. | Yes | Yes |
| `deactivated` | Account is suspended. User cannot log in. Collaborations are preserved but inaccessible. | No | Preserved but inaccessible |
| `pending` | Invitation sent but not yet accepted. User cannot log in until they accept. | No | Assigned but not yet accessible |

### What Happens When a User Is Deactivated

1. The user is immediately logged out of all active sessions.
2. All API tokens belonging to the user are revoked.
3. The user cannot log in or access any Airtable resources.
4. Their collaboration records are preserved (not deleted).
5. Records and content created by the user remain in their respective bases.
6. Automations owned by the user continue to run (they are not disabled).

### What Happens When a User Is Reactivated

1. The user can log in again with their existing credentials.
2. Base and workspace collaborations may need to be re-added by an admin.
3. Previously revoked API tokens are NOT automatically restored -- new tokens must be created.
4. Group memberships are restored.

---

## Collaborations Schema

### Base Collaborations

```json
{
  "bases": [
    {
      "baseId": "appXXXXXXXXXXXXXX",
      "permissionLevel": "edit"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `baseId` | string | The base ID |
| `permissionLevel` | string | One of: `none`, `read`, `comment`, `edit`, `create`, `owner` |

### Workspace Collaborations

```json
{
  "workspaces": [
    {
      "workspaceId": "wspXXXXXXXXXXXXXX",
      "permissionLevel": "owner"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `workspaceId` | string | The workspace ID |
| `permissionLevel` | string | One of: `read`, `comment`, `edit`, `create`, `owner` |

### Interface Collaborations

```json
{
  "interfaces": [
    {
      "interfaceId": "intXXXXXXXXXXXXXX",
      "baseId": "appXXXXXXXXXXXXXX",
      "permissionLevel": "editor"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `interfaceId` | string | The interface ID |
| `baseId` | string | The base ID the interface belongs to |
| `permissionLevel` | string | One of: `viewer`, `editor`, `owner` |

---

## Groups Schema

```json
{
  "groups": [
    {
      "groupId": "grpXXXXXXXXXXXXXX",
      "name": "Engineering"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `groupId` | string | The group ID |
| `name` | string | Human-readable group name |

Groups are managed via the Airtable admin panel. The API provides read-only access to group memberships.

---

## Error Reference

### HTTP Status Codes

| Status | Error Type | Description | Common Cause |
|--------|-----------|-------------|--------------|
| 400 | `BAD_REQUEST` | Request body is malformed | Invalid JSON or missing Content-Type header |
| 401 | `AUTHENTICATION_REQUIRED` | No valid authentication | Missing or expired token |
| 403 | `NOT_AUTHORIZED` | Insufficient permissions | Token lacks `enterprise.user:read` or `enterprise.user:write` scope, or enterprise plan is not active |
| 404 | `NOT_FOUND` | Resource not found | Invalid enterprise account ID or user ID |
| 422 | `INVALID_REQUEST` | Semantically invalid request | Invalid state transition, invalid email format, empty request body |
| 429 | `TOO_MANY_REQUESTS` | Rate limit exceeded | Too many requests per second |
| 500 | `SERVER_ERROR` | Internal server error | Retry with exponential backoff |

### Error Response Format

```json
{
  "error": {
    "type": "NOT_FOUND",
    "message": "Could not find user usrXXXXXXXXXXXXXX in enterprise account entXXXXXXXXXXXXXX."
  }
}
```

### Common Error Scenarios

**User not found in enterprise:**
```json
{
  "error": {
    "type": "NOT_FOUND",
    "message": "Could not find user usrXXXXXXXXXXXXXX in enterprise account entXXXXXXXXXXXXXX."
  }
}
```

**Invalid state transition (setting pending user to active):**
```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "Cannot transition user from 'pending' to 'active'. Pending users must accept their invitation."
  }
}
```

**Enterprise plan not active:**
```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "Enterprise features require an active Enterprise Scale plan."
  }
}
```

**Missing required scope:**
```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "Token requires the 'enterprise.user:write' scope to perform this operation."
  }
}
```

---

## Common Patterns

### Check User State Before Taking Action

```python
import requests, os

def get_user_state(enterprise_id, user_id):
    """Get the current state of an enterprise user."""
    headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}
    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

def deactivate_user_safely(enterprise_id, user_id):
    """Deactivate a user only if they are currently active."""
    user = get_user_state(enterprise_id, user_id)

    if user["state"] == "deactivated":
        print(f"User {user['email']} is already deactivated.")
        return user

    if user["state"] == "pending":
        print(f"User {user['email']} has a pending invitation. Cancelling...")

    headers = {
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    }
    response = requests.patch(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
        headers=headers,
        json={"state": "deactivated"},
    )
    response.raise_for_status()
    print(f"User {user['email']} has been deactivated.")
    return response.json()
```

### Audit a User's Access Across the Enterprise

```python
import requests, os

def audit_user_access(enterprise_id, user_id):
    """Generate a full access report for an enterprise user."""
    headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}
    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
        headers=headers,
    )
    response.raise_for_status()
    user = response.json()

    print(f"Access Report for {user['email']}")
    print(f"State: {user['state']}")
    print(f"Account Created: {user['createdTime']}")
    print(f"Last Activity: {user.get('lastActivityTime', 'Never')}")
    print()

    # Base access
    bases = user["collaborations"]["bases"]
    print(f"Base Collaborations ({len(bases)}):")
    for base in bases:
        print(f"  {base['baseId']} - {base['permissionLevel']}")

    # Workspace access
    workspaces = user["collaborations"]["workspaces"]
    print(f"\nWorkspace Collaborations ({len(workspaces)}):")
    for ws in workspaces:
        print(f"  {ws['workspaceId']} - {ws['permissionLevel']}")

    # Interface access
    interfaces = user["collaborations"]["interfaces"]
    print(f"\nInterface Collaborations ({len(interfaces)}):")
    for intf in interfaces:
        print(f"  {intf['interfaceId']} (base: {intf['baseId']}) - {intf['permissionLevel']}")

    # Groups
    groups = user["groups"]
    print(f"\nGroup Memberships ({len(groups)}):")
    for group in groups:
        print(f"  {group['name']} ({group['groupId']})")

    return user
```

### Bulk Offboarding -- Deactivate Multiple Users

```python
import requests, os, time

def bulk_deactivate(enterprise_id, user_ids):
    """Deactivate multiple users with rate limiting."""
    headers = {
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    }
    results = {"success": [], "failed": [], "skipped": []}

    for user_id in user_ids:
        try:
            # Check current state
            get_resp = requests.get(
                f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
                headers=headers,
            )
            get_resp.raise_for_status()
            user = get_resp.json()

            if user["state"] == "deactivated":
                results["skipped"].append({"userId": user_id, "email": user["email"], "reason": "already deactivated"})
                continue

            # Deactivate
            patch_resp = requests.patch(
                f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
                headers=headers,
                json={"state": "deactivated"},
            )
            patch_resp.raise_for_status()
            results["success"].append({"userId": user_id, "email": user["email"]})
            print(f"Deactivated: {user['email']}")

        except requests.exceptions.HTTPError as e:
            results["failed"].append({"userId": user_id, "error": str(e)})
            print(f"Failed to deactivate {user_id}: {e}")

        time.sleep(0.25)  # Rate limiting

    print(f"\nResults: {len(results['success'])} deactivated, "
          f"{len(results['skipped'])} skipped, {len(results['failed'])} failed")
    return results
```

---

## Best Practices

1. **Always check user state before modifying.** Avoid unnecessary API calls by checking the current state first.
2. **Use rate limiting.** When performing bulk operations, add delays between requests to respect the 5 req/sec limit.
3. **Log all state changes.** Keep your own records of user state transitions for compliance purposes.
4. **Handle deactivation gracefully.** When offboarding a user, consider documenting their collaborations before deactivation so access can be reassigned.
5. **Token scope principle of least privilege.** Use `enterprise.user:read` when you only need to view user information. Only request `enterprise.user:write` when you need to modify user state or email.
6. **Monitor for pending users.** Users in the `pending` state have been invited but have not yet accepted. Consider following up or cancelling stale invitations.
