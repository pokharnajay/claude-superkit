---
name: automations
description: Manage Airtable automations and scripting extensions. Use when the user wants to create automation triggers, actions, scripts, or integrate Airtable with external services via built-in automations.
---

# Airtable Automations

Guide the user through creating and managing Airtable automations — triggered workflows that run automatically when conditions are met.

## Important Note

Airtable automations are primarily configured through the Airtable UI (not the REST API). This skill guides users on designing and implementing automations.

## Automation Components

### Triggers (What starts the automation)

| Trigger | Description |
|---------|-------------|
| When record matches conditions | Fires when a record enters a filtered view |
| When record is created | Fires on new record creation |
| When record is updated | Fires when specific fields change |
| When form is submitted | Fires on Airtable form submission |
| At scheduled time | Fires on a cron schedule (hourly/daily/weekly/monthly) |
| When webhook received | Fires when external webhook hits Airtable |
| When button is clicked | Fires when a button field is clicked |

### Actions (What the automation does)

| Action | Description |
|--------|-------------|
| Create record | Create a new record in any table |
| Update record | Update fields in existing records |
| Find records | Query records matching conditions |
| Send email | Send email via Airtable |
| Send Slack message | Post to a Slack channel |
| Run script | Execute custom JavaScript |
| Call webhook | Send HTTP request to external URL |
| Create Google Calendar event | Add event to Google Calendar |
| Conditional logic | If/else branching |
| Repeat for each | Loop over a list of records |

## Scripting Extension Examples

### Script: Create Records from API Data

```javascript
// Fetch data from external API and create records
let table = base.getTable("Contacts");

let response = await fetch("https://api.example.com/contacts", {
    headers: { "Authorization": "Bearer " + input.config().apiKey }
});
let data = await response.json();

for (let contact of data.contacts) {
    await table.createRecordAsync({
        "Name": contact.name,
        "Email": contact.email,
        "Company": contact.company
    });
}
```

### Script: Update Records Based on Conditions

```javascript
let table = base.getTable("Tasks");
let query = await table.selectRecordsAsync({ fields: ["Status", "Due Date"] });

let today = new Date();
for (let record of query.records) {
    let dueDate = new Date(record.getCellValue("Due Date"));
    if (dueDate < today && record.getCellValue("Status") !== "Overdue") {
        await table.updateRecordAsync(record.id, {
            "Status": { name: "Overdue" }
        });
    }
}
```

### Script: Sync Data Between Tables

```javascript
let sourceTable = base.getTable("Orders");
let targetTable = base.getTable("Order Summary");

let sourceRecords = await sourceTable.selectRecordsAsync({
    fields: ["Customer", "Amount", "Status"]
});

let summaryByCustomer = {};
for (let record of sourceRecords.records) {
    let customer = record.getCellValue("Customer");
    let amount = record.getCellValue("Amount") || 0;
    if (!summaryByCustomer[customer]) {
        summaryByCustomer[customer] = { total: 0, count: 0 };
    }
    summaryByCustomer[customer].total += amount;
    summaryByCustomer[customer].count += 1;
}

for (let [customer, data] of Object.entries(summaryByCustomer)) {
    await targetTable.createRecordAsync({
        "Customer": customer,
        "Total Revenue": data.total,
        "Order Count": data.count
    });
}
```

## Automation Design Patterns

### 1. Approval Workflow
- **Trigger:** When record matches "Status = Pending Review"
- **Action 1:** Send email to approver with record details
- **Action 2:** Send Slack notification to channel
- **Action 3:** Update record "Notification Sent" = true

### 2. Data Enrichment
- **Trigger:** When record is created in Contacts
- **Action 1:** Run script to call Clearbit/enrichment API
- **Action 2:** Update record with enriched data

### 3. Cross-Table Sync
- **Trigger:** When record is updated in Orders
- **Action 1:** Find matching record in Inventory
- **Action 2:** Update Inventory stock count

### 4. Scheduled Reports
- **Trigger:** At scheduled time (every Monday 9am)
- **Action 1:** Find records matching "This Week's Tasks"
- **Action 2:** Run script to generate summary
- **Action 3:** Send email with report

## Best Practices

1. **Test with small datasets** before enabling on production data
2. **Use conditional logic** to prevent unnecessary actions
3. **Add error handling** in scripts with try/catch blocks
4. **Monitor automation runs** in the Automation History panel
5. **Be mindful of rate limits** — automations count toward API limits
6. **Use input.config()** in scripts for reusable configuration
7. **Log important steps** with `console.log()` for debugging
