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
