"""
Look up profiles, their events and merge policies (Chapter 7).

    python profile_lookup.py --ns Email --id asha.rao@example.com
    python profile_lookup.py --ns loyaltyId --id L-100234 --events
    python profile_lookup.py --merge-policies

For testing and support only; not a high-volume real-time API.
Docs: https://developer.adobe.com/experience-platform-apis/references/profile
"""
from __future__ import annotations

import argparse
import json

from aep_client import AEPClient

UPS = "/data/core/ups"


def lookup_profile(aep: AEPClient, ns: str, value: str, merge_policy: str | None) -> dict:
    params = {"schema.name": "_xdm.context.profile", "entityId": value, "entityIdNS": ns}
    if merge_policy:
        params["mergePolicyId"] = merge_policy
    return aep.get(f"{UPS}/access/entities", params=params)


def lookup_events(aep: AEPClient, ns: str, value: str, limit: int) -> dict:
    params = {
        "schema.name": "_xdm.context.experienceevent",
        "relatedSchema.name": "_xdm.context.profile",
        "relatedEntityId": value,
        "relatedEntityIdNS": ns,
        "orderby": "-timestamp",
        "limit": limit,
    }
    return aep.get(f"{UPS}/access/entities", params=params)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ns", help="identity namespace code, e.g. Email, ECID, loyaltyId")
    p.add_argument("--id", help="identity value")
    p.add_argument("--events", action="store_true", help="return recent events instead of attributes")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--merge-policy", help="merge policy ID (default: sandbox default)")
    p.add_argument("--merge-policies", action="store_true", help="list merge policies")
    args = p.parse_args()

    aep = AEPClient()
    if args.merge_policies:
        result = aep.get(f"{UPS}/config/mergePolicies")
        for mp in result.get("children", []):
            print(
                f"{mp.get('id')}  default={mp.get('default')}  edge={mp.get('activeOnEdge')}  "
                f"stitching={mp.get('identityGraph', {}).get('type')}  "
                f"merge={mp.get('attributeMerge', {}).get('type')}  name={mp.get('name')}"
            )
        return
    if not (args.ns and args.id):
        p.error("--ns and --id are required unless --merge-policies is used")

    if args.events:
        result = lookup_events(aep, args.ns, args.id, args.limit)
    else:
        result = lookup_profile(aep, args.ns, args.id, args.merge_policy)
    print(json.dumps(result, indent=2)[:20000])


if __name__ == "__main__":
    main()
