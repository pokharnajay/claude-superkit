# Squad Examples -- 5 Complete Real-World Patterns

> Sources: https://docs.vapi.ai/squads/examples/clinic-triage-scheduling-handoff-tool, https://docs.vapi.ai/squads/examples/clinic-triage-scheduling, https://docs.vapi.ai/squads/examples/ecommerce-order-management, https://docs.vapi.ai/squads/examples/property-management, https://docs.vapi.ai/squads/examples/multilingual-support

---

## Example 1: Clinic Triage and Scheduling (Handoff Tool)

> Source: https://docs.vapi.ai/squads/examples/clinic-triage-scheduling-handoff-tool

### Use Case

A healthcare clinic needs an automated phone system that:
1. Greets patients and collects their name
2. Determines if they need an appointment or have an emergency
3. Routes to the appropriate specialist
4. Passes patient name for personalized greetings at each stage

### Squad Architecture

```
                    [Triage Assistant]
                   /                  \
                  /                    \
    [Scheduler Assistant]     [Emergency Assistant]
    (appointment booking)     (urgent medical help)
```

- **Triage Assistant**: Entry point. Greets patient, collects name, assesses need (appointment vs. emergency). Uses Multiple Tools Pattern (OpenAI recommended) with separate handoff tools per destination.
- **Scheduler Assistant**: Books appointments. Receives `patientName` variable. Greets patient by name.
- **Emergency Assistant**: Handles urgent situations. Receives `patientName` variable. Provides immediate medical guidance.

### Key Design Decisions

1. **Multiple Tools Pattern**: Each destination gets its own handoff tool (`handoff_to_Scheduler`, `handoff_to_Emergency`) because this uses OpenAI's gpt-4o model
2. **Variable Extraction**: `patientName` is extracted from conversation and passed to receiving assistants via `variableExtractionPlan`
3. **Personalized Greetings**: Receiving assistants use `{{patientName}}` in `firstMessage` and system prompts
4. **Full Context Transfer**: `contextEngineeringPlan: { type: "all" }` ensures receiving assistants see the full triage conversation

### Complete JSON Configuration

```json
{
  "name": "Clinic Triage Squad (Handoff Tool)",
  "members": [
    {
      "assistant": {
        "name": "Triage",
        "firstMessage": "Hello, how can I help you today?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "model": "gpt-4o",
          "provider": "openai",
          "messages": [
            {
              "role": "system",
              "content": "[System context]\nYou are part of a multi-agent system designed to make agent coordination and execution easy.\nAgents uses two primary abstraction: **Agents** and **Handoffs**. An agent encompasses instructions and tools and can hand off a conversation to another agent when appropriate.\nHandoffs are achieved by calling a handoff function, generally named `handoff_to_<agent_name>`.\nHandoffs between agents are handled seamlessly in the background; do not mention or draw attention to these handoffs in your conversation with the user.\n\n[Identity]\nYou are a simple and efficient medical triage assistant. Your role is to ask the patient for their name and then determine if they need to be connected to a Scheduler for setting up an appointment or an Emergency line for urgent assistance.\n\n[Style]\n- Use a calm and professional tone.\n- Be concise and clear in communication.\n- Display empathy where needed.\n\n[Response Guidelines]\n- Begin with a polite greeting.\n- Request the patient's full name.\n- Confirm the appointment scheduling or emergency request.\n- Use simple language for clarity.\n\n[Task & Goals]\n1. Greet the user politely.\n2. Ask the user, \"Can I please have your full name?\"\n3. Ask if they want to manage an appointment or if they are experiencing an emergency.\n4. Determine user intent based on their need:\n   - If the user expresses the need to schedule an appointment, use handoff_to_Scheduler tool\n   - If the user indicates it's an emergency, use handoff_to_Emergency tool"
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_Scheduler",
                "description": "Use it when user needs help managing their appointment.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["<scheduler_assistant_uuid>"]
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
                  "assistantId": "<scheduler_assistant_uuid>",
                  "contextEngineeringPlan": {
                    "type": "all"
                  },
                  "variableExtractionPlan": {
                    "patientName": {
                      "type": "conversation",
                      "description": "Extract the patient's full name from the conversation history"
                    }
                  }
                }
              ]
            },
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_Emergency",
                "description": "Use it when user is having an emergency.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["<emergency_assistant_uuid>"]
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
                  "assistantId": "<emergency_assistant_uuid>",
                  "contextEngineeringPlan": {
                    "type": "all"
                  },
                  "variableExtractionPlan": {
                    "patientName": {
                      "type": "conversation",
                      "description": "Extract the patient's full name from the conversation history"
                    }
                  }
                }
              ]
            }
          ]
        }
      }
    },
    {
      "assistant": {
        "name": "Scheduler",
        "firstMessage": "Hello {{patientName}}, I'll help you schedule your appointment. Let me check our available times.",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "model": "gpt-4o",
          "provider": "openai",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are a clinic scheduling assistant. Your role is to help patients book, modify, or cancel appointments with healthcare providers.\n\n[Patient Information]\n- Patient Name: {{patientName}}\n- Use the patient's name throughout the conversation to provide personalized service\n- The patient has already been triaged and is ready for appointment scheduling\n\n[Style]\n- Use a friendly and professional tone.\n- Be patient and accommodating.\n- Provide clear options and confirmations.\n- Show flexibility with scheduling needs.\n- Address the patient by name to create a welcoming experience.\n\n[Response Guidelines]\n- Offer available time slots.\n- Confirm the selected appointment.\n- Provide any pre-visit instructions.\n\n[Task & Goals]\n1. Ask what type of appointment they need (general checkup, specialist, follow-up).\n2. Check available providers and time slots.\n3. Confirm the appointment details.\n4. Provide pre-visit instructions."
            }
          ],
          "toolIds": ["BOOKING_TOOL_ID", "PROVIDER_LOOKUP_ID", "CALENDAR_INTEGRATION_ID"]
        }
      }
    },
    {
      "assistant": {
        "name": "Emergency",
        "firstMessage": "Hello {{patientName}}, I understand this is an emergency. I'm connecting you with our emergency protocol immediately.",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "model": "gpt-4o",
          "provider": "openai",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are an emergency medical protocol assistant for a healthcare clinic. Your role is to handle urgent medical situations with immediate care and clear instructions.\n\n[Patient Information]\n- Patient Name: {{patientName}}\n- Use the patient's name to personalize your responses and maintain continuity from the triage conversation\n\n[Style]\n- Use a calm but urgent tone.\n- Be direct and clear.\n- Provide immediate actionable guidance.\n- Show empathy while maintaining efficiency.\n- Address the patient by name when appropriate.\n\n[Response Guidelines]\n- Acknowledge the emergency immediately and use the patient's name.\n- Gather essential information quickly (location, nature of emergency).\n- Provide immediate safety instructions if applicable.\n- Connect to emergency services or on-call medical staff.\n- Keep interactions brief but thorough.\n\n[Task & Goals]\n1. Assess the nature and severity of the emergency.\n2. Provide immediate safety instructions.\n3. Collect location information.\n4. Connect to emergency services (911) if life-threatening.\n5. Connect to on-call physician if urgent but not life-threatening."
            }
          ]
        }
      }
    }
  ]
}
```

---

## Example 2: Clinic Triage and Scheduling (Legacy assistantDestinations)

> Source: https://docs.vapi.ai/squads/examples/clinic-triage-scheduling

### Use Case

Same clinic triage scenario as Example 1, but using the **older `assistantDestinations` approach** instead of the modern handoff tool. This example is included for reference -- **the handoff tool (Example 1) is the recommended approach** for new implementations.

### Squad Architecture

```
                    [Triage Assistant]
                   /                  \
                  /                    \
    [Scheduler Assistant]     [Emergency Assistant]
```

### Key Differences from Handoff Tool Approach

| Feature | assistantDestinations (Legacy) | Handoff Tool (Recommended) |
|---------|-------------------------------|---------------------------|
| Context control | Transfer modes (rolling-history, etc.) | contextEngineeringPlan |
| Variable extraction | Not supported | variableExtractionPlan with {{variables}} |
| Custom function names | Not supported | handoff_to_<name> |
| Routing descriptions | Basic description field | Rich description + function.description |
| Configuration location | Squad member level | Assistant model.tools level |

### Complete JSON Configuration

```json
{
  "name": "Clinic Triage Squad (Legacy)",
  "members": [
    {
      "assistant": {
        "name": "Triage",
        "firstMessage": "Hello, how can I help you today?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "model": "gpt-4o",
          "provider": "openai",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are a medical triage assistant for a healthcare clinic.\n\n[Style]\n- Use a calm and professional tone.\n- Be concise and clear.\n\n[Task & Goals]\n1. Greet the patient.\n2. Ask for their name.\n3. Determine if they need an appointment or have an emergency.\n4. Route them to the appropriate assistant."
            }
          ]
        }
      },
      "assistantDestinations": [
        {
          "type": "assistant",
          "assistantName": "Scheduler",
          "description": "Transfer to this assistant when the patient needs to schedule, modify, or cancel an appointment.",
          "transferMode": "rolling-history"
        },
        {
          "type": "assistant",
          "assistantName": "Emergency",
          "description": "Transfer to this assistant when the patient indicates an emergency or urgent medical situation.",
          "transferMode": "rolling-history"
        }
      ]
    },
    {
      "assistant": {
        "name": "Scheduler",
        "firstMessage": "I'd be happy to help you with your appointment. What type of appointment do you need?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "model": "gpt-4o",
          "provider": "openai",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are a clinic scheduling assistant.\n\n[Style]\n- Be friendly and professional.\n- Offer clear time slot options.\n\n[Task & Goals]\n1. Determine appointment type.\n2. Check available providers.\n3. Offer time slots.\n4. Confirm the booking.\n5. Provide pre-visit instructions."
            }
          ]
        }
      }
    },
    {
      "assistant": {
        "name": "Emergency",
        "firstMessage": "I understand this is urgent. Let me help you right away.",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "model": "gpt-4o",
          "provider": "openai",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are an emergency medical protocol assistant.\n\n[Style]\n- Be calm but urgent.\n- Be direct and clear.\n\n[Task & Goals]\n1. Assess severity.\n2. Provide safety instructions.\n3. Connect to emergency services if needed.\n4. Connect to on-call physician if appropriate."
            }
          ]
        }
      }
    }
  ]
}
```

**Note**: The legacy approach cannot pass `{{patientName}}` variables between assistants. This is a significant limitation compared to the handoff tool approach.

---

## Example 3: E-commerce Order Management

> Source: https://docs.vapi.ai/squads/examples/ecommerce-order-management

### Use Case

An e-commerce company needs a multi-department customer service phone system:
- **Orders**: Track shipments, delivery status, order modifications
- **Returns**: Return eligibility checks, label generation, refund processing
- **VIP**: Premium customer concierge with priority handling

### Squad Architecture

```
  [Orders Assistant] <---> [Returns Assistant]
         |                        |
         +--------+  +-----------+
                  |  |
              [VIP Assistant]
```

- **Orders Assistant**: Entry point. Handles order tracking, delivery questions, and status updates. Can route to Returns or VIP.
- **Returns Assistant**: Handles return eligibility checks and label generation. Can route back to Orders or to VIP.
- **VIP Assistant**: Premium concierge for high-value customers or escalated issues. Can handle any issue with priority treatment.

### Key Design Decisions

1. **Orders as entry point**: Most customer calls start with order inquiries
2. **Bidirectional transfers**: Orders can route to Returns, and Returns can route back to Orders
3. **VIP escalation**: Any assistant can route to VIP based on customer value or sentiment
4. **External tools**: Each assistant has domain-specific tools (ORDER_LOOKUP, RETURNS_TOOL, etc.)

### Complete JSON Configuration

```json
{
  "name": "E-commerce Order Management Squad",
  "members": [
    {
      "assistant": {
        "name": "Orders",
        "firstMessage": "Hello, how can I help with your order?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Orders specialist for an e-commerce customer service team. Your expertise is in order tracking, delivery status, and order modifications.\n\n[Style]\n- Be helpful and efficient.\n- Provide specific order details when available.\n- Be proactive in offering solutions.\n\n[Task & Goals]\n1. Greet the customer.\n2. Ask for their order number or email to look up their account.\n3. Provide order status, tracking information, or delivery estimates.\n4. Handle order modification requests (cancel, change address, etc.).\n5. If the customer wants a return, use handoff_to_Returns.\n6. If the customer is a VIP or is dissatisfied, use handoff_to_VIP.\n\n[Handoff Instructions]\n- For return requests: trigger the 'handoff' tool with 'Returns' Assistant.\n- For VIP or escalated customers: trigger the 'handoff' tool with 'VIP' Assistant.\n- Never say 'transferring' or 'connecting you to'."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_Returns",
                "description": "Use when the customer wants to return an item, exchange a product, or request a refund.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["Returns"]
                    },
                    "orderNumber": {
                      "type": "string",
                      "description": "The customer's order number"
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "Returns",
                  "description": "customer wants to return an item, exchange a product, or request a refund",
                  "contextEngineeringPlan": {
                    "type": "all"
                  }
                }
              ],
              "messages": []
            },
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_VIP",
                "description": "Use when the customer is a VIP member, has spent over $1000, or is expressing significant dissatisfaction.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["VIP"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "VIP",
                  "description": "customer is a VIP member, high-value customer, or expressing significant dissatisfaction",
                  "contextEngineeringPlan": {
                    "type": "all"
                  }
                }
              ],
              "messages": []
            }
          ],
          "toolIds": ["ORDER_LOOKUP_ID"]
        }
      }
    },
    {
      "assistant": {
        "name": "Returns",
        "firstMessage": "",
        "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Returns specialist for an e-commerce customer service team. Your expertise is in return eligibility, label generation, exchanges, and refund processing.\n\n[Style]\n- Be empathetic and understanding.\n- Clearly explain return policies.\n- Make the process as simple as possible.\n\n[Response Guidelines]\n- Proceed directly to the Task section without any greetings or small talk.\n\n[Task & Goals]\n1. Verify the order is eligible for return (within 30-day window).\n2. Ask for reason for return.\n3. Generate a return shipping label.\n4. Explain the refund timeline (5-7 business days after receipt).\n5. If the customer has order questions unrelated to returns, use handoff_to_Orders.\n6. If the customer is VIP or dissatisfied, use handoff_to_VIP.\n\n[Handoff Instructions]\n- For order inquiries: trigger the 'handoff' tool with 'Orders' Assistant.\n- For VIP escalation: trigger the 'handoff' tool with 'VIP' Assistant."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_Orders",
                "description": "Use when the customer switches to asking about order status, tracking, or delivery questions.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["Orders"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "Orders",
                  "description": "customer has order status, tracking, or delivery questions",
                  "contextEngineeringPlan": {
                    "type": "all"
                  }
                }
              ],
              "messages": []
            },
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_VIP",
                "description": "Use when the customer is a VIP or is expressing significant dissatisfaction with the returns process.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["VIP"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "VIP",
                  "description": "customer is VIP or expressing significant dissatisfaction",
                  "contextEngineeringPlan": {
                    "type": "all"
                  }
                }
              ],
              "messages": []
            }
          ],
          "toolIds": ["RETURNS_TOOL_ID"]
        }
      }
    },
    {
      "assistant": {
        "name": "VIP",
        "firstMessage": "",
        "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the VIP concierge for an e-commerce customer service team. You provide premium, white-glove service to high-value customers and handle escalated situations.\n\n[Style]\n- Be exceptionally courteous and attentive.\n- Offer proactive solutions and accommodations.\n- Make the customer feel valued and prioritized.\n- Use phrases like 'I'll personally ensure...' and 'As a valued customer...'\n\n[Response Guidelines]\n- Proceed directly to the Task section without any greetings or small talk.\n\n[Task & Goals]\n1. Acknowledge the customer's importance.\n2. Review the full conversation context to understand their issue.\n3. Offer priority resolution:\n   - Expedited shipping at no cost.\n   - Extended return windows.\n   - Additional discount or store credit.\n   - Direct escalation to management if needed.\n4. Ensure complete satisfaction before ending the call.\n5. Provide a direct callback number for future issues."
            }
          ]
        }
      }
    }
  ]
}
```

### TypeScript SDK Example

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

await vapi.calls.create({
  transport: { type: "web" },
  squad: {
    members: [
      {
        assistant: {
          name: "Orders",
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [{
              role: "system",
              content: "Orders specialist. Handle tracking and delivery questions."
            }],
          },
          toolIds: ["ORDER_LOOKUP_ID"],
          firstMessage: "Hello, how can I help with your order?",
          firstMessageMode: "assistant-speaks-first",
        },
      },
      {
        assistant: {
          name: "Returns",
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [{
              role: "system",
              content: "Returns specialist. Check eligibility and generate labels."
            }],
          },
          toolIds: ["RETURNS_TOOL_ID"],
        },
      },
      {
        assistant: {
          name: "VIP",
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [{
              role: "system",
              content: "VIP concierge. Prioritize premium customers and coordinate resolutions."
            }],
          },
        },
      },
    ],
  },
});
```

---

## Example 4: Property Management Routing

> Source: https://docs.vapi.ai/squads/examples/property-management

### Use Case

A property management company needs an automated phone system for tenants:
- Route calls to the right department based on inquiry type
- Verify tenant identity via lookup tools
- Handle emergencies with priority routing
- Escalate to human staff when needed

### Squad Architecture

```
             [Router Assistant]
            /        |          \
           /         |           \
  [Maintenance]  [Leasing]   [Human Transfer]
  (repairs &     (rent &      (escalation)
   emergencies)   leasing)
```

- **Router Assistant**: Entry point. Classifies tenant inquiries into categories (emergency, maintenance, leasing, rent, general) and routes accordingly. Has tenant lookup tool for verification.
- **Maintenance Specialist**: Handles maintenance requests and emergency repairs. Prioritizes emergencies. Can escalate to human staff.
- **Leasing Specialist**: Manages leasing inquiries, rent questions, lease renewals, and general property questions.

### Key Design Decisions

1. **Router as gatekeeper**: Single entry point classifies all inquiries before routing
2. **Tenant verification**: Router has a tenant lookup tool to verify identity before transferring
3. **Emergency prioritization**: Emergencies route to Maintenance with highest priority
4. **Human escalation**: Dynamic transfer tool allows escalation to human property managers
5. **Dual-purpose Leasing**: Handles both leasing AND rent questions to minimize transfers

### Complete JSON Configuration

```json
{
  "name": "Property Management Squad",
  "members": [
    {
      "assistant": {
        "name": "Router",
        "firstMessage": "Thanks for calling Sunset Properties. How can I help you today?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the front-desk routing assistant for Sunset Properties, a property management company.\n\n[Style]\n- Be welcoming and professional.\n- Ask clarifying questions to classify the inquiry correctly.\n- Be efficient -- route the tenant quickly.\n\n[Task & Goals]\n1. Greet the caller.\n2. Ask for their name and unit number to verify their identity.\n3. Use the tenant_lookup tool to verify they are a current tenant.\n4. Ask how you can help them today.\n5. Classify the inquiry into one of these categories:\n   - EMERGENCY: Water leak, gas leak, fire, break-in, no heat in winter, no AC in extreme heat\n   - MAINTENANCE: Broken appliance, plumbing issue, electrical problem, pest control, general repair\n   - LEASING: Lease renewal, lease questions, move-in/move-out, new tenant inquiry\n   - RENT: Rent payment, payment plan, late fee questions, balance inquiry\n   - GENERAL: Noise complaint, parking, amenities, community events\n\n6. Route based on classification:\n   - EMERGENCY or MAINTENANCE: trigger handoff_to_Maintenance\n   - LEASING, RENT, or GENERAL: trigger handoff_to_Leasing\n\n7. Never say 'transferring' or 'connecting you to another department'."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_Maintenance",
                "description": "Use when the tenant has an emergency (water leak, gas leak, fire, no heat/AC) or a maintenance request (broken appliance, plumbing, electrical, pest control, repairs).",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["Maintenance"]
                    },
                    "tenantName": {
                      "type": "string",
                      "description": "Tenant's full name"
                    },
                    "unitNumber": {
                      "type": "string",
                      "description": "Tenant's unit number"
                    },
                    "isEmergency": {
                      "type": "boolean",
                      "description": "Whether this is an emergency situation"
                    }
                  },
                  "required": ["destination", "tenantName", "unitNumber"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "Maintenance",
                  "description": "tenant has an emergency or maintenance request",
                  "contextEngineeringPlan": {
                    "type": "all"
                  },
                  "variableExtractionPlan": {
                    "tenantName": {
                      "type": "conversation",
                      "description": "Extract the tenant's full name"
                    },
                    "unitNumber": {
                      "type": "conversation",
                      "description": "Extract the tenant's unit number"
                    }
                  }
                }
              ],
              "messages": []
            },
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_Leasing",
                "description": "Use when the tenant has questions about leasing, rent, payments, lease renewals, or general property questions.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["Leasing"]
                    },
                    "tenantName": {
                      "type": "string",
                      "description": "Tenant's full name"
                    },
                    "unitNumber": {
                      "type": "string",
                      "description": "Tenant's unit number"
                    }
                  },
                  "required": ["destination", "tenantName", "unitNumber"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "Leasing",
                  "description": "tenant has leasing, rent, or general property questions",
                  "contextEngineeringPlan": {
                    "type": "all"
                  },
                  "variableExtractionPlan": {
                    "tenantName": {
                      "type": "conversation",
                      "description": "Extract the tenant's full name"
                    },
                    "unitNumber": {
                      "type": "conversation",
                      "description": "Extract the tenant's unit number"
                    }
                  }
                }
              ],
              "messages": []
            }
          ],
          "toolIds": ["TENANT_LOOKUP_ID"]
        }
      }
    },
    {
      "assistant": {
        "name": "Maintenance",
        "firstMessage": "",
        "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Maintenance Specialist for Sunset Properties.\n\n[Tenant Information]\n- Name: {{tenantName}}\n- Unit: {{unitNumber}}\n\n[Style]\n- Be professional and reassuring.\n- For emergencies, be direct and efficient.\n- For routine maintenance, be thorough in collecting details.\n\n[Response Guidelines]\n- Proceed directly to the Task section without any greetings or small talk.\n- Address the tenant by name.\n\n[Task & Goals]\n1. Determine if this is an EMERGENCY or ROUTINE maintenance.\n2. For EMERGENCIES:\n   - Get the exact nature of the emergency.\n   - Provide immediate safety instructions (e.g., 'Turn off the water main valve under the sink').\n   - Dispatch emergency maintenance crew immediately.\n   - Provide ETA for crew arrival.\n3. For ROUTINE MAINTENANCE:\n   - Collect detailed description of the issue.\n   - Ask when the tenant is available for a technician visit.\n   - Schedule the maintenance visit.\n   - Provide a work order confirmation number.\n4. If the issue requires human intervention beyond your capabilities, escalate to the property manager."
            }
          ],
          "toolIds": ["MAINTENANCE_REQUEST_ID", "EMERGENCY_DISPATCH_ID"]
        }
      }
    },
    {
      "assistant": {
        "name": "Leasing",
        "firstMessage": "",
        "firstMessageMode": "assistant-speaks-first-with-model-generated-message",
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Leasing Specialist for Sunset Properties.\n\n[Tenant Information]\n- Name: {{tenantName}}\n- Unit: {{unitNumber}}\n\n[Style]\n- Be friendly and knowledgeable.\n- Provide clear information about policies.\n- Be helpful with payment arrangements.\n\n[Response Guidelines]\n- Proceed directly to the Task section without any greetings or small talk.\n- Address the tenant by name.\n\n[Task & Goals]\n1. Determine the nature of the inquiry:\n   - LEASE RENEWAL: Check current lease terms, offer renewal options, explain any rate changes.\n   - RENT PAYMENT: Provide balance information, accept payment, set up payment plans.\n   - LATE FEES: Explain late fee policies, process waiver requests if applicable.\n   - MOVE-IN/MOVE-OUT: Explain procedures, schedule inspections, handle deposits.\n   - GENERAL: Answer questions about amenities, parking, community policies.\n2. Provide accurate information based on the tenant's lease agreement.\n3. Process any payments or requests.\n4. If the issue requires human intervention, escalate to the leasing manager."
            }
          ],
          "toolIds": ["LEASE_LOOKUP_ID", "PAYMENT_PROCESSING_ID"]
        }
      }
    }
  ]
}
```

---

## Example 5: Multilingual Support

> Source: https://docs.vapi.ai/squads/examples/multilingual-support

### Use Case

A company needs to support customers in multiple languages (English, Spanish, French) with:
- A language selection router that greets in all three languages
- Language-specific assistants with native voices and culturally appropriate prompts
- Automatic language detection via multilingual transcriber

### Squad Architecture

```
           [Language Router]
          /       |         \
         /        |          \
  [English]  [Spanish]   [French]
  (en-US)    (es-ES)     (fr-FR)
```

- **Language Router**: Entry point. Greets the caller in all three languages and asks for language preference. Routes to the appropriate language specialist.
- **English Support**: Handles support in English. Direct, friendly, professional tone. Uses `en-US-AriaNeural` Azure voice.
- **Soporte Espanol**: Handles support in Spanish. Warm, respectful, formal "usted" form. Uses `es-ES-ElviraNeural` Azure voice.
- **Support Francais**: Handles support in French. Polite, courteous, formal. Uses `fr-FR-DeniseNeural` Azure voice.

### Key Design Decisions

1. **Explicit language selection**: Router asks the customer to choose their language (more reliable than auto-detection for a squad)
2. **Native voices**: Each assistant uses a language-appropriate Azure Neural voice
3. **Cultural tone**: Each assistant's prompt is tuned for cultural norms (e.g., Spanish uses "usted", French uses formal address)
4. **Multilingual transcriber**: Uses Deepgram with `language: "multi"` on the router for initial detection
5. **Dedicated assistants**: Each language gets its own assistant rather than one multilingual assistant, allowing for specialized voice and prompt configurations

### Complete JSON Configuration

```json
{
  "name": "Multilingual Support Squad",
  "members": [
    {
      "assistant": {
        "name": "LanguageRouter",
        "firstMessage": "Hello! Hola! Bonjour! Welcome to Global Support. For English, say 'English'. Para espanol, diga 'espanol'. Pour le francais, dites 'francais'.",
        "firstMessageMode": "assistant-speaks-first",
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2",
          "language": "multi"
        },
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are the Language Router for Global Support. Your sole job is to determine the customer's preferred language and route them to the appropriate specialist.\n\n[Style]\n- Be brief and efficient.\n- Speak clearly and slowly.\n\n[Task & Goals]\n1. Greet the customer in all three supported languages.\n2. Ask them to state their preferred language.\n3. Route based on their response:\n   - English or any English response: trigger handoff_to_EnglishSupport\n   - Spanish/Espanol or any Spanish response: trigger handoff_to_SoporteEspanol\n   - French/Francais or any French response: trigger handoff_to_SupportFrancais\n4. If you cannot determine the language, default to English.\n5. Never say 'transferring' -- just trigger the handoff."
            }
          ],
          "tools": [
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_EnglishSupport",
                "description": "Use when the customer indicates they want to speak in English.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["English Support"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "English Support",
                  "description": "customer wants to speak in English",
                  "contextEngineeringPlan": {
                    "type": "none"
                  }
                }
              ],
              "messages": []
            },
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_SoporteEspanol",
                "description": "Use when the customer indicates they want to speak in Spanish / espanol.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["Soporte Espanol"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "Soporte Espanol",
                  "description": "customer wants to speak in Spanish (espanol)",
                  "contextEngineeringPlan": {
                    "type": "none"
                  }
                }
              ],
              "messages": []
            },
            {
              "type": "handoff",
              "function": {
                "name": "handoff_to_SupportFrancais",
                "description": "Use when the customer indicates they want to speak in French / francais.",
                "parameters": {
                  "type": "object",
                  "properties": {
                    "destination": {
                      "type": "string",
                      "enum": ["Support Francais"]
                    }
                  },
                  "required": ["destination"]
                }
              },
              "destinations": [
                {
                  "type": "assistant",
                  "assistantName": "Support Francais",
                  "description": "customer wants to speak in French (francais)",
                  "contextEngineeringPlan": {
                    "type": "none"
                  }
                }
              ],
              "messages": []
            }
          ]
        },
        "voice": {
          "provider": "azure",
          "voiceId": "en-US-AriaNeural"
        }
      }
    },
    {
      "assistant": {
        "name": "English Support",
        "firstMessage": "Hello! How can I help you today?",
        "firstMessageMode": "assistant-speaks-first",
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2",
          "language": "en"
        },
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identity]\nYou are an English-speaking customer support agent for Global Support.\n\n[Style]\n- Be direct, friendly, and professional.\n- Use clear, simple language.\n- Be conversational but efficient.\n- Use American English conventions.\n\n[Task & Goals]\n1. Greet the customer warmly.\n2. Ask how you can help them.\n3. Handle their inquiry:\n   - Account questions\n   - Product support\n   - Billing inquiries\n   - Technical troubleshooting\n4. Resolve the issue or escalate as needed.\n5. Confirm resolution and thank the customer."
            }
          ]
        },
        "voice": {
          "provider": "azure",
          "voiceId": "en-US-AriaNeural"
        }
      }
    },
    {
      "assistant": {
        "name": "Soporte Espanol",
        "firstMessage": "Hola, bienvenido al soporte de Global Support. Como puedo ayudarle hoy?",
        "firstMessageMode": "assistant-speaks-first",
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2",
          "language": "es"
        },
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identidad]\nEres un agente de soporte al cliente que habla espanol para Global Support.\n\n[Estilo]\n- Se calido y respetuoso.\n- Usa 'usted' inicialmente hasta que el cliente prefiera un trato informal.\n- Se claro y servicial.\n- Usa convenciones del espanol de Espana.\n\n[Tareas y Objetivos]\n1. Saludar al cliente cordialmente.\n2. Preguntar como puede ayudarle.\n3. Manejar su consulta:\n   - Preguntas sobre su cuenta\n   - Soporte de productos\n   - Consultas de facturacion\n   - Solucion de problemas tecnicos\n4. Resolver el problema o escalar segun sea necesario.\n5. Confirmar la resolucion y agradecer al cliente."
            }
          ]
        },
        "voice": {
          "provider": "azure",
          "voiceId": "es-ES-ElviraNeural"
        }
      }
    },
    {
      "assistant": {
        "name": "Support Francais",
        "firstMessage": "Bonjour et bienvenue chez Global Support. Comment puis-je vous aider aujourd'hui?",
        "firstMessageMode": "assistant-speaks-first",
        "transcriber": {
          "provider": "deepgram",
          "model": "nova-2",
          "language": "fr"
        },
        "model": {
          "provider": "openai",
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "[Identite]\nVous etes un agent de support client francophone pour Global Support.\n\n[Style]\n- Soyez poli, courtois et formel.\n- Utilisez le vouvoiement.\n- Soyez clair et serviable.\n- Utilisez les conventions du francais de France.\n\n[Taches et Objectifs]\n1. Accueillir le client chaleureusement.\n2. Demander comment vous pouvez l'aider.\n3. Traiter sa demande:\n   - Questions sur son compte\n   - Support produit\n   - Questions de facturation\n   - Depannage technique\n4. Resoudre le probleme ou escalader si necessaire.\n5. Confirmer la resolution et remercier le client."
            }
          ]
        },
        "voice": {
          "provider": "azure",
          "voiceId": "fr-FR-DeniseNeural"
        }
      }
    }
  ]
}
```

### TypeScript SDK Example with Multilingual Transcriber

```typescript
import { VapiClient } from "@vapi-ai/server-sdk";

const vapi = new VapiClient({ token: process.env.VAPI_API_KEY! });

// Language-specific voice configurations
const voices = {
  english: { provider: "azure" as const, voiceId: "en-US-AriaNeural" },
  spanish: { provider: "azure" as const, voiceId: "es-ES-ElviraNeural" },
  french: { provider: "azure" as const, voiceId: "fr-FR-DeniseNeural" },
};

// Language-specific transcriber configurations
const transcribers = {
  multi: { provider: "deepgram" as const, model: "nova-2", language: "multi" },
  english: { provider: "deepgram" as const, model: "nova-2", language: "en" },
  spanish: { provider: "deepgram" as const, model: "nova-2", language: "es" },
  french: { provider: "deepgram" as const, model: "nova-2", language: "fr" },
};

await vapi.calls.create({
  transport: { type: "web" },
  squad: {
    members: [
      {
        assistant: {
          name: "LanguageRouter",
          firstMessage:
            "Hello! Hola! Bonjour! Welcome to Global Support. " +
            "For English, say 'English'. " +
            "Para espanol, diga 'espanol'. " +
            "Pour le francais, dites 'francais'.",
          firstMessageMode: "assistant-speaks-first",
          transcriber: transcribers.multi,
          voice: voices.english,
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [
              {
                role: "system",
                content:
                  "You are a language router. Determine the customer's preferred language " +
                  "and route them. Supported: English, Spanish, French. " +
                  "Default to English if unclear.",
              },
            ],
            tools: [
              {
                type: "handoff",
                function: {
                  name: "handoff_to_English",
                  description: "Customer wants English support",
                },
                destinations: [
                  {
                    type: "assistant",
                    assistantName: "English Support",
                    description: "customer wants English",
                    contextEngineeringPlan: { type: "none" },
                  },
                ],
                messages: [],
              },
              {
                type: "handoff",
                function: {
                  name: "handoff_to_Spanish",
                  description: "Customer wants Spanish support",
                },
                destinations: [
                  {
                    type: "assistant",
                    assistantName: "Soporte Espanol",
                    description: "customer wants Spanish",
                    contextEngineeringPlan: { type: "none" },
                  },
                ],
                messages: [],
              },
              {
                type: "handoff",
                function: {
                  name: "handoff_to_French",
                  description: "Customer wants French support",
                },
                destinations: [
                  {
                    type: "assistant",
                    assistantName: "Support Francais",
                    description: "customer wants French",
                    contextEngineeringPlan: { type: "none" },
                  },
                ],
                messages: [],
              },
            ],
          },
        },
      },
      {
        assistant: {
          name: "English Support",
          firstMessage: "Hello! How can I help you today?",
          firstMessageMode: "assistant-speaks-first",
          transcriber: transcribers.english,
          voice: voices.english,
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [
              {
                role: "system",
                content:
                  "English support agent. Direct, friendly, professional tone. " +
                  "Handle account, product, billing, and technical inquiries.",
              },
            ],
          },
        },
      },
      {
        assistant: {
          name: "Soporte Espanol",
          firstMessage:
            "Hola, bienvenido al soporte de Global Support. Como puedo ayudarle hoy?",
          firstMessageMode: "assistant-speaks-first",
          transcriber: transcribers.spanish,
          voice: voices.spanish,
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [
              {
                role: "system",
                content:
                  "Soporte en espanol. Calido y respetuoso; usa 'usted' inicialmente. " +
                  "Maneja consultas de cuenta, productos, facturacion y problemas tecnicos.",
              },
            ],
          },
        },
      },
      {
        assistant: {
          name: "Support Francais",
          firstMessage:
            "Bonjour et bienvenue chez Global Support. Comment puis-je vous aider aujourd'hui?",
          firstMessageMode: "assistant-speaks-first",
          transcriber: transcribers.french,
          voice: voices.french,
          model: {
            provider: "openai",
            model: "gpt-4o",
            messages: [
              {
                role: "system",
                content:
                  "Support francais. Poli, courtois et formel. Utilisez le vouvoiement. " +
                  "Traite les demandes de compte, produit, facturation et technique.",
              },
            ],
          },
        },
      },
    ],
  },
});
```

### Language-Specific Voice Configurations

| Language | Azure Voice ID | Character | Tone |
|----------|---------------|-----------|------|
| English (US) | `en-US-AriaNeural` | Professional female | Direct, friendly |
| Spanish (Spain) | `es-ES-ElviraNeural` | Professional female | Warm, respectful, formal |
| French (France) | `fr-FR-DeniseNeural` | Professional female | Polite, courteous, formal |

### Transcriber Configuration for Language Detection

```json
{
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-2",
    "language": "multi"
  }
}
```

The `language: "multi"` setting enables **automatic language detection** on the Deepgram transcriber. This is used on the Language Router so it can understand the customer's response regardless of which language they speak. Once routed, each language-specific assistant uses a fixed language transcriber (e.g., `language: "en"`) for optimal accuracy.

**Alternative**: Google transcriber with `language: "multilingual"`:

```json
{
  "transcriber": {
    "provider": "google",
    "model": "latest",
    "language": "multilingual"
  }
}
```

---

## Summary: Choosing the Right Pattern

| Example | Best For | Key Feature |
|---------|----------|-------------|
| **Clinic Triage (Handoff Tool)** | Healthcare routing with personalization | Variable extraction (patientName) |
| **Clinic Triage (Legacy)** | Understanding older squad patterns | assistantDestinations comparison |
| **E-commerce Order Management** | Multi-department customer service | Bidirectional transfers, VIP escalation |
| **Property Management** | Tenant services with verification | Tenant lookup tool, emergency prioritization |
| **Multilingual Support** | International customer service | Language-specific voices and transcribers |

---

Doc refs:
- https://docs.vapi.ai/squads/examples/clinic-triage-scheduling-handoff-tool
- https://docs.vapi.ai/squads/examples/clinic-triage-scheduling
- https://docs.vapi.ai/squads/examples/ecommerce-order-management
- https://docs.vapi.ai/squads/examples/property-management
- https://docs.vapi.ai/squads/examples/multilingual-support
