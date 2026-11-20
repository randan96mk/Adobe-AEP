"""
Identity helpers (Chapter 4).

    python identity_tools.py list
    python identity_tools.py create --name "CRM ID" --code crmId --type CROSS_DEVICE
    python identity_tools.py hash-email " Asha.Rao@Example.com "
    python identity_tools.py hash-phone "+44 1234 567890"

Hashing follows the common destination convention: normalize first, then SHA-256 (hex, lower case).
Check each destination's own documentation for its exact normalization rules.
"""
from __future__ import annotations

import argparse
import hashlib
import re

NAMESPACES = "/data/core/idnamespace/identities"
ID_TYPES = ["COOKIE", "CROSS_DEVICE", "DEVICE", "EMAIL", "MOBILE", "NON_PEOPLE", "PHONE"]


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_phone(phone: str) -> str:
    """Keep a leading + and digits only (E.164-style)."""
    phone = phone.strip()
    digits = re.sub(r"\D", "", phone)
    return f"+{digits}" if phone.startswith("+") else digits


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def list_namespaces() -> None:
    from aep_client import AEPClient

    aep = AEPClient()
    for ns in sorted(aep.get(NAMESPACES), key=lambda n: (not n.get("custom", False), n.get("code", ""))):
        kind = "custom" if ns.get("custom") else "standard"
        print(f"{ns.get('code'):<28} {ns.get('idType', ''):<14} {kind:<9} {ns.get('name')}")


def create_namespace(name: str, code: str, id_type: str, description: str) -> None:
    from aep_client import AEPClient

    aep = AEPClient()
    created = aep.post(
        NAMESPACES,
        headers={"Content-Type": "application/json"},
        json={"name": name, "code": code, "idType": id_type, "description": description},
    )
    print(f"Created namespace: {created.get('code')} (id {created.get('id')})")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    c = sub.add_parser("create")
    c.add_argument("--name", required=True)
    c.add_argument("--code", required=True)
    c.add_argument("--type", default="CROSS_DEVICE", choices=ID_TYPES)
    c.add_argument("--description", default="")
    sub.add_parser("hash-email").add_argument("value")
    sub.add_parser("hash-phone").add_argument("value")
    args = p.parse_args()

    if args.cmd == "list":
        list_namespaces()
    elif args.cmd == "create":
        create_namespace(args.name, args.code, args.type, args.description)
    elif args.cmd == "hash-email":
        norm = normalize_email(args.value)
        print(f"normalized: {norm}\nsha256:     {sha256_hex(norm)}")
    elif args.cmd == "hash-phone":
        norm = normalize_phone(args.value)
        print(f"normalized: {norm}\nsha256:     {sha256_hex(norm)}")


if __name__ == "__main__":
    main()
