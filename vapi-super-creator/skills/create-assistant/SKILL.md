---
name: create-assistant
description: Create and configure Vapi voice AI assistants with models, voices, transcribers, tools, hooks, and advanced settings. Use this skill whenever the user wants to build a voice assistant, voice agent, phone bot, AI caller, or anything related to Vapi.ai. Trigger for any mention of Vapi, voice AI, voice assistant creation, phone assistant, AI calling, assistant configuration, transcriber setup, voice provider selection, tool configuration for voice agents, squad setup, or campaign management. Also trigger when the user asks about configuring models, voices, transcribers, webhooks, server URLs, or any Vapi-specific concepts like firstMessage, endCallPhrases, startSpeakingPlan, or stopSpeakingPlan. This skill should be used even if the user just says "create an assistant" in a Vapi project context.
---

# Vapi Assistant Creation

Create fully configured voice AI assistants using the Vapi API. Assistants combine a language model, voice, and transcriber to handle real-time phone and web conversations. This guide covers the full lifecycle: creating, configuring, testing, optimizing, and documenting voice assistants.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Quick Start

### cURL

```bash
curl -X POST https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Assistant",
    "firstMessage": "Hello! How can I help you today?",
    "model": {
      "provider": "openai",
      "model": "gpt-5.2-instant",
      "messages": [
        {
          "role": "system",
          "content": "You are a friendly phone support assistant. Keep responses concise and under 30 words."
        }
      ],
      "tools": [{ "type": "endCall" }]
    },
    "voice": {
      "provider": "cartesia",
      "voiceId": "<cartesia-voice-id>"
    },
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-3",
      "language": "en"
    },
    "startSpeakingPlan": {
      "waitSeconds": 0.4,
      "smartEndpointingEnabled": true
    },
    "backgroundSound": "office"
  }'
```

### TypeScript (Server SDK)

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

const assistant = await vapi.assistants.create({
  name: "Support Assistant",
  firstMessage: "Hello! How can I help you today?",
  model: {
    provider: "openai",
    model: "gpt-5.2-instant",
    messages: [
      {
        role: "system",
        content: "You are a friendly phone support assistant. Keep responses concise and under 30 words.",
      },
    ],
    tools: [{ type: "endCall" }],
  },
  voice: {
    provider: "cartesia",
    voiceId: "<cartesia-voice-id>",
  },
  transcriber: {
    provider: "deepgram",
    model: "nova-3",
    language: "en",
  },
  backgroundSound: "office",
});

console.log("Assistant created:", assistant.id);
```

### Python

```python
import requests
import os

response = requests.post(
    "https://api.vapi.ai/assistant",
    headers={
        "Authorization": f"Bearer {os.environ['VAPI_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "name": "Support Assistant",
        "firstMessage": "Hello! How can I help you today?",
        "model": {
            "provider": "openai",
            "model": "gpt-5.2-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a friendly phone support assistant. Keep responses concise and under 30 words.",
                }
            ],
            "tools": [{"type": "endCall"}],
        },
        "voice": {"provider": "cartesia", "voiceId": "<cartesia-voice-id>"},
        "transcriber": {"provider": "deepgram", "model": "nova-3", "language": "en"},
        "backgroundSound": "office",
    },
)

assistant = response.json()
print(f"Assistant created: {assistant['id']}")
```

---

## Assistant Configuration Architecture

A Vapi assistant has these core components:

### 1. Model (LLM) Configuration

The brain of the assistant. Defines which LLM processes conversations.

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-5.2-instant",
    "temperature": 0.7,
    "maxTokens": 500,
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful customer service agent for Acme Corp..."
      }
    ],
    "tools": [],
    "toolIds": [],
    "emotionRecognitionEnabled": true,
    "numFastTurns": 1
  }
}
```

**Supported LLM Providers:**
- `openai` — gpt-5.2-instant (default, lowest cost + fast), gpt-4.1-mini, gpt-4.1-nano, gpt-4.1, gpt-4o, gpt-4o-mini, gpt-5-nano, gpt-5-mini, gpt-5, gpt-5.1, gpt-5.2, o3-mini, o4-mini
- `anthropic` — claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3-5-sonnet
- `google` — gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash
- `groq` — llama-3.1-70b, llama-3.1-8b, mixtral-8x7b
- `together-ai` — Various open-source models
- `deepinfra` — meta-llama/Meta-Llama-3.1-70B-Instruct
- `openrouter` — Access 100+ models
- `perplexity` — llama-3.1-sonar-large-128k-online (web-connected)
- `azure-openai` — Your Azure deployments (requires credential setup)
- `custom-llm` — Your own endpoint (OpenAI-compatible)

See [providers reference](references/providers.md) for full details.

### 2. Transcriber (STT) Configuration

Converts caller speech to text.

```json
{
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-3",
    "language": "en",
    "wordBoost": ["Acme", "HVAC"],
    "endpointing": 255
  }
}
```

**Transcriber Providers:**
- `deepgram` — nova-3 (default, recommended), nova-2, nova-2-general, nova-2-meeting, nova-2-phonecall
- `assembly-ai` — universal-streaming, nano
- `google` — latest_long, latest_short
- `gladia` — fast, accurate (multi-language)
- `speechmatics` — Enterprise STT
- `talkscriber` — Specialized
- `custom-transcriber` — Your own STT endpoint

The `keywords` / `wordBoost` field boosts recognition of specific words (useful for brand names, industry terms).

### 3. Voice (TTS) Configuration

Controls how the assistant sounds.

```json
{
  "voice": {
    "provider": "cartesia",
    "voiceId": "<cartesia-voice-id>",
    "speed": 1.0,
    "cachingEnabled": true,
    "chunkPlan": {
      "enabled": true,
      "minCharacters": 30,
      "formatPlan": {
        "enabled": true,
        "numberToDigitsCutoff": 2025
      }
    }
  }
}
```

**Voice Providers:**
- `cartesia` — Low-latency, high-quality, excellent for real-time (default, recommended)
- `vapi` — Vapi's optimized voices (Elliot, Lily, Rohan, Paola, Kian), lowest latency
- `11labs` — ElevenLabs, highest quality, most natural (premium option)
- `openai` — alloy, echo, fable, onyx, nova, shimmer
- `azure` — Microsoft voices, good multilingual support
- `playht` — PlayHT expressive voices
- `deepgram` — Aura voices, low latency
- `rime-ai`, `lmnt`, `tavus` — Specialized providers
- `custom-voice` — Your own TTS endpoint

See [voice selection guide](references/voice-selection.md) for complete voice IDs by language (English, Hindi, Spanish, French, and more).

---

## Behavior Configuration

### First Message

```json
{
  "firstMessage": "Hello! Thanks for calling Acme Corp. How can I help you today?",
  "firstMessageMode": "assistant-speaks-first"
}
```

**`firstMessageMode` options:**
- `"assistant-speaks-first"` — Assistant greets immediately (default)
- `"assistant-waits-for-user"` — Waits for caller to speak first
- `"assistant-speaks-first-with-model-generated-message"` — LLM generates the greeting

### Background Sound

```json
{
  "backgroundSound": "office"
}
```

Options: `"off"`, `"office"`, `"static"`. Use `"office"` for phone calls — ambient noise makes it feel real.

### Backchanneling

Enable natural conversational acknowledgments ("uh-huh", "I see"):

```json
{
  "backgroundDenoisingEnabled": true,
  "backchannelingEnabled": true
}
```

### HIPAA Compliance

```json
{
  "hipaaEnabled": true
}
```

When enabled, Vapi won't store call recordings or transcripts.

### Conversation Settings (Complete)

```json
{
  "firstMessage": "Hello! Thanks for calling Acme Corp. How can I help you today?",
  "firstMessageMode": "assistant-speaks-first",
  "firstMessageInterruptionsEnabled": false,
  "endCallMessage": "Thank you for calling. Goodbye!",
  "endCallPhrases": ["goodbye", "bye bye", "end call"],
  "voicemailMessage": "Hi, you've reached Acme Corp. Please leave a message.",
  "maxDurationSeconds": 600,
  "backgroundSound": "office",
  "backchannelingEnabled": true,
  "backgroundDenoisingEnabled": true,
  "name": "Acme Support Agent"
}
```

---

## System Prompt Creation Guide (REQUIRED)

**Every system prompt you create MUST follow this structure and these rules.** This framework is derived from proven production prompts and Vapi's official Prompting Guide. The goal is zero AI detection — the caller should never feel like they are talking to a machine.

### Prompt Structure Template

Every system prompt MUST use bracketed sections in this order. Adapt the content but NEVER skip sections.

```
[Identity]
You are <NAME>, the <ROLE> for <COMPANY/BUSINESS>.
<One sentence about what you do.>
<Whether the system has already introduced you or not.>
You never mention internal tools, APIs, databases, or systems. You simply say things like "let me check that" or "I can take a look for you."

[Context]
<What topics/domains you handle - be specific.>
<What you do NOT handle - redirect politely.>
<Timezone: All times follow <TIMEZONE>.>
<Today's date: Today's date is {{ "now" | date: "%b %d, %Y, %I:%M %p", "<TIMEZONE>" }}.>
<Key business details: hours, services, fees, policies.>

[Style]
Speak like a friendly, helpful <ROLE_DESCRIPTOR>.
Use natural language, contractions, and short clean sentences.
Use simple transitions like "Sure thing", "Alright", "No worries", "Let me just check that".
Avoid robotic tone.
Never mention tools or internal systems.
Keep all responses to 2-3 sentences max.
If the caller says bye or goodbye or clearly ends the conversation, stop speaking immediately and trigger the endCall tool.

[Response Handling]
When asking any question from the Task Flow, evaluate the caller's response to determine if it qualifies as a valid answer.
Use context awareness to assess relevance and appropriateness.
If the response is valid, proceed to the next relevant question or instruction.
If the response is unclear or off-topic, ask a clarifying question.
Avoid infinite loops by moving forward when a clear answer cannot be obtained after 2 attempts.

[Task Flow]

1. Initial Interaction
- Respond directly to the caller's first message.
- Do not introduce yourself (the system's First Message already did that).
- If the question is <TYPE_A>, go to Section 2.
- If the question is <TYPE_B>, go to Section 3.
- If the caller wants to speak to someone, go to Section <N>.

2. <Task Name>
- <Step-by-step instructions with clear branching logic>
- <wait for user response>
- If response indicates <condition A>: Proceed to step X.
- If response indicates <condition B>: Proceed to 'Call Closing'.
- After completing, ask: "Is there anything else I can help you with?"
- If caller ends conversation, trigger endCall.

3. <Next Task>
...

<N-1>. Call Closing
- Ask: "Is there anything else I can help you with?"
- <wait for user response>
- If caller needs more help, return to the relevant section.
- If caller says nothing else or goodbye, trigger the endCall tool.

<N>. Escalation / Transfer
- If transferring, do NOT send any text response. Silently trigger the transfer tool.
- <How to handle handoff to humans>

[Error Handling]
If the caller's response is unclear, ask clarifying questions politely.
If you encounter any issues with tools, inform the caller: "Let me try that again" or "One moment please."
If a tool call fails, do not expose the error. Say: "I'm having a bit of trouble with that, let me note this down and someone will get back to you."

[Warning]
Do not modify or attempt to correct user input parameters. Pass them directly into the function or tool as given.
Never say the word 'function', 'tools', 'API', or the name of any available functions.
Never say "ending the call" or announce internal actions.

[Critical Rules]
- Do not introduce yourself.
- Do not mention tools, APIs, or internal systems.
- Never ask for details already collected in the same call.
- Never go off topic. Redirect politely if the caller strays.
- Keep all responses short and natural.
- If caller ends the conversation, immediately trigger endCall.
- If about to transfer the call, do NOT send any text response. Simply trigger the tool silently.
- <Any additional hard constraints specific to this assistant.>
```

### Section-by-Section Guide

#### [Identity] Section
- Give the assistant a human name (Leo, Priya, Pixie, Chief, Riley)
- Define their role clearly in one line
- State "The system has already introduced you, so you must not introduce yourself again" if using firstMessage
- Add: "You never mention internal tools, APIs, databases, or systems"

#### [Context] Section
- Scope what the assistant handles AND what it does not handle
- Include timezone with Liquid template: `{{ "now" | date: "%b %d, %Y, %I:%M %p", "America/Los_Angeles" }}`
- List all tools by name (internal reference only — assistant must never say these names aloud)
- Include key business facts: hours, fees, policies, addresses

#### [Style] Section
ALWAYS include these rules (adapt language/fillers to target language):
```
- Speak like a friendly, helpful <role> - not like a chatbot.
- Use natural language, contractions, and short clean sentences.
- Use simple transitions: "Sure thing", "Alright", "No worries", "Got it", "Let me just check that".
- Keep responses to 2-3 sentences. This is a phone call, not an essay.
- Use contractions: "I'm", "you're", "we'll", "don't", "can't" - never formal "I am", "you are".
- Spell out numbers as words: say "seven thirty" not "7:30".
- For dates, use natural speech: "January twelfth" - never include the year.
- React before moving on: "Oh nice!", "Got it.", "Alright.", "Makes sense."
- If you need to pause or think, say "One sec..." or "Let me check on that..." - do not go silent.
- Never say the word "pause" or "break" out loud. Just stop speaking naturally.
- Avoid robotic tone and corporate jargon.
- Never mention tools, systems, or internal processes.
- If the caller says bye or goodbye, stop speaking immediately and trigger endCall.
```

**Voice realism techniques (add to [Style] for more human-like speech):**
```
- Add natural speech elements for realism:
  - Hesitations: Use fillers like "uh," "um," or "well" sparingly (e.g., "I was, uh, thinking about it").
  - Pauses: Use ellipses "..." to indicate thinking (e.g., "Let me see... okay, got it").
  - Emotional emphasis: Use capital letters or exclamation marks for tone (e.g., "Oh that's great!" or "No way!").
- Date formatting: Always spell out dates naturally.
  - Say: "January twenty fourth" — never "1/24" or "January 24th, 2026".
  - Never mention the year in dates.
- Time formatting: Always spell out times naturally.
  - Say: "four thirty PM" — never "4:30 PM" or "16:30".
  - Say: "eleven pee em" — never "11 PM".
- Number formatting: Spell out numbers in words.
  - Say: "three hundred seventy dollars" — never "$370".
  - For phone numbers, say each digit: "zero four one two, three four five, six seven eight".
```

**Language-specific style additions (add to [Style] based on language):**

For **Hindi/Hinglish** — add:
```
- Speak in natural Hinglish (Hindi + English mix), written in Roman script.
- Use slangs naturally: 'yaar', 'arre', 'accha', 'bas', 'theek hai', 'pakka', 'ekdum', 'bilkul'
- Add 'ji' for politeness: 'haan ji', 'bilkul ji', 'zaroor'
- Use 'na' at sentence endings: 'badhiya rahega na?'
- Use 'wala/wali': 'terrace wali table', 'evening wala slot'
- Mix English words freely: table, booking, confirm, available, cancel
- Say 'matlab' when explaining things
```

For **Spanish** — add:
```
- Use natural conversational Spanish with contractions and colloquialisms.
- Use 'vale', 'bueno', 'pues', 'mira', 'oye' as natural fillers.
- Address formally (usted) unless the caller switches to informal (tu).
- React naturally: 'Perfecto!', 'Claro que si!', 'Muy bien!'
```

For **French** — add:
```
- Use conversational French, not formal written French.
- Natural fillers: 'Alors...', 'Bon...', 'Eh bien...', 'Voila!'
- Use 'vous' unless the caller uses 'tu' first.
- React: 'Parfait!', 'Tres bien!', 'D accord!'
```

#### [Response Handling] Section
Add this section between [Style] and [Task Flow]:
```
[Response Handling]
When asking any question from the Task Flow, evaluate the caller's response to determine if it qualifies as a valid answer.
Use context awareness to assess relevance and appropriateness.
If the response is valid, proceed to the next relevant question or instruction.
If the response is unclear or off-topic, ask a clarifying question.
Avoid infinite loops by moving forward when a clear answer cannot be obtained after 2 attempts.
```

#### [Task Flow] Section
- Number each section (1, 2, 3...) and give it a clear name
- Use "go to Section X" for branching — this is critical for complex flows
- Use **conditional branching** with natural language:
  ```
  - If response indicates interest: Proceed to step 3.
  - If response indicates no interest: Proceed to 'Call Closing'.
  - If response indicates <condition>: Go to Section X.
  ```
- Use **`<wait for user response>`** markers to explicitly control turn-taking:
  ```
  3. Ask: "What date works best for you?"
  <wait for user response>
  4. Trigger the 'fetchSlots' tool with the caller's preferred date.
  ```
- Use **variable mapping** with `{{variable_name}}` for tool results:
  ```
  4. Trigger the 'fetchSlots' tool and map the result to {{available_slots}}.
  5. Ask: "I have a couple slots open: {{available_slots}}. Would any of those work?"
  6. <wait for user response>
  7. Set {{selectedSlot}} to the caller's chosen time.
  ```
- Collect details ONE AT A TIME in separate turns (never ask for name + phone + email in one message)
- For data collection (phone, email, name):
  - Accept input exactly as given — never auto-correct or phonetically guess
  - Confirm phone number ONCE by repeating digit by digit
  - NEVER reconfirm email
  - Ask only the scripted question with no extra words
- For slot/availability presentation:
  - Offer max 2-3 options at a time
  - Speak dates naturally ("January twelfth at ten AM") — never include the year
  - Separate the options and the follow-up question into two distinct sentences
  - Never invent or guess slots — always fetch from tools first
- Always include a **[Call Closing]** section at the end:
  ```
  [Call Closing]
  - Ask: "Is there anything else I can help you with?"
  - <wait for user response>
  - If caller needs more help, return to the relevant section.
  - If caller says nothing else or goodbye, trigger the endCall tool.
  ```
- Always include a **[Last Message]** fallback section:
  ```
  [Last Message]
  - Respond: "Looks like this is taking longer than expected. Let me have someone from our team get back to you."
  - Proceed to 'Call Closing'.
  ```
- Include escalation path for confused/upset callers
- **Silent transfers:** If transferring the call, do NOT send any text response. Simply trigger the transfer tool silently.

#### [Error Handling] Section
Always include:
```
[Error Handling]
If the caller's response is unclear, ask clarifying questions politely.
If you encounter any issues with tools, inform the caller: "Let me try that again" or "One moment please."
If a tool call fails, do not expose the error. Say: "I'm having a bit of trouble with that, let me note this down and someone will get back to you."
If the audio or the caller's message is unclear at any point, say: "Sorry, I didn't catch that. Could you say that again?"
```

#### [Warning] Section
Include these hard constraints:
```
[Warning]
Do not modify or attempt to correct user input parameters. Pass them directly into the function or tool as given.
Never say the word 'function', 'tools', 'API', or the name of any available functions.
Never say "ending the call" or announce internal actions.
If you think you are about to transfer the call, do not send any text response. Simply trigger the tool silently.
```

#### [Critical Rules] Section
ALWAYS include these baseline rules:
```
- Do not introduce yourself.
- Do not mention tools, APIs, or internal systems.
- Do not repeat or reconfirm details the caller already provided unless needed for clarification.
- Never ask for details already collected in the same call.
- Never go off topic. Redirect politely if the caller strays.
- Keep all responses short, natural, and conversational.
- If the caller ends the conversation (bye, goodbye, thanks), immediately trigger endCall.
- Never summarize or recap the entire call before ending.
- Sound warm, confident, and human - never robotic or scripted. If a reply sounds too formal, shorten it or rephrase it like normal conversation.
- If about to transfer the call, do NOT send any text response. Simply trigger the tool silently.
```

### Deterministic Data Handling (for collecting names, phones, emails)

When the assistant needs to collect personal information, switch to strict literal mode:

```
[Deterministic Data Handling]
When collecting names, phone numbers, or emails:
- Use the caller's provided information exactly as given, with no changes, corrections, or phonetic guesses.
- Do not infer or adjust unfamiliar names. If unclear, ask the caller politely to repeat or spell it.
- Ask only the exact scripted questions during data collection with no added words before or after them.
- Keep acknowledgments minimal ("Got it", "Thank you") with no commentary.
- Request clarification if unclear: "Could you please repeat or spell that again?"
- Confirm phone number once only by repeating it back digit by digit.
- Never reconfirm email addresses.
```

### Anti-Patterns (NEVER Do These in Any Prompt)

| Anti-Pattern | Why It Sounds AI | Fix |
|-------------|------------------|-----|
| "How can I assist you today?" | No human says "assist" | "How can I help you?" or "What do you need?" |
| "Is there anything else I can help you with today?" | Overly formal closing | "Anything else?" or "What else can I do?" |
| "I understand your concern." | Scripted empathy | "Oh I see." or "Ah, got it." or "No worries." |
| "Thank you for your patience." | Call center script | "Sorry about the wait!" or "Thanks for hanging on." |
| "Let me provide you with..." | Written language | "So here's the deal..." or "Okay so..." |
| "I apologize for the inconvenience." | Corporate boilerplate | "Sorry about that!" |
| "Absolutely!" (to every response) | Fake enthusiasm pattern | Vary: "Sure thing", "Alright", "Got it", "Done." |
| Long multi-sentence responses | No one monologues on calls | Max 2-3 sentences per turn |
| Perfect grammar at all times | Real people use fragments | "Right, so..." "Yeah, no, totally." |
| Asking multiple questions at once | Overwhelming on a phone call | One question per turn, always |
| Saying "pause" or "break" out loud | Stage direction leak | Just stop speaking naturally |
| Repeating the same info back | Wastes time, feels robotic | Confirm once, move on |
| Including the year in dates | No one says "January 12th, 2026" | Just say "January twelfth" |
| Using digit-by-digit for dates/times | Unnatural | Say "seven thirty" not "7-3-0" |

---

## Voice & Timing Configuration for Realism

**Use these settings for every assistant:**

```json
{
  "voice": {
    "provider": "cartesia",
    "voiceId": "<language-appropriate-voice-id>",
    "cachingEnabled": true,
    "chunkPlan": {
      "enabled": true,
      "minCharacters": 30
    }
  },
  "startSpeakingPlan": {
    "waitSeconds": 0.4,
    "smartEndpointingEnabled": true,
    "transcriptionEndpointingPlan": {
      "onPunctuationSeconds": 0.1,
      "onNoPunctuationSeconds": 1.5,
      "onNumberSeconds": 0.5
    }
  },
  "stopSpeakingPlan": {
    "numWords": 0,
    "voiceSeconds": 0.2,
    "backoffSeconds": 1.0
  },
  "backgroundSound": "office"
}
```

Why these values:
- `waitSeconds: 0.4` — slight pause before responding, like a human processing
- `smartEndpointingEnabled: true` — AI detects when the caller is done (prevents cutting off)
- `onPunctuationSeconds: 0.1` — fast response after clear sentence endings
- `onNoPunctuationSeconds: 1.5` — waits longer when caller might still be talking
- `onNumberSeconds: 0.5` — gives time after numbers (phone numbers, dates)
- `numWords: 0` — allows interruption immediately (natural conversation)
- `voiceSeconds: 0.2` — quick to detect caller is interrupting
- `backoffSeconds: 1.0` — waits 1s after being interrupted before trying again
- `backgroundSound: "office"` — ambient noise makes it feel real, not a digital void

---

## Advanced Plans

### Start Speaking Plan — Controls when assistant starts responding:
```json
{
  "startSpeakingPlan": {
    "waitSeconds": 0.4,
    "smartEndpointingEnabled": true,
    "transcriptionEndpointingPlan": {
      "onPunctuationSeconds": 0.1,
      "onNoPunctuationSeconds": 1.5,
      "onNumberSeconds": 0.5
    }
  }
}
```

### Stop Speaking Plan — Controls interruption handling:
```json
{
  "stopSpeakingPlan": {
    "numWords": 0,
    "voiceSeconds": 0.2,
    "backoffSeconds": 1
  }
}
```

### Analysis Plan — Post-call analysis:
```json
{
  "analysisPlan": {
    "summaryPlan": { "enabled": true },
    "structuredDataPlan": {
      "enabled": true,
      "schema": {
        "type": "object",
        "properties": {
          "customerName": { "type": "string" },
          "issue": { "type": "string" },
          "resolved": { "type": "boolean" }
        }
      }
    },
    "successEvaluationPlan": {
      "enabled": true,
      "rubric": "NumericScale"
    }
  }
}
```

---

## Adding Tools

Attach tools so the assistant can take actions during calls. See the `create-tool` skill for full tool creation details.

### endCall Tool (MANDATORY)

**Every assistant MUST include the `endCall` tool.** Without it, calls run until `maxDurationSeconds` or the caller hangs up.

```json
{
  "model": {
    "tools": [
      { "type": "endCall" }
    ]
  }
}
```

### Using saved tool IDs

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-5.2-instant",
    "toolIds": ["tool-id-1", "tool-id-2"],
    "messages": [{"role": "system", "content": "..."}]
  }
}
```

### Inline tool definition

```json
{
  "model": {
    "tools": [
      { "type": "endCall" },
      {
        "type": "function",
        "function": {
          "name": "check_availability",
          "description": "Check appointment availability for a given date",
          "parameters": {
            "type": "object",
            "properties": {
              "date": { "type": "string", "description": "Date in YYYY-MM-DD format" }
            },
            "required": ["date"]
          }
        },
        "server": { "url": "https://your-server.com/api/tools" }
      }
    ],
    "messages": [{"role": "system", "content": "..."}]
  }
}
```

---

## Hooks

Automate actions when specific call events occur. See [hooks reference](references/hooks.md) for full details.

```json
{
  "hooks": [
    {
      "on": "customer.speech.timeout",
      "options": {
        "timeoutSeconds": 10,
        "triggerMaxCount": 3
      },
      "do": [
        {
          "type": "say",
          "exact": "Are you still there?"
        }
      ]
    },
    {
      "on": "call.ending",
      "filters": [
        {
          "type": "oneOf",
          "key": "call.endedReason",
          "oneOf": ["pipeline-error"]
        }
      ],
      "do": [
        {
          "type": "tool",
          "tool": {
            "type": "transferCall",
            "destinations": [
              { "type": "number", "number": "+1234567890" }
            ]
          }
        }
      ]
    }
  ]
}
```

**Available hook events:** `call.ending`, `assistant.speech.interrupted`, `customer.speech.interrupted`, `customer.speech.timeout`, `assistant.transcriber.endpointedSpeechLowConfidence`

---

## Managing Assistants

### List

```bash
curl https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get

```bash
curl https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update

```bash
curl -X PATCH https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "firstMessage": "Updated greeting!"
  }'
```

### Delete

```bash
curl -X DELETE https://api.vapi.ai/assistant/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

---

## Common Patterns & Recipes

### Inbound Customer Support Agent
```json
{
  "name": "Support Agent",
  "firstMessage": "Thank you for calling support. How can I help you today?",
  "firstMessageMode": "assistant-speaks-first",
  "model": {
    "provider": "openai",
    "model": "gpt-5.2-instant",
    "messages": [{
      "role": "system",
      "content": "You are a friendly customer support agent. Be concise, helpful, and empathetic. If you cannot resolve the issue, offer to transfer to a human agent."
    }],
    "temperature": 0.3,
    "tools": [{ "type": "endCall" }]
  },
  "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "en" },
  "voice": { "provider": "cartesia", "voiceId": "<cartesia-voice-id>" },
  "endCallMessage": "Thank you for calling. Have a great day!",
  "endCallPhrases": ["goodbye", "that's all"],
  "maxDurationSeconds": 900,
  "backgroundSound": "office",
  "backchannelingEnabled": true
}
```

### Outbound Sales/Appointment Caller
```json
{
  "name": "Appointment Setter",
  "firstMessage": "Hi {{name}}, this is Sarah from Dr. Smith's office. I'm calling about your upcoming appointment. Do you have a moment?",
  "model": {
    "provider": "openai",
    "model": "gpt-5.2-instant",
    "messages": [{
      "role": "system",
      "content": "You are a friendly appointment coordinator. Your goal is to confirm or reschedule the patient's appointment. Be brief and professional."
    }],
    "temperature": 0.4,
    "tools": [{ "type": "endCall" }]
  },
  "voicemailDetection": {
    "provider": "twilio",
    "enabled": true
  },
  "voicemailMessage": "Hi {{name}}, this is Dr. Smith's office calling about your appointment. Please call us back at 555-0123.",
  "maxDurationSeconds": 300
}
```

### Conditional Call Forwarding Agent
```json
{
  "name": "Call Router",
  "firstMessage": "Welcome to Acme Corp. Let me connect you with the right department.",
  "model": {
    "provider": "openai",
    "model": "gpt-5.2-instant",
    "messages": [{
      "role": "system",
      "content": "You are a call routing agent. Determine the caller's need and transfer them. Departments: Sales (extension 1), Support (extension 2), Billing (extension 3)."
    }],
    "tools": [
      { "type": "endCall" },
      {
        "type": "transferCall",
        "destinations": [
          { "type": "number", "number": "+15551001001", "message": "Transferring to Sales..." },
          { "type": "number", "number": "+15551001002", "message": "Transferring to Support..." },
          { "type": "number", "number": "+15551001003", "message": "Transferring to Billing..." }
        ]
      }
    ]
  }
}
```

### Multilingual Agent
```json
{
  "name": "Multilingual Support",
  "firstMessage": "Hello! How can I help you? / Hola! Como puedo ayudarte?",
  "model": {
    "provider": "openai",
    "model": "gpt-5.2-instant",
    "messages": [{
      "role": "system",
      "content": "You are a multilingual support assistant. Detect the caller's language and respond in the same language. You support English and Spanish."
    }],
    "tools": [{ "type": "endCall" }]
  },
  "voice": { "provider": "vapi", "voiceId": "Paola" },
  "transcriber": { "provider": "deepgram", "model": "nova-3", "language": "multi" }
}
```

---

## Cost & Latency Optimization (DEFAULTS)

**Always optimize for the lowest per-minute cost and fastest response time unless the user explicitly requests a premium configuration.**

### Default Stack (Lowest Cost + Lowest Latency)

| Component | Default | Why |
|-----------|---------|-----|
| **LLM** | `openai` / `gpt-5.2-instant` | Fastest OpenAI model, lowest cost per token, excellent for conversational tasks |
| **Transcriber** | `deepgram` / `nova-3` | Industry-standard STT, low latency, best price-to-accuracy ratio |
| **Voice** | `cartesia` | Low-latency, high-quality voice provider, excellent for real-time |
| **Temperature** | `0.7` | Good balance of creativity and consistency for conversation |
| **Max Tokens** | `250` | Keep responses short for phone calls (2-3 sentences) |

### When to Upgrade

| Situation | Upgrade To | Trade-off |
|-----------|-----------|-----------|
| Complex reasoning / multi-step logic | `gpt-4o` or `gpt-5.2` | Higher cost, slower, but more capable |
| Multilingual with high accuracy needs | `gpt-4o` + `gladia` transcriber | Better cross-language understanding |
| Ultra-low latency requirement | `groq` / `llama-3.1-70b` | Fastest possible, slightly lower quality |
| Premium/luxury brand experience | `gpt-5.2` + `11labs` cloned voice | Highest quality, highest cost |

### Latency Tips
- Enable `cachingEnabled: true` on voice to cache common phrases
- Use `smartEndpointingEnabled: true` to reduce unnecessary waiting
- Set `maxTokens: 250` to prevent long monologues (faster TTS)
- Use `chunkPlan.minCharacters: 30` to start speaking sooner
- Background sound `"office"` adds realism without adding latency

---

## Testing & Debugging

1. **Test via dashboard:** Go to dashboard.vapi.ai → select assistant → "Talk to Assistant"
2. **Test via API:** Create a test call using the API:
   ```bash
   curl -X POST https://api.vapi.ai/call \
     -H "Authorization: Bearer $VAPI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "assistantId": "<assistant-id>",
       "type": "webCall"
     }'
   ```
3. **Test webhooks locally:**
   ```bash
   # Start a tunnel to expose your local server
   ngrok http 3000
   ```
   Then set the ngrok URL as your assistant's `serverUrl` via the API.
4. **View call logs:** Use the dashboard at dashboard.vapi.ai → Calls, or fetch via API:
   ```bash
   curl https://api.vapi.ai/call/<call-id> \
     -H "Authorization: Bearer $VAPI_API_KEY"
   ```

---

## Workflow for Claude Code Sessions

When working in a Claude Code session to build Vapi assistants:

1. **Set up environment:** Ensure `VAPI_API_KEY` is set

2. **Confirm configuration with user (MANDATORY):**
   Before creating any assistant, you MUST use `AskUserQuestion` to confirm the following. Present sensible defaults but let the user override:

   **Question 1 — Language & Voice:**
   - What language should the assistant speak? (Default: English)
   - What voice gender? (Default: Female)
   - These determine the voice selection from the Voice Selection Guide.

   **Question 2 — Model & Provider:**
   - LLM: gpt-5.2-instant (Recommended — lowest cost) vs gpt-4o (better reasoning) vs other
   - Voice provider: Cartesia (Recommended) vs ElevenLabs vs OpenAI vs other

   **Question 3 — Use Case Specifics:**
   - Inbound or outbound calls?
   - Does the assistant need tools/API integrations?
   - Any specific business details to include (hours, fees, policies)?

   Example AskUserQuestion:
   ```
   questions: [
     {
       question: "What language and voice gender should the assistant use?",
       header: "Voice",
       options: [
         { label: "Female English (Recommended)", description: "Sarah - soft, warm voice ideal for customer interactions" },
         { label: "Male English", description: "Chris - casual, friendly voice" },
         { label: "Female Hindi", description: "Kanika - friendly, approachable Hindi voice" },
         { label: "Male Hindi", description: "Viraj - warm, professional Hindi voice" }
       ],
       multiSelect: false
     },
     {
       question: "Which model should power the assistant?",
       header: "Model",
       options: [
         { label: "gpt-5.2-instant (Recommended)", description: "Lowest cost, fastest response, great for most use cases" },
         { label: "gpt-4o", description: "Good reasoning, moderate cost, for complex multi-step flows" },
         { label: "Claude 3.5 Sonnet", description: "Anthropic model, great instruction following" }
       ],
       multiSelect: false
     }
   ]
   ```

3. **Create assistant JSON config:** Build based on confirmed settings. **ALWAYS include the `endCall` tool**.
4. **Deploy via API:** Use `curl` or the SDK to POST to the API
5. **Save assistant folder:** Create a folder in `assistants/<slug-name>/` with `profile.md`
6. **Write sample transcripts:** Create `assistants/<slug-name>/transcripts.md` with 3-4 realistic call transcripts
7. **Assign phone number:** Use the API to create or update a phone number (see `create-phone-number` skill)
8. **Test:** Create a test call via the API or test from dashboard.vapi.ai
9. **Iterate:** PATCH the assistant via API with refined config — update profile and transcripts
10. **Monitor:** Check call logs in the dashboard at dashboard.vapi.ai → Calls

---

## Assistant Profile Files (REQUIRED)

**Every time a new assistant is created, you MUST create a dedicated folder and files for it.**

### Folder Structure

```
assistants/
├── able-hvac-support/
│   ├── profile.md
│   ├── tools.md
│   └── transcripts.md
├── restaurant-table-booking/
│   ├── profile.md
│   └── transcripts.md
└── ...
```

### Profile File (profile.md)

```markdown
# <Assistant Name>

## Overview
| Field | Value |
|-------|-------|
| **Assistant ID** | `<id from API response>` |
| **Created** | `<date>` |
| **Status** | Active / Inactive |

## Configuration Summary
| Component | Provider | Model/Voice |
|-----------|----------|-------------|
| **LLM** | <provider> | <model> |
| **Transcriber** | <provider> | <model> |
| **Voice** | <provider> | <voiceId> (<voice name>) |

## System Prompt
<Full system prompt text in a fenced code block>

## Conversation Settings
- **First Message:** <text>
- **End Call Message:** <text>
- **End Call Phrases:** <list>
- **Max Duration:** <seconds>
- **Background Sound:** <value>
- **Silence Timeout:** <seconds>

## Advanced Plans
<startSpeakingPlan, stopSpeakingPlan settings>

## Analysis Plan
<structuredDataPlan schema, successEvaluation settings>

## Full API Config (JSON)
<Complete JSON payload used to create/update the assistant>

## Change Log
| Date | Change |
|------|--------|
| <date> | Initial creation |
```

### Sample Transcripts File (transcripts.md) — REQUIRED

**You MUST create 3-4 sample call transcripts for every assistant.** These serve as documentation and QA testing material.

Each transcript must follow this structure:

```markdown
# <Assistant Name> — Sample Transcripts

These transcripts demonstrate how the <Assistant Name> assistant (<persona name>) handles different call scenarios.

---

## Transcript 1: <Scenario Title>

**Scenario:** <1-2 sentence description>

---

**<Persona>:** <firstMessage>

**Caller:** <realistic caller dialogue>

**<Persona>:** <assistant response following style and task flow>

...full conversation through to endCall...

*[endCall triggered]*

---

**Structured Data Output:**
<JSON block showing analysisPlan data extracted from this call>
```

**Transcript requirements:**
- Write **3-4 transcripts** covering different paths (happy path, edge case, escalation, off-topic redirect)
- Use the assistant's **exact persona name, firstMessage, and style rules**
- Dialogue must sound **natural** — include hesitations, interruptions, follow-up questions
- Follow the **one-question-at-a-time** rule
- Show the **endCall trigger** at the end
- Include **Structured Data Output** JSON block
- Cover: 1) Happy path, 2) New vs returning user, 3) Edge case/escalation, 4) Information-only call

---

## Important Notes

- Phone calls default to "office" background sound; web calls default to "off"
- Max call duration default is 600 seconds (10 minutes), configurable up to 43,200 (12 hours)
- Assistant names are limited to 40 characters
- For transferring between assistants in a squad, the `name` field is required

---

## References

- [API Reference](references/api-reference.md) — Complete REST API docs (Create, List, Get, Update, Delete) with cURL examples
- [Hooks Configuration](references/hooks.md) — Complete hook events and actions
- [Voice & Model Providers](references/providers.md) — All supported providers and models
- [Voice Selection Guide](references/voice-selection.md) — Voice IDs for English, Hindi, and 11+ languages
- [Vapi API Docs](https://docs.vapi.ai/assistants/quickstart) — Official documentation

## Red Flags — Common Mistakes

These shortcuts ALWAYS cause problems. Do not rationalize your way around them.

| Temptation | Why It Fails |
|------------|-------------|
| "I'll skip the system prompt for now" | Assistants without system prompts give generic, useless responses. Always write one. |
| "I know the voice ID from memory" | Voice IDs change. Always check `references/voice-selection.md` or the API. |
| "Default transcriber settings are fine" | Wrong language or model = garbled transcripts. Always set language explicitly. |
| "I'll add tools later" | If the prompt references tools, the assistant breaks without them. Add tools now. |
| "One big system prompt paragraph works" | Long unstructured prompts confuse the model. Use sections: Identity, Style, Task, Rules. |
| "I'll test it after I finish everything" | Create → Test → Fix. Don't batch. Test each assistant immediately after creation. |
| "I can guess the API payload format" | Vapi's API has specific field names and nesting. Always follow the skill's examples exactly. |
| "endCallPhrases aren't important" | Without them, calls hang or end abruptly. Always define natural goodbye phrases. |

## Required Sub-Skills

These skills MUST be invoked when their conditions are met — they are not optional:

- **REQUIRED:** `vapi-voice-ai:setup-api-key` — Before ANY API call, verify the API key is set
- **REQUIRED:** `vapi-voice-ai:create-tool` — When the assistant needs tools (booking, lookup, transfer, etc.)
- **REQUIRED:** `vapi-voice-ai:setup-webhook` — When tools need a server URL to handle function calls
- **REQUIRED:** `vapi-voice-ai:create-phone-number` — When the assistant needs to receive inbound calls
- **RECOMMENDED:** `vapi-voice-ai:create-call` — To test the assistant after creation

## Related Skills

- `setup-api-key` — Set up Vapi API key
- `create-tool` — Create custom tools for assistants
- `create-call` — Make outbound calls
- `create-squad` — Build multi-assistant squads
- `create-phone-number` — Set up phone numbers
- `setup-webhook` — Configure webhooks
- `create-workflow` — Build visual conversation workflows
