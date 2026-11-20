# Web SDK examples (Chapter 6)

| File | What it shows |
| --- | --- |
| `web-sdk-demo.html` | Complete demo page: configure, page view, product view, login identity, add to cart, purchase, consent |
| `commerce-events.js` | Reusable helpers for standard commerce events (XDM Commerce Details) |
| `consent.js` | `setConsent` with the Adobe 2.0 standard |
| `eds-delayed.js` | Loading the Web SDK in the delayed phase of an Edge Delivery Services site |
| `server-api-interact.sh` | Server-side event through the Edge Network Server API |

Before running, replace `<DATASTREAM_ID>` and `<ORG_ID>` with values from a **development** datastream.
The event schema behind the datastream should include the *AEP Web SDK ExperienceEvent*, *Web Details*
and *Commerce Details* field groups, plus a `crmId` identity namespace if you send it.

Check the current library version on the [Web SDK docs](https://experienceleague.adobe.com/en/docs/experience-platform/web-sdk/home)
(2.37.1 was the latest stable release on npm in November 2026).
