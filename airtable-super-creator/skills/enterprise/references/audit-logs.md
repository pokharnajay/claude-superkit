# Airtable Enterprise Audit Logs API Reference

Complete reference for the Airtable Enterprise audit log endpoints. Covers listing audit log events, filtering and pagination, bulk export requests, event types, and response schemas.

> **Base URL:** `https://api.airtable.com/v0`
> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Plan:** Enterprise Scale plan required
> **Required Scope:** `enterprise.auditLogs:read`

---

## Table of Contents

1. [List Audit Log Events](#list-audit-log-events)
2. [Create Audit Log Export Request](#create-audit-log-export-request)
3. [Get Audit Log Export Request Status](#get-audit-log-export-request-status)
4. [Event Object Schema](#event-object-schema)
5. [Event Types Reference](#event-types-reference)
6. [Actor Types](#actor-types)
7. [Model Types](#model-types)
8. [Action Contexts](#action-contexts)
9. [Filtering](#filtering)
10. [Pagination](#pagination)
11. [Bulk Export Workflow](#bulk-export-workflow)
12. [Error Reference](#error-reference)
13. [Common Patterns](#common-patterns)

---

## List Audit Log Events

### Endpoint

```
GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEvents
```

### Description

Returns a paginated list of audit log events for the enterprise account. Events capture user actions across the entire enterprise, including record operations, schema changes, collaborator management, authentication events, and more.

Events are returned in reverse chronological order by default (newest first).

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enterpriseAccountId` | string | Yes | The enterprise account ID (format: `entXXXXXXXXXXXXXX`) |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `startTime` | string | No | None | ISO 8601 timestamp. Only return events that occurred at or after this time. Example: `2024-06-01T00:00:00.000Z` |
| `endTime` | string | No | None | ISO 8601 timestamp. Only return events that occurred at or before this time. Example: `2024-06-30T23:59:59.999Z` |
| `originatingUserId` | string | No | None | Filter events to only those performed by this user ID (`usrXXX`). |
| `eventType` | string | No | None | Filter to a specific event type (e.g., `createRecord`, `deleteBase`). See [Event Types Reference](#event-types-reference). |
| `modelId` | string | No | None | Filter events to those affecting a specific model (record, table, base, etc.) by ID. |
| `pageSize` | integer | No | 100 | Number of events to return per page. Minimum: 1, Maximum: 1000. |
| `sortOrder` | string | No | `desc` | Sort order for events by timestamp. `asc` for oldest first, `desc` for newest first. |
| `cursor` | string | No | None | Pagination cursor from a previous response to get the next page. |
| `previous` | string | No | None | Pagination cursor for navigating backward to the previous page. |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

### Response Schema

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
      "payloadVersion": "1.0",
      "context": {
        "baseId": "appXXX789",
        "tableId": "tblXXX012",
        "viewId": "viwXXX345"
      }
    }
  ],
  "pagination": {
    "cursor": "aevXXXXXXXXXXXXXX",
    "previous": "aevYYYYYYYYYYYYYY"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `events` | array | Array of audit log event objects |
| `events[].id` | string | Unique event ID (format: `aevXXXXXXXXXXXXXX`) |
| `events[].timestamp` | string | ISO 8601 UTC timestamp when the event occurred |
| `events[].action` | string | The action that was performed (see [Event Types Reference](#event-types-reference)) |
| `events[].actionContext` | string | Context of how the action was triggered (see [Action Contexts](#action-contexts)) |
| `events[].actor` | object | The entity that performed the action |
| `events[].actor.userId` | string | User ID of the actor (if actor is a user) |
| `events[].actor.email` | string | Email of the actor (if actor is a user) |
| `events[].actor.type` | string | Type of actor (see [Actor Types](#actor-types)) |
| `events[].modelId` | string | ID of the resource that was acted upon |
| `events[].modelType` | string | Type of the resource (see [Model Types](#model-types)) |
| `events[].payloadVersion` | string | Version of the event payload schema |
| `events[].context` | object | Additional context about where the action occurred (optional) |
| `events[].context.baseId` | string | Base ID where the action occurred (if applicable) |
| `events[].context.tableId` | string | Table ID where the action occurred (if applicable) |
| `events[].context.viewId` | string | View ID where the action occurred (if applicable) |
| `pagination` | object | Pagination cursors for navigating results |
| `pagination.cursor` | string or null | Cursor for the next page. Null if no more results. |
| `pagination.previous` | string or null | Cursor for the previous page. Null if on the first page. |

### cURL Examples

```bash
# List recent audit events (default: newest first, 100 per page)
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# Filter by date range
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents?startTime=2024-06-01T00:00:00.000Z&endTime=2024-06-30T23:59:59.999Z" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# Filter by event type
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents?eventType=deleteRecord" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# Filter by user
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents?originatingUserId=usrGHI789JKL012" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# Filter by model (specific base)
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents?modelId=appXYZ789" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# Combine multiple filters
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents?startTime=2024-06-01T00:00:00.000Z&endTime=2024-06-30T23:59:59.999Z&eventType=deleteRecord&originatingUserId=usrGHI789JKL012&pageSize=50&sortOrder=asc" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"

# Paginate with cursor
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEvents?cursor=aevXXXXXXXXXXXXXX" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python Examples

```python
import requests, os

enterprise_id = "entABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

# Basic listing
response = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
    headers=headers,
)
response.raise_for_status()
data = response.json()

for event in data["events"]:
    print(f"{event['timestamp']} | {event['action']} | {event['actor']['email']} | {event['modelType']}:{event['modelId']}")

# With filters
response = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
    headers=headers,
    params={
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
        "eventType": "deleteRecord",
        "pageSize": 50,
        "sortOrder": "desc",
    },
)
```

### Required Scope

`enterprise.auditLogs:read`

---

## Create Audit Log Export Request

### Endpoint

```
POST /v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEventRequests
```

### Description

Creates an asynchronous bulk export request for audit log events. Use this instead of paginating through the list endpoint when you need to export a large volume of events (e.g., an entire month or quarter of logs).

The export is processed asynchronously. After creating the request, poll the status endpoint until the export is complete, then download the result from the provided URL.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enterpriseAccountId` | string | Yes | The enterprise account ID (format: `entXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |
| `Content-Type` | `application/json` |

### Request Body Schema

```json
{
  "startTime": "2024-01-01T00:00:00.000Z",
  "endTime": "2024-06-30T23:59:59.999Z",
  "eventTypes": ["createRecord", "updateRecord", "deleteRecord"],
  "sourceIpAddresses": ["192.168.1.0/24", "10.0.0.5"],
  "originatingUserIds": ["usrXXX123", "usrYYY456"]
}
```

### Request Body Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `startTime` | string | Yes | ISO 8601 start timestamp (inclusive). The earliest time for events to include. |
| `endTime` | string | Yes | ISO 8601 end timestamp (inclusive). The latest time for events to include. |
| `eventTypes` | array of strings | No | Filter to specific event types. If omitted, all event types are included. |
| `sourceIpAddresses` | array of strings | No | Filter by source IP addresses. Supports individual IPs and CIDR notation (e.g., `192.168.1.0/24`). |
| `originatingUserIds` | array of strings | No | Filter to events performed by specific user IDs (`usrXXX`). |

### Response Schema

```json
{
  "id": "alrABC123DEF456",
  "state": "pending",
  "createdTime": "2024-07-01T10:00:00.000Z"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique export request ID (format: `alrXXXXXXXXXXXXXX`) |
| `state` | string | Current state of the export request: `pending` |
| `createdTime` | string | ISO 8601 timestamp when the request was created |

### cURL Examples

```bash
# Export all events for a month
curl -X POST "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEventRequests" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "2024-06-01T00:00:00.000Z",
    "endTime": "2024-06-30T23:59:59.999Z"
  }'

# Export only record deletion events
curl -X POST "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEventRequests" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "2024-06-01T00:00:00.000Z",
    "endTime": "2024-06-30T23:59:59.999Z",
    "eventTypes": ["deleteRecord", "deleteTable", "deleteBase"]
  }'

# Export events from specific users and IP ranges
curl -X POST "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEventRequests" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startTime": "2024-06-01T00:00:00.000Z",
    "endTime": "2024-06-30T23:59:59.999Z",
    "originatingUserIds": ["usrXXX123"],
    "sourceIpAddresses": ["192.168.1.0/24"]
  }'
```

### Python Example

```python
import requests, os

enterprise_id = "entABC123DEF456"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

response = requests.post(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests",
    headers=headers,
    json={
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
        "eventTypes": ["createRecord", "updateRecord", "deleteRecord"],
    },
)
response.raise_for_status()
export_request = response.json()
print(f"Export request created: {export_request['id']} (state: {export_request['state']})")
```

### Required Scope

`enterprise.auditLogs:read`

---

## Get Audit Log Export Request Status

### Endpoint

```
GET /v0/meta/enterpriseAccounts/{enterpriseAccountId}/auditLogEventRequests/{requestId}
```

### Description

Check the current status of a previously created audit log export request. Poll this endpoint until the state transitions from `pending` to either `done` or `error`.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enterpriseAccountId` | string | Yes | The enterprise account ID (format: `entXXXXXXXXXXXXXX`) |
| `requestId` | string | Yes | The export request ID (format: `alrXXXXXXXXXXXXXX`) |

### Request Headers

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

### Response Schema (Pending)

```json
{
  "id": "alrABC123DEF456",
  "state": "pending",
  "createdTime": "2024-07-01T10:00:00.000Z"
}
```

### Response Schema (Completed)

```json
{
  "id": "alrABC123DEF456",
  "state": "done",
  "createdTime": "2024-07-01T10:00:00.000Z",
  "downloadUrl": "https://dl.airtable.com/auditlogs/entABC123DEF456/alrABC123DEF456.json.gz",
  "expiresTime": "2024-07-08T10:00:00.000Z"
}
```

### Response Schema (Error)

```json
{
  "id": "alrABC123DEF456",
  "state": "error",
  "createdTime": "2024-07-01T10:00:00.000Z",
  "error": {
    "type": "EXPORT_FAILED",
    "message": "The audit log export could not be completed. Please try again."
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Export request ID (`alrXXX`) |
| `state` | string | Current state: `pending`, `done`, or `error` |
| `createdTime` | string | ISO 8601 timestamp when the request was created |
| `downloadUrl` | string | URL to download the export (present only when `state` is `done`). The file is gzipped JSON. |
| `expiresTime` | string | ISO 8601 timestamp when the download URL expires (present only when `state` is `done`). Typically 7 days after completion. |
| `error` | object | Error details (present only when `state` is `error`) |
| `error.type` | string | Error type code |
| `error.message` | string | Human-readable error message |

### Export Request States

| State | Description | Has downloadUrl | Has error |
|-------|-------------|----------------|-----------|
| `pending` | Export is being generated. May take minutes to hours depending on volume. | No | No |
| `done` | Export is complete and ready for download. | Yes | No |
| `error` | Export failed. The request should be retried. | No | Yes |

### cURL Example

```bash
curl "https://api.airtable.com/v0/meta/enterpriseAccounts/entABC123DEF456/auditLogEventRequests/alrABC123DEF456" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python -- Poll Until Complete

```python
import requests, os, time

enterprise_id = "entABC123DEF456"
request_id = "alrABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

max_attempts = 120  # 120 * 15s = 30 minutes max wait
attempts = 0

while attempts < max_attempts:
    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests/{request_id}",
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()

    state = data["state"]
    print(f"Attempt {attempts + 1}: state = {state}")

    if state == "done":
        print(f"Export ready!")
        print(f"  Download URL: {data['downloadUrl']}")
        print(f"  Expires: {data['expiresTime']}")
        break
    elif state == "error":
        print(f"Export failed: {data.get('error', {}).get('message', 'Unknown error')}")
        break
    else:
        attempts += 1
        time.sleep(15)

if attempts >= max_attempts:
    print("Timed out waiting for export to complete")
```

### Required Scope

`enterprise.auditLogs:read`

---

## Event Object Schema

### Complete Event Object

```json
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
  "payloadVersion": "1.0",
  "context": {
    "baseId": "appXXX789",
    "tableId": "tblXXX012",
    "viewId": "viwXXX345",
    "interfaceId": "intXXX678",
    "workspaceId": "wspXXX901"
  }
}
```

### Event Fields

| Field | Type | Always Present | Description |
|-------|------|---------------|-------------|
| `id` | string | Yes | Unique event ID (`aevXXX`) |
| `timestamp` | string | Yes | ISO 8601 UTC timestamp |
| `action` | string | Yes | The action type (see [Event Types Reference](#event-types-reference)) |
| `actionContext` | string | Yes | How the action was triggered (see [Action Contexts](#action-contexts)) |
| `actor` | object | Yes | Who or what performed the action |
| `modelId` | string | Yes | ID of the affected resource |
| `modelType` | string | Yes | Type of the affected resource (see [Model Types](#model-types)) |
| `payloadVersion` | string | Yes | Schema version for the event payload |
| `context` | object | No | Additional context about where the action occurred. Fields within are optional and depend on the action type. |

---

## Event Types Reference

### Record Events

| Event Type | Description |
|-----------|-------------|
| `createRecord` | A record was created in a table |
| `updateRecord` | One or more fields of a record were updated |
| `deleteRecord` | A record was deleted from a table |
| `restoreRecord` | A previously deleted record was restored |
| `duplicateRecord` | A record was duplicated |

### Field Events

| Event Type | Description |
|-----------|-------------|
| `createField` | A new field (column) was added to a table |
| `updateField` | A field's configuration was modified (name, type, options) |
| `deleteField` | A field was deleted from a table |

### Table Events

| Event Type | Description |
|-----------|-------------|
| `createTable` | A new table was created in a base |
| `updateTable` | A table's metadata was updated (name, description) |
| `deleteTable` | A table was deleted from a base |
| `duplicateTable` | A table was duplicated |

### View Events

| Event Type | Description |
|-----------|-------------|
| `createView` | A new view was created in a table |
| `updateView` | A view's configuration was modified |
| `deleteView` | A view was deleted |
| `lockView` | A view was locked (collaborative views) |
| `unlockView` | A view was unlocked |

### Base Events

| Event Type | Description |
|-----------|-------------|
| `createBase` | A new base was created |
| `deleteBase` | A base was deleted |
| `duplicateBase` | A base was duplicated |
| `updateBase` | A base's metadata was updated (name, color, icon) |
| `moveBase` | A base was moved to a different workspace |
| `restoreBase` | A base was restored from trash |

### Collaborator Events

| Event Type | Description |
|-----------|-------------|
| `addCollaborator` | A collaborator was added to a base or workspace |
| `removeCollaborator` | A collaborator was removed from a base or workspace |
| `updateCollaborator` | A collaborator's permission level was changed |
| `inviteCollaborator` | An invitation was sent to a new collaborator |

### Share Events

| Event Type | Description |
|-----------|-------------|
| `createShare` | A share link was created for a base, view, or form |
| `updateShare` | A share link was enabled, disabled, or modified |
| `deleteShare` | A share link was deleted |
| `accessShare` | A share link was accessed by an external user |

### Authentication Events

| Event Type | Description |
|-----------|-------------|
| `login` | A user logged in to Airtable |
| `logout` | A user logged out of Airtable |
| `loginFailed` | A login attempt failed |
| `passwordChanged` | A user changed their password |
| `twoFactorEnabled` | A user enabled two-factor authentication |
| `twoFactorDisabled` | A user disabled two-factor authentication |

### API Token Events

| Event Type | Description |
|-----------|-------------|
| `createApiToken` | A new personal access token or API key was created |
| `deleteApiToken` | An API token was revoked or deleted |
| `updateApiToken` | An API token's scopes or configuration was updated |

### Automation Events

| Event Type | Description |
|-----------|-------------|
| `createAutomation` | A new automation was created |
| `updateAutomation` | An automation was modified |
| `deleteAutomation` | An automation was deleted |
| `enableAutomation` | An automation was enabled |
| `disableAutomation` | An automation was disabled |
| `runAutomation` | An automation was triggered and ran |

### Workspace Events

| Event Type | Description |
|-----------|-------------|
| `createWorkspace` | A new workspace was created |
| `updateWorkspace` | A workspace was renamed or modified |
| `deleteWorkspace` | A workspace was deleted |

### Enterprise Admin Events

| Event Type | Description |
|-----------|-------------|
| `deactivateUser` | An enterprise admin deactivated a user |
| `reactivateUser` | An enterprise admin reactivated a user |
| `updateUserEmail` | An enterprise admin changed a user's email |
| `claimUser` | An enterprise claimed a user account |
| `unclaimUser` | An enterprise released a claimed user account |

### Interface Events

| Event Type | Description |
|-----------|-------------|
| `createInterface` | A new interface was created |
| `updateInterface` | An interface was modified |
| `deleteInterface` | An interface was deleted |
| `publishInterface` | An interface was published |
| `unpublishInterface` | An interface was unpublished |

---

## Actor Types

| Type | Description | Fields Present |
|------|-------------|---------------|
| `user` | A human user performed the action | `userId`, `email` |
| `automationOwner` | An automation performed the action on behalf of its owner | `userId`, `email` |
| `system` | The Airtable system performed the action (e.g., scheduled cleanup) | None |
| `anonymous` | An unauthenticated user (e.g., form submission via share link) | None |

### Actor Object Examples

**User actor:**
```json
{
  "userId": "usrABC123DEF456",
  "email": "alice@company.com",
  "type": "user"
}
```

**Automation actor:**
```json
{
  "userId": "usrABC123DEF456",
  "email": "alice@company.com",
  "type": "automationOwner"
}
```

**System actor:**
```json
{
  "type": "system"
}
```

**Anonymous actor:**
```json
{
  "type": "anonymous"
}
```

---

## Model Types

| Model Type | Description | ID Format |
|-----------|-------------|-----------|
| `record` | A record within a table | `recXXXXXXXXXXXXXX` |
| `field` | A field (column) within a table | `fldXXXXXXXXXXXXXX` |
| `table` | A table within a base | `tblXXXXXXXXXXXXXX` |
| `view` | A view within a table | `viwXXXXXXXXXXXXXX` |
| `base` | A base (database) | `appXXXXXXXXXXXXXX` |
| `workspace` | A workspace containing bases | `wspXXXXXXXXXXXXXX` |
| `user` | A user account | `usrXXXXXXXXXXXXXX` |
| `share` | A share link | `shrXXXXXXXXXXXXXX` |
| `automation` | An automation within a base | `autXXXXXXXXXXXXXX` |
| `interface` | An interface page | `intXXXXXXXXXXXXXX` |
| `apiToken` | A personal access token | `patXXXXXXXXXXXXXX` |
| `group` | An enterprise group | `grpXXXXXXXXXXXXXX` |

---

## Action Contexts

The `actionContext` field describes how the action was initiated:

| Context | Description |
|---------|-------------|
| `directUserAction` | The user performed the action directly through the Airtable UI |
| `apiRequest` | The action was performed via an API call |
| `automationAction` | An automation triggered the action |
| `syncAction` | The action was performed by Airtable Sync |
| `systemAction` | The Airtable system performed the action automatically |
| `formSubmission` | The action was triggered by a form submission |
| `importAction` | The action was performed as part of a data import |
| `integrationAction` | A third-party integration triggered the action |

---

## Filtering

### Single Filter

Apply one filter at a time to narrow results:

```python
# Filter by event type
params = {"eventType": "deleteRecord"}

# Filter by user
params = {"originatingUserId": "usrABC123DEF456"}

# Filter by time range
params = {
    "startTime": "2024-06-01T00:00:00.000Z",
    "endTime": "2024-06-30T23:59:59.999Z",
}

# Filter by affected model
params = {"modelId": "appABC123DEF456"}
```

### Combined Filters

Multiple filters are combined with AND logic:

```python
# All record deletions by a specific user in June 2024
params = {
    "eventType": "deleteRecord",
    "originatingUserId": "usrABC123DEF456",
    "startTime": "2024-06-01T00:00:00.000Z",
    "endTime": "2024-06-30T23:59:59.999Z",
}
```

### Filter Limitations

- Only one `eventType` can be specified per request. To query multiple event types, make separate requests or use the bulk export endpoint with `eventTypes` (plural, array).
- The `modelId` filter matches the exact model. It does not filter by parent models (e.g., filtering by a base ID will not return events for records within that base).
- Time range filters are inclusive on both `startTime` and `endTime`.

---

## Pagination

### Cursor-Based Pagination

The audit log API uses cursor-based pagination for efficient traversal of large result sets.

### Forward Pagination

```python
import requests, os

enterprise_id = "entABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

all_events = []
cursor = None

while True:
    params = {"pageSize": 100, "sortOrder": "desc"}
    if cursor:
        params["cursor"] = cursor

    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
        headers=headers,
        params=params,
    )
    response.raise_for_status()
    data = response.json()

    events = data["events"]
    all_events.extend(events)
    print(f"Fetched {len(events)} events (total: {len(all_events)})")

    cursor = data.get("pagination", {}).get("cursor")
    if not cursor:
        print("No more pages")
        break

print(f"Total events retrieved: {len(all_events)}")
```

### Backward Pagination

Use the `previous` cursor to navigate backward:

```python
params = {"previous": data["pagination"]["previous"]}
```

### Pagination Best Practices

1. Use a consistent `pageSize` across all pages of the same query.
2. Do not modify filter parameters between pages of the same query.
3. Cursors are opaque strings -- do not attempt to parse or construct them.
4. Cursors may expire after a period of inactivity. If you receive a cursor-related error, restart the query from the beginning.
5. For very large result sets (100k+ events), consider using the bulk export endpoint instead.

---

## Bulk Export Workflow

### Complete Export Workflow

The bulk export follows a three-step process: create, poll, download.

```python
import requests, os, time, gzip, json

enterprise_id = "entABC123DEF456"
headers = {
    "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
    "Content-Type": "application/json",
}

# Step 1: Create export request
print("Creating export request...")
create_resp = requests.post(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests",
    headers=headers,
    json={
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
    },
)
create_resp.raise_for_status()
request_id = create_resp.json()["id"]
print(f"Export request created: {request_id}")

# Step 2: Poll until complete
print("Waiting for export to complete...")
read_headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}
download_url = None

while True:
    status_resp = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEventRequests/{request_id}",
        headers=read_headers,
    )
    status_resp.raise_for_status()
    status = status_resp.json()

    if status["state"] == "done":
        download_url = status["downloadUrl"]
        print(f"Export complete! Expires: {status['expiresTime']}")
        break
    elif status["state"] == "error":
        error_msg = status.get("error", {}).get("message", "Unknown error")
        raise Exception(f"Export failed: {error_msg}")

    print(f"  State: {status['state']}, waiting 15 seconds...")
    time.sleep(15)

# Step 3: Download and process
print("Downloading export...")
download_resp = requests.get(download_url)
download_resp.raise_for_status()

# Decompress gzipped JSON
events_data = json.loads(gzip.decompress(download_resp.content))
print(f"Downloaded {len(events_data)} events")

# Process events
for event in events_data[:5]:  # Print first 5
    print(f"  {event['timestamp']} | {event['action']} | {event['actor'].get('email', 'system')}")
```

### When to Use Bulk Export vs. List Endpoint

| Scenario | Recommended Approach |
|----------|---------------------|
| Recent events (last few hours) | List endpoint with filters |
| Specific event type investigation | List endpoint with `eventType` filter |
| Full month of logs for compliance | Bulk export |
| Quarterly audit report | Bulk export |
| Real-time monitoring | List endpoint with `startTime` set to last check |
| Exporting 100k+ events | Bulk export |

---

## Error Reference

### HTTP Status Codes

| Status | Error Type | Description | Common Cause |
|--------|-----------|-------------|--------------|
| 400 | `BAD_REQUEST` | Malformed request | Invalid JSON, missing required fields in export request |
| 401 | `AUTHENTICATION_REQUIRED` | No valid authentication | Missing or expired token |
| 403 | `NOT_AUTHORIZED` | Insufficient permissions | Token lacks `enterprise.auditLogs:read` scope, or enterprise plan not active |
| 404 | `NOT_FOUND` | Resource not found | Invalid enterprise account ID or export request ID |
| 422 | `INVALID_REQUEST` | Semantically invalid | Invalid timestamp format, `endTime` before `startTime`, invalid event type |
| 429 | `TOO_MANY_REQUESTS` | Rate limit exceeded | Too many requests per second |
| 500 | `SERVER_ERROR` | Internal error | Retry with exponential backoff |

### Error Response Format

```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "The endTime must be after the startTime."
  }
}
```

### Common Error Scenarios

**Invalid time range:**
```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "The endTime must be after the startTime."
  }
}
```

**Invalid event type:**
```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "Unknown event type: 'invalidEventType'. See documentation for valid event types."
  }
}
```

**Enterprise plan not active:**
```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "Enterprise audit log features require an active Enterprise Scale plan."
  }
}
```

**Expired cursor:**
```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "The provided cursor has expired. Please restart your query."
  }
}
```

---

## Common Patterns

### Real-Time Monitoring -- Check for New Events Periodically

```python
import requests, os, time
from datetime import datetime, timezone, timedelta

enterprise_id = "entABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

# Start monitoring from now
last_check = datetime.now(timezone.utc)
check_interval = 60  # Check every 60 seconds

print("Starting audit log monitor...")

while True:
    now = datetime.now(timezone.utc)
    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
        headers=headers,
        params={
            "startTime": last_check.isoformat(),
            "endTime": now.isoformat(),
            "pageSize": 100,
            "sortOrder": "asc",
        },
    )
    response.raise_for_status()
    events = response.json()["events"]

    if events:
        print(f"\n[{now.isoformat()}] Found {len(events)} new event(s):")
        for event in events:
            actor_email = event["actor"].get("email", event["actor"]["type"])
            print(f"  {event['timestamp']} | {event['action']:25s} | {actor_email} | {event['modelType']}:{event['modelId']}")

    last_check = now
    time.sleep(check_interval)
```

### Security Audit -- Find All Login Failures

```python
import requests, os

enterprise_id = "entABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

all_failures = []
cursor = None

while True:
    params = {
        "eventType": "loginFailed",
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
    response.raise_for_status()
    data = response.json()
    all_failures.extend(data["events"])

    cursor = data.get("pagination", {}).get("cursor")
    if not cursor:
        break

print(f"Total failed login attempts: {len(all_failures)}")

# Group by user
from collections import Counter
user_failures = Counter(
    event["actor"].get("email", "unknown") for event in all_failures
)
print("\nFailed logins by user:")
for email, count in user_failures.most_common():
    print(f"  {email}: {count} attempts")
```

### Compliance Report -- Summarize Activity by Action Type

```python
import requests, os
from collections import Counter

enterprise_id = "entABC123DEF456"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

all_events = []
cursor = None

while True:
    params = {
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
        "pageSize": 1000,
    }
    if cursor:
        params["cursor"] = cursor

    response = requests.get(
        f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
        headers=headers,
        params=params,
    )
    response.raise_for_status()
    data = response.json()
    all_events.extend(data["events"])

    cursor = data.get("pagination", {}).get("cursor")
    if not cursor:
        break

print(f"Audit Log Summary: {len(all_events)} total events\n")

# By action type
action_counts = Counter(e["action"] for e in all_events)
print("Events by action:")
for action, count in action_counts.most_common():
    print(f"  {action:30s} {count:>6d}")

# By actor
actor_counts = Counter(e["actor"].get("email", e["actor"]["type"]) for e in all_events)
print("\nTop 10 most active users:")
for email, count in actor_counts.most_common(10):
    print(f"  {email:40s} {count:>6d}")

# By action context
context_counts = Counter(e["actionContext"] for e in all_events)
print("\nEvents by context:")
for context, count in context_counts.most_common():
    print(f"  {context:30s} {count:>6d}")
```

### Track Changes to a Specific Base

```python
import requests, os

enterprise_id = "entABC123DEF456"
target_base_id = "appXXXXXXXXXXXXXX"
headers = {"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"}

response = requests.get(
    f"https://api.airtable.com/v0/meta/enterpriseAccounts/{enterprise_id}/auditLogEvents",
    headers=headers,
    params={
        "modelId": target_base_id,
        "startTime": "2024-06-01T00:00:00.000Z",
        "endTime": "2024-06-30T23:59:59.999Z",
        "pageSize": 100,
    },
)
response.raise_for_status()
events = response.json()["events"]

print(f"Changes to base {target_base_id}:")
for event in events:
    actor_email = event["actor"].get("email", event["actor"]["type"])
    print(f"  {event['timestamp']} | {event['action']} by {actor_email}")
```
