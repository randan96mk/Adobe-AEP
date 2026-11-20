# AEP cheat sheets

Keep this open in project meetings. Each sheet links to the chapter with the full explanation.

## 1. Which class? (Ch 3)

| Question | Class |
| --- | --- |
| Describes who the person is *now* (name, tier, consent) | XDM Individual Profile (record) |
| Something that *happened* at a time (view, purchase, open) | XDM ExperienceEvent (time-series) |
| Reference data (products, stores) | Custom record class + relationship (lookup) |
| Companies, opportunities (B2B) | XDM Business Account / Opportunity |

## 2. Batch, streaming or edge? (Ch 2, 5, 8)

| Need | Choose | Typical latency |
| --- | --- | --- |
| Daily reports, nightly CRM updates | Batch ingestion + batch audience | hours |
| Abandoned cart, real-time triggers | Streaming ingestion + streaming audience | minutes |
| Personalize the same page/visit | Web SDK + edge audience | milliseconds |

## 3. Data lake vs Profile (Ch 2, 7)

| Lake only | Profile-enabled |
| --- | --- |
| Full history, analytics, Query Service, CJA | Audiences, destinations, AJO, edge personalization |
| Cheaper, no profile licence impact | Counts towards profile richness and licence |

## 4. Schema change rules (Ch 3)

Allowed after Profile enablement: **add** fields/field groups/descriptors.
Not allowed: remove, rename, change type, make required, change primary identity once data exists.

## 5. API essentials (Ch 2, 15)

```text
Base:  https://platform.adobe.io
Token: POST https://ims-na1.adobelogin.com/ims/token/v3 (client_credentials)
Headers: Authorization: Bearer <token> | x-api-key | x-gw-ims-org-id | x-sandbox-name
```

| Service | Path |
| --- | --- |
| Schema Registry | `/data/foundation/schemaregistry` |
| Catalog (datasets, batches) | `/data/foundation/catalog` |
| Batch ingestion | `/data/foundation/import` |
| Flow Service (sources, destinations) | `/data/foundation/flowservice` |
| Identity namespaces | `/data/core/idnamespace` |
| Profile | `/data/core/ups` |
| Query Service | `/data/foundation/query` |
| Sandbox management | `/data/foundation/sandbox-management` |

## 6. Guardrails to quote (Ch 2; check the live pages)

| Limit | Default |
| --- | --- |
| ExperienceEvents per profile used in segmentation | latest 5,000 |
| Max ExperienceEvent size | 10 KB (hard) |
| ExperienceEvent datasets in Profile | 20 recommended |
| Profile + event batches per day per sandbox | 90 |

## 7. Questions to ask in any design meeting (Ch 1)

1. Which sandbox, and how do we promote?
2. Primary identity per dataset? Profile-enabled?
3. Batch, streaming or edge for this use case?
4. Which merge policy?
5. Labels and consent before activation?
6. Volumes vs guardrails?
7. How do we measure success?

## 8. Troubleshooting quick map

| Symptom | Look at |
| --- | --- |
| Data missing in dataset | Dataflow / batch status, error diagnostics, mapping |
| Web events missing | Tags rule, Web SDK in Debugger/Assurance, datastream, dataset |
| Profile not found | Dataset Profile flag, primary identity, namespace value format |
| Profiles over-merged | Identity graph viewer, shared identifiers, graph linking rules |
| Audience count unexpected | Definition, merge policy, evaluation job, source data freshness |
| Destination failing | Activation monitoring, identity mapping, consent policy, partner errors |

## 9. Merge policy quick choice (Ch 7)

| Situation | Choose |
| --- | --- |
| Person-level use cases | ID stitching = Private graph |
| Latest value should win | Timestamp ordered (default) |
| One source must always win (consent platform, CRM) | Dataset precedence, list **all** datasets |
| Edge personalization | Mark one policy active-on-edge |

## 10. Journey Optimizer quick choice (Ch 12)

| Need | Use |
| --- | --- |
| Newsletter, scheduled broadcast | Campaign |
| Transactional message triggered by another system | API-triggered campaign |
| React to one person's action | Unitary event journey |
| React to entering/exiting an audience | Audience qualification journey (streaming audience) |
| Scheduled multi-step flow for an audience | Read audience journey |
| Something happened to many people (back in stock) | Business event journey |

Guardrails to quote: unitary + qualification journeys share 5,000 events/s per org; 5-minute default re-entrance; 64 KB journey event size.

## 11. Governance quick reference (Ch 14)

| Label | Meaning |
| --- | --- |
| C2 | No export to third parties (core policy "3rd party export restriction") |
| C12 | No export at all |
| I1 / I2 | Directly / indirectly identifiable |
| S1 / S2 | Precise location / broad geofence |

Policy = label + marketing action. Destinations need marketing actions. Consent: model on profile, dataset precedence, consent policies (by licence).

## 12. CJA in one line each (Ch 13)

- **Connection**: datasets + person ID. **Data view**: how fields behave in reports. **Stitching**: field-based (dataset fields) or graph-based (identity graph).
