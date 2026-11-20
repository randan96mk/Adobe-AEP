"""
Print a quick inventory of a sandbox: tenant ID, custom schemas, datasets (with Profile flag).
Useful on day 2 of a project (Chapter 1, section 3).

Run:
    python explore_sandbox.py
"""
from aep_client import AEPClient

XED_ID = {"Accept": "application/vnd.adobe.xed-id+json"}


def main() -> None:
    aep = AEPClient()
    print(f"Sandbox: {aep.sandbox}")

    stats = aep.get("/data/foundation/schemaregistry/stats", headers={"Accept": "application/json"})
    print(f"Tenant ID: {stats.get('tenantId')}")

    schemas = aep.get("/data/foundation/schemaregistry/tenant/schemas", headers=XED_ID)
    results = schemas.get("results", [])
    print(f"\nCustom schemas ({len(results)}; first page only):")
    for s in results:
        print(f"  - {s.get('title')}  [{s.get('$id')}]")

    datasets = aep.get(
        "/data/foundation/catalog/dataSets",
        params={"limit": 100, "properties": "name,schemaRef,tags,lastBatchStatus"},
    )
    print(f"\nDatasets ({len(datasets)}; first 100):")
    for ds_id, ds in sorted(datasets.items(), key=lambda kv: kv[1].get("name", "")):
        tags = ds.get("tags", {})
        profile = "yes" if "true" in tags.get("unifiedProfile", ["enabled:false"])[0] else "no"
        schema = (ds.get("schemaRef") or {}).get("id", "-")
        print(f"  - {ds.get('name')}  id={ds_id}  profile={profile}  last_batch={ds.get('lastBatchStatus', '-')}")
        print(f"      schema: {schema}")


if __name__ == "__main__":
    main()
