# Integration Tools Reference

> Sources: Google Calendar, Google Sheets, Slack, MCP, GoHighLevel

### 6.1 Google Calendar

> **Doc reference:** https://docs.vapi.ai/tools/google-calendar

#### Prerequisites
- Google Calendar account
- Access to the Vapi Dashboard
- An assistant created in Vapi

#### Setup
1. Dashboard > **Integrations** > **Tools Provider** > **Google Calendar** > **Connect**
2. Authorize Vapi to access your Google Calendar
3. Dashboard > **Tools** > **Create Tool** > Select **Google Calendar**

#### Tool Types

**Create Event Tool** (`google.calendar.event.create`)

| Parameter | Description |
|-----------|-------------|
| `summary` | Title/description of the calendar event |
| `startDateTime` | Start date and time (ISO 8601 format) |
| `endDateTime` | End date and time (ISO 8601 format) |
| `attendees` | List of email addresses to invite |
| `timeZone` | Timezone for the event (defaults to UTC) |
| `calendarId` | Calendar ID (defaults to primary) |

**Check Availability Tool** (`google.calendar.availability.check`)

| Parameter | Description |
|-----------|-------------|
| `startDateTime` | Start of the time range to check |
| `endDateTime` | End of the time range to check |
| `timeZone` | Timezone for the check (defaults to UTC) |
| `calendarId` | Calendar ID (defaults to primary) |

All datetimes must be in ISO 8601 format.

#### Complete Assistant Config Example

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a scheduling assistant. When users want to schedule an appointment, first check their availability using the Check Availability tool, then use the Create Event tool to schedule the event if they're available.\n\n- Gather date and time range to check availability.\n- To book an appointment, gather the purpose of the appointment.\n\nNotes\n- Use the purpose as summary for booking appointment.\n- Current date: {{now}}"
      }
    ],
    "tools": [
      {
        "type": "google.calendar.availability.check",
        "name": "checkAvailability",
        "description": "Use this tool to check calendar availability."
      },
      {
        "type": "google.calendar.event.create",
        "name": "scheduleAppointment",
        "description": "Use this tool to schedule appointments and create calendar events. Notes: - All appointments are 30 mins. \n- Current date/time: {{now}}"
      }
    ]
  }
}
```

#### Best Practices
- Provide clear instructions about when to use each calendar tool
- Include fallback responses for tool failures
- Always specify the correct timezone
- Check availability before attempting to schedule events

---

### 6.2 Google Sheets

> **Doc reference:** https://docs.vapi.ai/tools/google-sheets

#### Prerequisites
- Google Sheets account
- Vapi Dashboard access
- An assistant created in Vapi
- A Google Sheet already created and ready to receive data

#### Setup
1. Dashboard > **Providers Keys** > **Tools Provider** > **Google Sheets** > **Connect**
2. Complete Google authorization
3. Dashboard > **Tools** > **Create Tool** > Select **Google Sheets**
4. Choose the Google Sheets Add Row Tool

#### Tool Type: `google.sheets.row.append`

| Parameter | Description |
|-----------|-------------|
| `spreadsheetId` | Unique ID from the sheet URL (between `/d/` and `/edit`) |
| `range` | Sheet name (`"Sheet1"`) or range (`"Sheet1!A:Z"`) |
| `values` | Array of values to add as a new row |

**Finding Spreadsheet ID:**
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
                                       ^^^^^^^^^^^^^^^^
                                       Copy this part
```

**Note:** This integration only supports appending new rows. It cannot read or modify existing data.

#### Complete Feedback Collection Example

```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a customer feedback assistant. After each customer service call, collect feedback using the following process:\n\n1. Ask the customer if they would like to provide feedback\n2. If yes, ask for their rating (1-5 stars)\n3. Ask for specific comments about their experience\n4. Ask for any suggestions for improvement\n5. Confirm the feedback before adding it to the spreadsheet\n\nUse the Add Row tool to record the feedback with the following columns:\n- Timestamp\n- Rating (1-5)\n- Comments\n- Suggestions\n\nAlways be polite and thank the customer for their feedback."
      }
    ],
    "tools": [
      {
        "type": "google.sheets.row.append",
        "name": "addFeedback",
        "description": "Use this tool to add customer feedback to the feedback spreadsheet. Collect all required information (rating, comments, suggestions) before adding the row."
      }
    ]
  }
}
```

#### Best Practices
- Validate data before adding to the spreadsheet
- Include fallback responses for tool failures
- Always confirm with the user before adding data
- Be aware of the spreadsheet's structure and column requirements

---

### 6.3 Slack

> **Doc reference:** https://docs.vapi.ai/tools/slack

#### Setup
1. Dashboard > **Providers Keys** > **Tools Provider** > **Slack** > **Connect**
2. Authorize Vapi to access your Slack workspace
3. Dashboard > **Tools** > **Create Tool** > Select **Slack**
4. Choose Slack Send Message Tool

#### Tool Type: `slack.message.send`

**Channel is specified in the `description` field** (e.g., "#customer-support"). The Slack bot must be added to the target channel.

#### Complete Assistant Config Example

```json
{
  "tools": [
    {
      "type": "slack.message.send",
      "name": "notifySupport",
      "description": "Send urgent notifications to the #customer-support channel when a customer needs immediate attention or requests a callback. Include customer name, phone number, reason for callback, and any time constraints."
    }
  ]
}
```

#### Advanced: Webhook for Call Failure Monitoring

You can also use Slack webhooks via serverless functions for automated notifications (e.g., call failure alerts):

```typescript
// Serverless function for Slack webhook
const SLACK_WEBHOOK_URL = env.SLACK_WEBHOOK_URL;

const response = await fetch(SLACK_WEBHOOK_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: `Call failure detected: ${args.reason}`,
    channel: '#alerts'
  })
});
```

#### Best Practices
- Ensure the Slack bot has been added to the target channel
- Be specific about scenarios and conditions in descriptions
- The AI dynamically generates message content based on conversation context
- Always confirm with the user before sending notifications

---

### 6.4 MCP Tool (Model Context Protocol)

> **Doc reference:** https://docs.vapi.ai/tools/mcp

#### What It Is

MCP (Model Context Protocol) allows your assistant to dynamically connect to external MCP servers and access their tools during calls or chats. This enables integration with platforms like Zapier, Make, and Composio without individual integrations for each service.

#### Configuration

```json
{
  "type": "mcp",
  "server": {
    "url": "https://mcp.zapier.com/mcp/?client=vapi",
    "headers": {
      "Authorization": "Bearer YOUR_TOKEN"
    }
  },
  "metadata": {
    "protocol": "shttp"
  }
}
```

#### Protocols

| Protocol | `metadata.protocol` | Description |
|----------|---------------------|-------------|
| **Streamable HTTP** (recommended) | `"shttp"` | Default, better performance |
| **Server-Sent Events** | `"sse"` | Legacy protocol support |

#### How It Works

1. **Initial Connection** - At conversation start, Vapi connects to your MCP server
2. **Dynamic Tool Injection** - Available tools are fetched and added to assistant's toolkit
3. **Tool Execution** - When invoked, Vapi creates a new connection with `X-Call-Id` or `X-Chat-Id` headers
4. **Multiple Sessions** - Each tool call creates a new session per conversation

#### MCP Providers

| Provider | URL | Description |
|----------|-----|-------------|
| **Zapier** | `https://mcp.zapier.com/mcp/?client=vapi` | 7,000+ apps, 30,000+ actions |
| **Make** | Profile > API Access tab > MCP token | Business tech stack automation |
| **Composio** | `https://mcp.composio.dev/dashboard` | Tool-specific MCP servers |

#### Vapi MCP Server

Vapi provides its own MCP server at `https://mcp.vapi.ai/mcp` that exposes Vapi APIs as tools:

| Tool | Description |
|------|-------------|
| `list_assistants` | List all Vapi assistants |
| `create_assistant` | Create a new assistant |
| `get_assistant` | Get assistant by ID |
| `list_calls` | List all calls |
| `create_call` | Create outbound call (now or scheduled) |
| `get_call` | Get call details |
| `list_phone_numbers` | List all phone numbers |
| `get_phone_number` | Get phone number details |
| `list_tools` | List all tools |
| `get_tool` | Get tool details |

#### IDE Integration

**Cursor config** (`.cursor/mcp.json`):
```json
{
  "servers": {
    "vapi-docs": {
      "command": "npx",
      "args": ["@vapi-ai/mcp-server"]
    }
  }
}
```

**VSCode config** (workspace settings):
```json
{
  "github.copilot.advanced": {
    "mcp.servers": {
      "vapi-docs": {
        "command": "npx",
        "args": ["@vapi-ai/mcp-server"]
      }
    }
  }
}
```

**Claude Desktop config** (remote MCP server):
```json
{
  "mcpServers": {
    "vapi-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.vapi.ai/mcp",
        "--header",
        "Authorization: Bearer ${VAPI_TOKEN}"
      ],
      "env": {
        "VAPI_TOKEN": "YOUR_VAPI_API_KEY"
      }
    }
  }
}
```

#### Best Practices
- Use Streamable HTTP protocol (default) for better performance
- Treat MCP server URLs as credentials (they contain auth tokens)
- Include error handling for tool failures
- Configure tools to return focused, relevant data to avoid exceeding model context limits
- Provide clear instructions in system messages about handling dynamic tools

---

### 6.5 GoHighLevel

> **Doc reference:** https://docs.vapi.ai/tools/go-high-level

#### Overview

GoHighLevel (GHL) integration allows voice agents to interact with GHL calendars and contacts for seamless appointment scheduling and contact management.

#### Available Tools

| Tool | Type | Description |
|------|------|-------------|
| **Get Contact** | `ghl` | Retrieve existing contact by email or phone |
| **Create Contact** | `ghl` | Create new leads/clients |
| **Check Availability** | `ghl` | Query GHL calendars for open slots |
| **Create Event** | `ghl` | Schedule appointments with a contact |

#### Prerequisites
- GoHighLevel account with calendar permissions
- Access to the Vapi Dashboard

#### Setup
1. Dashboard > **Providers Keys** > **Tools Provider** > **GoHighLevel** > **Connect**
2. Dashboard > **Tools** > **Create Tool** > **GoHighLevel**
3. For Check Availability and Create Event tools, provide a valid `calendarId` (found in GHL under **Settings** > **Calendars**)

#### Tool Parameters

**Get Contact:**
- `email` (optional) - Email address to search for
- `phone` (optional) - Phone number to search for

**Create Contact:**
- `firstName` (required) - Contact's first name
- `lastName` (required) - Contact's last name
- `email` (required) - Contact's email address
- `phone` (required) - Contact's phone number

**Check Availability:**
- `calendarId` (required) - GHL calendar ID
- `startDate` (required) - Start time in epoch milliseconds
- `endDate` (required) - End time in epoch milliseconds
- `timezone` (required) - e.g., "America/New_York"

**Create Event:**
- `calendarId` (required) - GHL calendar ID
- `contactId` (required) - GHL contact ID
- `title` (required) - Event title/summary
- `startTime` (required) - ISO 8601 format
- `endTime` (required) - ISO 8601 format

#### Recommended System Prompt

```text
You are a helpful and efficient scheduling assistant. Your primary goal is to book appointments for users. Follow these steps carefully:

1. **Gather Information**: Start by asking for the caller's full name and email address.
2. **Check Existing Contact**: Use the `ghl_contact_get` tool to see if a contact already exists with the provided email.
3. **Create Contact (if needed)**: If no contact is found, use the `ghl_contact_create` tool to create a new contact with their name and email.
4. **Discuss Appointment Time**: Once you have a contact ID, ask the user for their preferred date and time.
5. **Check Availability**: Use the `ghl_check_availability` tool to check for open slots.
6. **Confirm Time**: Discuss available options and agree on a suitable time.
7. **Book Appointment**: Use the `ghl_create_event` tool to book the appointment with the correct contact ID.

**Important Guidelines:**
- Always use `ghl_contact_get` before attempting to create a contact
- You must have a contact ID before booking an appointment
- Always confirm availability before attempting to book
```

#### Best Practices
- Always check for existing contacts before creating new ones to avoid duplicates
- Follow the proper sequence: gather info > check contact > create if needed > check availability > book
- Always specify the correct timezone
- Format current date/time with your desired timezone in tool descriptions

---

