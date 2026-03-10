---
name: airtable-webhooks
description: Create, list, refresh, and delete webhooks for real-time Airtable notifications. Use when user wants to monitor changes in a base, set up real-time data sync, or process webhook payloads. Triggers on "airtable webhook", "create webhook", "list webhooks", "webhook payload", "real-time notifications", "webhook events".
license: MIT
compatibility: Requires AIRTABLE_ACCESS_TOKEN environment variable
metadata:
  author: airtable-skills
  version: "1.0"
---

# Airtable Webhooks API

Set up real-time notifications when data changes in an Airtable base. Webhooks push change events to your server so you can react immediately to record creates, updates, deletes, and schema changes.

> **Auth:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`
> **Base URL:** `https://api.airtable.com/v0`
> **Rate limit:** 5 requests/second per base

## Key Concepts

- **Max 10 webhooks per base** — plan carefully which tables/fields to watch
- **Webhooks expire after 7 days** unless explicitly refreshed via the refresh endpoint
- **Notification URL receives a POST** with a short ping — it does NOT contain the actual payload data
- **Payloads must be fetched separately** via the list-webhook-payloads endpoint using a cursor
- **macSecretBase64** is returned ONLY at creation time — store it immediately for HMAC validation

## Quick Start

### Create a Webhook + Fetch Payloads

```python
import requests, os, time

token = os.environ["AIRTABLE_ACCESS_TOKEN"]
base_id = "appABC123"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# Step 1: Create webhook
webhook_resp = requests.post(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks",
    headers=headers,
    json={
        "notificationUrl": "https://example.com/airtable-webhook",
        "specification": {
            "options": {
                "filters": {
                    "dataTypes": ["tableData"],
                    "recordChangeScope": "tblXYZ789",
                }
            }
        },
    },
)
webhook = webhook_resp.json()
webhook_id = webhook["id"]
mac_secret_base64 = webhook["macSecretBase64"]  # SAVE THIS — only returned once
cursor = webhook["cursorForNextPayload"]

print(f"Webhook created: {webhook_id}")
print(f"Expires: {webhook['expirationTime']}")
print(f"MAC secret: {mac_secret_base64}")

# Step 2: Poll for payloads (after changes occur)
payloads_resp = requests.get(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads",
    headers={"Authorization": f"Bearer {token}"},
    params={"cursor": cursor},
)
data = payloads_resp.json()
for payload in data.get("payloads", []):
    print(f"Change at {payload['timestamp']}: {payload['changedTablesById']}")

# Update cursor for next poll
if data.get("cursor"):
    cursor = data["cursor"]
```

### cURL — Create a Webhook

```bash
curl -X POST "https://api.airtable.com/v0/bases/{baseId}/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notificationUrl": "https://example.com/airtable-webhook",
    "specification": {
      "options": {
        "filters": {
          "dataTypes": ["tableData"],
          "recordChangeScope": "tblXYZ789"
        }
      }
    }
  }'
```

## Endpoints

### 1. List Webhooks

**`GET /v0/bases/{baseId}/webhooks`**

Returns all webhooks registered on a base.

**cURL:**

```bash
curl "https://api.airtable.com/v0/bases/{baseId}/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
webhooks = response.json()["webhooks"]
for wh in webhooks:
    print(f"{wh['id']}: enabled={wh['isHookEnabled']}, expires={wh['expirationTime']}")
```

**Response:**

```json
{
  "webhooks": [
    {
      "id": "ach00000000000001",
      "type": "client",
      "notificationUrl": "https://example.com/airtable-webhook",
      "cursorForNextPayload": 1,
      "isHookEnabled": true,
      "areNotificationsEnabled": true,
      "expirationTime": "2024-01-22T10:30:00.000Z",
      "specification": {
        "options": {
          "filters": {
            "dataTypes": ["tableData"],
            "recordChangeScope": "tblXYZ789"
          }
        }
      }
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Webhook ID (achXXX) |
| `type` | string | Always `"client"` for user-created webhooks |
| `notificationUrl` | string | URL that receives POST pings (null if not set) |
| `specification` | object | Filter configuration |
| `cursorForNextPayload` | integer | Cursor to use when fetching payloads |
| `isHookEnabled` | boolean | Whether the webhook is active |
| `expirationTime` | string | ISO 8601 timestamp when webhook expires |
| `areNotificationsEnabled` | boolean | Whether POST notifications are being sent |

### 2. Create a Webhook

**`POST /v0/bases/{baseId}/webhooks`**

Register a new webhook on a base. Returns a `macSecretBase64` that is ONLY available at creation time.

**Request Body:**

```json
{
  "notificationUrl": "https://example.com/airtable-webhook",
  "specification": {
    "options": {
      "filters": {
        "dataTypes": ["tableData"],
        "recordChangeScope": "tblXYZ789",
        "watchDataInFieldIds": ["fldABC123", "fldDEF456"],
        "watchSchemasOfFieldIds": ["fldABC123"]
      }
    }
  }
}
```

**Specification Filters:**

| Filter | Type | Description |
|--------|------|-------------|
| `dataTypes` | array | Types of changes to watch: `"tableData"`, `"tableFields"`, `"tableMetadata"` |
| `recordChangeScope` | string | Table ID (`tblXXX`) or view ID (`viwXXX`) to scope record changes |
| `watchDataInFieldIds` | array | Specific field IDs — only trigger on changes to these fields' cell values |
| `watchSchemasOfFieldIds` | array | Specific field IDs — only trigger on schema changes to these fields |

- `dataTypes`: `"tableData"` watches record cell value changes, `"tableFields"` watches field create/update/delete, `"tableMetadata"` watches table name/description changes
- `notificationUrl` is optional — you can poll for payloads without receiving push notifications
- `recordChangeScope` scoped to a view will only report changes for records visible in that view

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/bases/{baseId}/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notificationUrl": "https://example.com/airtable-webhook",
    "specification": {
      "options": {
        "filters": {
          "dataTypes": ["tableData", "tableFields"],
          "recordChangeScope": "tblXYZ789"
        }
      }
    }
  }'
```

**Response:**

```json
{
  "id": "ach00000000000001",
  "macSecretBase64": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
  "cursorForNextPayload": 1,
  "expirationTime": "2024-01-22T10:30:00.000Z"
}
```

**IMPORTANT:** `macSecretBase64` is returned **only** on creation. Save it immediately — you will need it to validate incoming webhook notifications via HMAC-SHA256.

### 3. List Webhook Payloads

**`GET /v0/bases/{baseId}/webhooks/{webhookId}/payloads`**

Fetch the actual change data for a webhook. Payloads are paginated using a cursor.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `cursor` | integer | Start position — use `cursorForNextPayload` from webhook or `cursor` from previous payload response |

**cURL:**

```bash
curl "https://api.airtable.com/v0/bases/{baseId}/webhooks/{webhookId}/payloads?cursor=1" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.get(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
    params={"cursor": cursor},
)
data = response.json()
for payload in data.get("payloads", []):
    print(f"Transaction #{payload['baseTransactionNumber']} at {payload['timestamp']}")
    for table_id, changes in payload.get("changedTablesById", {}).items():
        if "createdRecordsById" in changes:
            print(f"  Created {len(changes['createdRecordsById'])} records in {table_id}")
        if "changedRecordsById" in changes:
            print(f"  Changed {len(changes['changedRecordsById'])} records in {table_id}")
        if "destroyedRecordIds" in changes:
            print(f"  Deleted {len(changes['destroyedRecordIds'])} records in {table_id}")
```

**Response:**

```json
{
  "cursor": 5,
  "mightHaveMore": false,
  "payloads": [
    {
      "timestamp": "2024-01-15T10:30:00.000Z",
      "baseTransactionNumber": 42,
      "payloadFormat": "v0",
      "actionMetadata": {
        "source": "client",
        "sourceMetadata": {
          "user": {
            "id": "usrABC123",
            "email": "user@example.com",
            "name": "Jane Doe"
          }
        }
      },
      "changedTablesById": {
        "tblXYZ789": {
          "changedRecordsById": {
            "recDEF456": {
              "current": {
                "cellValuesByFieldId": {
                  "fldABC123": "Updated Value"
                }
              },
              "previous": {
                "cellValuesByFieldId": {
                  "fldABC123": "Old Value"
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

- If `mightHaveMore` is `true`, call again with the returned `cursor` to get more payloads
- `actionMetadata.source` can be `"client"` (UI), `"publicApi"`, `"formSubmission"`, `"automation"`, or `"system"`

### 4. Refresh a Webhook

**`POST /v0/bases/{baseId}/webhooks/{webhookId}/refresh`**

Extend the webhook expiration by 7 days from now. Must be called before the webhook expires.

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/bases/{baseId}/webhooks/{webhookId}/refresh" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.post(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/refresh",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
new_expiration = response.json()["expirationTime"]
print(f"Webhook refreshed, new expiration: {new_expiration}")
```

**Response:**

```json
{
  "expirationTime": "2024-01-29T10:30:00.000Z"
}
```

### 5. Enable Notifications

**`POST /v0/bases/{baseId}/webhooks/{webhookId}/enableNotifications`**

Re-enable POST notifications for a webhook that had notifications disabled.

**cURL:**

```bash
curl -X POST "https://api.airtable.com/v0/bases/{baseId}/webhooks/{webhookId}/enableNotifications" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Note:** Notifications may be automatically disabled if your notification URL returns errors repeatedly. Use this endpoint to re-enable them.

### 6. Delete a Webhook

**`DELETE /v0/bases/{baseId}/webhooks/{webhookId}`**

Permanently remove a webhook. No response body on success (HTTP 200).

**cURL:**

```bash
curl -X DELETE "https://api.airtable.com/v0/bases/{baseId}/webhooks/{webhookId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

**Python:**

```python
response = requests.delete(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
if response.status_code == 200:
    print("Webhook deleted successfully")
```

## Common Patterns

### Poll for Changes (Without Notification URL)

You can create a webhook without a `notificationUrl` and poll the payloads endpoint on a schedule:

```python
import time

def poll_webhook(base_id, webhook_id, cursor, token):
    """Poll for new webhook payloads and process changes."""
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        response = requests.get(
            f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads",
            headers=headers,
            params={"cursor": cursor},
        )
        data = response.json()

        for payload in data.get("payloads", []):
            process_payload(payload)

        cursor = data.get("cursor", cursor)

        if not data.get("mightHaveMore"):
            time.sleep(30)  # wait before next poll
```

### Webhook Refresh Loop

Keep a webhook alive indefinitely by refreshing it on a schedule:

```python
import threading

def refresh_loop(base_id, webhook_id, token, interval_hours=24):
    """Refresh a webhook every N hours to prevent expiration."""
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        time.sleep(interval_hours * 3600)
        response = requests.post(
            f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/refresh",
            headers=headers,
        )
        if response.status_code == 200:
            exp = response.json()["expirationTime"]
            print(f"Webhook refreshed, expires: {exp}")
        else:
            print(f"Refresh failed: {response.status_code}")

# Run in background thread
thread = threading.Thread(
    target=refresh_loop,
    args=(base_id, webhook_id, token),
    daemon=True,
)
thread.start()
```

### Validate Webhook Signatures (HMAC-SHA256)

When Airtable sends a POST to your `notificationUrl`, it includes an `X-Airtable-Content-MAC` header. Validate it using the `macSecretBase64` from webhook creation:

```python
import hmac, hashlib, base64

def validate_webhook_signature(mac_secret_base64, request_body_bytes, received_mac_header):
    """Validate that a webhook notification actually came from Airtable."""
    mac_secret = base64.b64decode(mac_secret_base64)
    computed = hmac.new(mac_secret, request_body_bytes, hashlib.sha256).hexdigest()
    is_valid = hmac.compare_digest(computed, received_mac_header)
    return is_valid

# Flask example
from flask import Flask, request

app = Flask(__name__)
MAC_SECRET_BASE64 = "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo="  # saved from creation

@app.route("/airtable-webhook", methods=["POST"])
def handle_webhook():
    mac_header = request.headers.get("X-Airtable-Content-MAC", "")
    if not validate_webhook_signature(MAC_SECRET_BASE64, request.data, mac_header):
        return "Invalid signature", 401

    # Notification received — now fetch the actual payloads
    # The POST body is just a ping, not the full payload
    fetch_and_process_payloads()
    return "OK", 200
```

### Watch Specific Fields Only

Create a webhook that only fires when specific fields change:

```python
response = requests.post(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks",
    headers=headers,
    json={
        "notificationUrl": "https://example.com/webhook",
        "specification": {
            "options": {
                "filters": {
                    "dataTypes": ["tableData"],
                    "recordChangeScope": "tblXYZ789",
                    "watchDataInFieldIds": ["fldSTATUS", "fldPRIORITY"],
                }
            }
        },
    },
)
```

## Required Scopes

| Endpoint | Required Scope |
|----------|---------------|
| List webhooks | `webhook:manage` |
| Create webhook | `webhook:manage` |
| List webhook payloads | `webhook:manage` |
| Refresh webhook | `webhook:manage` |
| Delete webhook | `webhook:manage` |

All webhook operations require the `webhook:manage` scope on the personal access token.

## Error Handling

| Status | Error Type | Meaning |
|--------|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | Missing or invalid token |
| 403 | `NOT_AUTHORIZED` | Token lacks `webhook:manage` scope |
| 404 | `NOT_FOUND` | Invalid base ID or webhook ID |
| 422 | `INVALID_REQUEST` | Invalid specification, filters, or notification URL |
| 422 | `WEBHOOK_LIMIT_REACHED` | Base already has 10 webhooks — delete one first |
| 429 | `TOO_MANY_REQUESTS` | Rate limited — retry after backoff |

## References

For complete request/response schemas, payload formats, and filter details, see [references/webhooks-api.md](references/webhooks-api.md).
