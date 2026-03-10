# Custom Function Tools & Troubleshooting Reference

> Sources: https://docs.vapi.ai/tools/custom-tools, https://docs.vapi.ai/tools/custom-tools-troubleshooting

Custom function tools let Vapi POST to your server URL when the tool is invoked during a conversation.

> **Doc reference:** https://docs.vapi.ai/tools/custom-tools

### How They Work

1. You define a tool with `type: "function"` and a `server.url`
2. When the assistant invokes the tool, Vapi sends a POST request to your URL
3. Your server processes the request and returns results
4. Vapi feeds the results back to the assistant

### Creating via Dashboard

1. Navigate to **Tools** in your Vapi Dashboard
2. Click **Create Tool** and select "Function"
3. Configure with server URL pointing to your webhook endpoint
4. Add the tool to your assistant

### Creating via API

```bash
curl --location 'https://api.vapi.ai/tool' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_API_KEY>' \
--data '{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Retrieves current weather information for any location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location to get weather for"
                }
            },
            "required": ["location"]
        }
    },
    "server": {
        "url": "https://your-server.com/webhook"
    }
}'
```

### Webhook Request Format

Your server receives a POST with this structure:

```json
{
    "message": {
        "timestamp": 1678901234567,
        "type": "tool-calls",
        "toolCallList": [
            {
                "id": "toolu_01DTPAzUm5Gk3zxrpJ969oMF",
                "name": "get_weather",
                "arguments": {
                    "location": "San Francisco"
                }
            }
        ],
        "toolWithToolCallList": [
            {
                "type": "function",
                "name": "get_weather",
                "parameters": { ... },
                "description": "Retrieves the current weather for a specified location",
                "server": {
                    "url": "https://api.openweathermap.org/data/2.5/weather"
                },
                "messages": [],
                "toolCall": {
                    "id": "toolu_01DTPAzUm5Gk3zxrpJ969oMF",
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "parameters": {
                            "location": "San Francisco"
                        }
                    }
                }
            }
        ],
        "artifact": { "messages": [] },
        "assistant": { "name": "Weather Assistant", "description": "..." },
        "call": { "id": "call-uuid", "orgId": "org-uuid", "type": "webCall" }
    }
}
```

### Required Response Format (Success)

```json
{
    "results": [
        {
            "toolCallId": "toolu_01DTPAzUm5Gk3zxrpJ969oMF",
            "result": "San Francisco's weather today is 62F, partly cloudy."
        }
    ]
}
```

### Error Response Format

```json
{
    "results": [
        {
            "toolCallId": "toolu_01DTPAzUm5Gk3zxrpJ969oMF",
            "error": "Unable to fetch weather data at this time"
        }
    ]
}
```

### Critical Requirements

| Rule | Details |
|------|---------|
| **Always return HTTP 200** | Even for errors! Any other status code causes the response to be ignored |
| **Use single-line strings** | No `\n` line breaks in `result` or `error` fields |
| **Match toolCallId exactly** | Must match the `id` from the incoming request |
| **Include results array** | Individual result objects without the array wrapper will not work |
| **String types only** | Both `result` and `error` must be strings, not objects or arrays |

### Correct vs Incorrect Response

```json
// WRONG - has line breaks
{
    "result": "Temperature: 72F\nCondition: Sunny\nHumidity: 45%"
}

// CORRECT - single line
{
    "results": [
        {
            "toolCallId": "call_123",
            "result": "Temperature: 72F, Condition: Sunny, Humidity: 45%"
        }
    ]
}
```

### Multiple Tool Call Handling

Return results in the same order:

```json
{
    "results": [
        { "toolCallId": "call_1", "result": "First tool success" },
        { "toolCallId": "call_2", "error": "Second tool failed" },
        { "toolCallId": "call_3", "result": "Third tool success" }
    ]
}
```

### Sync vs Async Tools

| Mode | Config | Behavior | Use Case |
|------|--------|----------|----------|
| **Sync** (default) | `"async": false` or omit | Waits for webhook response | Data retrieval, validation, calculations |
| **Async** | `"async": true` | Tool resolves immediately, no wait | Logging, notifications, long-running operations |

### maxTokens Configuration

- **Default:** 100 tokens (can cause truncation for complex tools)
- **Recommendation:** Increase to 500+ for tools with large parameters or responses

```json
{
  "name": "complex_tool",
  "maxTokens": 500,
  "strict": true,
  "async": false
}
```

---

## 5. Custom Tools Troubleshooting

> **Doc reference:** https://docs.vapi.ai/tools/custom-tools-troubleshooting

### Tool Won't Trigger

**Problem:** Assistant doesn't call the tool when it should.

**Solutions:**

1. **Use specific prompting** - Reference the exact tool name:
   - BAD: "Handle weather requests"
   - GOOD: "When user asks for weather, use get_weather with city parameter"

2. **Verify required parameters** - Ensure schema includes all required params:
   ```json
   {
     "name": "get_weather",
     "parameters": {
       "type": "object",
       "properties": {
         "city": {
           "type": "string",
           "description": "City name for weather lookup"
         }
       },
       "required": ["city"]
     }
   }
   ```

3. **Enable `"strict": true`** to catch schema validation errors early:
   ```json
   {
     "name": "get_weather",
     "description": "Get current weather for a city",
     "parameters": { ... },
     "strict": true,
     "maxTokens": 500
   }
   ```

4. **Check call logs** for "Schema validation errors"

### No Result Returned

**Problem:** Logs show "ok, no result returned" or similar.

**Checklist:**
- Always return HTTP 200 (even for errors)
- Use single-line strings (no `\n`)
- Match toolCallId exactly from request
- Include `results` array wrapper
- Both `result` and `error` must be strings

### Response Ignored

**Problem:** Tool executes but response is ignored.

| Issue | Problem | Solution |
|-------|---------|----------|
| Wrong HTTP status | Any status other than 200 | Always return HTTP 200, even for errors |
| Line breaks | `\n` characters in responses | Use single-line strings only |
| Missing results array | Individual result objects | Must use `results` array structure |
| Tool call ID mismatch | ID doesn't match request | Use exact `toolCallId` from request |
| Wrong data type | Objects/arrays in result field | Both `result` and `error` must be strings |

### Debugging Steps

1. **Test in Dashboard** - Use the "Test" button in Tools section to verify responses with sample data
2. **Check Call Logs** - Navigate to `Observe > Call Logs` to see tool execution results and errors
3. **Verify Token Limits** - Default is only 100. Increase `maxTokens` to 500+ for complex tools
4. **Validate JSON** - Use a JSON validator to ensure your webhook response structure is valid

### Token Truncation

If parameters or responses are being cut off, increase `maxTokens`:

```json
{
  "name": "my_tool",
  "maxTokens": 500
}
```

---

