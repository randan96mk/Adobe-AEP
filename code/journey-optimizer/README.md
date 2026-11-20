# Journey Optimizer examples (Chapter 12)

| File | What it shows |
| --- | --- |
| `unitary-event-cart-abandoned.json` | Event payload for a unitary-event journey, including the orchestration event ID |
| `custom-action-crm-task.json` | What to configure for a custom action calling a CRM API |
| `personalization-examples.md` | Profile, condition, loop and audience personalization syntax |

Send the event with `code/api/stream_record.py` (HTTP API) or from the website with the Web SDK
(`code/web-sdk`). The schema must include the journey orchestration field group so
`_experience.campaign.orchestration.eventID` exists.
