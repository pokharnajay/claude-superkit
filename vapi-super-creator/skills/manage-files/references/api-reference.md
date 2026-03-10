# Vapi Files API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json` (except file uploads which use `multipart/form-data`)

This reference covers 5 endpoints in the Files API for uploading, retrieving, updating, and deleting files used in Vapi knowledge bases and assistant context.

---

## Table of Contents

- [Files API](#files-api)
  - [1. List Files](#1-list-files)
  - [2. Upload File](#2-upload-file)
  - [3. Get File](#3-get-file)
  - [4. Delete File](#4-delete-file)
  - [5. Update File](#5-update-file)
- [File Object Schema](#file-object-schema)

---

## Files API

### 1. List Files

Retrieves a paginated list of all files in the organization.

#### HTTP Request

```
GET https://api.vapi.ai/file
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | number | No | Page number for pagination |
| `limit` | number | No | Number of results per page |
| `sortOrder` | string | No | Sort order: `asc` or `desc` |
| `createdAtGt` | string | No | Filter: created after this ISO 8601 timestamp |
| `createdAtLt` | string | No | Filter: created before this ISO 8601 timestamp |
| `createdAtGe` | string | No | Filter: created at or after this ISO 8601 timestamp |
| `createdAtLe` | string | No | Filter: created at or before this ISO 8601 timestamp |
| `updatedAtGt` | string | No | Filter: updated after this ISO 8601 timestamp |
| `updatedAtLt` | string | No | Filter: updated before this ISO 8601 timestamp |
| `updatedAtGe` | string | No | Filter: updated at or after this ISO 8601 timestamp |
| `updatedAtLe` | string | No | Filter: updated at or before this ISO 8601 timestamp |

#### Response

- **200 OK** -- Array of File objects

#### cURL Example

```bash
curl https://api.vapi.ai/file \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**With pagination and filtering:**

```bash
curl "https://api.vapi.ai/file?page=1&limit=10&sortOrder=desc&createdAtGt=2026-01-01T00:00:00Z" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/file"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}
params = {
    "page": 1,
    "limit": 10,
    "sortOrder": "desc",
}

response = requests.get(url, headers=headers, params=params)
files = response.json()

for f in files:
    print(f"ID: {f['id']}, Name: {f['name']}, Status: {f['status']}, Bytes: {f['bytes']}")
```

#### TypeScript Example

```typescript
const params = new URLSearchParams({
  page: "1",
  limit: "10",
  sortOrder: "desc",
});

const response = await fetch(`https://api.vapi.ai/file?${params}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const files = await response.json();
files.forEach((f: any) => {
  console.log(`ID: ${f.id}, Name: ${f.name}, Status: ${f.status}, Bytes: ${f.bytes}`);
});
```

#### Example Response

```json
[
  {
    "id": "file_abc123",
    "orgId": "org_xyz789",
    "name": "product-manual.pdf",
    "originalName": "product-manual.pdf",
    "bytes": 245760,
    "mimetype": "application/pdf",
    "purpose": "knowledge-base",
    "metadata": {},
    "key": "files/org_xyz789/file_abc123",
    "path": "files/org_xyz789/file_abc123/product-manual.pdf",
    "bucket": "vapi-files",
    "url": "https://storage.vapi.ai/files/org_xyz789/file_abc123/product-manual.pdf",
    "status": "done",
    "parsedTextUrl": "https://storage.vapi.ai/files/org_xyz789/file_abc123/parsed.txt",
    "parsedTextBytes": 52480,
    "object": "file",
    "createdAt": "2026-02-15T10:30:00.000Z",
    "updatedAt": "2026-02-15T10:31:05.000Z"
  }
]
```

---

### 2. Upload File

Uploads a new file to Vapi. The file will be processed asynchronously (text extraction, parsing). Check the `status` field to track processing progress.

#### HTTP Request

```
POST https://api.vapi.ai/file
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `multipart/form-data` |

#### Request Body (multipart/form-data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | binary | Yes | The file to upload |

#### Response

- **201 Created** -- File object

#### cURL Example

```bash
curl -X POST https://api.vapi.ai/file \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -F "file=@/path/to/document.pdf"
```

#### Python Example

```python
import requests

url = "https://api.vapi.ai/file"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

with open("/path/to/document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    response = requests.post(url, headers=headers, files=files)

file_obj = response.json()
print(f"Uploaded: {file_obj['id']} — Status: {file_obj['status']}")
```

#### TypeScript Example

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
console.log(`Uploaded: ${fileObj.id} — Status: ${fileObj.status}`);
```

#### Example Response

```json
{
  "id": "file_def456",
  "orgId": "org_xyz789",
  "name": "document.pdf",
  "originalName": "document.pdf",
  "bytes": 102400,
  "mimetype": "application/pdf",
  "purpose": "knowledge-base",
  "metadata": {},
  "key": "files/org_xyz789/file_def456",
  "path": "files/org_xyz789/file_def456/document.pdf",
  "bucket": "vapi-files",
  "url": "https://storage.vapi.ai/files/org_xyz789/file_def456/document.pdf",
  "status": "processing",
  "parsedTextUrl": null,
  "parsedTextBytes": null,
  "object": "file",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:00.000Z"
}
```

---

### 3. Get File

Retrieves a single file by its ID.

#### HTTP Request

```
GET https://api.vapi.ai/file/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique file identifier |

#### Response

- **200 OK** -- File object

#### cURL Example

```bash
curl https://api.vapi.ai/file/file_def456 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

file_id = "file_def456"
url = f"https://api.vapi.ai/file/{file_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.get(url, headers=headers)
file_obj = response.json()

print(f"Name: {file_obj['name']}")
print(f"Status: {file_obj['status']}")
print(f"URL: {file_obj['url']}")
print(f"Size: {file_obj['bytes']} bytes")
```

#### TypeScript Example

```typescript
const fileId = "file_def456";

const response = await fetch(`https://api.vapi.ai/file/${fileId}`, {
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const fileObj = await response.json();
console.log(`Name: ${fileObj.name}`);
console.log(`Status: ${fileObj.status}`);
console.log(`URL: ${fileObj.url}`);
console.log(`Size: ${fileObj.bytes} bytes`);
```

#### Example Response

```json
{
  "id": "file_def456",
  "orgId": "org_xyz789",
  "name": "document.pdf",
  "originalName": "document.pdf",
  "bytes": 102400,
  "mimetype": "application/pdf",
  "purpose": "knowledge-base",
  "metadata": {},
  "key": "files/org_xyz789/file_def456",
  "path": "files/org_xyz789/file_def456/document.pdf",
  "bucket": "vapi-files",
  "url": "https://storage.vapi.ai/files/org_xyz789/file_def456/document.pdf",
  "status": "done",
  "parsedTextUrl": "https://storage.vapi.ai/files/org_xyz789/file_def456/parsed.txt",
  "parsedTextBytes": 25600,
  "object": "file",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:30.000Z"
}
```

---

### 4. Delete File

Deletes a file by its ID. Returns the deleted file object.

#### HTTP Request

```
DELETE https://api.vapi.ai/file/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique file identifier |

#### Response

- **200 OK** -- Deleted File object

#### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/file/file_def456 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

#### Python Example

```python
import requests

file_id = "file_def456"
url = f"https://api.vapi.ai/file/{file_id}"
headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}

response = requests.delete(url, headers=headers)
deleted_file = response.json()
print(f"Deleted file: {deleted_file['id']} ({deleted_file['name']})")
```

#### TypeScript Example

```typescript
const fileId = "file_def456";

const response = await fetch(`https://api.vapi.ai/file/${fileId}`, {
  method: "DELETE",
  headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
});

const deletedFile = await response.json();
console.log(`Deleted file: ${deletedFile.id} (${deletedFile.name})`);
```

#### Example Response

```json
{
  "id": "file_def456",
  "orgId": "org_xyz789",
  "name": "document.pdf",
  "originalName": "document.pdf",
  "bytes": 102400,
  "mimetype": "application/pdf",
  "purpose": "knowledge-base",
  "metadata": {},
  "key": "files/org_xyz789/file_def456",
  "path": "files/org_xyz789/file_def456/document.pdf",
  "bucket": "vapi-files",
  "url": "https://storage.vapi.ai/files/org_xyz789/file_def456/document.pdf",
  "status": "done",
  "parsedTextUrl": "https://storage.vapi.ai/files/org_xyz789/file_def456/parsed.txt",
  "parsedTextBytes": 25600,
  "object": "file",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T14:00:30.000Z"
}
```

---

### 5. Update File

Updates a file's properties. Currently supports renaming the file.

#### HTTP Request

```
PATCH https://api.vapi.ai/file/{id}
```

#### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The unique file identifier |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | New name for the file |

#### Response

- **200 OK** -- Updated File object

#### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/file/file_def456 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{ "name": "renamed-document.pdf" }'
```

#### Python Example

```python
import requests

file_id = "file_def456"
url = f"https://api.vapi.ai/file/{file_id}"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}
payload = {"name": "renamed-document.pdf"}

response = requests.patch(url, headers=headers, json=payload)
updated_file = response.json()
print(f"Updated name: {updated_file['name']}")
```

#### TypeScript Example

```typescript
const fileId = "file_def456";

const response = await fetch(`https://api.vapi.ai/file/${fileId}`, {
  method: "PATCH",
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ name: "renamed-document.pdf" }),
});

const updatedFile = await response.json();
console.log(`Updated name: ${updatedFile.name}`);
```

#### Example Response

```json
{
  "id": "file_def456",
  "orgId": "org_xyz789",
  "name": "renamed-document.pdf",
  "originalName": "document.pdf",
  "bytes": 102400,
  "mimetype": "application/pdf",
  "purpose": "knowledge-base",
  "metadata": {},
  "key": "files/org_xyz789/file_def456",
  "path": "files/org_xyz789/file_def456/document.pdf",
  "bucket": "vapi-files",
  "url": "https://storage.vapi.ai/files/org_xyz789/file_def456/document.pdf",
  "status": "done",
  "parsedTextUrl": "https://storage.vapi.ai/files/org_xyz789/file_def456/parsed.txt",
  "parsedTextBytes": 25600,
  "object": "file",
  "createdAt": "2026-03-10T14:00:00.000Z",
  "updatedAt": "2026-03-10T15:20:00.000Z"
}
```

---

## File Object Schema

The File object is returned by all file endpoints.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique file identifier |
| `orgId` | string | Organization ID that owns the file |
| `name` | string | Display name of the file (can be updated via PATCH) |
| `originalName` | string | Original filename at time of upload |
| `bytes` | number | File size in bytes |
| `mimetype` | string | MIME type of the file (e.g., `application/pdf`, `text/plain`, `text/csv`) |
| `purpose` | string | Intended purpose of the file |
| `metadata` | object | Additional key-value metadata associated with the file |
| `key` | string | Internal storage key |
| `path` | string | Internal storage path |
| `bucket` | string | Storage bucket name |
| `url` | string | Public URL to access the file |
| `status` | string | Processing status. One of: `processing` (being parsed), `done` (ready to use), `failed` (processing error) |
| `parsedTextUrl` | string \| null | URL to the extracted/parsed text content. Available when `status` is `done` |
| `parsedTextBytes` | number \| null | Size of the parsed text content in bytes. Available when `status` is `done` |
| `object` | string | Always `"file"` |
| `createdAt` | string | ISO 8601 timestamp of when the file was created |
| `updatedAt` | string | ISO 8601 timestamp of when the file was last updated |

### Status Values

| Status | Description |
|--------|-------------|
| `processing` | File has been uploaded and is being parsed/processed |
| `done` | File processing is complete; `parsedTextUrl` is available |
| `failed` | File processing encountered an error |
