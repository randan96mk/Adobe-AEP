-- Chapter 9 / Chapter 1 day-2 exploration. Replace table names with your dataset table names.

-- All tables (datasets) in the sandbox
SHOW TABLES;

-- Peek at a dataset
SELECT * FROM acme_web_events LIMIT 10;

-- Rows per day for the last 14 days (freshness and volume check)
SELECT to_date(timestamp) AS day, COUNT(*) AS events
FROM acme_web_events
WHERE timestamp >= date_sub(current_date, 14)
GROUP BY to_date(timestamp)
ORDER BY day;

-- Event types in the last 7 days
SELECT eventType, COUNT(*) AS events
FROM acme_web_events
WHERE timestamp >= date_sub(current_date, 7)
GROUP BY eventType
ORDER BY events DESC;
