#!/usr/bin/env bash
# Send one event through the Edge Network Server API (Chapter 6, section 8).
# Requires: TOKEN (see code/api), AEP_CLIENT_ID, AEP_ORG_ID, DATASTREAM_ID.
# 'interact' returns a response (e.g. personalization); use 'collect' for fire-and-forget.
# Docs: https://developer.adobe.com/data-collection-apis/docs/endpoints/interact/
set -euo pipefail

curl -s -X POST "https://server.adobedc.net/ee/v2/interact?dataStreamId=${DATASTREAM_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "x-api-key: ${AEP_CLIENT_ID}" \
  -H "x-gw-ims-org-id: ${AEP_ORG_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "xdm": {
        "eventType": "callCenter.callCompleted",
        "timestamp": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
        "identityMap": {
          "crmId": [ { "id": "CRM-778899", "authenticatedState": "authenticated", "primary": true } ]
        }
      }
    }
  }'
