---
name: setup-api-key
description: Guide users through obtaining and configuring an Airtable API key or personal access token. Use when API calls fail due to missing keys, when the user needs to set up Airtable access, or when the user mentions needing Airtable API credentials.
---

# Setup Airtable API Key

Guide the user through obtaining and configuring their Airtable personal access token.

## Step 1: Check Existing Configuration

Check if the user already has an Airtable token configured:

```bash
echo "${AIRTABLE_ACCESS_TOKEN:-NOT SET}"
```

If already set, verify it works:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  https://api.airtable.com/v0/meta/bases
```

- `200` = Token is valid
- `401` = Token is invalid or expired
- `403` = Token lacks required scopes

## Step 2: Create a Personal Access Token

If no token exists or it's invalid, guide the user:

1. Go to **https://airtable.com/create/tokens**
2. Click **"Create new token"**
3. Give it a descriptive name (e.g., "Claude Code Integration")
4. Add the required scopes based on what they need:

| Scope | Purpose |
|-------|---------|
| `data.records:read` | Read records from tables |
| `data.records:write` | Create, update, delete records |
| `data.recordComments:read` | Read comments on records |
| `data.recordComments:write` | Create, update, delete comments |
| `schema.bases:read` | List bases, tables, fields, views |
| `schema.bases:write` | Create/modify tables, fields |
| `webhook:manage` | Create and manage webhooks |
| `enterprise.user:read` | Read enterprise user info |
| `enterprise.user:write` | Manage enterprise users |
| `enterprise.auditLogs:read` | Access audit logs |

5. Under **Access**, select which bases the token can access (all bases or specific ones)
6. Click **"Create token"** and copy it immediately (it won't be shown again)

## Step 3: Configure the Token

Set the token as an environment variable:

```bash
export AIRTABLE_ACCESS_TOKEN="patXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

For persistence, add to shell profile:

```bash
echo 'export AIRTABLE_ACCESS_TOKEN="patXXXXXXXX..."' >> ~/.zshrc
```

Or use a `.env` file in the project:

```bash
echo 'AIRTABLE_ACCESS_TOKEN=patXXXXXXXX...' >> .env
```

## Step 4: Verify Access

Test the token by listing bases:

```bash
curl -s -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
  https://api.airtable.com/v0/meta/bases | python3 -m json.tool
```

## Token Format

Airtable personal access tokens follow this format:
- Start with `pat` prefix
- Contain a dot separator
- Total length ~80+ characters
- Example: `patAbCdEf12345.67890abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMN`

## Important Notes

- **Never commit tokens to git** — use environment variables or `.env` files
- **Tokens can be scoped** — only grant the minimum scopes needed
- **Tokens can be base-scoped** — only grant access to the bases needed
- **Rate limits apply** — 5 requests/second per base, 50 across all bases
- **Tokens can be revoked** at https://airtable.com/create/tokens
