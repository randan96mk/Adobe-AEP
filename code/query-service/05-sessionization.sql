-- Sessions with an Adobe-defined function (30-minute inactivity timeout)
SELECT ecid,
       timestamp,
       page,
       SESS_TIMEOUT(timestamp, 60 * 30)
         OVER (PARTITION BY ecid ORDER BY timestamp
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session
FROM (
  SELECT identityMap['ECID'][0].id   AS ecid,
         timestamp,
         web.webPageDetails.name     AS page
  FROM acme_web_events
  WHERE timestamp >= date_sub(current_date, 1)
)
LIMIT 200;
