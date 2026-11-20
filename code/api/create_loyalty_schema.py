"""
Build the Chapter 3 loyalty model end to end in a DEVELOPMENT sandbox:

  1. read tenant ID
  2. create custom identity namespace 'loyaltyId' (if missing)
  3. create the custom field group from code/xdm-schemas/fieldgroup-loyalty.json
  4. create the Profile schema (standard + custom field groups)
  5. add the identity descriptor (loyaltyId = primary identity)
  6. enable the schema for Real-Time Customer Profile ('union' tag)
  7. create a dataset enabled for Profile and Identity

Run:
    python create_loyalty_schema.py            # does everything
    python create_loyalty_schema.py --dry-run  # prints the payloads only

Docs:
    https://experienceleague.adobe.com/en/docs/experience-platform/xdm/tutorials/create-schema-api
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote

from aep_client import AEPClient

ROOT = Path(__file__).resolve().parents[1] / "xdm-schemas"
SR = "/data/foundation/schemaregistry"
JSON = {"Content-Type": "application/json", "Accept": "application/vnd.adobe.xed+json"}
NAMESPACE_CODE = "loyaltyId"


def load(name: str, tenant: str) -> dict:
    text = (ROOT / name).read_text().replace("<TENANT_ID>", tenant)
    return json.loads(text)


def ensure_namespace(aep: AEPClient) -> None:
    existing = aep.get("/data/core/idnamespace/identities")
    if any(ns.get("code") == NAMESPACE_CODE for ns in existing):
        print(f"Namespace '{NAMESPACE_CODE}' already exists")
        return
    aep.post(
        "/data/core/idnamespace/identities",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Loyalty ID",
            "code": NAMESPACE_CODE,
            "idType": "CROSS_DEVICE",
            "description": "Acme loyalty member number",
        },
    )
    print(f"Created namespace '{NAMESPACE_CODE}'")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print payloads, call nothing except stats")
    args = parser.parse_args()

    aep = AEPClient()
    if aep.sandbox == "prod":
        raise SystemExit("Refusing to run in 'prod'. Set AEP_SANDBOX to a development sandbox.")

    tenant = aep.get(f"{SR}/stats", headers={"Accept": "application/json"})["tenantId"]
    print(f"Tenant: {tenant}  Sandbox: {aep.sandbox}")

    field_group = load("fieldgroup-loyalty.json", tenant)
    if args.dry_run:
        print(json.dumps(field_group, indent=2))
        return

    # 2. identity namespace
    ensure_namespace(aep)

    # 3. custom field group
    fg = aep.post(f"{SR}/tenant/fieldgroups", headers=JSON, json=field_group)
    fg_id = fg["$id"]
    print(f"Field group: {fg_id}")

    # 4. schema
    schema_body = load("schema-loyalty-members.json", tenant)
    schema_body["allOf"][-1]["$ref"] = fg_id
    schema = aep.post(f"{SR}/tenant/schemas", headers=JSON, json=schema_body)
    schema_id, schema_alt = schema["$id"], schema["meta:altId"]
    print(f"Schema: {schema_id}")

    # 5. identity descriptor (primary identity)
    descriptor = load("descriptor-identity-loyaltyid.json", tenant)
    descriptor["xdm:sourceSchema"] = schema_id
    aep.post(f"{SR}/tenant/descriptors", headers={"Content-Type": "application/json"}, json=descriptor)
    print("Identity descriptor added (loyaltyId, primary)")

    # 6. enable for Profile
    aep.patch(
        f"{SR}/tenant/schemas/{quote(schema_alt, safe='')}",
        headers=JSON,
        json=[{"op": "add", "path": "/meta:immutableTags", "value": ["union"]}],
    )
    print("Schema enabled for Profile")

    # 7. dataset enabled for Profile + Identity
    ds = aep.post(
        "/data/foundation/catalog/dataSets",
        headers={"Content-Type": "application/json"},
        json={
            "name": "Acme - Loyalty Members - CRM",
            "schemaRef": {"id": schema_id, "contentType": "application/vnd.adobe.xed-full+json;version=1"},
            "tags": {"unifiedProfile": ["enabled:true"], "unifiedIdentity": ["enabled:true"]},
        },
    )
    print(f"Dataset: {ds}")
    print("Done. Next: ingest code/xdm-schemas/sample-profile-record.json (Chapter 5).")


if __name__ == "__main__":
    main()
