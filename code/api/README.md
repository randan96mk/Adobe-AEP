# Platform API scripts (Python)

## 1. One-time setup

1. In **Adobe Developer Console** (developer.adobe.com/console), open or create a project in the client's organization.
2. **Add API → Experience Platform API → OAuth Server-to-Server**. Assign the product profile(s) that give access to the sandbox you will use.
3. Copy the **Client ID**, **Client secret**, **Organization ID** and the **scopes** shown on the credential.
4. Ask the AEP admin to give the credential's technical account a **role** in AEP Permissions for your development sandbox.
5. Locally:

```bash
cd code/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then edit .env
python explore_sandbox.py
```

Never commit `.env` (it is in `.gitignore`). Tokens last about 24 hours; `aep_client.py` caches and renews them.

## 2. Scripts

| Script | What it does | Chapter |
| --- | --- | --- |
| `aep_client.py` | Token + headers + request helpers used by every script | 2, 15 |
| `explore_sandbox.py` | Tenant ID, custom schemas, datasets with Profile flag | 1 |
| `create_loyalty_schema.py` | Namespace, field group, schema, identity, Profile enablement, dataset | 3 |
| `identity_tools.py` | List/create identity namespaces; normalize and SHA-256 hash emails and phones | 4 |
| `batch_ingest.py` | Create batch, upload JSON, complete, poll status | 5 |
| `stream_record.py` | Send an XDM record/event to an HTTP API streaming inlet | 5 |
| `profile_lookup.py` | Look up a merged profile, its events, list merge policies | 7 |
| `audiences.py` | List/create segment definitions, run and check evaluation jobs | 8 |
| `query_job.py` | Run SQL via the Query Service API and wait for the result state | 9 |
| `destination_flows.py` | List destination dataflows and recent activation runs | 10 |
| `privacy_request.py` | Submit and track Privacy Service access/delete requests | 14 |


## 3. The four headers

```text
Authorization: Bearer <access_token>
x-api-key: <client_id>
x-gw-ims-org-id: <org_id>@AdobeOrg
x-sandbox-name: <sandbox_name>
```

## 4. curl equivalent (token)

```bash
curl -s -X POST 'https://ims-na1.adobelogin.com/ims/token/v3' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "grant_type=client_credentials&client_id=$AEP_CLIENT_ID&client_secret=$AEP_CLIENT_SECRET&scope=$AEP_SCOPES"
```

Docs: [Getting started with Platform APIs](https://experienceleague.adobe.com/en/docs/experience-platform/landing/platform-apis/api-guide) · [API reference](https://developer.adobe.com/experience-platform-apis/)
