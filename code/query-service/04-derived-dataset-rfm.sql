-- Data Distiller: RFM (recency, frequency, monetary) per loyalty member from purchase events.
-- First run creates the table; schedule the SELECT with an output dataset for daily refresh.
-- For a Profile-enabled result, create the table on an XDM schema with an identity
-- (see "Create derived datasets with SQL" in Chapter 9).

CREATE TABLE IF NOT EXISTS acme_customer_rfm AS
SELECT loyalty_id,
       datediff(current_date, to_date(MAX(ts))) AS recency_days,
       COUNT(*)                                  AS frequency_12m,
       ROUND(SUM(order_total), 2)                AS monetary_12m
FROM (
  SELECT identityMap['loyaltyId'][0].id AS loyalty_id,
         timestamp                        AS ts,
         commerce.order.priceTotal        AS order_total
  FROM acme_pos_transactions
  WHERE eventType = 'commerce.purchases'
    AND timestamp >= add_months(current_date, -12)
) t
WHERE loyalty_id IS NOT NULL
GROUP BY loyalty_id;
