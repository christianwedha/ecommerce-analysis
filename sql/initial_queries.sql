-- E-COMMERCE ANALYSIS - SQL QUERIES
-- Database: ecommerce.db
-- Created: January 4, 2026
-- Author: Christian Wedha

-- ============================================================

-- QUERY 1: Total Revenue Summary
-- Purpose: Overall business metrics

SELECT
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT o.customer_id) as total_customers,
    SUM(p.total_payment_value) as total_revenue,
    AVG(p.total_payment_value) as avg_order_value,
    MIN(o.order_purchase_timestamp) as firsr_order,
    MAX(o.order_purchase_timestamp) as last_order
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id

-- ============================================================

-- QUERY 2: Top 10 States by Revenue
-- Purpose: Geographic revenue analysis

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(p.total_payment_value) as total_revenue,
    AVG(p.total_payment_value) as avg_order_value,
    ROUND(SUM(p.total_payment_value) * 100.0 /
            (SELECT SUM(total_payment_value) FROM order_payments), 2) as revenue_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC
LIMIT 10

-- ============================================================
-- QUERY 3: Delivery Performance Metrics
-- Purpose: Operational efficiency analysis

SELECT
    COUNT(*) as total_delivered_orders,
    ROUND(AVG(delivery_time_days), 1) as avg_delivery_days,
    MIN(delivery_time_days) as fastest_delivery,
    MAX(delivery_time_days) as slowest_delivery,
    ROUND(AVG(CAST(on_time_delivery AS FLOAT)) * 100) as on_time_pct,
    SUM(CASE WHEN delivery_delay_days > 0 THEN 1 ELSE 0 END) as late_deliveries,
    ROUND(SUM(CASE WHEN delivery_delay_days >0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_pct
FROM orders
WHERE delivery_time_days IS NOT NULL

-- ============================================================

