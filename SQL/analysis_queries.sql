-- ============================================================
-- RetailPulse | Phase 5: SQL Analysis
-- Author: Your Name
-- Date: May 2026
-- ============================================================

USE retailpulse;

-- ── Query 1: Total Revenue KPIs ─────────────────────────────
-- Business question: What is our overall revenue performance?
SELECT 
    ROUND(SUM(payment_value), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(payment_value), 2) AS avg_order_value
FROM payments;



-- ── Query 2: Monthly Revenue Trend ──────────────────────────
-- Business question: Is revenue growing month over month?
SELECT 
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    ROUND(SUM(p.payment_value), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;



-- ── Query 3: Top 10 Customers by Lifetime Value ─────────────
-- Business question: Who are our most valuable customers?
SELECT 
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS lifetime_value,
    ROUND(AVG(p.payment_value), 2) AS avg_order_value,
    MIN(DATE(o.order_purchase_timestamp)) AS first_order,
    MAX(DATE(o.order_purchase_timestamp)) AS last_order
FROM customers c
JOIN orders o   ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id
ORDER BY lifetime_value DESC
LIMIT 10;



-- ── Query 4: Repeat Purchase Rate ───────────────────────────
-- Business question: How loyal are our customers?
SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) 
        / COUNT(DISTINCT customer_unique_id) * 100, 2) AS repeat_rate_pct
FROM (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) AS customer_orders;



-- ── Query 5: Delivery Performance by State ──────────────────
-- Business question: Which states have the worst delivery times?
SELECT 
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(AVG(o.delivery_days), 1) AS avg_delivery_days,
    ROUND(AVG(o.delivery_delay_days), 1) AS avg_delay_days
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered'
    AND o.delivery_days IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days DESC
LIMIT 10;