---
name: setup-api-key
description: Guide users through obtaining API keys and configuring the development environment. Use when the user needs to set up Vapi, when API calls fail due to missing keys, or when setting up a new project for Vapi voice AI development.
---

# Setup API Key & Environment

This skill guides you through obtaining API keys from the dashboard, configuring environment variables, and verifying authentication for Vapi voice AI development.

## Prerequisites

- A Vapi account (sign up at https://dashboard.vapi.ai)
- Terminal / command-line access
- Node.js 18+ (for SDK projects) or Python 3.8+ (for Python SDK)

## Step 1 — Obtain Your API Key

1. Open the [Vapi Dashboard](https://dashboard.vapi.ai).
2. Navigate to **Organization Settings** (gear icon) > **API Keys**.
3. Click **Create API Key** or copy an existing key.
4. Store the key securely — you will not be able to view it again after leaving the page.

> **Tip:** Vapi provides two key types:
> - **Private Key** (server-side) — full access, use in backend API calls.
> - **Public Key** — limited access, safe for client-side Web SDK.

## Step 2 — Validate the API Key

Confirm your key works by making a test request:

```bash
curl -s https://api.vapi.ai/assistant \
  -H "Authorization: Bearer YOUR_API_KEY" \
  | head -c 200
```

A successful response returns a JSON array of assistants (or `[]` if none exist). A `401` error means the key is invalid or expired.

## Step 3 — Configure Environment Variables

### .env File Setup

Create a `.env` file in your project root:

```bash
# .env
VAPI_API_KEY=your-private-api-key-here
VAPI_PUBLIC_KEY=your-public-key-here
VAPI_BASE_URL=https://api.vapi.ai
VAPI_WEBHOOK_URL=https://your-domain.com/api/vapi/webhook
```

### Verify .gitignore

**Critical:** Ensure `.env` is in your `.gitignore` to avoid leaking secrets:

```bash
# Check if .env is ignored
grep -q "^\.env$" .gitignore && echo "OK: .env is ignored" || echo "WARNING: Add .env to .gitignore!"
```

If missing, add it:

```bash
echo ".env" >> .gitignore
```

### Environment Variable Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `VAPI_API_KEY` | Yes | Private API key for server-side access |
| `VAPI_PUBLIC_KEY` | For Web SDK | Public key for client-side Web SDK |
| `VAPI_BASE_URL` | No | API base URL (default: `https://api.vapi.ai`) |
| `VAPI_WEBHOOK_URL` | For tools/webhooks | Your server endpoint for Vapi events |

### Using in Code

**TypeScript (Server SDK):**
```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({
    token: process.env.VAPI_API_KEY!
});
```

**Python (Server SDK):**
```python
from vapi import VapiClient

client = VapiClient(token=os.environ["VAPI_API_KEY"])
```

**Web SDK (Client-side):**
```javascript
import Vapi from '@vapi-ai/web';

const vapi = new Vapi('YOUR_PUBLIC_API_KEY');
```

### CI/CD Integration

```yaml
# GitHub Actions example
env:
  VAPI_API_KEY: ${{ secrets.VAPI_PROD_KEY }}

steps:
  - name: Test API Key
    run: |
      curl -s https://api.vapi.ai/assistant \
        -H "Authorization: Bearer $VAPI_API_KEY" \
        | head -c 200
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Regenerate API key from dashboard, re-export `VAPI_API_KEY` |
| API key not loading | Ensure `.env` file is in project root and your code loads it (e.g., `dotenv` package) |
| `VAPI_API_KEY` empty | Check `echo $VAPI_API_KEY` in terminal; re-run `export VAPI_API_KEY=...` if needed |

## Related Skills

- See the `create-assistant` skill to build your first voice assistant after setup.
- See the `setup-webhook` skill to configure server URLs and event handling.
- See the `create-phone-number` skill to provision phone numbers for calls.
