# Query Service / Data Distiller SQL (Chapter 9)

| File | Purpose |
| --- | --- |
| `01-explore.sql` | Tables, sample rows, volume per day, event types |
| `02-commerce-analysis.sql` | Product revenue (exploding arrays), cart-to-purchase rate |
| `03-data-quality-and-identity.sql` | Placeholder IDs, shared emails, shared devices, duplicate events |
| `04-derived-dataset-rfm.sql` | Data Distiller derived dataset: RFM per member |
| `05-sessionization.sql` | Sessions with `SESS_TIMEOUT` |

Table names (`acme_web_events`, `acme_loyalty_members`, `acme_pos_transactions`) and the tenant
namespace (`_acmeretail`) are examples: replace them with your dataset table names and tenant.
Run in the UI (Queries → Create query), with `psql`, or with `code/api/query_job.py`.
