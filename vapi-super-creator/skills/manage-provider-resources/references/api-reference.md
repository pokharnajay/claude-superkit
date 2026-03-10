# Vapi Provider Resources API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`
> **Content-Type:** `application/json`

This reference covers 5 endpoints for managing provider-specific resources such as pronunciation dictionaries.

---

## Table of Contents

- [1. List Provider Resources](#1-list-provider-resources)
- [2. Create Provider Resource](#2-create-provider-resource)
- [3. Get Provider Resource](#3-get-provider-resource)
- [4. Delete Provider Resource](#4-delete-provider-resource)
- [5. Update Provider Resource](#5-update-provider-resource)
- [Provider Resource Response Schema](#provider-resource-response-schema)

---

## 1. List Provider Resources

Lists all resources of a given type for a provider.

### HTTP Request

```
GET https://api.vapi.ai/provider/{provider}/{resourceName}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Voice provider: `cartesia` or `11labs` |
| `resourceName` | string | Yes | Resource type: `pronunciation-dictionary` |

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

### cURL Example

```bash
curl https://api.vapi.ai/provider/cartesia/pronunciation-dictionary \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Response

Returns an array of provider resource objects.

```json
[
  {
    "id": "resource-uuid-1",
    "orgId": "org-uuid",
    "provider": "cartesia",
    "resourceName": "pronunciation-dictionary",
    "resourceId": "provider-side-id",
    "resource": {
      "name": "Company Terms",
      "rules": [
        {
          "stringToReplace": "Vapi",
          "type": "phoneme",
          "phoneme": "ˈvɑːpiː",
          "alphabet": "ipa"
        }
      ]
    },
    "createdAt": "2026-03-01T12:00:00.000Z",
    "updatedAt": "2026-03-01T12:00:00.000Z"
  }
]
```

---

## 2. Create Provider Resource

Creates a new resource for the specified provider.

### HTTP Request

```
POST https://api.vapi.ai/provider/{provider}/{resourceName}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Voice provider: `cartesia` or `11labs` |
| `resourceName` | string | Yes | Resource type: `pronunciation-dictionary` |

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

### Request Body (pronunciation-dictionary)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name for the dictionary |
| `rules` | array | No | Array of pronunciation rule objects |

### Rule Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `stringToReplace` | string | Yes | The word or phrase to apply the rule to |
| `type` | string | Yes | Rule type: `phoneme` or `alias` |
| `phoneme` | string | Conditional | Phonetic representation (required when `type` is `phoneme`) |
| `alphabet` | string | Conditional | Phonetic alphabet: `ipa` or `cmu-arpabet` (required when `type` is `phoneme`) |
| `alias` | string | Conditional | Replacement word/phrase (required when `type` is `alias`) |

### cURL Example

```bash
curl -X POST https://api.vapi.ai/provider/cartesia/pronunciation-dictionary \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Company Terms",
    "rules": [
      {
        "stringToReplace": "Vapi",
        "type": "phoneme",
        "phoneme": "ˈvɑːpiː",
        "alphabet": "ipa"
      },
      {
        "stringToReplace": "API",
        "type": "alias",
        "alias": "A P I"
      }
    ]
  }'
```

### Response

Returns the created provider resource object.

```json
{
  "id": "resource-uuid",
  "orgId": "org-uuid",
  "provider": "cartesia",
  "resourceName": "pronunciation-dictionary",
  "resourceId": "provider-side-id",
  "resource": {
    "name": "Company Terms",
    "rules": [
      {
        "stringToReplace": "Vapi",
        "type": "phoneme",
        "phoneme": "ˈvɑːpiː",
        "alphabet": "ipa"
      },
      {
        "stringToReplace": "API",
        "type": "alias",
        "alias": "A P I"
      }
    ]
  },
  "createdAt": "2026-03-10T12:00:00.000Z",
  "updatedAt": "2026-03-10T12:00:00.000Z"
}
```

---

## 3. Get Provider Resource

Retrieves a specific provider resource by ID.

### HTTP Request

```
GET https://api.vapi.ai/provider/{provider}/{resourceName}/{id}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Voice provider: `cartesia` or `11labs` |
| `resourceName` | string | Yes | Resource type: `pronunciation-dictionary` |
| `id` | string | Yes | Resource ID |

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

### cURL Example

```bash
curl https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/resource-uuid \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Response

Returns a single provider resource object.

```json
{
  "id": "resource-uuid",
  "orgId": "org-uuid",
  "provider": "cartesia",
  "resourceName": "pronunciation-dictionary",
  "resourceId": "provider-side-id",
  "resource": {
    "name": "Company Terms",
    "rules": [
      {
        "stringToReplace": "Vapi",
        "type": "phoneme",
        "phoneme": "ˈvɑːpiː",
        "alphabet": "ipa"
      }
    ]
  },
  "createdAt": "2026-03-01T12:00:00.000Z",
  "updatedAt": "2026-03-01T12:00:00.000Z"
}
```

---

## 4. Delete Provider Resource

Deletes a provider resource by ID.

### HTTP Request

```
DELETE https://api.vapi.ai/provider/{provider}/{resourceName}/{id}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Voice provider: `cartesia` or `11labs` |
| `resourceName` | string | Yes | Resource type: `pronunciation-dictionary` |
| `id` | string | Yes | Resource ID |

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |

### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/resource-uuid \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Response

Returns the deleted provider resource object.

---

## 5. Update Provider Resource

Updates an existing provider resource by ID.

### HTTP Request

```
PATCH https://api.vapi.ai/provider/{provider}/{resourceName}/{id}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Voice provider: `cartesia` or `11labs` |
| `resourceName` | string | Yes | Resource type: `pronunciation-dictionary` |
| `id` | string | Yes | Resource ID |

### Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| `Authorization` | string | Yes | `Bearer $VAPI_API_KEY` |
| `Content-Type` | string | Yes | `application/json` |

### Request Body (pronunciation-dictionary)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Updated display name |
| `rules` | array | No | Updated array of pronunciation rule objects (replaces existing rules) |

### cURL Example

```bash
curl -X PATCH https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/resource-uuid \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Updated Company Terms",
    "rules": [
      {
        "stringToReplace": "Vapi",
        "type": "phoneme",
        "phoneme": "ˈvɑːpiː",
        "alphabet": "ipa"
      },
      {
        "stringToReplace": "SQL",
        "type": "alias",
        "alias": "sequel"
      }
    ]
  }'
```

### Response

Returns the updated provider resource object.

---

## Provider Resource Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique resource identifier (UUID) |
| `orgId` | string | Organization ID |
| `provider` | string | Voice provider (`cartesia` or `11labs`) |
| `resourceName` | string | Resource type (e.g., `pronunciation-dictionary`) |
| `resourceId` | string | Provider-side resource identifier |
| `resource` | object | The resource data containing `name` and `rules` |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |
