-- Data quality and identity health checks (run after every new load)

-- 1. Missing or placeholder loyalty IDs in the CRM dataset
SELECT _acmeretail.loyalty.loyaltyId AS loyalty_id, COUNT(*) AS rows
FROM acme_loyalty_members
WHERE _acmeretail.loyalty.loyaltyId IS NULL
   OR lower(_acmeretail.loyalty.loyaltyId) IN ('unknown', 'n/a', 'null', 'test', '0')
GROUP BY _acmeretail.loyalty.loyaltyId;

-- 2. The same email on many loyalty IDs (a common over-merge risk)
SELECT lower(trim(personalEmail.address)) AS email,
       COUNT(DISTINCT _acmeretail.loyalty.loyaltyId) AS loyalty_ids
FROM acme_loyalty_members
GROUP BY lower(trim(personalEmail.address))
HAVING COUNT(DISTINCT _acmeretail.loyalty.loyaltyId) > 3
ORDER BY loyalty_ids DESC
LIMIT 100;

-- 3. Devices (ECIDs) that logged in as many different people (shared devices)
SELECT identityMap['ECID'][0].id AS ecid,
       COUNT(DISTINCT identityMap['crmId'][0].id) AS people
FROM acme_web_events
WHERE identityMap['crmId'] IS NOT NULL
  AND timestamp >= date_sub(current_date, 30)
GROUP BY identityMap['ECID'][0].id
HAVING COUNT(DISTINCT identityMap['crmId'][0].id) > 1
ORDER BY people DESC
LIMIT 100;

-- 4. Duplicate event IDs
SELECT _id, COUNT(*) AS copies
FROM acme_web_events
WHERE timestamp >= date_sub(current_date, 7)
GROUP BY _id
HAVING COUNT(*) > 1
LIMIT 100;
