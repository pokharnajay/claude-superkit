---
name: update-tool
description: Update an existing Vapi tool — function name, description, parameters, server URL, or any other config. Use when modifying a tool that already exists. Requires tool ID from profile.md or GET /tool.
---

# Update Vapi Tool

Updates an existing tool via `PATCH /tool/:id`. Only the fields you send are changed — but **nested objects are replaced entirely**.

## API Endpoint

```bash
curl -s -w "\n%{http_code}" \
  -X PATCH "https://api.vapi.ai/tool/{TOOL_ID}" \
  -H "Authorization: Bearer $VAPI_PRIVATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/vapi_tool_patch.json
```

## Critical Rules

- **`function` is fully replaced** — when patching `function`, always include `name`, `description`, AND `parameters` together. Omitting any field removes it.
- **`parameters.properties` is fully replaced** — send the entire properties object. Vapi does not merge parameters; it replaces the whole object.
- **`server` is fully replaced** — when patching server URL, include the full server object.
- **Always write payload to `/tmp/vapi_tool_patch.json`** first, then curl it. Never inline large JSON in a curl command.
- **Verify response** — check HTTP 200 and spot-check the returned fields.
- **Re-attach to assistant if needed** — updating a tool does NOT automatically update assistants that reference it. If the tool is embedded in an assistant's `model.tools`, use `update-assistant` to push the updated tool config there too.

## What You Can Patch

| Field | Notes |
|-------|-------|
| `function.name` | Rename the tool (must also update assistant references) |
| `function.description` | LLM instruction for when to call the tool |
| `function.parameters` | Full JSON schema for parameters — replaces entirely |
| `server.url` | Webhook endpoint that receives tool calls |
| `server.timeoutSeconds` | How long Vapi waits for server response |
| `server.secret` | HMAC secret for request verification |
| `messages` | Request/response/delayed messages during tool execution |
| `async` | Whether tool call is async (true = fire-and-forget) |

## Tool Types

| Type | Updatable Fields |
|------|-----------------|
| `function` | `function`, `server`, `messages`, `async` |
| `apiRequest` | `url`, `method`, `headers`, `body`, `output` |
| `transferCall` | `destinations`, `message` |
| `endCall` | `messages` |
| `dtmf` | N/A (no update fields) |
| `voicemail` | `messages` |

## Workflow

1. **Get the tool ID** — from `profile.md` or via `GET https://api.vapi.ai/tool`
2. **Build the minimal patch payload** — only include what's changing
3. **Write payload** to `/tmp/vapi_tool_patch.json`
4. **PATCH** via curl
5. **Verify** — check HTTP 200, spot-check key fields in the response
6. **Re-attach to assistant if needed** — use `update-assistant` skill if the tool is embedded in `model.tools`
7. **Update `profile.md`** — update the relevant section + add a change log entry

## Example: Update function description + parameters

```python
import json

payload = {
    "function": {
        "name": "checkAvailability",
        "description": "Check available appointment slots for a given date. Call this when customer asks about scheduling.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                },
                "serviceType": {
                    "type": "string",
                    "description": "Type of service requested",
                    "enum": ["drain_cleaning", "repipe", "emergency"]
                }
            },
            "required": ["date"]
        }
    }
}

with open("/tmp/vapi_tool_patch.json", "w") as f:
    json.dump(payload, f)
```

## Example: Update server URL only

```json
{
  "server": {
    "url": "https://new-server.example.com/vapi/tools",
    "timeoutSeconds": 20,
    "secret": "your-hmac-secret"
  }
}
```

## Example: Make tool async (fire-and-forget)

```json
{
  "async": true
}
```

## Example: Update messages shown during tool execution

```json
{
  "messages": [
    {
      "type": "request-start",
      "content": "Let me check that for you."
    },
    {
      "type": "request-complete",
      "content": "Got it."
    },
    {
      "type": "request-failed",
      "content": "I wasn't able to pull that up. Let me take your info and have someone call you back."
    }
  ]
}
```

## List All Tools (find tool ID)

```bash
curl -s "https://api.vapi.ai/tool" \
  -H "Authorization: Bearer $VAPI_PRIVATE_API_KEY" \
  | python3 -c "import json,sys; tools=json.load(sys.stdin); [print(t['id'], t.get('function',{}).get('name','('+t.get('type','?')+')')) for t in tools]"
```

## Verification

```python
import json, urllib.request, os

TOOL_ID = "your-tool-id"
API_KEY = os.environ["VAPI_PRIVATE_API_KEY"]

req = urllib.request.Request(
    f"https://api.vapi.ai/tool/{TOOL_ID}",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    fn = result.get("function", {})
    print("Name:", fn.get("name"))
    print("Description:", fn.get("description"))
    print("Parameters:", list(fn.get("parameters", {}).get("properties", {}).keys()))
    print("Server URL:", result.get("server", {}).get("url"))
```

## After Updating

Always update `profile.md` in the assistant's folder:
- Update the Tools section with the new config
- Add a change log entry: `| YYYY-MM-DD | vX.Y — description of change |`
- If this tool is embedded in `model.tools` on an assistant, use `update-assistant` to sync
