-- E-COMMERCE ANALYSIS SQL QUERIES
-- Database: ecommerce.db
-- Date: January 5, 2026

-- QUERY 1: Monthly Revenue Trend

SELECT 
    order_year,
    order_month,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    ROUND(SUM(p.total_payment_value), 2) as total_revenue,
    ROUND(AVG(p.total_payment_value), 2) as avg_order_value
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY order_year, order_month
ORDER BY order_year, order_month


-- QUERY 2: Top 10 Product Categories

SELECT 
    pr.product_category_name_english as category,
    COUNT(DISTINCT oi.order_id) as total_orders,
    COUNT(oi.product_id) as items_sold,
    ROUND(SUM(oi.price), 2) as total_revenue,
    ROUND(AVG(oi.price), 2) as avg_item_price
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10


-- QUERY 3: Revenue by State

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT c.customer_unique_id) as unique_customers,
    ROUND(SUM(p.total_payment_value), 2) as total_revenue,
    ROUND(AVG(p.total_payment_value), 2) as avg_order_value,
    ROUND(SUM(p.total_payment_value) / COUNT(DISTINCT c.customer_unique_id), 2) as revenue_per_customer
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC
LIMIT 10


-- QUERY 4: Delivery Performance by State

SELECT
    c.customer_state,
    COUNT(o.order_id) as total_orders,
    ROUND(AVG(o.delivery_time_days), 1) as avg_delivery_days,
    ROUND(AVG(o.delivery_delay_days), 1) as acg_delay_days,
    ROUND(AVG(CAST(o.on_time_delivery AS FLOAT)) *100, 1) as on_time_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.delivery_time_days IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days DESC
LIMIT 15


-- QUERY 5: Late Delivery Hotspots

SELECT
    c.customer_state,
    COUNT(o.order_id) as total_orders,
    SUM(CASE WHEN o.delivery_delay_days > 0 THEN 1 ELSE 0 END) as late_deliveries,
    ROUND(
        CAST(SUM(CASE WHEN o.delivery_delay_days > 0 THEN 1 ELSE 0 END) AS FLOAT) /
        COUNT(o.order_id) * 100,
        1
    ) as late_pct,
    ROUND(AVG(CASE WHEN o.delivery_delay_days > 0 THEN o.delivery_delay_days END), 1) as avg_days_late
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.delivery_delay_days IS NOT NULL
GROUP BY c.customer_state
HAVING late_pct > 20
ORDER BY late_pct DESC


-- QUERY 6: Freight Cost Analysis

SELECT
    pr.product_category_name_english as category,
    COUNT(oi.order_id)as total_orders,
    ROUND(AVG(oi.price), 2) as avg_product_price,
    ROUND(AVG(oi.freight_value), 2) as avg_freight,
    ROUND(AVG(oi.freight_pct_of_price), 1) as avg_freight_pct
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name_english
HAVING COUNT(oi.order_id) > 50
ORDER BY avg_freight_pct DESC
LIMIT 10

-- QUERY 7: Customer Segmentation

SELECT
    CASE
        WHEN order_count = 1 THEN 'One-time'
        WHEN order_count BETWEEN 2 AND 3 THEN 'Repeat'
        ELSE 'Loyal'
    END as customer_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(lifetime_value), 2) as avg_lifetime_value,
    ROUND(SUM(lifetime_value), 2) as total_segment_revenue
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(p.total_payment_value) as lifetime_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_payments p ON o.order_id = p.order_id
    GROUP BY c.customer_unique_id
) customer_stats
GROUP BY customer_segment
ORDER BY avg_lifetime_value DESC


-- QUERY 8: Top 20 Customers

SELECT 
    c.customer_unique_id,
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(p.total_payment_value), 2) as lifetime_value,
    ROUND(AVG(p.total_payment_value), 2) as avg_order_value,
    MIN(o.order_purchase_timestamp) as first_order,
    MAX(o.order_purchase_timestamp) as last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_unique_id, c.customer_state
ORDER BY lifetime_value DESC
LIMIT 20


-- QUERY 9: Order Patterns by Day

SELECT 
    order_day_of_week,
    CASE order_day_of_week
        WHEN 0 THEN 'Monday'
        WHEN 1 THEN 'Tuesday'
        WHEN 2 THEN 'Wednesday'
        WHEN 3 THEN 'Thursday'
        WHEN 4 THEN 'Friday'
        WHEN 5 THEN 'Saturday'
        WHEN 6 THEN 'Sunday'
    END as day_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(p.total_payment_value), 2) as total_revenue,
    ROUND(AVG(p.total_payment_value), 2) as avg_order_value
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY order_day_of_week
ORDER BY order_day_of_week


-- QUERY 10: Payment Methods

SELECT 
    payment_methods,
    COUNT(order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(max_installments), 1) as avg_installments
FROM order_payments
GROUP BY payment_methods
ORDER BY total_orders DESC
LIMIT 10

