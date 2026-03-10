---
name: sync
description: Set up and manage Airtable Sync integrations to keep data synchronized between Airtable bases, external services, and third-party tools. Use when the user wants to sync data between bases, import external data, or set up real-time data pipelines.
---

# Airtable Sync

Guide the user through setting up data synchronization between Airtable bases and external sources.

## Sync Types

### 1. Airtable-to-Airtable Sync (Shared Views)

Sync data from one base to another using shared views:

**Source base setup:**
1. Create a view with the records you want to share
2. Click "Share view" and enable "Allow viewers to copy data"
3. Copy the share link

**Destination base setup:**
1. Click "+" to add a new table
2. Select "Sync from another base"
3. Paste the share link
4. Configure field mapping
5. Set sync frequency (manual, every 5 min, hourly, daily)

### 2. External Data Sync

Airtable supports syncing from these external sources:

| Source | Type |
|--------|------|
| Google Calendar | Events → Records |
| Google Sheets | Rows → Records |
| Jira | Issues → Records |
| Salesforce | Objects → Records |
| GitHub | Issues/PRs → Records |
| Zendesk | Tickets → Records |
| Box | Files → Records |
| Typeform | Responses → Records |

### 3. API-Based Sync (Custom)

For sources Airtable doesn't natively support, build custom sync using the API:

#### Pull Pattern: External → Airtable

```bash
# Fetch external data and upsert into Airtable
curl -X PATCH "https://api.airtable.com/v0/{baseId}/{tableId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "performUpsert": {
      "fieldsToMergeOn": ["External ID"]
    },
    "records": [
      {
        "fields": {
          "External ID": "ext_123",
          "Name": "Updated Name",
          "Status": "Active"
        }
      }
    ]
  }'
```

#### Push Pattern: Airtable → External (via Webhooks)

1. Create a webhook to monitor table changes:

```bash
curl -X POST "https://api.airtable.com/v0/bases/{baseId}/webhooks" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notificationUrl": "https://your-server.com/airtable-webhook",
    "specification": {
      "options": {
        "filters": {
          "dataTypes": ["tableData"],
          "recordChangeScope": "{tableId}"
        }
      }
    }
  }'
```

2. Process webhook payloads and push to external system

#### Bidirectional Sync Pattern

```python
import requests
import time

AIRTABLE_TOKEN = "patXXX..."
BASE_ID = "appXXX..."
TABLE_ID = "tblXXX..."

def get_airtable_records():
    """Pull all records from Airtable."""
    records = []
    offset = None
    while True:
        params = {}
        if offset:
            params["offset"] = offset
        resp = requests.get(
            f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}",
            headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}"},
            params=params
        )
        data = resp.json()
        records.extend(data["records"])
        offset = data.get("offset")
        if not offset:
            break
    return records

def upsert_to_airtable(records):
    """Upsert records into Airtable (batch of 10)."""
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        resp = requests.patch(
            f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}",
            headers={
                "Authorization": f"Bearer {AIRTABLE_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "performUpsert": {
                    "fieldsToMergeOn": ["External ID"]
                },
                "records": [{"fields": r} for r in batch]
            }
        )
        time.sleep(0.2)  # Rate limit: 5 req/sec
```

## Sync Configuration Best Practices

1. **Use upsert with `performUpsert`** — prevents duplicate records by merging on a unique field
2. **Batch operations** — process up to 10 records per API call
3. **Handle rate limits** — respect 5 req/sec per base, use exponential backoff
4. **Use `fieldsToMergeOn`** — specify which field(s) identify unique records
5. **Track sync timestamps** — add a "Last Synced" field to track freshness
6. **Use webhooks for real-time** — avoid polling when possible
7. **Idempotent operations** — ensure re-running sync doesn't create duplicates

## Sync Troubleshooting

| Issue | Solution |
|-------|----------|
| Duplicate records | Use `performUpsert` with unique field |
| Missing fields | Check token has `schema.bases:read` scope |
| 422 errors | Validate field types match (e.g., don't send string to number field) |
| Stale data | Reduce sync interval or switch to webhooks |
| Rate limit (429) | Add delays between batches, use exponential backoff |
