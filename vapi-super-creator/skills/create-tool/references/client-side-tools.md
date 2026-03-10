# Client-Side Tools (Web SDK) Reference

> Source: https://docs.vapi.ai/tools/client-side-websdk

> **Doc reference:** https://docs.vapi.ai/tools/client-side-websdk

Client-side tools process tool calls entirely in the browser without requiring a server.

### How It Works

1. **Omit the server URL** from your tool definition -- this makes it a client-side tool
2. Subscribe to `clientMessages: ['tool-calls']`
3. Handle `message.type === 'tool-calls'` events in your frontend code

**Key Limitation:** Client-side tools **cannot send results back to the model**. They are designed for one-way side effects only (UI updates, local processing, state changes).

### Setup

```bash
npm install @vapi-ai/web
```

### Tool Definition (No Server URL)

```typescript
const tool = {
  type: 'function',
  async: true,
  function: {
    name: 'updateUI',
    description: 'Call this function to initiate any UI update whenever the user requests changes to the interface',
    parameters: {
      type: 'object',
      properties: {
        message: {
          description: 'Brief message describing the UI update',
          type: 'string',
          default: '',
        },
      },
      required: ['message'],
    },
  },
  messages: [
    {
      type: 'request-start',
      content: 'Updating UI...',
      blocking: false,
    },
  ],
};
```

### Handling Tool Calls

```typescript
import Vapi from '@vapi-ai/web';

const vapi = new Vapi('YOUR_PUBLIC_KEY');

// Listen for tool-calls messages
vapi.on('message', (message) => {
  if (message.type === 'tool-calls') {
    const toolCalls = message.toolCallList;

    toolCalls.forEach((toolCall) => {
      const functionName = toolCall.function?.name;
      let parameters = {};

      try {
        const args = toolCall.function?.arguments;
        if (typeof args === 'string') {
          parameters = JSON.parse(args || '{}');
        } else if (typeof args === 'object' && args !== null) {
          parameters = args;
        }
      } catch (err) {
        console.error('Failed to parse toolCall arguments:', err);
        return;
      }

      if (functionName === 'updateUI') {
        handleUIUpdate(parameters.message);
      }
    });
  }
});
```

### Starting a Call with Client-Side Tools

```typescript
vapi.start({
  model: {
    provider: 'openai',
    model: 'gpt-4o',
    tools: [tool],
  },
  voice: { provider: 'vapi', voiceId: 'Elliot' },
  clientMessages: ['tool-calls'],
});
```

### Complete React Example

```tsx
import React, { useState, useCallback } from 'react';
import Vapi from '@vapi-ai/web';

const vapi = new Vapi('YOUR_PUBLIC_KEY');

function VoiceApp() {
  const [notification, setNotification] = useState<string | null>(null);

  const handleUIUpdate = useCallback((message?: string) => {
    setNotification(message || 'UI Update Triggered!');
    setTimeout(() => setNotification(null), 3000);
  }, []);

  vapi.on('message', (message) => {
    if (message.type === 'tool-calls') {
      const toolCalls = message.toolCallList;
      toolCalls.forEach((toolCall) => {
        const functionName = toolCall.function?.name;
        let parameters = {};
        try {
          const args = toolCall.function?.arguments;
          parameters = typeof args === 'string' ? JSON.parse(args || '{}') : args || {};
        } catch (err) {
          console.error('Failed to parse toolCall arguments:', err);
          return;
        }
        if (functionName === 'updateUI') {
          handleUIUpdate(parameters.message);
        }
      });
    }
  });

  const startCall = useCallback(() => {
    vapi.start({
      model: {
        provider: 'openai',
        model: 'gpt-4o',
        messages: [{
          role: 'system',
          content: "You can interact with the UI by calling the 'updateUI' tool when users request interface changes."
        }],
        tools: [{
          type: 'function',
          async: true,
          function: {
            name: 'updateUI',
            description: 'Update the user interface with a message',
            parameters: {
              type: 'object',
              properties: {
                message: { type: 'string', description: 'Message to display' }
              },
              required: ['message']
            }
          }
        }]
      },
      voice: { provider: 'vapi', voiceId: 'Elliot' },
      clientMessages: ['tool-calls'],
    });
  }, []);

  return (
    <div>
      {notification && (
        <div style={{ padding: '10px', background: '#e7f3ff', border: '1px solid #b3d9ff' }}>
          {notification}
        </div>
      )}
      <button onClick={startCall}>Start Voice Call</button>
      <button onClick={() => vapi.stop()}>End Call</button>
    </div>
  );
}
```

### Adding Context During Calls

Inject additional context mid-call using `addMessage`:

```typescript
// Inject system-level context
vapi.addMessage({
  role: 'system',
  content: 'Context: userId=123, plan=premium, theme=dark',
});

// Inject user message
vapi.addMessage({
  role: 'user',
  content: 'FYI: I switched to the settings tab.',
});
```

### Security Considerations
- Process sensitive data locally
- Use secure storage for any credentials
- Validate all input from tool calls

---

