# Silent Handoffs Complete Guide

> Source: https://docs.vapi.ai/squads/silent-handoffs

---

## What Are Silent Handoffs?

Silent handoffs enable **seamless transfers between assistants** without the customer hearing any transfer announcements like "Please hold while I transfer you to our billing department." The customer remains unaware that multiple assistants are involved in the conversation -- the entire interaction feels like one continuous conversation with a single agent.

### Why Use Silent Handoffs?

- **Uninterrupted conversation flow**: No awkward pauses or "please hold" messages
- **Customer unawareness**: The caller never knows multiple specialized assistants are handling different parts of the conversation
- **Higher satisfaction**: Smoother interactions boost customer experience and NPS scores
- **Professional appearance**: The system appears as one cohesive, knowledgeable assistant
- **Reduced call abandonment**: Customers are less likely to hang up during seamless transitions

---

## 4 Configuration Steps

Silent handoffs require changes to **four areas** of your squad configuration. All four must be configured correctly for a truly silent experience.

### Step 1: Update Destination Assistant's First Message

Configure the assistant that **receives** the handoff so it does not speak a canned greeting:

- Set `firstMessage` to an empty string `""`
- Set `firstMessageMode` to `"assistant-speaks-first-with-model-generated-message"`

This combination means: "Don't use a static first message, but let the model generate an appropriate first response based on the conversation context."

```json
{
  "name": "PaymentAssistant",
  "firstMessage": "",
  "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
  "model": {
    "model": "gpt-4o",
    "provider": "openai",
    "messages": [
      {
        "role": "system",
        "content": "You are the Payment Processing Assistant..."
      }
    ]
  }
}
```

**Why both settings are needed**:
- `firstMessage: ""` -- Ensures no static greeting is spoken
- `firstMessageMode: "assistant-speaks-first-with-model-generated-message"` -- Tells the system to let the model decide what to say first based on context, rather than waiting for the user to speak

### Step 2: Update Squad Handoff Messages

For **every handoff tool** in your squad members, disable the default transfer announcement messages:

- Set `messages` to an empty array `[]` OR
- Set `messages` to `null`

Both achieve the same result: no transfer announcement is spoken to the caller.

```json
{
  "type": "handoff",
  "destinations": [
    {
      "type": "assistant",
      "assistantName": "PaymentAssistant",
      "description": "customer is ready to make a payment"
    }
  ],
  "messages": []
}
```

Or using null:

```json
{
  "type": "handoff",
  "destinations": [
    {
      "type": "assistant",
      "assistantName": "PaymentAssistant",
      "description": "customer is ready to make a payment"
    }
  ],
  "messages": null
}
```

**Important**: You must do this on **every** handoff tool in **every** squad member. Missing even one will cause an audible transfer announcement.

### Step 3: Configure Source Assistant Prompts

The assistant that **initiates** the handoff must be instructed to:
1. Trigger the handoff tool without announcing the transfer
2. Never say words like "transferring", "connecting you", or "please hold"

Add these instructions to the source assistant's system prompt:

```
[Handoff Instructions]
- When the customer needs payment processing, trigger the 'handoff' tool with 'PaymentAssistant' Assistant.
- Never say "transferring", "connecting you to", "please hold", or similar transfer language.
- Do not announce or acknowledge the handoff in any way.
- Simply trigger the tool and the transition will happen seamlessly.
```

**Full source assistant system prompt example**:

```
[System context]
You are part of a multi-agent system designed to make agent coordination and execution easy.
Agents uses two primary abstraction: **Agents** and **Handoffs**. An agent encompasses
instructions and tools and can hand off a conversation to another agent when appropriate.
Handoffs are achieved by calling a handoff function, generally named `handoff_to_<agent_name>`.
Handoffs between agents are handled seamlessly in the background;
do not mention or draw attention to these handoffs in your conversation with the user.

[Identity]
You are the Main Assistant (HPMA) for HealthPlus Medical. Your role is to greet patients, collect their information, and route them appropriately.

[Style]
- Use a calm and professional tone.
- Be concise and clear in communication.
- Display empathy where needed.

[Task & Goals]
1. Greet the patient politely.
2. Ask for the patient's name and reason for calling.
3. Determine if the patient needs:
   - Payment processing: trigger the 'handoff' tool with 'HPPA' Assistant.
   - Appointment scheduling: trigger the 'handoff' tool with 'SchedulerAssistant' Assistant.
4. Never say "transferring", "let me connect you", or "please hold".
5. Simply proceed with the handoff when appropriate.
```

### Step 4: Direct Destination Assistant Behavior

The assistant that **receives** the handoff must be instructed to skip greetings and jump straight into its task:

Add this instruction to the receiving assistant's system prompt:

```
Proceed directly to the Task section without any greetings or small talk.
```

**Full destination assistant system prompt example**:

```
[Identity]
You are the Payment Processing Assistant (HPPA) for HealthPlus Medical. Your role is to securely collect and process patient payments.

[Patient Information]
- Patient Name: {{patientName}}

[Style]
- Use a professional and reassuring tone.
- Be clear about payment amounts and methods.
- Address the patient by name.

[Response Guidelines]
- Proceed directly to the Task section without any greetings or small talk.
- Do not say "hello" or "how can I help you" -- the patient has already been speaking with the system.
- Immediately begin with the payment-related task.

[Task & Goals]
1. Confirm the patient's outstanding balance.
2. Ask for preferred payment method.
3. Process the payment securely.
4. Provide confirmation details.
5. When complete, trigger the 'handoff' tool with 'HPMA-SA' Assistant for follow-up.
```

---

## Complete Payment Processing Example

This example shows a full 3-assistant squad for a healthcare payment flow: Main Assistant (HPMA) --> Payment Assistant (HPPA) --> Sub-Agent (HPMA-SA).

### Squad Configuration

```json
{
  "name": "HP Payment Squad With SubAgent",
  "members": [
    {
      "assistant": {
        "name": "HPMA",
        "firstMessage": "Hello! Thank you for calling HealthPlus Medical. How can I assist you today?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[System context]\nYou are part of a multi-agent system designed to make agent coordination and execution easy.\nAgents uses two primary abstraction: **Agents** and **Handoffs**. An agent encompasses instructions and tools and can hand off a conversation to another agent when appropriate.\nHandoffs are achieved by calling a handoff function, generally named `handoff_to_<agent_name>`.\nHandoffs between agents are handled seamlessly in the background; do not mention or draw attention to these handoffs in your conversation with the user.\n\n[Identity]\nYou are the Main Assistant (HPMA) for HealthPlus Medical. Your role is to greet patients, understand their needs, and route them to the appropriate department.\n\n[Style]\n- Use a calm and professional tone.\n- Be concise and clear in communication.\n- Display empathy where needed.\n\n[Task & Goals]\n1. Greet the patient politely.\n2. Ask for the patient's name.\n3. Ask how you can help them today.\n4. Determine user intent:\n   - If the user needs to make a payment, trigger the 'handoff' tool with 'HPPA' Assistant.\n   - If the user needs to schedule an appointment, trigger the 'handoff' tool with 'SchedulerAssistant' Assistant.\n5. Never say 'transferring', 'let me connect you', or 'please hold'.\n6. Simply proceed with the handoff when the intent is clear."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_HPPA",
                "description": "Use when the patient needs to make a payment or has billing questions.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["HPPA"]
                    },
                    "patientName": {
                      "type": "string",
                      "description": "Full name of the patient"
                    }
                  },
                  "required": ["destination", "patientName"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "HPPA",
                  "description": "patient needs to make a payment or has billing questions",
                  "contextEngineeringPlan": {
                    "type": "all"
                  },
                  "variableExtractionPlan": {
                    "patientName": {
                      "type": "conversation",
                      "description": "Extract the patient's full name from the conversation"
                    }
                  }
                }
              ],
              "messages": []
            }
          ]
        }
      }
    },
    {
      "assistant": {
        "name": "HPPA",
        "firstMessage": "",
        "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Payment Processing Assistant (HPPA) for HealthPlus Medical.\n\n[Patient Information]\n- Patient Name: {{patientName}}\n\n[Style]\n- Use a professional and reassuring tone.\n- Be clear about payment amounts and methods.\n- Address the patient by name.\n\n[Response Guidelines]\n- Proceed directly to the Task section without any greetings or small talk.\n- Do not say 'hello' or re-introduce yourself.\n- The patient has already been speaking with the system.\n\n[Task & Goals]\n1. Confirm the patient's outstanding balance using their name.\n2. Ask for preferred payment method (credit card, debit card, bank transfer).\n3. Collect payment details securely.\n4. Process the payment.\n5. Provide a confirmation number.\n6. When complete, trigger the 'handoff' tool with 'HPMA-SA' Assistant."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_HPMA_SA",
                "description": "Use when payment processing is complete and the patient needs follow-up assistance.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["HPMA-SA"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "HPMA-SA",
                  "description": "payment is complete and patient needs follow-up or closing",
                  "contextEngineeringPlan": {
                    "type": "all"
                  }
                }
              ],
              "messages": null
            }
          ]
        }
      }
    },
    {
      "assistant": {
        "name": "HPMA-SA",
        "firstMessage": "",
        "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Follow-Up Sub-Agent (HPMA-SA) for HealthPlus Medical.\n\n[Response Guidelines]\n- Proceed directly to the Task section without any greetings or small talk.\n- Do not re-introduce yourself or say hello.\n\n[Task & Goals]\n1. Confirm the payment was processed successfully.\n2. Ask if the patient needs anything else.\n3. If no further needs, thank them and end the call politely.\n4. If they need additional help, assist them directly."
            }
          ]
        }
      }
    }
  ]
}
```

### Customer Experience Flow

```
Customer calls in
        |
        v
  [HPMA - Main Assistant]
  "Hello! Thank you for calling HealthPlus Medical. How can I assist you today?"
        |
  Customer: "Hi, I'm John Smith. I need to make a payment."
        |
  HPMA internally: (triggers handoff_to_HPPA with patientName="John Smith")
  (NO audible transfer announcement -- messages: [])
        |
        v
  [HPPA - Payment Assistant]  (firstMessage: "", model generates response)
  "Sure, John. Let me pull up your account. Your outstanding balance is $150. Would you like to pay by credit card, debit card, or bank transfer?"
        |
  Customer: "Credit card please."
        |
  (Payment processing conversation continues...)
  HPPA: "Your payment of $150 has been processed. Your confirmation number is HP-2024-7823."
  HPPA internally: (triggers handoff_to_HPMA_SA)
  (NO audible transfer announcement -- messages: null)
        |
        v
  [HPMA-SA - Follow-Up Sub-Agent]  (firstMessage: "", model generates response)
  "Your payment has been confirmed, John. Is there anything else I can help you with today?"
        |
  Customer: "No, that's all. Thank you!"
        |
  HPMA-SA: "You're welcome, John. Have a great day!"
  (Call ends)
```

**Key observation**: The customer experienced one continuous conversation. They were never told about transfers, never heard "please hold", and interacted with three different specialized assistants without knowing it.

---

## Key Rules for Silent Handoffs

### Rule 1: Never Say "Transferring" in Any Prompt

Every assistant's system prompt must explicitly prohibit transfer language:

```
- Never say "transferring", "connecting you to", "please hold", or "let me transfer you".
- Do not acknowledge or announce the handoff in any way.
```

### Rule 2: Empty firstMessage on Receiving Assistants

Every assistant that can **receive** a handoff must have:

```json
{
  "firstMessage": "",
  "firstMessageMode": "assistant-speaks-first-with-model-generated-message"
}
```

**Exception**: The very first assistant in the squad (the entry point) should have a normal `firstMessage` since it greets the initial caller.

### Rule 3: Use Model-Generated First Message Mode

The `firstMessageMode` must be `"assistant-speaks-first-with-model-generated-message"` -- not `"assistant-speaks-first"` (which would use the static `firstMessage`).

### Rule 4: Clear Handoff Messages

Every handoff tool must have its messages cleared:

```json
// Option A: Empty array
"messages": []

// Option B: Null
"messages": null
```

Both are equivalent. Choose whichever you prefer and be consistent.

### Rule 5: Instruct Receiving Assistants to Skip Greetings

Add to every receiving assistant's system prompt:

```
Proceed directly to the Task section without any greetings or small talk.
Do not say "hello", "hi there", or re-introduce yourself.
The customer has already been speaking with the system.
```

---

## Silent Handoffs with Variable Extraction

You can combine silent handoffs with variable extraction for personalized, seamless experiences:

```json
{
  "type": "handoff",
  "function": {
    "name": "handoff_to_Specialist",
    "description": "Route to the appropriate specialist based on the customer's need.",
    "parameters": {
      "type": "object",
      "properties": {
        "destination": {
          "type": "string",
          "enum": ["specialist-uuid"]
        },
        "customerName": {
          "type": "string",
          "description": "The customer's full name"
        },
        "issueCategory": {
          "type": "string",
          "description": "Category of the customer's issue"
        }
      },
      "required": ["destination", "customerName"]
    }
  },
  "destinations": [
    {
      "type": "assistant",
      "assistantId": "specialist-uuid",
      "description": "customer needs specialized help",
      "contextEngineeringPlan": {
        "type": "all"
      },
      "variableExtractionPlan": {
        "customerName": {
          "type": "conversation",
          "description": "Extract the customer's full name"
        },
        "issueCategory": {
          "type": "conversation",
          "description": "Determine the category of the customer's issue"
        }
      }
    }
  ],
  "messages": []
}
```

The receiving assistant's prompt then uses the variables:

```
[Response Guidelines]
- Proceed directly to the Task section without any greetings or small talk.
- Address the customer as {{customerName}}.
- The customer's issue category is: {{issueCategory}}.
- Begin handling their {{issueCategory}} issue immediately.
```

---

## Common Mistakes to Avoid

### Mistake 1: Forgetting to clear messages on one handoff tool

If you have 5 handoff tools and clear messages on 4 but forget 1, that one transfer will still announce itself.

**Fix**: Audit every handoff tool in every squad member and ensure `messages: []` or `messages: null`.

### Mistake 2: Using `"assistant-speaks-first"` instead of `"assistant-speaks-first-with-model-generated-message"`

Using `"assistant-speaks-first"` will cause the assistant to speak the static `firstMessage`, which is empty -- resulting in silence/awkward pause.

**Fix**: Always use `"assistant-speaks-first-with-model-generated-message"` so the model generates a contextual response.

### Mistake 3: Not instructing the receiving assistant to skip greetings

Even with proper firstMessage configuration, the model might still generate a greeting like "Hi there! How can I help?" unless explicitly told not to.

**Fix**: Add `"Proceed directly to the Task section without any greetings or small talk."` to the receiving assistant's system prompt.

### Mistake 4: Source assistant says "Let me transfer you"

The LLM might naturally want to say "Let me connect you with our payment team" before triggering the handoff.

**Fix**: Explicitly prohibit transfer language in the source assistant's prompt:
```
Never say "transferring", "connecting you to", "please hold", or similar transfer language.
```

### Mistake 5: Using the wrong firstMessage for the entry assistant

The very first assistant (entry point) SHOULD have a normal `firstMessage` and `firstMessageMode: "assistant-speaks-first"`. Only the receiving assistants need the silent configuration.

---

## Checklist for Silent Handoff Configuration

Use this checklist when configuring a squad with silent handoffs:

- [ ] **Entry assistant**: Has normal `firstMessage` and `firstMessageMode: "assistant-speaks-first"`
- [ ] **All receiving assistants**: `firstMessage: ""`
- [ ] **All receiving assistants**: `firstMessageMode: "assistant-speaks-first-with-model-generated-message"`
- [ ] **All handoff tools**: `messages: []` or `messages: null`
- [ ] **All source assistant prompts**: Include "Never say transferring" instruction
- [ ] **All source assistant prompts**: Include "trigger the handoff tool with [AssistantName]" instruction
- [ ] **All receiving assistant prompts**: Include "Proceed directly to the Task section without any greetings or small talk"
- [ ] **All receiving assistant prompts**: Include "Do not say hello or re-introduce yourself"
- [ ] **Tested end-to-end**: Called the squad and verified no transfer announcements are heard

---

Doc ref: https://docs.vapi.ai/squads/silent-handoffs
