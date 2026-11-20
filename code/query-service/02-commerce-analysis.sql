-- Product revenue from purchase events (arrays exploded to one row per product)
SELECT p.SKU,
       p.name,
       SUM(p.quantity)   AS units,
       SUM(p.priceTotal) AS revenue
FROM acme_web_events
LATERAL VIEW explode(productListItems) AS p
WHERE eventType = 'commerce.purchases'
  AND timestamp >= date_sub(current_date, 30)
GROUP BY p.SKU, p.name
ORDER BY revenue DESC
LIMIT 50;

-- Cart-to-purchase rate per day
SELECT to_date(timestamp) AS day,
       SUM(CASE WHEN eventType = 'commerce.productListAdds' THEN 1 ELSE 0 END) AS cart_adds,
       SUM(CASE WHEN eventType = 'commerce.purchases' THEN 1 ELSE 0 END)       AS purchases
FROM acme_web_events
WHERE timestamp >= date_sub(current_date, 14)
GROUP BY to_date(timestamp)
ORDER BY day;
