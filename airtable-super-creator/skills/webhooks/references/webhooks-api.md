# Airtable Webhooks API — Complete Reference

Full request/response schemas, payload formats, filter configurations, HMAC validation, and cursor behavior for the Airtable Webhooks API.

> **Base URL:** `https://api.airtable.com/v0`
> **Required Scope:** `webhook:manage` for all endpoints
> **Auth Header:** `Authorization: Bearer $AIRTABLE_ACCESS_TOKEN`

---

## Table of Contents

1. [Webhooks Overview](#webhooks-overview)
2. [List Webhooks](#1-list-webhooks)
3. [Create a Webhook](#2-create-a-webhook)
4. [List Webhook Payloads](#3-list-webhook-payloads)
5. [Refresh a Webhook](#4-refresh-a-webhook)
6. [Delete a Webhook](#5-delete-a-webhook)
7. [Webhook Specification Filters](#webhook-specification-filters)
8. [Payload Format — changedTablesById](#payload-format--changedtablesbyid)
9. [Action Metadata](#action-metadata)
10. [Cursor Behavior](#cursor-behavior)
11. [HMAC Signature Validation](#hmac-signature-validation)
12. [Webhook Lifecycle and Expiration](#webhook-lifecycle-and-expiration)
13. [Notification POST Body](#notification-post-body)
14. [Error Responses](#error-responses)
15. [Rate Limits and Quotas](#rate-limits-and-quotas)

---

## Webhooks Overview

Webhooks provide real-time change tracking for Airtable bases. When data or schema changes occur in a base, the webhook system records payloads that describe exactly what changed. Optionally, Airtable sends a lightweight POST notification to a URL you specify, signaling that new payloads are available.

**Key characteristics:**

- Maximum **10 webhooks per base**
- Webhooks **expire after 7 days** from creation (or last refresh)
- The notification POST is a **ping only** — it does not contain full change data
- Full change data must be retrieved via the **List Webhook Payloads** endpoint
- The `macSecretBase64` for HMAC validation is returned **only at creation time**
- Payloads are retained for **7 days** after the webhook event occurs
- Webhook payloads are **ordered** by `baseTransactionNumber`

---

## 1. List Webhooks

### Request

```
GET /v0/bases/{baseId}/webhooks
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (appXXX) |

**Headers:**

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

### Response

**Status:** `200 OK`

```json
{
  "webhooks": [
    {
      "id": "ach00000000000001",
      "type": "client",
      "notificationUrl": "https://example.com/airtable-webhook",
      "cursorForNextPayload": 14,
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
    },
    {
      "id": "ach00000000000002",
      "type": "client",
      "notificationUrl": null,
      "cursorForNextPayload": 1,
      "isHookEnabled": true,
      "areNotificationsEnabled": false,
      "expirationTime": "2024-01-25T08:00:00.000Z",
      "specification": {
        "options": {
          "filters": {
            "dataTypes": ["tableData", "tableFields", "tableMetadata"]
          }
        }
      }
    }
  ]
}
```

### Response Schema

**Top-level object:**

| Field | Type | Description |
|-------|------|-------------|
| `webhooks` | array | Array of webhook objects |

**Webhook object:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | Unique webhook ID (achXXX format) |
| `type` | string | No | Always `"client"` for user-created webhooks |
| `notificationUrl` | string | Yes | URL receiving POST pings. `null` if polling-only |
| `cursorForNextPayload` | integer | No | Starting cursor for fetching new payloads |
| `isHookEnabled` | boolean | No | `false` if webhook has been disabled (e.g., too many notification failures) |
| `areNotificationsEnabled` | boolean | No | `false` if notification delivery has been disabled due to repeated failures |
| `expirationTime` | string | No | ISO 8601 UTC timestamp when webhook expires |
| `specification` | object | No | The filter configuration for this webhook |

**Specification object:**

| Field | Type | Description |
|-------|------|-------------|
| `options` | object | Contains filter configuration |
| `options.filters` | object | Defines which changes this webhook tracks |

---

## 2. Create a Webhook

### Request

```
POST /v0/bases/{baseId}/webhooks
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (appXXX) |

**Headers:**

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |
| `Content-Type` | `application/json` |

### Request Body Schema

```json
{
  "notificationUrl": "https://example.com/airtable-webhook",
  "specification": {
    "options": {
      "filters": {
        "dataTypes": ["tableData", "tableFields"],
        "recordChangeScope": "tblXYZ789",
        "watchDataInFieldIds": ["fldABC123", "fldDEF456"],
        "watchSchemasOfFieldIds": ["fldABC123"]
      }
    }
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `notificationUrl` | string | No | HTTPS URL to receive POST notifications. Omit for polling-only mode |
| `specification` | object | Yes | Webhook configuration |
| `specification.options` | object | Yes | Options container |
| `specification.options.filters` | object | Yes | Filter configuration (see [Webhook Specification Filters](#webhook-specification-filters)) |

**notificationUrl requirements:**

- Must use HTTPS protocol
- Must be publicly reachable
- Must respond with 2xx status within 10 seconds
- If the URL fails to respond repeatedly, `areNotificationsEnabled` will be set to `false`

### Response

**Status:** `200 OK`

```json
{
  "id": "ach00000000000001",
  "macSecretBase64": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
  "cursorForNextPayload": 1,
  "expirationTime": "2024-01-22T10:30:00.000Z"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique webhook ID (achXXX format) |
| `macSecretBase64` | string | Base64-encoded HMAC secret for validating notifications. **ONLY returned at creation time — store it immediately** |
| `cursorForNextPayload` | integer | Initial cursor value (typically `1`) |
| `expirationTime` | string | ISO 8601 UTC timestamp — 7 days from creation |

### cURL Example — Full Specification

```bash
curl -X POST "https://api.airtable.com/v0/bases/appABC123/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notificationUrl": "https://example.com/airtable-webhook",
    "specification": {
      "options": {
        "filters": {
          "dataTypes": ["tableData", "tableFields"],
          "recordChangeScope": "tblXYZ789",
          "watchDataInFieldIds": ["fldABC123", "fldDEF456"],
          "watchSchemasOfFieldIds": ["fldABC123"]
        }
      }
    }
  }'
```

### cURL Example — Minimal (Polling-Only, All Changes)

```bash
curl -X POST "https://api.airtable.com/v0/bases/appABC123/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "specification": {
      "options": {
        "filters": {
          "dataTypes": ["tableData"]
        }
      }
    }
  }'
```

### Python Example

```python
import requests, os, json

response = requests.post(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks",
    headers={
        "Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "notificationUrl": "https://example.com/airtable-webhook",
        "specification": {
            "options": {
                "filters": {
                    "dataTypes": ["tableData"],
                    "recordChangeScope": table_id,
                    "watchDataInFieldIds": [status_field_id, priority_field_id],
                }
            }
        },
    },
)
webhook = response.json()

# CRITICAL: Save macSecretBase64 — it is NEVER returned again
with open("webhook_secret.json", "w") as f:
    json.dump({
        "webhook_id": webhook["id"],
        "mac_secret_base64": webhook["macSecretBase64"],
        "cursor": webhook["cursorForNextPayload"],
    }, f)
```

---

## 3. List Webhook Payloads

### Request

```
GET /v0/bases/{baseId}/webhooks/{webhookId}/payloads
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (appXXX) |
| `webhookId` | string | Yes | The ID of the webhook (achXXX) |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cursor` | integer | No | Payload cursor position. Use `cursorForNextPayload` from webhook creation or from a previous payloads response. Defaults to 1 if omitted |

**Headers:**

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

### Response

**Status:** `200 OK`

```json
{
  "cursor": 5,
  "mightHaveMore": true,
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
          "createdRecordsById": {
            "recNEW001": {
              "createdTime": "2024-01-15T10:30:00.000Z",
              "cellValuesByFieldId": {
                "fldABC123": "New Task",
                "fldDEF456": "Active"
              }
            }
          },
          "changedRecordsById": {
            "recOLD002": {
              "current": {
                "cellValuesByFieldId": {
                  "fldDEF456": "Completed"
                }
              },
              "previous": {
                "cellValuesByFieldId": {
                  "fldDEF456": "In Progress"
                }
              }
            }
          },
          "destroyedRecordIds": ["recDEL003"]
        }
      }
    },
    {
      "timestamp": "2024-01-15T10:31:00.000Z",
      "baseTransactionNumber": 43,
      "payloadFormat": "v0",
      "actionMetadata": {
        "source": "publicApi",
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
          "changedFieldsById": {
            "fldABC123": {
              "current": {
                "name": "Task Title",
                "type": "singleLineText"
              },
              "previous": {
                "name": "Task Name"
              }
            }
          }
        }
      }
    }
  ]
}
```

### Response Schema

**Top-level object:**

| Field | Type | Description |
|-------|------|-------------|
| `cursor` | integer | Cursor to use in the next request to get subsequent payloads |
| `mightHaveMore` | boolean | `true` if there may be additional payloads after this batch |
| `payloads` | array | Array of payload objects (may be empty if no new changes) |

**Payload object:**

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | ISO 8601 UTC timestamp of when the change occurred |
| `baseTransactionNumber` | integer | Monotonically increasing transaction number for ordering |
| `payloadFormat` | string | Always `"v0"` currently |
| `actionMetadata` | object | Information about what triggered the change |
| `changedTablesById` | object | Map of table ID to table change object (see [Payload Format](#payload-format--changedtablesbyid)) |

### cURL Example

```bash
curl "https://api.airtable.com/v0/bases/appABC123/webhooks/ach00000000000001/payloads?cursor=1" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python — Paginate Through All Payloads

```python
import requests, os

def fetch_all_payloads(base_id, webhook_id, cursor, token):
    """Fetch all available payloads starting from cursor."""
    headers = {"Authorization": f"Bearer {token}"}
    all_payloads = []

    while True:
        response = requests.get(
            f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads",
            headers=headers,
            params={"cursor": cursor},
        )
        response.raise_for_status()
        data = response.json()

        all_payloads.extend(data.get("payloads", []))
        cursor = data["cursor"]

        if not data.get("mightHaveMore"):
            break

    return all_payloads, cursor
```

---

## 4. Refresh a Webhook

### Request

```
POST /v0/bases/{baseId}/webhooks/{webhookId}/refresh
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (appXXX) |
| `webhookId` | string | Yes | The ID of the webhook (achXXX) |

**Headers:**

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

**Request Body:** None required.

### Response

**Status:** `200 OK`

```json
{
  "expirationTime": "2024-01-29T10:30:00.000Z"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `expirationTime` | string | New ISO 8601 UTC expiration timestamp — 7 days from now |

### cURL Example

```bash
curl -X POST "https://api.airtable.com/v0/bases/appABC123/webhooks/ach00000000000001/refresh" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python Example

```python
import requests, os

response = requests.post(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/refresh",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
response.raise_for_status()
print(f"New expiration: {response.json()['expirationTime']}")
```

---

## 5. Delete a Webhook

### Request

```
DELETE /v0/bases/{baseId}/webhooks/{webhookId}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `baseId` | string | Yes | The ID of the base (appXXX) |
| `webhookId` | string | Yes | The ID of the webhook (achXXX) |

**Headers:**

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer $AIRTABLE_ACCESS_TOKEN` |

**Request Body:** None.

### Response

**Status:** `200 OK`

No response body. An HTTP 200 status indicates success.

### cURL Example

```bash
curl -X DELETE "https://api.airtable.com/v0/bases/appABC123/webhooks/ach00000000000001" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN"
```

### Python Example

```python
import requests, os

response = requests.delete(
    f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}",
    headers={"Authorization": f"Bearer {os.environ['AIRTABLE_ACCESS_TOKEN']}"},
)
response.raise_for_status()
print("Webhook deleted successfully")
```

---

## Webhook Specification Filters

The `specification.options.filters` object controls which changes a webhook tracks. All filter fields are optional except `dataTypes`.

### Filter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dataTypes` | array of strings | Yes | Types of changes to watch |
| `recordChangeScope` | string | No | Restrict record changes to a specific table or view |
| `watchDataInFieldIds` | array of strings | No | Only report cell value changes for these specific fields |
| `watchSchemasOfFieldIds` | array of strings | No | Only report schema changes for these specific fields |

### dataTypes Values

| Value | Description | Changes Tracked |
|-------|-------------|-----------------|
| `"tableData"` | Record cell value changes | `createdRecordsById`, `changedRecordsById`, `destroyedRecordIds` in payload |
| `"tableFields"` | Field schema changes | `createdFieldsById`, `changedFieldsById`, `destroyedFieldIds` in payload |
| `"tableMetadata"` | Table-level metadata changes | `changedMetadata` in payload (table name, description changes) |

You can combine multiple data types:

```json
{
  "dataTypes": ["tableData", "tableFields", "tableMetadata"]
}
```

### recordChangeScope

Restricts which records are tracked for `tableData` changes.

| Value | Effect |
|-------|--------|
| Table ID (`tblXXX`) | Track changes to all records in that specific table |
| View ID (`viwXXX`) | Track changes only to records currently visible in that view |
| Omitted | Track changes to records in ALL tables in the base |

**View-scoped behavior:**
- If a record enters the view (e.g., its field values now match the view's filter), it appears as a `createdRecordsById` entry
- If a record leaves the view (e.g., its field values no longer match), it appears as a `destroyedRecordIds` entry
- Actual record changes while visible in the view appear in `changedRecordsById`

### watchDataInFieldIds

When specified, the webhook only reports cell value changes for the listed field IDs. Other field changes are silently ignored.

```json
{
  "dataTypes": ["tableData"],
  "recordChangeScope": "tblXYZ789",
  "watchDataInFieldIds": ["fldSTATUS", "fldPRIORITY", "fldASSIGNEE"]
}
```

**Behavior notes:**
- Only cell values for the specified fields appear in `cellValuesByFieldId`
- Record creation and deletion events are still reported, but only include values for watched fields
- If a record change only affects non-watched fields, no payload is generated

### watchSchemasOfFieldIds

When specified, the webhook only reports field schema changes (rename, type change, option changes) for the listed field IDs.

```json
{
  "dataTypes": ["tableFields"],
  "watchSchemasOfFieldIds": ["fldSTATUS", "fldPRIORITY"]
}
```

### Complete Filter Examples

**Watch all record changes in one table:**

```json
{
  "dataTypes": ["tableData"],
  "recordChangeScope": "tblXYZ789"
}
```

**Watch specific fields in a specific view:**

```json
{
  "dataTypes": ["tableData"],
  "recordChangeScope": "viwABC123",
  "watchDataInFieldIds": ["fldSTATUS", "fldDUE_DATE"]
}
```

**Watch everything — records, fields, and metadata across all tables:**

```json
{
  "dataTypes": ["tableData", "tableFields", "tableMetadata"]
}
```

**Watch record data and field schema changes for specific fields:**

```json
{
  "dataTypes": ["tableData", "tableFields"],
  "recordChangeScope": "tblXYZ789",
  "watchDataInFieldIds": ["fldSTATUS"],
  "watchSchemasOfFieldIds": ["fldSTATUS"]
}
```

---

## Payload Format — changedTablesById

The `changedTablesById` object in each payload maps table IDs to their respective changes. The structure depends on which `dataTypes` the webhook is configured to watch.

### Top-Level Structure

```json
{
  "changedTablesById": {
    "tblXYZ789": {
      "createdRecordsById": { ... },
      "changedRecordsById": { ... },
      "destroyedRecordIds": [ ... ],
      "createdFieldsById": { ... },
      "changedFieldsById": { ... },
      "destroyedFieldIds": [ ... ],
      "changedMetadata": { ... }
    }
  }
}
```

All sub-keys are optional — only present when relevant changes occurred.

### createdRecordsById (dataType: tableData)

Map of record ID to created record data.

```json
{
  "createdRecordsById": {
    "recNEW001": {
      "createdTime": "2024-01-15T10:30:00.000Z",
      "cellValuesByFieldId": {
        "fldABC123": "Task Title",
        "fldDEF456": "Active",
        "fldGHI789": 42
      }
    },
    "recNEW002": {
      "createdTime": "2024-01-15T10:30:01.000Z",
      "cellValuesByFieldId": {
        "fldABC123": "Another Task",
        "fldDEF456": "Pending"
      }
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `createdTime` | string | ISO 8601 timestamp of record creation |
| `cellValuesByFieldId` | object | Map of field ID to cell value at creation time |

**Cell value types in cellValuesByFieldId:**

| Airtable Field Type | JSON Value Type | Example |
|---------------------|-----------------|---------|
| Single line text | string | `"Hello"` |
| Number | number | `42` |
| Checkbox | boolean | `true` |
| Single select | object | `{"id": "selABC", "name": "Active", "color": "greenLight2"}` |
| Multiple select | array of objects | `[{"id": "selABC", "name": "Tag1"}]` |
| Date | string | `"2024-01-15"` |
| Date with time | string | `"2024-01-15T10:30:00.000Z"` |
| Collaborator | object | `{"id": "usrABC", "email": "user@example.com", "name": "Jane"}` |
| Attachment | array of objects | `[{"id": "attABC", "url": "https://...", "filename": "file.pdf"}]` |
| Link to another record | array of strings | `["recABC", "recDEF"]` |
| Rich text | string | `"Hello **world**"` |
| URL | string | `"https://example.com"` |
| Email | string | `"user@example.com"` |
| Phone | string | `"+1-555-0100"` |
| Currency | number | `19.99` |
| Percent | number | `0.75` |
| Duration | number | `3600` (seconds) |
| Rating | number | `4` |
| Barcode | object | `{"text": "ABC123"}` |

### changedRecordsById (dataType: tableData)

Map of record ID to change details, showing `current` and `previous` values.

```json
{
  "changedRecordsById": {
    "recOLD002": {
      "current": {
        "cellValuesByFieldId": {
          "fldDEF456": "Completed",
          "fldGHI789": 100
        }
      },
      "previous": {
        "cellValuesByFieldId": {
          "fldDEF456": "In Progress",
          "fldGHI789": 50
        }
      }
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `current` | object | Contains `cellValuesByFieldId` with new values |
| `previous` | object | Contains `cellValuesByFieldId` with old values |
| `current.cellValuesByFieldId` | object | Field ID to new cell value |
| `previous.cellValuesByFieldId` | object | Field ID to previous cell value |

**Notes:**
- Only changed fields appear in `cellValuesByFieldId` — unchanged fields are omitted
- If a field was empty before, it will not appear in `previous.cellValuesByFieldId`
- If a field was cleared, its value in `current.cellValuesByFieldId` will be `null`
- When `unchanged` is present instead of `previous`, it means the record was changed but no previous value information is available (e.g., webhook was created after the record)

### destroyedRecordIds (dataType: tableData)

Array of record IDs that were deleted.

```json
{
  "destroyedRecordIds": ["recDEL003", "recDEL004", "recDEL005"]
}
```

### createdFieldsById (dataType: tableFields)

Map of field ID to the new field's configuration.

```json
{
  "createdFieldsById": {
    "fldNEW001": {
      "name": "Priority",
      "type": "singleSelect"
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name of the new field |
| `type` | string | Airtable field type identifier |

### changedFieldsById (dataType: tableFields)

Map of field ID to field schema changes, with `current` and `previous` values.

```json
{
  "changedFieldsById": {
    "fldABC123": {
      "current": {
        "name": "Task Title",
        "type": "singleLineText"
      },
      "previous": {
        "name": "Task Name"
      }
    },
    "fldDEF456": {
      "current": {
        "type": "singleSelect"
      },
      "previous": {
        "type": "singleLineText"
      }
    }
  }
}
```

**Field change properties:**

| Property | Appears in `current` | Appears in `previous` | Description |
|----------|---------------------|-----------------------|-------------|
| `name` | When name changed | Previous name | Field display name |
| `type` | When type changed | Previous type (`previousFieldType`) | Airtable field type |

**Field type change (`currentFieldType` / `previousFieldType`):**
When a field's type is converted, the payload shows both the new and old types. For example, converting a `singleLineText` to `singleSelect`:

```json
{
  "changedFieldsById": {
    "fldDEF456": {
      "current": {
        "type": "singleSelect"
      },
      "previous": {
        "type": "singleLineText"
      }
    }
  }
}
```

### destroyedFieldIds (dataType: tableFields)

Array of field IDs that were deleted.

```json
{
  "destroyedFieldIds": ["fldOLD001", "fldOLD002"]
}
```

### changedMetadata (dataType: tableMetadata)

Changes to table-level metadata (name, description).

```json
{
  "changedMetadata": {
    "current": {
      "name": "Project Tasks",
      "description": "Updated description for task tracking"
    },
    "previous": {
      "name": "Tasks",
      "description": "Task tracking table"
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `current.name` | string | New table name (if changed) |
| `current.description` | string | New table description (if changed) |
| `previous.name` | string | Previous table name |
| `previous.description` | string | Previous table description |

### changedViewsById (dataType: tableData with view-scoped recordChangeScope)

When a webhook is scoped to a view, additional view change information may appear:

```json
{
  "changedViewsById": {
    "viwABC123": {
      "changedRecordsById": {
        "recMOVED001": {
          "current": {
            "cellValuesByFieldId": {
              "fldSTATUS": "Active"
            }
          },
          "previous": {
            "cellValuesByFieldId": {
              "fldSTATUS": "Archived"
            }
          }
        }
      },
      "createdRecordsById": {
        "recENTERED002": {
          "createdTime": "2024-01-15T10:30:00.000Z",
          "cellValuesByFieldId": {
            "fldSTATUS": "Active"
          }
        }
      },
      "destroyedRecordIds": ["recLEFT003"]
    }
  }
}
```

---

## Action Metadata

Every payload includes `actionMetadata` describing what triggered the change.

### Structure

```json
{
  "actionMetadata": {
    "source": "client",
    "sourceMetadata": {
      "user": {
        "id": "usrABC123",
        "email": "user@example.com",
        "name": "Jane Doe"
      }
    }
  }
}
```

### Source Values

| Source | Description |
|--------|-------------|
| `"client"` | Change made via Airtable web UI or mobile app |
| `"publicApi"` | Change made via REST API |
| `"formSubmission"` | Record created via a shared form |
| `"automation"` | Change triggered by an Airtable automation |
| `"system"` | System-level change (e.g., computed field recalculation) |
| `"sync"` | Change from Airtable Sync |
| `"anonymousUser"` | Change by an anonymous user (e.g., shared view) |

### sourceMetadata

| Field | Type | Present When |
|-------|------|-------------|
| `user` | object | Present for `client`, `publicApi`, `automation` sources |
| `user.id` | string | Always present in user object |
| `user.email` | string | Always present in user object |
| `user.name` | string | Always present in user object |

---

## Cursor Behavior

Cursors are integers that track your position in the webhook's payload stream.

### How Cursors Work

1. When you **create a webhook**, you receive `cursorForNextPayload` (typically `1`)
2. When you **list payloads** with a cursor, the response includes a new `cursor` value
3. Use the response's `cursor` value in your next request to get subsequent payloads
4. If `mightHaveMore` is `true`, immediately request the next page with the new cursor
5. If `mightHaveMore` is `false`, all currently available payloads have been fetched

### Cursor Lifecycle

```
Create webhook -> cursorForNextPayload: 1
                                        |
Fetch payloads (cursor=1) -----------> cursor: 5, mightHaveMore: true
                                        |
Fetch payloads (cursor=5) -----------> cursor: 8, mightHaveMore: false
                                        |
(wait for new changes...)               |
                                        |
Fetch payloads (cursor=8) -----------> cursor: 12, mightHaveMore: false
```

### Important Cursor Rules

- **Always persist the latest cursor** — if you lose it, you may miss changes or re-process old ones
- **Cursors are monotonically increasing** — never decrease the cursor value
- **Cursors survive webhook refreshes** — refreshing does not reset the cursor
- **Old payloads expire** — payloads older than 7 days are no longer available. If your cursor points to expired payloads, you will receive an empty response and a new cursor
- **The cursor from the webhook list endpoint** (`cursorForNextPayload`) always points to the next unread payload

### Recommended Polling Pattern

```python
import time

cursor = initial_cursor  # from webhook creation or last saved cursor

while True:
    response = requests.get(
        f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads",
        headers={"Authorization": f"Bearer {token}"},
        params={"cursor": cursor},
    )
    data = response.json()

    for payload in data.get("payloads", []):
        process_change(payload)

    cursor = data["cursor"]
    save_cursor(cursor)  # persist to database or file

    if data.get("mightHaveMore"):
        continue  # immediately fetch next page
    else:
        time.sleep(30)  # wait before polling again
```

---

## HMAC Signature Validation

When Airtable sends a POST notification to your `notificationUrl`, it includes an `X-Airtable-Content-MAC` header containing an HMAC-SHA256 signature. Use this to verify the notification is genuinely from Airtable.

### Validation Algorithm

1. Take the `macSecretBase64` value saved from webhook creation
2. Base64-decode it to get the raw secret bytes
3. Compute HMAC-SHA256 of the raw request body bytes using the secret
4. Hex-encode the result
5. Compare with the `X-Airtable-Content-MAC` header value using constant-time comparison

### Python Implementation

```python
import hmac, hashlib, base64

def validate_webhook_signature(mac_secret_base64, request_body_bytes, received_mac_header):
    """
    Validate an Airtable webhook notification signature.

    Args:
        mac_secret_base64: The macSecretBase64 value from webhook creation
        request_body_bytes: Raw bytes of the HTTP request body
        received_mac_header: Value of the X-Airtable-Content-MAC header

    Returns:
        True if the signature is valid, False otherwise
    """
    mac_secret = base64.b64decode(mac_secret_base64)
    computed = hmac.new(mac_secret, request_body_bytes, hashlib.sha256).hexdigest()
    is_valid = hmac.compare_digest(computed, received_mac_header)
    return is_valid
```

### Flask Integration

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store this securely — from webhook creation response
MAC_SECRET_BASE64 = "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo="

@app.route("/airtable-webhook", methods=["POST"])
def handle_webhook_notification():
    # Step 1: Validate signature
    mac_header = request.headers.get("X-Airtable-Content-MAC", "")
    if not validate_webhook_signature(MAC_SECRET_BASE64, request.data, mac_header):
        return jsonify({"error": "Invalid signature"}), 401

    # Step 2: Acknowledge the notification quickly (return 200)
    # The POST body is a ping — it does NOT contain change data
    # Process payloads asynchronously

    # Step 3: Fetch actual payloads in background
    # (use a task queue like Celery in production)
    fetch_and_process_payloads()

    return jsonify({"status": "ok"}), 200
```

### FastAPI Integration

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
MAC_SECRET_BASE64 = "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo="

@app.post("/airtable-webhook")
async def handle_webhook(request: Request):
    body = await request.body()
    mac_header = request.headers.get("X-Airtable-Content-MAC", "")

    if not validate_webhook_signature(MAC_SECRET_BASE64, body, mac_header):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Process payloads asynchronously
    return {"status": "ok"}
```

### Node.js Implementation

```javascript
const crypto = require("crypto");

function validateWebhookSignature(macSecretBase64, requestBodyBuffer, receivedMacHeader) {
  const macSecret = Buffer.from(macSecretBase64, "base64");
  const computed = crypto
    .createHmac("sha256", macSecret)
    .update(requestBodyBuffer)
    .digest("hex");
  return crypto.timingSafeEqual(
    Buffer.from(computed, "hex"),
    Buffer.from(receivedMacHeader, "hex")
  );
}
```

### Security Notes

- **Always use constant-time comparison** (`hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node.js) to prevent timing attacks
- **Store the `macSecretBase64` securely** — treat it like a password or API key
- **Validate before processing** — reject any request with an invalid or missing signature
- **Use the raw request body bytes** — do not parse/re-serialize JSON before computing the HMAC

---

## Webhook Lifecycle and Expiration

### Timeline

```
Day 0: Create webhook
       |-- Webhook active, payloads accumulating
       |
Day 3: Refresh webhook (optional but recommended)
       |-- Expiration extended to Day 10
       |
Day 7: Original expiration would have occurred
       |-- Webhook still active because it was refreshed
       |
Day 10: Webhook expires if not refreshed again
        |-- isHookEnabled set to false
        |-- No more payloads generated
        |-- Existing payloads still available for 7 more days
```

### Expiration Behavior

| Event | What Happens |
|-------|-------------|
| Webhook expires | `isHookEnabled` becomes `false`, no new payloads generated |
| Refresh before expiry | `expirationTime` set to 7 days from refresh time |
| Refresh after expiry | Not possible — must create a new webhook |
| Notification failures | After repeated failures, `areNotificationsEnabled` set to `false` but webhook remains active |

### Recommended Refresh Strategy

- Refresh every **24-48 hours** to maintain a comfortable buffer
- Set up monitoring to alert if a refresh fails
- If a webhook expires, create a new one and start with fresh cursors

```python
import schedule, time

def refresh_webhook():
    response = requests.post(
        f"https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        print(f"Refreshed: expires {response.json()['expirationTime']}")
    else:
        print(f"ALERT: Refresh failed with status {response.status_code}")

# Refresh daily
schedule.every(24).hours.do(refresh_webhook)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Notification POST Body

When Airtable sends a POST to your `notificationUrl`, the request body is a lightweight JSON ping:

```json
{
  "base": {
    "id": "appABC123"
  },
  "webhook": {
    "id": "ach00000000000001"
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `base.id` | string | ID of the base where changes occurred |
| `webhook.id` | string | ID of the webhook that was triggered |
| `timestamp` | string | ISO 8601 timestamp of the notification |

**Important:** The notification body does NOT contain change details. You must call the List Webhook Payloads endpoint to retrieve the actual changes.

### Notification Headers

| Header | Description |
|--------|-------------|
| `Content-Type` | `application/json` |
| `X-Airtable-Content-MAC` | HMAC-SHA256 signature for validation |
| `User-Agent` | Airtable user agent string |

### Notification Delivery

- Airtable expects a **2xx response within 10 seconds**
- If your server fails to respond, Airtable retries with exponential backoff
- After **repeated failures** (typically several hours of failures), `areNotificationsEnabled` is set to `false`
- The webhook continues to accumulate payloads even when notifications are disabled
- You can still poll for payloads manually when notifications are disabled

---

## Error Responses

### 401 — Authentication Required

```json
{
  "error": {
    "type": "AUTHENTICATION_REQUIRED",
    "message": "You must provide a valid API key to perform this operation"
  }
}
```

### 403 — Not Authorized

```json
{
  "error": {
    "type": "NOT_AUTHORIZED",
    "message": "You are not authorized to perform this operation"
  }
}
```

Causes: Token lacks `webhook:manage` scope, or user does not have access to the base.

### 404 — Not Found

```json
{
  "error": {
    "type": "NOT_FOUND",
    "message": "Could not find what you are looking for"
  }
}
```

Causes: Invalid `baseId` or `webhookId`.

### 422 — Invalid Request

```json
{
  "error": {
    "type": "INVALID_REQUEST",
    "message": "Invalid specification: dataTypes is required"
  }
}
```

Causes:
- Missing required `specification.options.filters.dataTypes`
- Invalid `notificationUrl` (not HTTPS, not reachable)
- Invalid `recordChangeScope` (not a valid table or view ID)
- Invalid field IDs in `watchDataInFieldIds` or `watchSchemasOfFieldIds`

### 422 — Webhook Limit Reached

```json
{
  "error": {
    "type": "WEBHOOK_LIMIT_REACHED",
    "message": "This base already has the maximum number of webhooks (10)"
  }
}
```

Solution: Delete an existing webhook before creating a new one.

### 429 — Rate Limited

```json
{
  "error": {
    "type": "TOO_MANY_REQUESTS",
    "message": "You have made too many requests in a short period of time. Please retry your request later"
  }
}
```

The `Retry-After` header indicates how many seconds to wait before retrying.

---

## Rate Limits and Quotas

| Resource | Limit |
|----------|-------|
| Webhooks per base | 10 |
| API requests per second per base | 5 |
| API requests per second per token (across all bases) | 50 |
| Webhook expiration | 7 days from creation or last refresh |
| Payload retention | 7 days from when the change occurred |
| Notification URL response timeout | 10 seconds |
| Maximum payload batch size | Varies — use `mightHaveMore` for pagination |

### Best Practices

1. **Scope webhooks narrowly** — use `recordChangeScope` and `watchDataInFieldIds` to minimize unnecessary payloads
2. **Persist cursors** — store the latest cursor in a database to survive application restarts
3. **Handle `mightHaveMore`** — always check and paginate until `false`
4. **Refresh proactively** — refresh webhooks daily, not just before they expire
5. **Validate signatures** — always verify `X-Airtable-Content-MAC` before processing notifications
6. **Process asynchronously** — return 200 quickly from your notification endpoint, then fetch payloads in the background
7. **Monitor webhook health** — check `isHookEnabled` and `areNotificationsEnabled` regularly via the List Webhooks endpoint
8. **Use idempotent processing** — payloads may be fetched multiple times if your cursor persistence fails, so design your processing to handle duplicates
