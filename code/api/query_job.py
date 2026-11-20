"""
Run a SQL statement with the Query Service API and wait for it to finish (Chapter 9).

    python query_job.py "SELECT COUNT(*) FROM acme_web_events"
    python query_job.py --file ../query-service/04-derived-dataset-rfm.sql --name rfm-build

The API returns the query state, not result rows. To keep results, use CREATE TABLE AS / INSERT INTO
(Data Distiller) or connect a PostgreSQL client with Query Service credentials.

Docs: https://experienceleague.adobe.com/en/docs/experience-platform/query/home
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from aep_client import AEPClient

QUERIES = "/data/foundation/query/queries"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("sql", nargs="?", help="SQL text")
    p.add_argument("--file", type=Path, help="read SQL from a file")
    p.add_argument("--name", default="course-query")
    p.add_argument("--timeout", type=int, default=3600)
    args = p.parse_args()
    sql = args.file.read_text() if args.file else args.sql
    if not sql:
        p.error("give SQL text or --file")

    aep = AEPClient()
    query = aep.post(
        QUERIES,
        headers={"Content-Type": "application/json"},
        json={"dbName": f"{aep.sandbox}:all", "sql": sql, "name": args.name},
    )
    qid = query["id"]
    print(f"Query {qid} submitted")

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        state = aep.get(f"{QUERIES}/{qid}")
        status = state.get("state")
        print(f"  state: {status}")
        if status in {"SUCCESS", "FAILED", "KILLED"}:
            for err in state.get("errors", []) or []:
                print(f"  error: {err}")
            return
        time.sleep(15)
    print("Timed out; check Queries -> Log in the UI.")


if __name__ == "__main__":
    main()
