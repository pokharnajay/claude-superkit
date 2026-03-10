---
name: user-info
description: Get current authenticated user information, token scopes, and validate API access. Use when checking who is authenticated, what permissions a token has, or debugging authentication issues.
---

# Airtable User Info

Retrieve information about the currently authenticated user and their token scopes.

## Endpoint

### Get Current User (whoami)

```
GET https://api.airtable.com/v0/meta/whoami
```

**Headers:**
```
Authorization: Bearer $AIRTABLE_ACCESS_TOKEN
```

**Response:**
```json
{
  "id": "usrXXXXXXXXXXXXXX",
  "email": "user@example.com",
  "scopes": [
    "data.records:read",
    "data.records:write",
    "data.recordComments:read",
    "data.recordComments:write",
    "schema.bases:read",
    "schema.bases:write",
    "webhook:manage"
  ]
}
```

## Usage Examples

### Check Authentication

```bash
curl -s -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  https://api.airtable.com/v0/meta/whoami | python3 -m json.tool
```

### Verify Token Scopes

```python
import requests

resp = requests.get(
    "https://api.airtable.com/v0/meta/whoami",
    headers={"Authorization": f"Bearer {AIRTABLE_ACCESS_TOKEN}"}
)
user = resp.json()

required_scopes = ["data.records:read", "data.records:write", "schema.bases:read"]
missing = [s for s in required_scopes if s not in user.get("scopes", [])]

if missing:
    print(f"Token missing scopes: {missing}")
else:
    print(f"Authenticated as: {user['email']} (all scopes present)")
```

## Available Scopes Reference

| Scope | Purpose |
|-------|---------|
| `data.records:read` | Read records from tables |
| `data.records:write` | Create, update, delete records |
| `data.recordComments:read` | Read comments on records |
| `data.recordComments:write` | Create, update, delete comments |
| `schema.bases:read` | List bases, tables, fields, views |
| `schema.bases:write` | Create/modify tables and fields |
| `webhook:manage` | Create and manage webhooks |
| `enterprise.user:read` | Read enterprise user info |
| `enterprise.user:write` | Manage enterprise users |
| `enterprise.auditLogs:read` | Access audit logs |
| `user.email:read` | Read user email via whoami |

## Error Responses

| Status | Meaning |
|--------|---------|
| 200 | Success — token is valid |
| 401 | Invalid or expired token |
| 403 | Token exists but lacks required scopes |
