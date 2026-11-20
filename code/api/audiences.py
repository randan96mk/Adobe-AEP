"""
Work with audiences (segment definitions) by API (Chapter 8).

    python audiences.py list
    python audiences.py create ../segmentation/gold-members-uk.json --tenant acmeretail
    python audiences.py evaluate <SEGMENT_ID>
    python audiences.py job <JOB_ID>

Docs:
  https://experienceleague.adobe.com/en/docs/experience-platform/segmentation/api/segment-definitions
  https://experienceleague.adobe.com/en/docs/experience-platform/segmentation/api/segment-jobs
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from aep_client import AEPClient

SEG = "/data/core/ups/segment"


def list_definitions(aep: AEPClient) -> None:
    result = aep.get(f"{SEG}/definitions", params={"limit": 100})
    for d in result.get("segments", []):
        ev = d.get("evaluationInfo", {})
        method = (
            "edge" if ev.get("synchronous", {}).get("enabled")
            else "streaming" if ev.get("continuous", {}).get("enabled")
            else "batch"
        )
        print(f"{d.get('id')}  {method:<9}  {d.get('name')}")


def create_definition(aep: AEPClient, path: Path, tenant: str | None) -> None:
    text = path.read_text()
    if tenant:
        text = text.replace("<TENANT_ID>", tenant)
    body = json.loads(text)
    created = aep.post(f"{SEG}/definitions", headers={"Content-Type": "application/json"}, json=body)
    print(f"Created: {created.get('id')}  {created.get('name')}")


def evaluate(aep: AEPClient, segment_id: str) -> None:
    job = aep.post(f"{SEG}/jobs", headers={"Content-Type": "application/json"}, json=[{"segmentId": segment_id}])
    print(f"Segment job: {job.get('id')}  status={job.get('status')}")


def job_status(aep: AEPClient, job_id: str) -> None:
    job = aep.get(f"{SEG}/jobs/{job_id}")
    print(json.dumps({k: job.get(k) for k in ("id", "status", "metrics", "errors")}, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    c = sub.add_parser("create")
    c.add_argument("file", type=Path)
    c.add_argument("--tenant", help="replaces <TENANT_ID> in the file")
    sub.add_parser("evaluate").add_argument("segment_id")
    sub.add_parser("job").add_argument("job_id")
    args = p.parse_args()

    aep = AEPClient()
    if args.cmd == "list":
        list_definitions(aep)
    elif args.cmd == "create":
        create_definition(aep, args.file, args.tenant)
    elif args.cmd == "evaluate":
        evaluate(aep, args.segment_id)
    elif args.cmd == "job":
        job_status(aep, args.job_id)


if __name__ == "__main__":
    main()
