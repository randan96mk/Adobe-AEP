"""
List destination dataflows and their latest run status (Chapter 10).

    python destination_flows.py
    python destination_flows.py --runs <FLOW_ID>

Uses the Flow Service API.
Docs: https://experienceleague.adobe.com/en/docs/experience-platform/destinations/home
"""
from __future__ import annotations

import argparse
import json

from aep_client import AEPClient

FLOWS = "/data/foundation/flowservice/flows"
RUNS = "/data/foundation/flowservice/runs"


def list_destination_flows(aep: AEPClient) -> None:
    result = aep.get(FLOWS, params={"property": "inheritedAttributes.properties.isDestinationFlow==true"})
    for flow in result.get("items", []):
        last_run = (flow.get("lastRunDetails") or {}).get("state", "-")
        print(f"{flow.get('id')}  state={flow.get('state'):<9} last_run={last_run:<10} {flow.get('name')}")


def list_runs(aep: AEPClient, flow_id: str) -> None:
    result = aep.get(RUNS, params={"property": f"flowId=={flow_id}"})
    for run in result.get("items", [])[:20]:
        metrics = run.get("metrics", {})
        print(json.dumps({
            "runId": run.get("id"),
            "status": (run.get("status") or {}).get("value"),
            "started": metrics.get("durationSummary", {}).get("startedAtUTC"),
            "recordSummary": metrics.get("recordSummary"),
        }))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--runs", metavar="FLOW_ID", help="show recent runs for one destination dataflow")
    args = p.parse_args()
    aep = AEPClient()
    if args.runs:
        list_runs(aep, args.runs)
    else:
        list_destination_flows(aep)


if __name__ == "__main__":
    main()
