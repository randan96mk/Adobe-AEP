"""
Submit and track a Privacy Service request (Chapter 14).

    python privacy_request.py access --email asha.rao@example.com --crm CRM-778899
    python privacy_request.py delete --email asha.rao@example.com --regulation gdpr
    python privacy_request.py status <JOB_ID>

Use a test identity first. Delete requests are irreversible.
Docs: https://experienceleague.adobe.com/en/docs/experience-platform/privacy/api/getting-started
"""
from __future__ import annotations

import argparse
import json

from aep_client import AEPClient

JOBS = "/data/core/privacy/jobs"


def submit(aep: AEPClient, action: str, email: str | None, crm: str | None, regulation: str) -> None:
    user_ids = []
    if email:
        user_ids.append({"namespace": "email", "value": email, "type": "standard"})
    if crm:
        user_ids.append({"namespace": "crmId", "value": crm, "type": "custom"})
    if not user_ids:
        raise SystemExit("Give at least one identity (--email and/or --crm). Send all known identities.")
    body = {
        "companyContexts": [{"namespace": "imsOrgID", "value": aep.org_id}],
        "users": [{"key": f"{action}-request", "action": [action], "userIDs": user_ids}],
        "include": ["aepDataLake", "profileService", "identity"],
        "expandIds": False,
        "priority": "normal",
        "regulation": regulation,
    }
    result = aep.post(JOBS, headers={"Content-Type": "application/json"}, json=body)
    print(json.dumps(result, indent=2))


def status(aep: AEPClient, job_id: str) -> None:
    print(json.dumps(aep.get(f"{JOBS}/{job_id}"), indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for action in ("access", "delete"):
        s = sub.add_parser(action)
        s.add_argument("--email")
        s.add_argument("--crm")
        s.add_argument("--regulation", default="gdpr", help="e.g. gdpr, ccpa (see docs for the full list)")
    sub.add_parser("status").add_argument("job_id")
    args = p.parse_args()

    aep = AEPClient()
    if args.cmd == "status":
        status(aep, args.job_id)
    else:
        if args.cmd == "delete":
            confirm = input("Delete requests cannot be undone. Type DELETE to continue: ")
            if confirm != "DELETE":
                raise SystemExit("Cancelled.")
        submit(aep, args.cmd, args.email, args.crm, args.regulation)


if __name__ == "__main__":
    main()
