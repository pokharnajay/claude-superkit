# Code Tools (Serverless) Reference

> Source: https://docs.vapi.ai/tools/code-tool

Code tools execute TypeScript directly on Vapi's infrastructure without requiring you to set up or maintain a server.

> **Doc reference:** https://docs.vapi.ai/tools/code-tool

### Execution Environment

| Property | Value |
|----------|-------|
| **Language** | TypeScript only |
| **Default Timeout** | 10 seconds |
| **Max Timeout** | 60 seconds |
| **Memory** | Limited allocation |
| **Network** | Outbound HTTP/HTTPS only |
| **File System** | No access |
| **Available APIs** | `fetch()`, `console.log()` |

### Code Structure and Access

Your TypeScript code has access to two main objects:

- **`args`** - Contains parameters passed by the assistant (from the tool's `parameters` schema)
- **`env`** - Contains your environment variables for secure storage of API keys and secrets

```typescript
// Access parameters from the assistant
const { customerId, orderType } = args;

// Access secure environment variables
const { API_KEY, API_URL } = env;

// Make HTTP requests to external services
const response = await fetch(`${API_URL}/customers/${customerId}`, {
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
});

const customer = await response.json();

// Return data to the assistant
return {
  name: customer.name,
  email: customer.email,
  memberSince: customer.createdAt
};
```

### Creating Code Tools via API

```bash
curl --location 'https://api.vapi.ai/tool' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_API_KEY>' \
--data '{
    "type": "code",
    "name": "get_customer",
    "description": "Retrieves customer information by their ID",
    "code": "const { customerId } = args;\nconst { API_KEY } = env;\n\nconst response = await fetch(`https://api.example.com/customers/${customerId}`, {\n  headers: { \"Authorization\": `Bearer ${API_KEY}` }\n});\n\nreturn await response.json();",
    "parameters": {
        "type": "object",
        "properties": {
            "customerId": {
                "type": "string",
                "description": "The unique customer identifier"
            }
        },
        "required": ["customerId"]
    },
    "environmentVariables": [
        {
            "name": "API_KEY",
            "value": "your-api-key-here"
        }
    ]
}'
```

### Environment Variables

- Defined as an array of `{ name, value }` objects
- Support Liquid templates to reference call variables
- **Security:** Always store API keys and secrets in environment variables, never hardcode in code

### Testing Code Tools

Use the test endpoint:
```
POST https://api.vapi.ai/tool/code/test
```

### Complete Customer Lookup Example with Error Handling

```typescript
const { customerId } = args;

try {
  const response = await fetch(`${env.API_URL}/customers/${customerId}`);

  if (!response.ok) {
    return {
      error: true,
      message: `Customer ${customerId} not found`
    };
  }

  return await response.json();
} catch (error) {
  return {
    error: true,
    message: 'Unable to reach customer service'
  };
}
```

### Best Practices

- **Security:** Store secrets in env vars, never in code
- **Performance:** Keep execution under timeout, use efficient API calls, consider caching
- **Error Handling:** Always handle potential errors from API calls, return meaningful messages
- **Limitations:** No file system access, no npm packages, outbound HTTP/HTTPS only

---

