# AEP glossary

Plain-language definitions, with the chapter that explains each term.

| Term | Meaning | Ch |
| --- | --- | --- |
| **Activation** | Sending audiences or data from AEP to a destination | 10 |
| **Active-on-edge merge policy** | The merge policy used for edge segmentation and edge profiles | 7 |
| **AJO (Adobe Journey Optimizer)** | AEP application for journeys, campaigns, messaging and decisioning | 12 |
| **Attribute-based access control (ABAC)** | Restricting access to fields/objects by labels | 14 |
| **Audience** | A group of profiles matching a definition (formerly "segment") | 8 |
| **Audience Composition** | Visual tool to combine, split, exclude and enrich audiences | 8 |
| **Audience Portal** | Central inventory of all audiences, whatever their origin | 8 |
| **Batch ingestion** | Loading files into datasets (create batch, upload, complete) | 5 |
| **Business event** | AJO event that affects many profiles at once | 12 |
| **Campaign (AJO)** | Scheduled/recurring or API-triggered send to an audience | 12 |
| **Class** | Base type of a schema: Individual Profile, ExperienceEvent, B2B classes, custom | 3 |
| **CJA (Customer Journey Analytics)** | AEP-based analytics application using Analysis Workspace | 13 |
| **Computed attribute** | Profile field calculated by AEP from events (e.g. spend last 30 days) | 7 |
| **Connection (CJA)** | The datasets and person IDs CJA reads | 13 |
| **Consent** | A person's permissions (collect, marketing, personalization), stored on the profile | 6, 14 |
| **Custom action** | AJO call to an external REST API from a journey | 12 |
| **Data Distiller** | Licensed add-on for batch SQL, derived datasets and scheduling | 9 |
| **Data Prep** | Mapping and transformation of fields during ingestion | 5 |
| **Data usage label** | Tag describing restrictions on data (C, I, S families, custom) | 14 |
| **Data view (CJA)** | Defines dimensions, metrics and settings on a connection | 13 |
| **Dataset** | A table in the data lake holding data for one schema | 2, 5 |
| **Dataset precedence** | Merge method where higher-ranked datasets win | 7 |
| **Datastream** | Edge configuration that routes SDK data to AEP, Target, Analytics, AJO... | 6 |
| **Destination** | An outside (or Adobe) system that receives activated data | 10 |
| **Destination SDK** | Framework to build custom streaming/file destinations by configuration | 10 |
| **ECID** | Experience Cloud ID: anonymous browser/device ID | 4, 6 |
| **Edge Network** | Adobe's global network receiving SDK calls and doing same-page personalization | 2, 6 |
| **Edge segmentation** | Audience evaluation in milliseconds on the Edge Network | 8 |
| **Event forwarding** | Server-side forwarding of Edge data to third parties | 6 |
| **ExperienceEvent** | Time-series XDM class for things that happened | 3 |
| **Federated Audience Composition** | Build audiences on the client's data warehouse without copying data | 8 |
| **Field group** | Reusable block of fields added to schemas (formerly "mixin") | 3 |
| **Guardrails** | Adobe's documented default limits (hard or performance) | 2 |
| **Identity graph** | Linked identities that belong to one person | 4 |
| **Identity graph linking rules** | Unique namespaces + namespace priority to prevent over-merging | 4 |
| **identityMap** | Map of identities sent inside an event | 3, 6 |
| **Individual Profile (class)** | Record XDM class for attributes about a person | 3 |
| **Marketing action** | A declared data use (e.g. Export to third party) checked by policies | 10, 14 |
| **Merge policy** | Rules for stitching identities and resolving attribute conflicts | 7 |
| **Namespace** | The type of an identity (ECID, Email, crmId...) | 4 |
| **OAuth Server-to-Server** | Credential type for scripts and integrations calling Adobe APIs | 15 |
| **Over-merging (graph collapse)** | Different people wrongly merged into one profile | 4 |
| **PQL (Profile Query Language)** | Language behind audience definitions | 8 |
| **Primary identity** | The identity that decides which profile a record/event is stored against | 3, 4 |
| **Privacy Service** | Processes access/delete requests (GDPR, CCPA...) | 14 |
| **Profile fragment** | Data from one dataset for one identity; merged at read time | 7 |
| **Query Service** | SQL over the data lake | 9 |
| **Real-Time CDP** | AEP application for profiles, audiences and activation (B2C, B2B, B2P; Prime, Ultimate) | 11 |
| **Real-Time Customer Profile** | AEP's merged, real-time view of each person | 7 |
| **Sandbox** | Isolated environment (production or development) | 2 |
| **Sandbox tooling** | Packages to move configuration between sandboxes | 15 |
| **Schema** | Structure of data: a class plus field groups | 3 |
| **Source (connector)** | Configured connection that brings data into AEP | 5 |
| **Stitching (CJA)** | Re-keying anonymous events to a person ID (field-based or graph-based) | 13 |
| **Streaming ingestion** | Sending records/events over HTTP in real time | 5 |
| **Streaming segmentation** | Audience evaluation within minutes as data arrives | 8 |
| **Tags** | Adobe's tag manager (formerly Launch) used to deploy the Web SDK | 6 |
| **Tenant namespace** | `_<tenantId>` object holding an organization's custom fields | 3 |
| **Union schema** | Combined view of all Profile-enabled schemas of a class | 3 |
| **Unitary event** | AJO event about one person that starts/moves a journey | 12 |
| **Web SDK (alloy.js)** | JavaScript library sending web data to the Edge Network | 6 |
| **XDM** | Experience Data Model: Adobe's standard data model | 3 |
