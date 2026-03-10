# Voicemail Tool Reference

> Sources: https://docs.vapi.ai/tools/voicemail-tool, https://docs.vapi.ai/calls/voicemail-detection

> **Doc reference:** https://docs.vapi.ai/tools/voicemail-tool

Vapi provides two approaches for handling voicemail: the **Voicemail Tool** (assistant-controlled) and **Automatic Detection** (system-level).

### 7.1 Voicemail Tool (Assistant-Controlled)

The assistant listens for voicemail indicators, calls the tool, delivers a message, and the call ends.

#### Configuration

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "messages": [
      {
        "type": "system",
        "content": "You are a sales representative for Acme Corp. If at any point you determine you're speaking to a voicemail system (greeting mentions 'unavailable', 'leave a message', 'voicemail', etc.), immediately use the leave_voicemail tool."
      }
    ],
    "tools": [
      {
        "type": "voicemail",
        "function": {
          "name": "leave_voicemail",
          "description": "Leave a voicemail message when you detect you've reached a voicemail system"
        },
        "messages": [
          {
            "type": "request-start",
            "content": "Hi, this is {{company}}. {{message}}. Please call us back at {{phone}}."
          }
        ]
      }
    ]
  }
}
```

#### TTS Messages with Liquid Templates

Use template variables for dynamic content:
- `{{company}}` - Company name
- `{{message}}` - Custom message
- `{{phone}}` - Callback phone number

#### Pre-Recorded Audio Messages

For consistent quality, use pre-recorded audio files (`.wav` or `.mp3`):

```json
{
  "messages": [
    {
      "type": "request-start",
      "content": "https://example.com/voicemail.mp3"
    }
  ]
}
```

#### System Prompt Guidance for Detection

Be specific about voicemail indicators:
- "unavailable"
- "leave a message"
- "voicemail"
- "at the tone"
- "beep"

### 7.2 Automatic Voicemail Detection (System-Level)

Operates independently of your assistant at the system level.

#### Detection Providers

| Provider | Strengths | Weaknesses | Recommendation |
|----------|-----------|------------|----------------|
| **Vapi** (recommended) | Fast, accurate, graceful interruption handling | None significant | Strongly recommended |
| **Google** | Very good accuracy, reliable | Slightly longer detection time | Recommended |
| **OpenAI** | High accuracy, flexible phrasing | Higher cost | Good if budget allows |
| **Twilio** (legacy) | Very fast machine beep detection | Prone to false positives | Use only in special cases |

#### Configuration

```json
{
  "voicemailDetection": {
    "provider": "vapi",
    "backoffPlan": {
      "startAtSeconds": 2,
      "frequencySeconds": 2.5,
      "maxRetries": 5
    },
    "beepMaxAwaitSeconds": 12
  }
}
```

#### backoffPlan Parameters

| Parameter | Description |
|-----------|-------------|
| `startAtSeconds` | How long to wait before starting detection |
| `frequencySeconds` | How frequently to check after initial delay (minimum: 2.5s) |
| `maxRetries` | Maximum detection attempts before stopping |

#### beepMaxAwaitSeconds

- **Purpose:** Maximum time from call start to wait for a beep before the bot starts speaking
- **Default:** 30 seconds (range: 0-60)
- **If beep detected early:** Bot speaks immediately after beep (optimal)
- **If no beep by timeout:** Bot starts speaking anyway
- **If set too low:** Bot may start speaking before the actual beep and get cut off
- **Conservative:** 25-30 seconds
- **Aggressive:** 15-20 seconds (requires testing)

> **Warning:** Setting below 15-20 seconds may cause your voicemail message to be cut off. Most voicemail systems play 10-20 seconds of greeting before the beep.

#### Provider-Specific Configs

**Vapi Provider (Recommended):**
```json
{
  "voicemailDetection": {
    "provider": "vapi",
    "backoffPlan": {
      "maxRetries": 5,
      "startAtSeconds": 2,
      "frequencySeconds": 2.5
    },
    "beepMaxAwaitSeconds": 12
  }
}
```

**Google Provider:**
```json
{
  "voicemailDetection": {
    "provider": "google",
    "backoffPlan": {
      "maxRetries": 8,
      "startAtSeconds": 3,
      "frequencySeconds": 3
    },
    "beepMaxAwaitSeconds": 20
  }
}
```

### 7.3 Choosing Between Approaches

| Feature | Voicemail Tool | Automatic Detection |
|---------|---------------|---------------------|
| **Control** | Assistant-driven | System-driven |
| **Flexibility** | High - custom logic | Medium - predefined behavior |
| **Cost** | Lower - only when used | Higher - continuous monitoring |
| **Setup Complexity** | Simple - just add tool | Moderate - configure detection |
| **Message Customization** | Full control | Limited to configured message |
| **Detection Accuracy** | Depends on prompt | Provider-specific |

**Important:** Do not combine both approaches. Using the voicemail tool with automatic detection could result in false positives and complications.

---

