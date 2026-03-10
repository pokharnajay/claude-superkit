---
name: create-phone-number
description: Set up and manage phone numbers in Vapi for inbound and outbound voice AI calls. Use when importing Twilio, Vonage, or Telnyx numbers, buying Vapi numbers, or configuring phone numbers for assistants.
---

# Create & Manage Phone Numbers

This skill covers provisioning, importing, configuring, and managing phone numbers in Vapi for inbound and outbound voice AI calls. Phone numbers are required to make or receive real phone calls with your voice assistants.

## Prerequisites

- Vapi account with API key configured (see the `setup-api-key` skill)
- For imports: an active account with Twilio, Vonage, or Telnyx

## Quick Start — Buy a Vapi Number

The fastest way to get a phone number is to buy a free Vapi number via the API:

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "provider": "vapi",
    "numberDesiredAreaCode": "415"
  }'
```

Or via the Dashboard:
1. Open [Vapi Dashboard](https://dashboard.vapi.ai) > **Phone Numbers** tab.
2. Click **Create a Phone Number**.
3. Select **Vapi** as the provider and pick an area code.

### Free Number Limitations

- Limited to **US national use only** (no international calling).
- Maximum **10 free numbers** per account.
- Daily outbound call limits apply.
- No SMS support.
- For international or high-volume use, import from Twilio, Vonage, or Telnyx.

## Import from Twilio

Import an existing Twilio number by providing your Twilio credentials:

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "provider": "twilio",
    "number": "+14155551234",
    "twilioAccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "twilioAuthToken": "your_twilio_auth_token"
  }'
```

**What happens during import:**
- Vapi verifies the number with Twilio using your credentials.
- The number's webhook is updated to point to Vapi's SIP infrastructure.
- Inbound calls to this number will be routed through Vapi.

> **Note:** You can also import via the Dashboard: **Phone Numbers** > **Create a Phone Number** > select **Twilio** tab.

## Import from Vonage

Import a Vonage number using a Vapi credential ID:

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "provider": "vonage",
    "number": "+14155551234",
    "credentialId": "your-vonage-credential-id"
  }'
```

**Setup steps:**
1. Add your Vonage API key and secret in the [Vapi Dashboard](https://dashboard.vapi.ai) under **Integrations** > **Vonage**.
2. Note the `credentialId` returned after adding the credential.
3. Use that `credentialId` in the import request above.

## Import from Telnyx

Import a Telnyx number using a Vapi credential ID:

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "provider": "telnyx",
    "number": "+14155551234",
    "credentialId": "your-telnyx-credential-id"
  }'
```

**Setup steps:**
1. Add your Telnyx API key in the [Vapi Dashboard](https://dashboard.vapi.ai) under **Integrations** > **Telnyx**.
2. Note the `credentialId`.
3. Use it in the import request above.

**Outbound calling with Telnyx** requires additional configuration:
1. Log in to the [Telnyx Portal](https://portal.telnyx.com/#/outbound-profiles).
2. Create or edit an **Outbound Voice Profile**.
3. Under **Connections and Applications**, add Vapi as a connection.
4. Save the configuration.

Without this step, outbound calls from Telnyx numbers will fail.

## Assign an Assistant to a Phone Number

Assign a saved assistant so all inbound calls are handled automatically:

```bash
curl -X PATCH https://api.vapi.ai/phone-number/<phone-number-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistantId": "your-assistant-id"
  }'
```

> See the `create-assistant` skill for building the assistant to attach.

## Assign a Squad to a Phone Number

For multi-assistant workflows, assign a squad instead:

```bash
curl -X PATCH https://api.vapi.ai/phone-number/<phone-number-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "squadId": "your-squad-id"
  }'
```

> See the `create-squad` skill for building squads with handoff logic.

## Phone Number Hooks

Hooks let you dynamically control which assistant handles calls. Leave `assistantId` blank and configure a server URL to receive the `assistant-request` event:

```json
{
  "serverUrl": "https://your-server.com/api/vapi",
  "serverUrlSecret": "optional-shared-secret"
}
```

Your server receives a webhook with caller info and returns the assistant configuration:

```json
{
  "assistant": {
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant for the caller from {{callerNumber}}."
        }
      ]
    },
    "voice": { "provider": "cartesia", "voiceId": "your-voice-id" },
    "firstMessage": "Hello! How can I help you today?"
  }
}
```

This allows routing different callers to different assistants based on caller ID, time of day, or any custom logic.

## Managing Phone Numbers

### List All Numbers

```bash
curl https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Get a Specific Number

```bash
curl https://api.vapi.ai/phone-number/<phone-number-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### Update a Number

```bash
curl -X PATCH https://api.vapi.ai/phone-number/<phone-number-id> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "name": "Support Line",
    "assistantId": "new-assistant-id"
  }'
```

### Delete a Number

```bash
curl -X DELETE https://api.vapi.ai/phone-number/<phone-number-id> \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Inbound Call Flow

When someone calls your Vapi phone number, the following happens:

1. **Ring** — Vapi receives the inbound call from the telephony provider (Vapi, Twilio, Vonage, or Telnyx).
2. **Assistant Resolution** — Vapi checks if an `assistantId` is assigned. If not, it sends an `assistant-request` webhook to your `serverUrl`.
3. **Call Setup** — The resolved assistant's transcriber, model, and voice are initialized. The `firstMessage` is spoken.
4. **Conversation** — The assistant handles the conversation, calling tools and following its prompt until the call ends.

## Outbound Call Flow

When you initiate an outbound call via the API:

1. **API Request** — You POST to `/call` with `phoneNumberId`, `assistantId` (or inline `assistant`), and `customer.number`.
2. **Dialing** — Vapi places the call through the phone number's provider. Call status transitions: `queued` > `ringing` > `in-progress`.
3. **Conversation** — Once the customer answers, the assistant begins the conversation using its configured `firstMessage` and prompt.

> See the `create-call` skill for making outbound calls.

## Provider Comparison

| Feature | Vapi (Free) | Twilio | Vonage | Telnyx |
|---------|-------------|--------|--------|--------|
| Cost | Free | Pay-as-you-go | Pay-as-you-go | Pay-as-you-go |
| US Numbers | Yes | Yes | Yes | Yes |
| International | No | Yes | Yes | Yes |
| SMS | No | Yes | Yes | Yes |
| Limit | 10/account | Unlimited | Unlimited | Unlimited |
| Best For | Testing/prototyping | Production US/intl | Production intl | Production intl |

## References

- [API Reference](references/api-reference.md) — Complete REST API docs for Phone Numbers (5 endpoints) with provider-specific examples

## Related Skills

- See the `setup-api-key` skill if you need to configure your API key first.
- See the `create-assistant` skill to build an assistant to attach to a number.
- See the `create-squad` skill for multi-assistant setups on a single number.
- See the `create-call` skill to make outbound calls using your numbers.
- See the `setup-webhook` skill to configure dynamic assistant routing via webhooks.
