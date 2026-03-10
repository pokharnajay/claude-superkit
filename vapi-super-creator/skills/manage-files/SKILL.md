---
name: manage-files
description: Upload, manage, and organize files in Vapi for knowledge bases and assistant context. Use when uploading documents, managing file storage, or working with knowledge base content.
---

# Manage Files Skill

This skill covers uploading, retrieving, updating, and deleting files in Vapi. Files are used to provide knowledge base content, documents, and other reference material that voice assistants can draw from during calls.

> **See also:** `create-assistant` (attaching knowledge bases to assistants), `create-tool` (building tools that reference files)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- Files to upload in a supported format (PDF, TXT, DOCX, CSV, etc.)

---

## Quick Start

### Upload a File via cURL

```bash
curl -X POST https://api.vapi.ai/file \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -F "file=@/path/to/document.pdf"
```

### Upload a File via Python

```python
import requests

url = "https://api.vapi.ai/file"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

with open("/path/to/document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    response = requests.post(url, headers=headers, files=files)

file_obj = response.json()
print(f"File uploaded: {file_obj['id']} — Status: {file_obj['status']}")
```

### Upload a File via TypeScript

```typescript
import fs from "fs";
import FormData from "form-data";
import fetch from "node-fetch";

const form = new FormData();
form.append("file", fs.createReadStream("/path/to/document.pdf"));

const response = await fetch("https://api.vapi.ai/file", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    ...form.getHeaders(),
  },
  body: form,
});

const fileObj = await response.json();
console.log(`File uploaded: ${fileObj.id} — Status: ${fileObj.status}`);
```

---

## CRUD Operations

### List All Files

```bash
curl https://api.vapi.ai/file \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination and filtering:**

```bash
curl "https://api.vapi.ai/file?page=1&limit=20&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
import requests

response = requests.get(
    "https://api.vapi.ai/file",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    params={"page": 1, "limit": 20, "sortOrder": "desc"},
)
files = response.json()
for f in files:
    print(f"{f['name']} ({f['bytes']} bytes) — {f['status']}")
```

**TypeScript:**

```typescript
const response = await fetch("https://api.vapi.ai/file?page=1&limit=20&sortOrder=desc", {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const files = await response.json();
files.forEach((f: any) => console.log(`${f.name} (${f.bytes} bytes) — ${f.status}`));
```

### Get a Specific File

```bash
curl https://api.vapi.ai/file/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/file/{file_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
file_obj = response.json()
print(f"{file_obj['name']} — {file_obj['status']} — {file_obj['url']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/file/${fileId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const fileObj = await response.json();
console.log(`${fileObj.name} — ${fileObj.status} — ${fileObj.url}`);
```

### Update a File

Rename or update file metadata:

```bash
curl -X PATCH https://api.vapi.ai/file/{id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{ "name": "updated-document-name.pdf" }'
```

**Python:**

```python
response = requests.patch(
    f"https://api.vapi.ai/file/{file_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={"name": "updated-document-name.pdf"},
)
updated_file = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/file/${fileId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ name: "updated-document-name.pdf" }),
});
const updatedFile = await response.json();
```

### Delete a File

```bash
curl -X DELETE https://api.vapi.ai/file/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/file/{file_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted_file = response.json()
print(f"Deleted: {deleted_file['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(`https://api.vapi.ai/file/${fileId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});
const deletedFile = await response.json();
console.log(`Deleted: ${deletedFile.id}`);
```

---

## Common Patterns

### Upload a File for a Knowledge Base

Upload a document and then attach it to an assistant's knowledge base configuration:

```bash
# 1. Upload the file
FILE_RESPONSE=$(curl -s -X POST https://api.vapi.ai/file \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -F "file=@/path/to/knowledge-doc.pdf")

FILE_ID=$(echo $FILE_RESPONSE | jq -r '.id')

# 2. Use the file ID when creating or updating a knowledge base
echo "File ID for knowledge base: $FILE_ID"
```

### Check File Processing Status

After uploading, files go through processing (text extraction, parsing). Poll the status until it completes:

```python
import requests
import time

file_id = "your-file-id"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

while True:
    response = requests.get(f"https://api.vapi.ai/file/{file_id}", headers=headers)
    file_obj = response.json()
    status = file_obj["status"]
    print(f"Status: {status}")

    if status == "done":
        print(f"Processing complete. Parsed text URL: {file_obj.get('parsedTextUrl')}")
        break
    elif status == "failed":
        print("File processing failed.")
        break

    time.sleep(2)
```

### List Recently Updated Files

```bash
# Files updated after a specific date
curl "https://api.vapi.ai/file?updatedAtGt=2026-01-01T00:00:00Z&sortOrder=desc" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Bulk Upload Multiple Files

```python
import requests
from pathlib import Path

headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}
folder = Path("/path/to/documents")

uploaded = []
for filepath in folder.glob("*.pdf"):
    with open(filepath, "rb") as f:
        files = {"file": (filepath.name, f, "application/pdf")}
        response = requests.post("https://api.vapi.ai/file", headers=headers, files=files)
        file_obj = response.json()
        uploaded.append(file_obj)
        print(f"Uploaded: {filepath.name} -> {file_obj['id']}")

print(f"\nUploaded {len(uploaded)} files.")
```

---

## File Object Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique file identifier |
| `orgId` | string | Organization ID |
| `name` | string | Display name of the file |
| `originalName` | string | Original filename at upload |
| `bytes` | number | File size in bytes |
| `mimetype` | string | MIME type (e.g., `application/pdf`) |
| `purpose` | string | Intended purpose of the file |
| `metadata` | object | Additional metadata |
| `key` | string | Storage key |
| `path` | string | Storage path |
| `bucket` | string | Storage bucket |
| `url` | string | URL to access the file |
| `status` | string | Processing status: `processing`, `done`, or `failed` |
| `parsedTextUrl` | string | URL to the extracted/parsed text content |
| `parsedTextBytes` | number | Size of the parsed text in bytes |
| `object` | string | Always `"file"` |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Files (5 endpoints) with full examples
