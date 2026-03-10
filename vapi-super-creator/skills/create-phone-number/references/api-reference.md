# Phone Number API Reference

> **Base URL:** `https://api.vapi.ai`
> **Authentication:** `Authorization: Bearer $VAPI_API_KEY`

---

## Table of Contents

- [1. Create Phone Number](#1-create-phone-number)
- [2. List Phone Numbers](#2-list-phone-numbers)
- [3. Get Phone Number](#3-get-phone-number)
- [4. Update Phone Number](#4-update-phone-number)
- [5. Delete Phone Number](#5-delete-phone-number)
- [PhoneNumber Response Schema](#phonenumber-response-schema)
- [Inbound vs Outbound Call Flow](#inbound-vs-outbound-call-flow)
- [Provider-Specific Limitations](#provider-specific-limitations)

---

## 1. Create Phone Number

Provisions a new phone number from one of the supported providers (Vapi, Twilio, Vonage, Telnyx) and registers it with your Vapi organization.

### HTTP Request

```
POST https://api.vapi.ai/phone-number
```

### Headers

| Header          | Value                        | Required |
|-----------------|------------------------------|----------|
| `Authorization` | `Bearer $VAPI_API_KEY`       | Yes      |
| `Content-Type`  | `application/json`           | Yes      |

### Request Body

The request body structure depends on the `provider` field. Four providers are supported:

#### Provider: `vapi` (Free Vapi Numbers)

Vapi provisions a number for you automatically. You only specify an optional area code.

```json
{
  "provider": "vapi",
  "assistantId": "string (optional) - ID of the assistant to handle inbound calls",
  "squadId": "string (optional) - ID of the squad to handle inbound calls (mutually exclusive with assistantId)",
  "name": "string (optional) - Friendly display name for the phone number",
  "numberDesiredAreaCode": "string (optional) - Desired US area code, e.g. '415'"
}
```

#### Provider: `twilio` (Bring Your Own Twilio)

You must supply a Twilio number you already own plus your Twilio credentials.

```json
{
  "provider": "twilio",
  "number": "string (required) - E.164 format phone number, e.g. '+14155551234'",
  "twilioAccountSid": "string (required) - Your Twilio Account SID",
  "twilioAuthToken": "string (required) - Your Twilio Auth Token",
  "assistantId": "string (optional) - ID of the assistant to handle inbound calls",
  "squadId": "string (optional) - ID of the squad to handle inbound calls",
  "name": "string (optional) - Friendly display name",
  "smsEnabled": "boolean (optional) - Enable SMS capabilities (Twilio US numbers only)"
}
```

#### Provider: `vonage` (Bring Your Own Vonage)

You must supply a Vonage number and a pre-configured Vonage credential ID.

```json
{
  "provider": "vonage",
  "number": "string (required) - E.164 format phone number, e.g. '+14155551234'",
  "credentialId": "string (required) - ID of the Vonage credential in Vapi",
  "assistantId": "string (optional) - ID of the assistant to handle inbound calls",
  "squadId": "string (optional) - ID of the squad to handle inbound calls",
  "name": "string (optional) - Friendly display name"
}
```

#### Provider: `telnyx` (Bring Your Own Telnyx)

You must supply a Telnyx number and a pre-configured Telnyx credential ID.

```json
{
  "provider": "telnyx",
  "number": "string (required) - E.164 format phone number, e.g. '+14155551234'",
  "credentialId": "string (required) - ID of the Telnyx credential in Vapi",
  "assistantId": "string (optional) - ID of the assistant to handle inbound calls",
  "squadId": "string (optional) - ID of the squad to handle inbound calls",
  "name": "string (optional) - Friendly display name"
}
```

### Response

**Status:** `201 Created`

Returns the full [PhoneNumber object](#phonenumber-response-schema).

```json
{
  "id": "phn_abc123def456",
  "orgId": "org_xyz789",
  "number": "+14155551234",
  "provider": "vapi",
  "assistantId": "asst_abc123",
  "squadId": null,
  "name": "Sales Line",
  "serverUrl": null,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

#### Vapi Provider (Free Number)

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "vapi",
    "name": "Sales Line",
    "numberDesiredAreaCode": "415",
    "assistantId": "asst_abc123def456"
  }'
```

#### Twilio Provider (Bring Your Own)

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "twilio",
    "number": "+14155551234",
    "twilioAccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "twilioAuthToken": "your_twilio_auth_token",
    "name": "Twilio Support Line",
    "assistantId": "asst_abc123def456",
    "smsEnabled": true
  }'
```

#### Vonage Provider (Bring Your Own)

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "vonage",
    "number": "+442071234567",
    "credentialId": "cred_vonage_abc123",
    "name": "UK Support Line",
    "assistantId": "asst_abc123def456"
  }'
```

#### Telnyx Provider (Bring Your Own)

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "telnyx",
    "number": "+14085559876",
    "credentialId": "cred_telnyx_def456",
    "name": "Telnyx Inbound Line",
    "assistantId": "asst_abc123def456"
  }'
```

### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// Vapi provider (free number)
const vapiNumber = await vapi.phoneNumbers.create({
  provider: "vapi",
  name: "Sales Line",
  numberDesiredAreaCode: "415",
  assistantId: "asst_abc123def456",
});
console.log("Created Vapi number:", vapiNumber.number);

// Twilio provider (bring your own)
const twilioNumber = await vapi.phoneNumbers.create({
  provider: "twilio",
  number: "+14155551234",
  twilioAccountSid: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  twilioAuthToken: "your_twilio_auth_token",
  name: "Twilio Support Line",
  assistantId: "asst_abc123def456",
  smsEnabled: true,
});
console.log("Registered Twilio number:", twilioNumber.number);

// Vonage provider (bring your own)
const vonageNumber = await vapi.phoneNumbers.create({
  provider: "vonage",
  number: "+442071234567",
  credentialId: "cred_vonage_abc123",
  name: "UK Support Line",
  assistantId: "asst_abc123def456",
});
console.log("Registered Vonage number:", vonageNumber.number);

// Telnyx provider (bring your own)
const telnyxNumber = await vapi.phoneNumbers.create({
  provider: "telnyx",
  number: "+14085559876",
  credentialId: "cred_telnyx_def456",
  name: "Telnyx Inbound Line",
  assistantId: "asst_abc123def456",
});
console.log("Registered Telnyx number:", telnyxNumber.number);
```

### Python Example

```python
import requests
import os

VAPI_API_KEY = os.environ["VAPI_API_KEY"]
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

# Vapi provider (free number)
response = requests.post(
    f"{BASE_URL}/phone-number",
    headers=HEADERS,
    json={
        "provider": "vapi",
        "name": "Sales Line",
        "numberDesiredAreaCode": "415",
        "assistantId": "asst_abc123def456",
    },
)
vapi_number = response.json()
print(f"Created Vapi number: {vapi_number['number']}")

# Twilio provider (bring your own)
response = requests.post(
    f"{BASE_URL}/phone-number",
    headers=HEADERS,
    json={
        "provider": "twilio",
        "number": "+14155551234",
        "twilioAccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "twilioAuthToken": "your_twilio_auth_token",
        "name": "Twilio Support Line",
        "assistantId": "asst_abc123def456",
        "smsEnabled": True,
    },
)
twilio_number = response.json()
print(f"Registered Twilio number: {twilio_number['number']}")

# Vonage provider (bring your own)
response = requests.post(
    f"{BASE_URL}/phone-number",
    headers=HEADERS,
    json={
        "provider": "vonage",
        "number": "+442071234567",
        "credentialId": "cred_vonage_abc123",
        "name": "UK Support Line",
        "assistantId": "asst_abc123def456",
    },
)
vonage_number = response.json()
print(f"Registered Vonage number: {vonage_number['number']}")

# Telnyx provider (bring your own)
response = requests.post(
    f"{BASE_URL}/phone-number",
    headers=HEADERS,
    json={
        "provider": "telnyx",
        "number": "+14085559876",
        "credentialId": "cred_telnyx_def456",
        "name": "Telnyx Inbound Line",
        "assistantId": "asst_abc123def456",
    },
)
telnyx_number = response.json()
print(f"Registered Telnyx number: {telnyx_number['number']}")
```

### Doc Reference

- [https://docs.vapi.ai/api-reference/phone-numbers/create](https://docs.vapi.ai/api-reference/phone-numbers/create)

---

## 2. List Phone Numbers

Retrieves all phone numbers registered to your organization with optional filtering and pagination.

### HTTP Request

```
GET https://api.vapi.ai/phone-number
```

### Headers

| Header          | Value                        | Required |
|-----------------|------------------------------|----------|
| `Authorization` | `Bearer $VAPI_API_KEY`       | Yes      |

### Query Parameters

| Parameter       | Type   | Description                                                      |
|-----------------|--------|------------------------------------------------------------------|
| `limit`         | number | Maximum number of results to return. Default varies by plan.     |
| `createdAtGt`   | string | Filter: created after this ISO 8601 timestamp (exclusive).       |
| `createdAtLt`   | string | Filter: created before this ISO 8601 timestamp (exclusive).      |
| `createdAtGe`   | string | Filter: created at or after this ISO 8601 timestamp (inclusive). |
| `createdAtLe`   | string | Filter: created at or before this ISO 8601 timestamp (inclusive).|
| `updatedAtGt`   | string | Filter: updated after this ISO 8601 timestamp (exclusive).      |
| `updatedAtLt`   | string | Filter: updated before this ISO 8601 timestamp (exclusive).     |
| `updatedAtGe`   | string | Filter: updated at or after this ISO 8601 timestamp (inclusive). |
| `updatedAtLe`   | string | Filter: updated at or before this ISO 8601 timestamp (inclusive).|

### Response

**Status:** `200 OK`

Returns an array of [PhoneNumber objects](#phonenumber-response-schema).

```json
[
  {
    "id": "phn_abc123def456",
    "orgId": "org_xyz789",
    "number": "+14155551234",
    "provider": "vapi",
    "assistantId": "asst_abc123",
    "squadId": null,
    "name": "Sales Line",
    "serverUrl": null,
    "createdAt": "2025-01-15T10:30:00.000Z",
    "updatedAt": "2025-01-15T10:30:00.000Z"
  },
  {
    "id": "phn_def789ghi012",
    "orgId": "org_xyz789",
    "number": "+14085559876",
    "provider": "twilio",
    "assistantId": "asst_def456",
    "squadId": null,
    "name": "Support Line",
    "serverUrl": "https://myserver.com/vapi-webhook",
    "createdAt": "2025-01-10T08:00:00.000Z",
    "updatedAt": "2025-01-12T14:22:00.000Z"
  }
]
```

### cURL Example

```bash
# List all phone numbers
curl -X GET https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY"

# List with filters
curl -X GET "https://api.vapi.ai/phone-number?limit=10&createdAtGe=2025-01-01T00:00:00.000Z" \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// List all phone numbers
const phoneNumbers = await vapi.phoneNumbers.list();
console.log(`Found ${phoneNumbers.length} phone numbers`);

for (const pn of phoneNumbers) {
  console.log(`  ${pn.name || "(unnamed)"} - ${pn.number} (${pn.provider})`);
}

// List with filters
const recentNumbers = await vapi.phoneNumbers.list({
  limit: 10,
  createdAtGe: "2025-01-01T00:00:00.000Z",
});
console.log(`Found ${recentNumbers.length} recent phone numbers`);
```

### Python Example

```python
import requests
import os

VAPI_API_KEY = os.environ["VAPI_API_KEY"]
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
}

# List all phone numbers
response = requests.get(f"{BASE_URL}/phone-number", headers=HEADERS)
phone_numbers = response.json()
print(f"Found {len(phone_numbers)} phone numbers")

for pn in phone_numbers:
    name = pn.get("name", "(unnamed)")
    print(f"  {name} - {pn['number']} ({pn['provider']})")

# List with filters
response = requests.get(
    f"{BASE_URL}/phone-number",
    headers=HEADERS,
    params={
        "limit": 10,
        "createdAtGe": "2025-01-01T00:00:00.000Z",
    },
)
recent_numbers = response.json()
print(f"Found {len(recent_numbers)} recent phone numbers")
```

### Doc Reference

- [https://docs.vapi.ai/api-reference/phone-numbers/list](https://docs.vapi.ai/api-reference/phone-numbers/list)

---

## 3. Get Phone Number

Retrieves the details of a single phone number by its ID.

### HTTP Request

```
GET https://api.vapi.ai/phone-number/{id}
```

### Headers

| Header          | Value                        | Required |
|-----------------|------------------------------|----------|
| `Authorization` | `Bearer $VAPI_API_KEY`       | Yes      |

### Path Parameters

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `id`      | string | Yes      | The unique ID of the phone number.       |

### Response

**Status:** `200 OK`

Returns the full [PhoneNumber object](#phonenumber-response-schema).

```json
{
  "id": "phn_abc123def456",
  "orgId": "org_xyz789",
  "number": "+14155551234",
  "provider": "vapi",
  "assistantId": "asst_abc123",
  "squadId": null,
  "name": "Sales Line",
  "serverUrl": null,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-15T10:30:00.000Z"
}
```

### cURL Example

```bash
curl -X GET https://api.vapi.ai/phone-number/phn_abc123def456 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const phoneNumber = await vapi.phoneNumbers.get("phn_abc123def456");

console.log("Phone Number Details:");
console.log(`  ID:        ${phoneNumber.id}`);
console.log(`  Number:    ${phoneNumber.number}`);
console.log(`  Provider:  ${phoneNumber.provider}`);
console.log(`  Name:      ${phoneNumber.name}`);
console.log(`  Assistant: ${phoneNumber.assistantId || "none"}`);
console.log(`  Squad:     ${phoneNumber.squadId || "none"}`);
console.log(`  Server:    ${phoneNumber.serverUrl || "none"}`);
console.log(`  Created:   ${phoneNumber.createdAt}`);
console.log(`  Updated:   ${phoneNumber.updatedAt}`);
```

### Python Example

```python
import requests
import os

VAPI_API_KEY = os.environ["VAPI_API_KEY"]
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
}

phone_number_id = "phn_abc123def456"
response = requests.get(
    f"{BASE_URL}/phone-number/{phone_number_id}",
    headers=HEADERS,
)
phone_number = response.json()

print("Phone Number Details:")
print(f"  ID:        {phone_number['id']}")
print(f"  Number:    {phone_number['number']}")
print(f"  Provider:  {phone_number['provider']}")
print(f"  Name:      {phone_number.get('name', 'none')}")
print(f"  Assistant: {phone_number.get('assistantId', 'none')}")
print(f"  Squad:     {phone_number.get('squadId', 'none')}")
print(f"  Server:    {phone_number.get('serverUrl', 'none')}")
print(f"  Created:   {phone_number['createdAt']}")
print(f"  Updated:   {phone_number['updatedAt']}")
```

### Doc Reference

- [https://docs.vapi.ai/api-reference/phone-numbers/get](https://docs.vapi.ai/api-reference/phone-numbers/get)

---

## 4. Update Phone Number

Updates properties of an existing phone number. Only the fields you include in the request body are changed; all other fields remain untouched.

### HTTP Request

```
PATCH https://api.vapi.ai/phone-number/{id}
```

### Headers

| Header          | Value                        | Required |
|-----------------|------------------------------|----------|
| `Authorization` | `Bearer $VAPI_API_KEY`       | Yes      |
| `Content-Type`  | `application/json`           | Yes      |

### Path Parameters

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `id`      | string | Yes      | The unique ID of the phone number.       |

### Request Body

All fields are optional. Only include the fields you want to change.

```json
{
  "assistantId": "string (optional) - New assistant ID for inbound calls. Set to null to unassign.",
  "squadId": "string (optional) - New squad ID for inbound calls. Set to null to unassign. Mutually exclusive with assistantId.",
  "name": "string (optional) - New friendly display name.",
  "serverUrl": "string (optional) - Webhook URL for server events on this number. Overrides org-level server URL.",
  "smsEnabled": "boolean (optional) - Enable/disable SMS. Only supported for Twilio US numbers."
}
```

| Field        | Type    | Description                                                                                   |
|--------------|---------|-----------------------------------------------------------------------------------------------|
| `assistantId`| string  | ID of the assistant to handle inbound calls. Set to `null` to unassign. Mutually exclusive with `squadId`. |
| `squadId`    | string  | ID of the squad to handle inbound calls. Set to `null` to unassign. Mutually exclusive with `assistantId`. |
| `name`       | string  | A human-readable display name for the phone number.                                           |
| `serverUrl`  | string  | A webhook URL that overrides the organization-level server URL for this specific number.       |
| `smsEnabled` | boolean | Enable or disable SMS capabilities. Only works with Twilio US numbers.                         |

### Response

**Status:** `200 OK`

Returns the updated [PhoneNumber object](#phonenumber-response-schema).

```json
{
  "id": "phn_abc123def456",
  "orgId": "org_xyz789",
  "number": "+14155551234",
  "provider": "vapi",
  "assistantId": "asst_new789",
  "squadId": null,
  "name": "Updated Sales Line",
  "serverUrl": "https://myserver.com/vapi-webhook",
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-20T16:45:00.000Z"
}
```

### cURL Example

```bash
# Update assistant and name
curl -X PATCH https://api.vapi.ai/phone-number/phn_abc123def456 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_new789",
    "name": "Updated Sales Line",
    "serverUrl": "https://myserver.com/vapi-webhook"
  }'

# Unassign assistant (set to null)
curl -X PATCH https://api.vapi.ai/phone-number/phn_abc123def456 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": null
  }'

# Enable SMS (Twilio US only)
curl -X PATCH https://api.vapi.ai/phone-number/phn_abc123def456 \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "smsEnabled": true
  }'
```

### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

// Update assistant and name
const updated = await vapi.phoneNumbers.update("phn_abc123def456", {
  assistantId: "asst_new789",
  name: "Updated Sales Line",
  serverUrl: "https://myserver.com/vapi-webhook",
});
console.log("Updated phone number:", updated.name);

// Unassign assistant
const unassigned = await vapi.phoneNumbers.update("phn_abc123def456", {
  assistantId: null,
});
console.log("Assistant unassigned, assistantId:", unassigned.assistantId);

// Enable SMS (Twilio US only)
const smsEnabled = await vapi.phoneNumbers.update("phn_abc123def456", {
  smsEnabled: true,
});
console.log("SMS enabled:", smsEnabled.smsEnabled);
```

### Python Example

```python
import requests
import os

VAPI_API_KEY = os.environ["VAPI_API_KEY"]
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

phone_number_id = "phn_abc123def456"

# Update assistant and name
response = requests.patch(
    f"{BASE_URL}/phone-number/{phone_number_id}",
    headers=HEADERS,
    json={
        "assistantId": "asst_new789",
        "name": "Updated Sales Line",
        "serverUrl": "https://myserver.com/vapi-webhook",
    },
)
updated = response.json()
print(f"Updated phone number: {updated['name']}")

# Unassign assistant
response = requests.patch(
    f"{BASE_URL}/phone-number/{phone_number_id}",
    headers=HEADERS,
    json={"assistantId": None},
)
unassigned = response.json()
print(f"Assistant unassigned, assistantId: {unassigned.get('assistantId')}")

# Enable SMS (Twilio US only)
response = requests.patch(
    f"{BASE_URL}/phone-number/{phone_number_id}",
    headers=HEADERS,
    json={"smsEnabled": True},
)
sms_enabled = response.json()
print(f"SMS enabled: {sms_enabled.get('smsEnabled')}")
```

### Doc Reference

- [https://docs.vapi.ai/api-reference/phone-numbers/update](https://docs.vapi.ai/api-reference/phone-numbers/update)

---

## 5. Delete Phone Number

Permanently deletes a phone number from your organization. For Vapi-provisioned numbers, the number is released back to the pool. For BYOC (Twilio/Vonage/Telnyx) numbers, the number is unregistered from Vapi but remains in your provider account.

### HTTP Request

```
DELETE https://api.vapi.ai/phone-number/{id}
```

### Headers

| Header          | Value                        | Required |
|-----------------|------------------------------|----------|
| `Authorization` | `Bearer $VAPI_API_KEY`       | Yes      |

### Path Parameters

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `id`      | string | Yes      | The unique ID of the phone number.       |

### Response

**Status:** `200 OK`

Returns the deleted [PhoneNumber object](#phonenumber-response-schema) (a snapshot of the object at the time of deletion).

```json
{
  "id": "phn_abc123def456",
  "orgId": "org_xyz789",
  "number": "+14155551234",
  "provider": "vapi",
  "assistantId": "asst_abc123",
  "squadId": null,
  "name": "Sales Line",
  "serverUrl": null,
  "createdAt": "2025-01-15T10:30:00.000Z",
  "updatedAt": "2025-01-20T16:45:00.000Z"
}
```

### cURL Example

```bash
curl -X DELETE https://api.vapi.ai/phone-number/phn_abc123def456 \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

### TypeScript SDK Example

```typescript
import Vapi from "@vapi-ai/server-sdk";

const vapi = new Vapi({ token: process.env.VAPI_API_KEY });

const deleted = await vapi.phoneNumbers.delete("phn_abc123def456");

console.log(`Deleted phone number: ${deleted.number} (${deleted.name})`);
console.log(`Provider: ${deleted.provider}`);
```

### Python Example

```python
import requests
import os

VAPI_API_KEY = os.environ["VAPI_API_KEY"]
BASE_URL = "https://api.vapi.ai"
HEADERS = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
}

phone_number_id = "phn_abc123def456"

response = requests.delete(
    f"{BASE_URL}/phone-number/{phone_number_id}",
    headers=HEADERS,
)
deleted = response.json()

print(f"Deleted phone number: {deleted['number']} ({deleted.get('name', 'unnamed')})")
print(f"Provider: {deleted['provider']}")
```

### Doc Reference

- [https://docs.vapi.ai/api-reference/phone-numbers/delete](https://docs.vapi.ai/api-reference/phone-numbers/delete)

---

## PhoneNumber Response Schema

Every phone number endpoint returns objects conforming to this schema.

| Field         | Type   | Description                                                                                     |
|---------------|--------|-------------------------------------------------------------------------------------------------|
| `id`          | string | Unique identifier for the phone number resource (e.g., `phn_abc123def456`).                     |
| `orgId`       | string | ID of the organization that owns this phone number.                                             |
| `number`      | string | The phone number in E.164 format (e.g., `+14155551234`).                                        |
| `provider`    | string | The telephony provider: `"vapi"`, `"twilio"`, `"vonage"`, or `"telnyx"`.                        |
| `assistantId` | string | ID of the assistant assigned to handle inbound calls on this number. `null` if unassigned.       |
| `squadId`     | string | ID of the squad assigned to handle inbound calls on this number. `null` if unassigned. Mutually exclusive with `assistantId`. |
| `name`        | string | Human-readable display name. `null` if not set.                                                  |
| `serverUrl`   | string | Webhook URL for server events specific to this number. Overrides org-level server URL. `null` if not set. |
| `createdAt`   | string | ISO 8601 timestamp of when the phone number was created.                                        |
| `updatedAt`   | string | ISO 8601 timestamp of when the phone number was last updated.                                   |

### Provider-Specific Fields

Depending on the provider, additional fields may be present:

| Field              | Provider | Type    | Description                                              |
|--------------------|----------|---------|----------------------------------------------------------|
| `twilioAccountSid` | twilio   | string  | The Twilio Account SID used for this number.             |
| `twilioAuthToken`  | twilio   | string  | The Twilio Auth Token (may be redacted in responses).    |
| `credentialId`     | vonage, telnyx | string | The Vapi credential ID linking to the provider account. |
| `smsEnabled`       | twilio   | boolean | Whether SMS is enabled on this number.                   |

---

## Inbound vs Outbound Call Flow

### Inbound Calls (Receiving Calls)

When someone dials your Vapi phone number, the following happens:

```
Caller dials your number
        |
        v
Telephony provider receives call
        |
        v
Provider routes call to Vapi
        |
        v
Vapi checks phone number config
        |
        +--- assistantId set? --> Use that assistant
        |
        +--- squadId set? --> Use that squad
        |
        +--- Neither set? --> Send "assistant-request" webhook
        |                     to your server URL
        |                     (you respond with assistant config)
        |
        v
Call begins with the resolved assistant
        |
        v
Server events sent to your server URL
(status-update, transcript, end-of-call-report, etc.)
```

**Key points for inbound:**
- The phone number MUST have either `assistantId`, `squadId`, or a server URL that handles `assistant-request` webhooks.
- If none are configured, the inbound call will fail.
- Server URL priority: Phone Number `serverUrl` > Assistant `serverUrl` > Organization default server URL.

### Outbound Calls (Making Calls)

When you initiate a call via the Vapi API (`POST /call`), you specify both the phone number to call FROM and the assistant to use:

```
You call POST /call with:
  - phoneNumberId (your Vapi number to call from)
  - customer.number (the number to dial)
  - assistantId or assistant (inline config)
        |
        v
Vapi initiates outbound call
via the phone number's provider
        |
        v
Customer's phone rings
        |
        v
Customer answers --> Call begins with specified assistant
        |
        v
Server events sent to your server URL
```

**Key points for outbound:**
- The assistant is specified in the `/call` request, NOT on the phone number.
- The phone number's `assistantId` is only used for inbound calls.
- You must have a phone number registered in Vapi to make outbound calls.

---

## Provider-Specific Limitations

### Vapi Free Numbers

| Limitation                | Detail                                                             |
|---------------------------|--------------------------------------------------------------------|
| **Country**               | United States only. No international numbers available.            |
| **Maximum numbers**       | Up to 10 free Vapi numbers per organization.                       |
| **International calling** | Not supported. Cannot dial or receive international calls.         |
| **SMS**                   | Not supported on Vapi free numbers.                                |
| **Area code**             | Best-effort matching via `numberDesiredAreaCode`. Not guaranteed.   |
| **Number portability**    | Not supported. Cannot port Vapi free numbers to another provider.  |

### Twilio (BYOC)

| Limitation                | Detail                                                             |
|---------------------------|--------------------------------------------------------------------|
| **Country**               | Any country where you have a Twilio number.                        |
| **SMS**                   | Supported, but **only for US Twilio numbers**. Set `smsEnabled: true`. |
| **International calling** | Supported if your Twilio account allows it.                        |
| **Credentials**           | Requires `twilioAccountSid` and `twilioAuthToken` at creation time.|
| **Number management**     | The number must already exist in your Twilio account.              |

### Vonage (BYOC)

| Limitation                | Detail                                                             |
|---------------------------|--------------------------------------------------------------------|
| **Country**               | Any country where you have a Vonage number.                        |
| **SMS**                   | Not supported through Vapi.                                        |
| **International calling** | Supported if your Vonage account allows it.                        |
| **Credentials**           | Requires a pre-configured Vonage credential in Vapi (`credentialId`). |
| **Number management**     | The number must already exist in your Vonage account.              |

### Telnyx (BYOC)

| Limitation                | Detail                                                             |
|---------------------------|--------------------------------------------------------------------|
| **Country**               | Any country where you have a Telnyx number.                        |
| **SMS**                   | Not supported through Vapi.                                        |
| **International calling** | Supported if your Telnyx account allows it.                        |
| **Credentials**           | Requires a pre-configured Telnyx credential in Vapi (`credentialId`). |
| **Number management**     | The number must already exist in your Telnyx account.              |

### Quick Comparison

| Feature              | Vapi (Free) | Twilio | Vonage | Telnyx |
|----------------------|:-----------:|:------:|:------:|:------:|
| US Numbers           | Yes         | Yes    | Yes    | Yes    |
| International Numbers| No          | Yes    | Yes    | Yes    |
| SMS Support          | No          | US Only| No     | No     |
| Max Free Numbers     | 10          | N/A    | N/A    | N/A    |
| BYOC                 | No          | Yes    | Yes    | Yes    |
| Credential Required  | No          | Yes*   | Yes    | Yes    |

*Twilio requires `twilioAccountSid` + `twilioAuthToken` directly (not a Vapi credential ID).
