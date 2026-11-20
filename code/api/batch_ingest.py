"""
Batch-ingest a JSON file into a dataset (Chapter 5).

    python batch_ingest.py --dataset <DATASET_ID> --file ../xdm-schemas/sample-profile-record.json

Steps: create batch -> upload file -> complete batch -> poll status.
The file must contain XDM records that match the dataset's schema
(one JSON object, a JSON array, or JSON Lines). Replace <TENANT_ID> placeholders first,
or pass --tenant to have this script do it.

Docs: https://experienceleague.adobe.com/en/docs/experience-platform/ingestion/batch/api-overview
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from aep_client import AEPClient

IMPORT = "/data/foundation/import"
CATALOG = "/data/foundation/catalog"


def prepare_file(path: Path, tenant: str | None) -> bytes:
    text = path.read_text()
    if tenant:
        text = text.replace("<TENANT_ID>", tenant)
    data = json.loads(text) if text.lstrip().startswith(("{", "[")) else None
    if isinstance(data, dict):  # single object -> array (multi-line JSON)
        text = json.dumps([data])
    return text.encode("utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True, help="dataset ID")
    p.add_argument("--file", required=True, type=Path)
    p.add_argument("--tenant", help="tenant ID to substitute for <TENANT_ID> (default: read from API)")
    p.add_argument("--timeout", type=int, default=900, help="seconds to wait for processing")
    args = p.parse_args()

    aep = AEPClient()
    tenant = args.tenant or aep.get(
        "/data/foundation/schemaregistry/stats", headers={"Accept": "application/json"}
    )["tenantId"]
    payload = prepare_file(args.file, tenant)

    # 1. create batch
    batch = aep.post(
        f"{IMPORT}/batches",
        headers={"Content-Type": "application/json"},
        json={"datasetId": args.dataset, "inputFormat": {"format": "json", "isMultiLineJson": True}},
    )
    batch_id = batch["id"]
    print(f"Batch created: {batch_id}")

    # 2. upload file
    aep.put(
        f"{IMPORT}/batches/{batch_id}/datasets/{args.dataset}/files/{args.file.name}",
        headers={"Content-Type": "application/octet-stream"},
        data=payload,
    )
    print(f"Uploaded {args.file.name} ({len(payload)} bytes)")

    # 3. complete batch (processing starts only now)
    aep.post(f"{IMPORT}/batches/{batch_id}", params={"action": "COMPLETE"})
    print("Batch marked complete; waiting for processing...")

    # 4. poll status
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        info = aep.get(f"{CATALOG}/batches/{batch_id}").get(batch_id, {})
        status = info.get("status")
        print(f"  status: {status}")
        if status in {"success", "failed", "failure", "aborted", "abandoned"}:
            metrics = info.get("metrics", {})
            print(f"Records read: {metrics.get('inputRecordCount')}, written: {metrics.get('outputRecordCount')}")
            for err in info.get("errors", []):
                print(f"  error {err.get('code')}: {err.get('description')}")
            return
        time.sleep(30)
    print("Timed out waiting; check the dataset's batch list in the UI.")


if __name__ == "__main__":
    main()
