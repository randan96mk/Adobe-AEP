"""
Send one XDM record or event to an HTTP API streaming inlet (Chapter 5).

Prerequisites (Sources -> HTTP API in the UI, or Flow Service API):
  - a streaming connection -> inlet URL, e.g. https://dcs.adobedc.net/collection/<CONNECTION_ID>
  - a dataflow from that connection to your dataset (gives the flow ID)

    python stream_record.py --inlet <INLET_URL> --schema <SCHEMA_$ID> --dataset <DATASET_ID> \
        --flow <FLOW_ID> --file ../xdm-schemas/sample-profile-record.json --validate

--validate adds ?syncValidation=true (development only: returns validation errors immediately).
For an authenticated connection the Platform headers are sent; for an unauthenticated one use --no-auth.

Docs: https://experienceleague.adobe.com/en/docs/experience-platform/ingestion/tutorials/streaming-record-data
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import requests

CONTENT_TYPE = "application/vnd.adobe.xed-full+json;version=1"


def build_message(schema_id: str, org_id: str, dataset_id: str, flow_id: str | None, entity: dict) -> dict:
    header = {
        "schemaRef": {"id": schema_id, "contentType": CONTENT_TYPE},
        "imsOrgId": org_id,
        "datasetId": dataset_id,
    }
    if flow_id:
        header["flowId"] = flow_id
    return {
        "header": header,
        "body": {"xdmMeta": {"schemaRef": {"id": schema_id, "contentType": CONTENT_TYPE}}, "xdmEntity": entity},
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--inlet", required=True)
    p.add_argument("--schema", required=True)
    p.add_argument("--dataset", required=True)
    p.add_argument("--flow")
    p.add_argument("--file", required=True, type=Path)
    p.add_argument("--tenant", help="tenant ID to substitute for <TENANT_ID>")
    p.add_argument("--validate", action="store_true")
    p.add_argument("--no-auth", action="store_true")
    args = p.parse_args()

    text = args.file.read_text()
    if args.tenant:
        text = text.replace("<TENANT_ID>", args.tenant)
    entity = json.loads(text)

    headers = {"Content-Type": "application/json"}
    if not args.no_auth:
        from aep_client import AEPClient

        aep = AEPClient()
        headers.update(aep.headers())
        org_id = aep.org_id
        if not args.tenant and "<TENANT_ID>" in text:
            tenant = aep.get("/data/foundation/schemaregistry/stats", headers={"Accept": "application/json"})["tenantId"]
            entity = json.loads(text.replace("<TENANT_ID>", tenant))
    else:
        org_id = os.environ["AEP_ORG_ID"]

    message = build_message(args.schema, org_id, args.dataset, args.flow, entity)
    url = args.inlet + ("?syncValidation=true" if args.validate else "")
    resp = requests.post(url, headers=headers, json=message, timeout=60)
    print(resp.status_code)
    print(resp.text)


if __name__ == "__main__":
    main()
