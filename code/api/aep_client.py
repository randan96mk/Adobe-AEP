"""
Minimal Adobe Experience Platform API client.

- Gets an access token with an OAuth Server-to-Server credential (client credentials grant).
- Adds the four headers every Platform API call needs.
- Raises a readable error when a call fails.

Usage:
    from aep_client import AEPClient
    aep = AEPClient()                      # reads settings from environment / .env
    stats = aep.get("/data/foundation/schemaregistry/stats")

Docs:
    https://experienceleague.adobe.com/en/docs/experience-platform/landing/platform-apis/api-guide
"""
from __future__ import annotations

import os
import time
from typing import Any

import requests

try:  # optional: load a local .env file if python-dotenv is installed
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

IMS_TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"
PLATFORM_URL = "https://platform.adobe.io"
DEFAULT_SCOPES = "openid,session,AdobeID,read_organizations,additional_info.projectedProductContext"


class AEPError(RuntimeError):
    """Raised when a Platform API call returns an error status."""


class AEPClient:
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        org_id: str | None = None,
        sandbox: str | None = None,
        scopes: str | None = None,
        timeout: int = 60,
        max_retries: int = 4,
    ) -> None:
        self.max_retries = max_retries
        self.client_id = client_id or _require("AEP_CLIENT_ID")
        self.client_secret = client_secret or _require("AEP_CLIENT_SECRET")
        self.org_id = org_id or _require("AEP_ORG_ID")
        self.sandbox = sandbox or os.getenv("AEP_SANDBOX", "prod")
        self.scopes = scopes or os.getenv("AEP_SCOPES", DEFAULT_SCOPES)
        self.timeout = timeout
        self._token: str | None = None
        self._token_expires_at = 0.0
        self.session = requests.Session()

    # ---------- authentication ----------
    def token(self) -> str:
        """Return a cached access token, requesting a new one shortly before expiry."""
        if self._token and time.time() < self._token_expires_at - 300:
            return self._token
        resp = self.session.post(
            IMS_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": self.scopes,
            },
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise AEPError(f"Token request failed ({resp.status_code}): {resp.text}")
        body = resp.json()
        self._token = body["access_token"]
        self._token_expires_at = time.time() + int(body.get("expires_in", 86400))
        return self._token

    def headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        h = {
            "Authorization": f"Bearer {self.token()}",
            "x-api-key": self.client_id,
            "x-gw-ims-org-id": self.org_id,
            "x-sandbox-name": self.sandbox,
        }
        if extra:
            h.update(extra)
        return h

    # ---------- HTTP helpers ----------
    def request(self, method: str, path: str, *, headers: dict[str, str] | None = None, **kwargs: Any) -> Any:
        url = path if path.startswith("http") else f"{PLATFORM_URL}{path}"
        # Retry rate limits (429) and transient server errors with exponential back-off.
        # Only idempotent methods are retried on 5xx, so a POST is never sent twice by accident.
        for attempt in range(self.max_retries + 1):
            resp = self.session.request(method, url, headers=self.headers(headers), timeout=self.timeout, **kwargs)
            retryable = resp.status_code == 429 or (resp.status_code >= 500 and method in ("GET", "PUT", "DELETE"))
            if not retryable or attempt == self.max_retries:
                break
            try:
                wait = float(resp.headers.get("Retry-After", 2 ** attempt))
            except ValueError:  # Retry-After given as an HTTP date
                wait = 2 ** attempt
            time.sleep(min(wait, 60))
        if resp.status_code >= 400:
            raise AEPError(f"{method} {url} -> {resp.status_code}: {resp.text[:2000]}")
        if not resp.content:
            return None
        ctype = resp.headers.get("Content-Type", "")
        return resp.json() if "json" in ctype else resp.text

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Any:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing environment variable {name}. Copy .env.example to .env and fill it in.")
    return value
