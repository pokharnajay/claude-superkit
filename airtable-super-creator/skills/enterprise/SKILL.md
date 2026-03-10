---
name: airtable-enterprise
description: Manage enterprise users, audit logs, and enterprise administration in Airtable. Use when user wants to manage enterprise accounts, deactivate users, review audit trails, export audit logs, or perform enterprise-level administration. Triggers on "airtable enterprise", "manage user", "audit log", "enterprise admin", "user management", "claim user", "audit trail".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable and Enterprise Scale plan
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Enterprise API

Manage enterprise-level user administration and audit logging. Get user information, change user states, review audit trails, and export audit log events in bulk.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base
> **Plan requirement:** Enterprise Scale plan required for all enterprise endpoints.

## Quick Start

### cURL -- Get Enterprise User

```bash
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python -- Get Enterprise User

```python
import requests, os

enterprise_id = "entXXXXXXXXXXXXXX"
user_id = "usrXXXXXXXXXXXXXX"

response = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
user = response.json()
print(f"{user['email']} - {user['state']}")
```

### cURL -- List Audit Log Events

```bash
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEvents" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

## Endpoints

### 1. Get Enterprise User

**`GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}`**

Retrieve detailed information about a specific user in the enterprise account.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `enterpriseAccountId` | string | The enterprise account ID (entXXX) |
| `userId` | string | The user ID (usrXXX) |

**Response:**

```json
{
  "id": "usrABC123DEF456",
  "email": "alice@company.com",
  "state": "active",
  "createdTime": "2024-01-15T10:30:00.000Z",
  "lastActivityTime": "2024-06-01T14:22:00.000Z",
  "collaborations": {
    "bases": [
      {
        "baseId": "appXXX123",
        "permissionLevel": "edit"
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
    }
  ]
}
```

**User States:**

| State | Description |
|-------|-------------|
| `active` | User account is active and can access Airtable |
| `deactivated` | User account is deactivated and cannot access Airtable |
| `pending` | User has been invited but has not yet activated their account |

### 2. Manage Enterprise User

**`PATCH /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}`**

Update a user's state, email, or collaborations within the enterprise account.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `enterpriseAccountId` | string | The enterprise account ID (entXXX) |
| `userId` | string | The user ID (usrXXX) |

**Request Body:**

```json
{
  "state": "deactivated"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `state` | string | No | New user state: `active` or `deactivated` |
| `email` | string | No | New email address for the user |

**cURL -- Deactivate a user:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "deactivated"}'
```

**cURL -- Reactivate a user:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "active"}'
```

**cURL -- Update a user's email:**

```bash
curl -X PATCH "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@company.com"}'
```

**Python -- Deactivate a user:**

```python
response = requests.patch(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={"state": "deactivated"},
)
response.raise_for_status()
print(f"User state updated: {response.json()['state']}")
```

### 3. Grant Admin Access

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/grantAdminAccess`**

Grant enterprise admin access to one or more users.

**Request Body:**

```json
{
  "userIds": ["usrXXX123", "usrXXX456"]
}
```

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/grantAdminAccess" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"userIds": ["usrXXX123"]}'
```

### 4. Revoke Admin Access

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/revokeAdminAccess`**

Revoke enterprise admin access from one or more users.

**Request Body:**

```json
{
  "userIds": ["usrXXX123"]
}
```

### 5. Claim/Manage Users (Batch)

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/claim/users`**

Batch claim users into the enterprise by email domain.

**Request Body:**

```json
{
  "emails": ["user1@company.com", "user2@company.com"]
}
```

### 6. Remove User from Enterprise

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}/remove`**

Completely remove a user from the enterprise account.

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/users/{userId}/remove" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### 7. Delete Users by Email (Batch)

**`DELETE /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users`**

Delete multiple users from the enterprise by email.

**Query Parameters:** `email[]=user1@company.com&email[]=user2@company.com`

### 8. List Enterprise Users

**`GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/users`**

List all users in the enterprise account with pagination.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `email` | string | Filter by email address |
| `state` | string | Filter by state: `active`, `deactivated`, `pending` |
| `sortField` | string | Sort by field |
| `sortDirection` | string | `asc` or `desc` |

### 9. Get User Group

**`GET /v0/meta/groups/{groupId}`**

Get details about a user group including its members.

### 10. Move Workspaces Between Enterprise Accounts

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/moveWorkspaces`**

Move workspaces to a different enterprise account (for restructuring).

### 11. Create Descendant Enterprise

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/descendants`**

Create a child enterprise account under the current one.

### 12. List Audit Log Events

**`GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEvents`**

Returns a paginated list of audit log events for the enterprise account. Events capture actions taken by users across the enterprise.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `enterpriseAccountId` | string | The enterprise account ID (entXXX) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `startTime` | string | ISO 8601 timestamp. Only return events after this time. |
| `endTime` | string | ISO 8601 timestamp. Only return events before this time. |
| `originatingUserId` | string | Filter by the user who performed the action (usrXXX) |
| `eventType` | string | Filter by event type (e.g., `createRecord`, `deleteBase`) |
| `modelId` | string | Filter by the model (record, table, base, etc.) the action was performed on |
| `pageSize` | integer | Number of events per page (default 100, max 1000) |
| `sortOrder` | string | `asc` or `desc` (default `desc`) |
| `cursor` | string | Pagination cursor from previous response |
| `previous` | string | Cursor for paginating backward |

**Response:**

```json
{
  "events": [
    {
      "id": "aevABC123DEF456",
      "timestamp": "2024-06-15T14:30:00.000Z",
      "action": "updateRecord",
      "actionContext": "directUserAction",
      "actor": {
        "userId": "usrXXX123",
        "email": "alice@company.com",
        "type": "user"
      },
      "modelId": "recXXX456",
      "modelType": "record",
      "payloadVersion": "1.0"
    },
    {
      "id": "aevGHI789JKL012",
      "timestamp": "2024-06-15T14:25:00.000Z",
      "action": "addCollaborator",
      "actionContext": "directUserAction",
      "actor": {
        "userId": "usrXXX789",
        "email": "bob@company.com",
        "type": "user"
      },
      "modelId": "appXXX123",
      "modelType": "base",
      "payloadVersion": "1.0"
    }
  ],
  "pagination": {
    "cursor": "aevXXXXXX",
    "previous": null
  }
}
```

**Common Event Types:**

| Category | Event Types |
|----------|-------------|
| Records | `createRecord`, `updateRecord`, `deleteRecord` |
| Fields | `createField`, `updateField`, `deleteField` |
| Tables | `createTable`, `updateTable`, `deleteTable` |
| Bases | `createBase`, `deleteBase`, `duplicateBase` |
| Collaborators | `addCollaborator`, `removeCollaborator`, `updateCollaborator` |
| Auth | `login`, `logout`, `createApiToken`, `deleteApiToken` |
| Shares | `createShare`, `updateShare`, `deleteShare` |
| Views | `createView`, `updateView`, `deleteView` |

**cURL with filters:**

```bash
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEvents?startTime=2024-06-01T00:00:00.000Z&endTime=2024-06-30T23:59:59.999Z&eventType=deleteRecord&pageSize=50" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python with filters:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    params={
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
        "eventType": "deleteRecord",
        "pageSize": 50,
        "sortOrder": "desc",
    },
)
events = response.json()["events"]
for event in events:
    print(f"{event['timestamp']} - {event['action']} by {event['actor']['email']}")
```

### 4. Create Audit Log Export Request

**`POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEventRequests`**

Create a bulk export request for audit log events. Use this for large-scale exports instead of paginating through the list endpoint.

**Request Body:**

```json
{
  "startTime": "2024-01-01T00:00:00.000Z",
  "endTime": "2024-06-30T23:59:59.999Z",
  "eventTypes": ["createRecord", "updateRecord", "deleteRecord"],
  "sourceIpAddresses": ["192.168.1.0/24"],
  "originatingUserIds": ["usrXXX123", "usrXXX456"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `startTime` | string | Yes | ISO 8601 start timestamp |
| `endTime` | string | Yes | ISO 8601 end timestamp |
| `eventTypes` | array | No | Filter to specific event types |
| `sourceIpAddresses` | array | No | Filter by source IP (supports CIDR notation) |
| `originatingUserIds` | array | No | Filter by users who performed the actions |

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEventRequests" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "2024-01-01T00:00:00.000Z",
    "endTime": "2024-06-30T23:59:59.999Z"
  }'
```

**Response:**

```json
{
  "id": "alrABC123DEF456",
  "state": "pending",
  "createdTime": "2024-07-01T10:00:00.000Z"
}
```

### 5. Get Audit Log Export Request Status

**`GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEventRequests/{requestId}`**

Check the status of a previously created audit log export request.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `enterpriseAccountId` | string | The enterprise account ID (entXXX) |
| `requestId` | string | The export request ID (alrXXX) |

**Response (pending):**

```json
{
  "id": "alrABC123DEF456",
  "state": "pending",
  "createdTime": "2024-07-01T10:00:00.000Z"
}
```

**Response (completed):**

```json
{
  "id": "alrABC123DEF456",
  "state": "done",
  "createdTime": "2024-07-01T10:00:00.000Z",
  "downloadUrl": "https://dl.airtable.com/auditlogs/...",
  "expiresTime": "2024-07-08T10:00:00.000Z"
}
```

**Export Request States:**

| State | Description |
|-------|-------------|
| `pending` | The export is being generated |
| `done` | Export is ready; `downloadUrl` is available |
| `error` | Export failed |

**cURL:**

```bash
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEventRequests/{requestId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python -- Poll until complete:**

```python
import time

request_id = "alrABC123DEF456"

while True:
    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests/{request_id}",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    )
    data = response.json()

    if data["state"] == "done":
        print(f"Download URL: {data['downloadUrl']}")
        print(f"Expires: {data['expiresTime']}")
        break
    elif data["state"] == "error":
        print("Export failed")
        break
    else:
        print("Still pending, waiting 10 seconds...")
        time.sleep(10)
```

## Common Patterns

### Deactivate a user when they leave the company

```python
import requests, os

enterprise_id = "entXXXXXXXXXXXXXX"
user_id = "usrXXXXXXXXXXXXXX"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

# Get user info first
user_resp = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers=headers,
)
user = user_resp.json()
print(f"Deactivating user: {user['email']} (current state: {user['state']})")

# Deactivate the user
response = requests.patch(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/users/{user_id}",
    headers=headers,
    json={"state": "deactivated"},
)
response.raise_for_status()
print(f"User deactivated successfully")
```

### Search audit logs for deleted records in a specific base

```python
import requests, os

enterprise_id = "entXXXXXXXXXXXXXX"
target_base_id = "appXXXXXXXXXXXXXX"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

all_events = []
cursor = None

while True:
    params = {
        "eventType": "deleteRecord",
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
        "pageSize": 100,
    }
    if cursor:
        params["cursor"] = cursor

    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
        headers=headers,
        params=params,
    )
    data = response.json()
    all_events.extend(data["events"])

    cursor = data.get("pagination", {}).get("cursor")
    if not cursor:
        break

print(f"Found {len(all_events)} delete events in the time range")
for event in all_events:
    print(f"  {event['timestamp']} - {event['actor']['email']} deleted {event['modelId']}")
```

### Export a full month of audit logs

```python
import requests, os, time

enterprise_id = "entXXXXXXXXXXXXXX"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

# Create export request
response = requests.post(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests",
    headers=headers,
    json={
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
    },
)
request_id = response.json()["id"]
print(f"Export request created: {request_id}")

# Poll until complete
while True:
    status_resp = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests/{request_id}",
        headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    )
    status = status_resp.json()

    if status["state"] == "done":
        print(f"Export ready: {status['downloadUrl']}")
        break
    elif status["state"] == "error":
        print("Export failed")
        break

    print("Waiting for export to complete...")
    time.sleep(15)
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| Get enterprise user | `enterprise.user:read` |
| Manage enterprise user | `enterprise.user:write` |
| List audit log events | `enterprise.auditLogs:read` |
| Create audit log export | `enterprise.auditLogs:read` |
| Get audit log export status | `enterprise.auditLogs:read` |

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks required scope or enterprise plan not active |
| 404 | `NOT_FOUND` | Invalid enterprise account ID, user ID, or request ID |
| 422 | `INVALID_REQUEST` | Invalid parameters (e.g., invalid state value, malformed timestamps) |
| 429 | `TOO_MANY_REQUESTS` | Rate limited, retry after 30s |

**Note:** All enterprise endpoints require an Enterprise Scale plan. If the enterprise plan is not active, requests will return a `403` error with a message indicating the feature is unavailable.

## References

For complete user management details, see [references/enterprise-api.md](references/enterprise-api.md).
For comprehensive audit log reference, see [references/audit-logs.md](references/audit-logs.md).
