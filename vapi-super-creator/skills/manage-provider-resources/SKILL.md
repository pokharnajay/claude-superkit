---
name: manage-provider-resources
description: Create and manage provider resources in Vapi like pronunciation dictionaries for Cartesia and ElevenLabs voices. Use when customizing voice pronunciation, adding phoneme rules, or managing provider-specific configurations.
---

# Manage Provider Resources

This skill covers creating, retrieving, updating, and deleting provider-specific resources in Vapi. Currently supports pronunciation dictionaries for Cartesia and ElevenLabs voice providers, allowing you to customize how your voice assistants pronounce specific words, names, and technical terms.

> **See also:** `create-assistant` (configuring voices on assistants), `create-call` (testing pronunciation in calls)

## Prerequisites

- Vapi API key available (from https://dashboard.vapi.ai)
- A voice provider configured (Cartesia or ElevenLabs)

---

## Quick Start

### Create a Pronunciation Dictionary via cURL

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
      }
    ]
  }'
```

### Create via Python

```python
import requests

url = "https://api.vapi.ai/provider/cartesia/pronunciation-dictionary"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "name": "Company Terms",
    "rules": [
        {
            "stringToReplace": "Vapi",
            "type": "phoneme",
            "phoneme": "ˈvɑːpiː",
            "alphabet": "ipa",
        }
    ],
}

response = requests.post(url, headers=headers, json=data)
resource = response.json()
print(f"Created: {resource['id']} — Provider: {resource['provider']}")
```

### Create via TypeScript

```typescript
const response = await fetch(
  "https://api.vapi.ai/provider/cartesia/pronunciation-dictionary",
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "Company Terms",
      rules: [
        {
          stringToReplace: "Vapi",
          type: "phoneme",
          phoneme: "ˈvɑːpiː",
          alphabet: "ipa",
        },
      ],
    }),
  }
);

const resource = await response.json();
console.log(`Created: ${resource.id} — Provider: ${resource.provider}`);
```

---

## Supported Providers and Resources

| Provider | Resource Name | Description |
|----------|--------------|-------------|
| `cartesia` | `pronunciation-dictionary` | Pronunciation rules for Cartesia voices |
| `11labs` | `pronunciation-dictionary` | Pronunciation rules for ElevenLabs voices |

---

## Rule Types

### Phoneme Rules

Define exact pronunciation using IPA or CMU-ARPABET phonetic alphabets. Best for precise control over how words are spoken.

```json
{
  "stringToReplace": "Vapi",
  "type": "phoneme",
  "phoneme": "ˈvɑːpiː",
  "alphabet": "ipa"
}
```

**Supported alphabets:**
- `ipa` — International Phonetic Alphabet (e.g., `ˈvɑːpiː`)
- `cmu-arpabet` — Carnegie Mellon ARPABET (e.g., `V AA1 P IY0`)

### Alias Rules

Map a word to another word or phrase that the voice provider already pronounces correctly. Simpler than phonemes but less precise.

```json
{
  "stringToReplace": "API",
  "type": "alias",
  "alias": "A P I"
}
```

---

## CRUD Operations

### List All Pronunciation Dictionaries

```bash
curl https://api.vapi.ai/provider/cartesia/pronunciation-dictionary \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    "https://api.vapi.ai/provider/cartesia/pronunciation-dictionary",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
dictionaries = response.json()
for d in dictionaries:
    print(f"{d['id']} — {d['resource']['name']} ({len(d['resource']['rules'])} rules)")
```

**TypeScript:**

```typescript
const response = await fetch(
  "https://api.vapi.ai/provider/cartesia/pronunciation-dictionary",
  { headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` } }
);
const dictionaries = await response.json();
dictionaries.forEach((d: any) =>
  console.log(`${d.id} — ${d.resource.name} (${d.resource.rules.length} rules)`)
);
```

### Get a Specific Dictionary

```bash
curl https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.get(
    f"https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/{resource_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
resource = response.json()
print(f"{resource['resource']['name']} — {len(resource['resource']['rules'])} rules")
```

**TypeScript:**

```typescript
const response = await fetch(
  `https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/${resourceId}`,
  { headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` } }
);
const resource = await response.json();
console.log(`${resource.resource.name} — ${resource.resource.rules.length} rules`);
```

### Update a Dictionary

Add or modify rules in an existing pronunciation dictionary:

```bash
curl -X PATCH https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/{id} \
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

**Python:**

```python
response = requests.patch(
    f"https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/{resource_id}",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Updated Company Terms",
        "rules": [
            {
                "stringToReplace": "Vapi",
                "type": "phoneme",
                "phoneme": "ˈvɑːpiː",
                "alphabet": "ipa",
            },
            {
                "stringToReplace": "SQL",
                "type": "alias",
                "alias": "sequel",
            },
        ],
    },
)
updated = response.json()
```

**TypeScript:**

```typescript
const response = await fetch(
  `https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/${resourceId}`,
  {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "Updated Company Terms",
      rules: [
        {
          stringToReplace: "Vapi",
          type: "phoneme",
          phoneme: "ˈvɑːpiː",
          alphabet: "ipa",
        },
        {
          stringToReplace: "SQL",
          type: "alias",
          alias: "sequel",
        },
      ],
    }),
  }
);
const updated = await response.json();
```

### Delete a Dictionary

```bash
curl -X DELETE https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

**Python:**

```python
response = requests.delete(
    f"https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/{resource_id}",
    headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
)
deleted = response.json()
print(f"Deleted: {deleted['id']}")
```

**TypeScript:**

```typescript
const response = await fetch(
  `https://api.vapi.ai/provider/cartesia/pronunciation-dictionary/${resourceId}`,
  {
    method: "DELETE",
    headers: { Authorization: `Bearer ${process.env.VAPI_API_KEY}` },
  }
);
const deleted = await response.json();
console.log(`Deleted: ${deleted.id}`);
```

---

## Common Patterns

### Pronunciation Dictionary for Brand Names

```json
{
  "name": "Brand Pronunciations",
  "rules": [
    {
      "stringToReplace": "Vapi",
      "type": "phoneme",
      "phoneme": "ˈvɑːpiː",
      "alphabet": "ipa"
    },
    {
      "stringToReplace": "OpenAI",
      "type": "alias",
      "alias": "Open A I"
    },
    {
      "stringToReplace": "ElevenLabs",
      "type": "alias",
      "alias": "Eleven Labs"
    }
  ]
}
```

### Technical Acronyms Dictionary

```json
{
  "name": "Technical Acronyms",
  "rules": [
    {
      "stringToReplace": "API",
      "type": "alias",
      "alias": "A P I"
    },
    {
      "stringToReplace": "SQL",
      "type": "alias",
      "alias": "sequel"
    },
    {
      "stringToReplace": "CLI",
      "type": "alias",
      "alias": "C L I"
    },
    {
      "stringToReplace": "SDK",
      "type": "alias",
      "alias": "S D K"
    }
  ]
}
```

### ElevenLabs Pronunciation Dictionary

The same structure works for ElevenLabs — just change the provider in the URL:

```bash
curl -X POST https://api.vapi.ai/provider/11labs/pronunciation-dictionary \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Medical Terms",
    "rules": [
      {
        "stringToReplace": "acetaminophen",
        "type": "phoneme",
        "phoneme": "əˌsiːtəˈmɪnəfən",
        "alphabet": "ipa"
      }
    ]
  }'
```

---

## Provider Resource Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique resource identifier |
| `orgId` | string | Organization ID |
| `provider` | string | Voice provider (`cartesia` or `11labs`) |
| `resourceName` | string | Resource type (e.g., `pronunciation-dictionary`) |
| `resourceId` | string | Provider-side resource identifier |
| `resource` | object | The resource data (name, rules, etc.) |
| `createdAt` | string | ISO 8601 creation timestamp |
| `updatedAt` | string | ISO 8601 last update timestamp |

---

## References

- [API Reference](references/api-reference.md) -- REST API docs for Provider Resources (5 endpoints) with full parameter details

## Related Skills

- See the `setup-api-key` skill if you need to configure your API key first.
- See the `create-assistant` skill for configuring voices that use pronunciation dictionaries.
- See the `create-call` skill to test pronunciation in live calls.
