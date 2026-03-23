---
name: update-assistant
description: Update an existing Vapi voice AI assistant — system prompt, model, tools, voice, transcriber, hooks, or any other config. Use when modifying an assistant that already exists. Requires assistant ID from profile.md or GET /assistant.
---

# Update Vapi Assistant

Updates an existing assistant's **system prompt** and/or **firstMessage** via `PATCH /assistant/:id`. This skill is strictly scoped to prompt and greeting changes — it never changes the provider, model, voice, transcriber, tools, or any other configuration.

## Critical Rules

1. **NEVER change provider, model, voice, transcriber, tools, or any non-prompt config.** If the user asks to change those, tell them to use the `create-assistant` skill or do it manually.
2. **Always fetch the existing assistant first** via `GET /assistant/:id` to retrieve the current `model` object (provider, model, temperature, maxTokens, tools). You need these to reconstruct the `model` payload since Vapi replaces the entire `model` object on PATCH.
3. **`model` is fully replaced on PATCH** — you MUST include `provider`, `model`, `temperature`, `maxTokens`, `messages`, AND `tools` together. Omitting any field removes it. Copy all non-prompt fields exactly from the GET response.
4. **Always write payload to `/tmp/vapi_patch.json`** first, then curl it. Never inline large JSON in a curl command.
5. **Verify response** — check HTTP 200 and spot-check the returned fields match existing config.

## Workflow

1. **Get the assistant ID** — from `profile.md` or ask the user
2. **Fetch existing assistant** — `GET /assistant/:id` to capture current model config, tools, and all settings
3. **Write the updated system prompt** — invoke the `write-system-prompt` skill first (see below)
4. **Build the patch payload** — use the EXACT existing `provider`, `model`, `temperature`, `maxTokens`, and `tools` from the GET response, only replacing `messages[0].content` with the new prompt
5. **Optionally update `firstMessage`** — include as a top-level field in the patch if it needs changing
6. **Write payload** to `/tmp/vapi_patch.json`
7. **PATCH** via curl
8. **Verify** — check HTTP 200, confirm provider/model/voice/tools are unchanged
9. **Update `profile.md`** — update the System Prompt section + add a change log entry

## System Prompt Writing

> **REQUIRED: Before writing or rewriting any system prompt, you MUST invoke the `vapi-super-creator:write-system-prompt` skill using the Skill tool.** That skill contains the complete prompt philosophy, structure template, section-by-section guide, style rules, voice realism techniques, language-specific additions, data handling rules, and anti-patterns table. Do not write a system prompt without it.

## Step 2: Fetch Existing Assistant

```bash
curl -s "https://api.vapi.ai/assistant/{ASSISTANT_ID}" \
  -H "Authorization: Bearer $VAPI_PRIVATE_API_KEY" | python3 -m json.tool > /tmp/vapi_existing.json
```

Extract the fields you need to preserve:

```python
import json

with open("/tmp/vapi_existing.json") as f:
    existing = json.load(f)

# These MUST be preserved exactly
model_config = existing["model"]
provider = model_config["provider"]
model = model_config["model"]
temperature = model_config.get("temperature", 0.7)
max_tokens = model_config.get("maxTokens", 250)
tools = model_config.get("tools", [])
```

## Step 4: Build the Patch Payload

```python
import json

# Read from profile.md or construct the new prompt
system_prompt = """...updated prompt..."""

# Preserve ALL existing model config — only replace the prompt
payload = {
    "model": {
        "provider": provider,           # FROM GET — do not change
        "model": model,                 # FROM GET — do not change
        "temperature": temperature,     # FROM GET — do not change
        "maxTokens": max_tokens,        # FROM GET — do not change
        "messages": [{"role": "system", "content": system_prompt}],  # UPDATED
        "tools": tools                  # FROM GET — do not change
    }
}

# Only include firstMessage if it's changing
# payload["firstMessage"] = "Updated greeting here"

with open("/tmp/vapi_patch.json", "w") as f:
    json.dump(payload, f)
```

## Step 7: PATCH

```bash
curl -s -w "\n%{http_code}" \
  -X PATCH "https://api.vapi.ai/assistant/{ASSISTANT_ID}" \
  -H "Authorization: Bearer $VAPI_PRIVATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/vapi_patch.json
```

## Step 8: Verify

After patching, confirm nothing else changed:

```python
import json

# Parse the PATCH response (or do another GET)
# Verify these match the original:
# - model.provider
# - model.model
# - model.temperature
# - model.maxTokens
# - model.tools (same count, same names)
# - voice (untouched)
# - transcriber (untouched)
```

## After Updating

Always update `profile.md` in the assistant's folder:
- Update the System Prompt section with the new prompt
- Add a change log entry: `| YYYY-MM-DD | vX.Y — description of change |`
