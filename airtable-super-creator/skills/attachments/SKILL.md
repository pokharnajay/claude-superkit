---
name: attachments
description: Upload and manage file attachments on Airtable records. Use when the user wants to upload files, images, PDFs, or any attachments to Airtable record fields.
---

# Airtable Attachments

Upload and manage file attachments on Airtable records.

## Endpoints

### Upload Attachment

```
POST https://content.airtable.com/v0/{baseId}/{recordId}/{fieldIdOrName}/uploadAttachment
```

**Important:** This endpoint uses `content.airtable.com`, NOT `api.airtable.com`.

**Headers:**
```
Authorization: Bearer $AIRTABLE_ACCESS_TOKEN
Content-Type: multipart/form-data
```

**cURL Example:**
```bash
curl -X POST "https://content.airtable.com/v0/{baseId}/{recordId}/{fieldIdOrName}/uploadAttachment" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "id": "attXXXXXXXXXXXXXX",
  "url": "https://v5.airtableusercontent.com/...",
  "filename": "document.pdf",
  "size": 102400,
  "type": "application/pdf",
  "width": null,
  "height": null,
  "thumbnails": null
}
```

### Upload Image with Thumbnails

```bash
curl -X POST "https://content.airtable.com/v0/{baseId}/{recordId}/Photos/uploadAttachment" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -F "file=@/path/to/photo.jpg"
```

**Response (for images):**
```json
{
  "id": "attXXXXXXXXXXXXXX",
  "url": "https://v5.airtableusercontent.com/...",
  "filename": "photo.jpg",
  "size": 524288,
  "type": "image/jpeg",
  "width": 1920,
  "height": 1080,
  "thumbnails": {
    "small": {
      "url": "https://v5.airtableusercontent.com/...",
      "width": 48,
      "height": 36
    },
    "large": {
      "url": "https://v5.airtableusercontent.com/...",
      "width": 640,
      "height": 480
    },
    "full": {
      "url": "https://v5.airtableusercontent.com/...",
      "width": 1920,
      "height": 1080
    }
  }
}
```

### Add Attachment via URL (Records API)

You can also add attachments by URL when creating or updating records:

```bash
curl -X PATCH "https://api.airtable.com/v0/{baseId}/{tableId}/{recordId}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Attachments": [
        {
          "url": "https://example.com/image.png",
          "filename": "image.png"
        }
      ]
    }
  }'
```

**Note:** When updating attachment fields, you must include ALL existing attachments plus new ones. Sending only new attachments will replace the existing ones.

### Preserve Existing Attachments When Adding New

```python
import requests

BASE_ID = "appXXX"
TABLE_ID = "tblXXX"
RECORD_ID = "recXXX"
TOKEN = "patXXX"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Get existing attachments
resp = requests.get(
    f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{RECORD_ID}",
    headers=headers
)
existing = resp.json()["fields"].get("Attachments", [])

# 2. Append new attachment
existing.append({
    "url": "https://example.com/new-file.pdf",
    "filename": "new-file.pdf"
})

# 3. Update with all attachments
requests.patch(
    f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{RECORD_ID}",
    headers=headers,
    json={"fields": {"Attachments": existing}}
)
```

## Supported File Types

| Category | Types |
|----------|-------|
| Images | jpg, jpeg, png, gif, svg, webp, bmp, tiff |
| Documents | pdf, doc, docx, xls, xlsx, ppt, pptx, csv, txt |
| Media | mp3, mp4, wav, avi, mov, webm |
| Archives | zip, tar, gz, rar |
| Other | Any file type up to 100MB |

## Attachment Field Schema

When reading records, attachment fields return an array:

```json
{
  "Attachments": [
    {
      "id": "attXXX",
      "url": "https://v5.airtableusercontent.com/...",
      "filename": "report.pdf",
      "size": 102400,
      "type": "application/pdf"
    }
  ]
}
```

## Important Notes

1. **Upload endpoint uses `content.airtable.com`** — not the regular API domain
2. **Attachment URLs expire** — they are signed URLs with limited lifetime. Re-fetch the record to get fresh URLs
3. **Max file size: 100MB** per attachment
4. **URL-based attachments** must be publicly accessible URLs
5. **Updating replaces all** — when using the Records API to update attachment fields, include all existing attachments or they will be removed
6. **Token scopes needed:** `data.records:write` for upload and URL-based attachments
