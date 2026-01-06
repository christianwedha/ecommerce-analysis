-- E-COMMERCE ANALYSIS - ADVANCED SQL QUERIES
-- Database: ecommerce.db
-- Date: January 6, 2026
-- Author: Christian Wedha

-- ============================================================
-- QUERY 11: Running Total Revenue by Month
-- Purpose: Calculate cumulative revenue growth over time
-- Technique: Window function (SUM OVER with frame specification)
-- ============================================================


SELECT
    order_year,
    order_month,
    ROUND(SUM(p.total_payment_value), 2) as monthly_revenue,
    ROUND(SUM(SUM(p.total_payment_value)) OVER (
        ORDER BY order_year, order_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) as running_total_revenue
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY order_year, order_month
ORDER BY order_year, order_month


-- ============================================================
-- QUERY 12: Customer Value Segmentation
-- Purpose: Segment customers by lifetime value (High/Medium/Low)
-- Technique: Common Table Expressions (CTEs)
-- ============================================================


WITH customer_ltv AS (
    SELECT
        c.customer_unique_id,
        c.customer_state,
        COUNT(DISTINCT o.order_id) as total_orders,
        ROUND(SUM(p.total_payment_value), 2) as lifetime_value,
        ROUND(AVG(p.total_payment_value), 2) as avg_order_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_payments p ON o.order_id = p.order_id
    GROUP BY c.customer_unique_id, c.customer_state
),
ltv_segments AS(
    SELECT
        customer_unique_id,
        customer_state,
        total_orders,
        lifetime_value,
        avg_order_value,
        CASE
            WHEN lifetime_value >= 1000 THEN 'High Value'
            WHEN lifetime_value >= 500 THEN 'Medium Value'
            ELSE 'Low Value'
        END as value_segment
    FROM customer_ltv
)
SELECT
    value_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(lifetime_value), 2) as avg_ltv,
    ROUND(AVG(total_orders), 2) as avg_orders,
    ROUND(SUM(lifetime_value), 2) as total_segment_revenue
FROM ltv_segments
GROUP BY value_segment
ORDER BY avg_ltv DESC


-- ============================================================
-- QUERY 13: Monthly Customer Acquisition Cohorts
-- Purpose: Track new customer acquisition by month with cumulative total
-- Technique: CTE + window function for running sum
-- ============================================================


WITH first_purchase AS (
    SELECT
        c.customer_unique_id,
        MIN(o.order_purchase_timestamp) as first_order_date,
        strftime('%Y=%m', MIN(o.order_purchase_timestamp)) as cohort_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    cohort_month,
    COUNT(DISTINCT customer_unique_id) as customers_acquired,
    SUM(COUNT(DISTINCT customer_unique_id)) OVER (
        ORDER BY cohort_month
    ) as cumulative_customers
FROM first_purchase
GROUP BY cohort_month
ORDER BY cohort_month


-- ============================================================
-- QUERY 14: Order Basket Size Analysis
-- Purpose: Analyze distribution of items per order
-- Technique: Subquery + CASE WHEN categorization + percentage calculation
-- ============================================================


WITH order_size AS (
    SELECT
        order_id,
        COUNT(DISTINCT product_id) as items_count,
        ROUND(SUM(price), 2) as order_value
    FROM order_items
    GROUP BY order_id
)
SELECT
    CASE
        WHEN items_count = 1 THEN '1 item'
        WHEN items_count BETWEEN 2 AND 3 THEN '2-3 items'
        WHEN items_count BETWEEN 4 ANd 5 THEN '4-5 items'
        ELSE '6+ items'
    END as basket_size,
    COUNT(*) as order_count,
    ROUND(AVG(order_value), 2) as avg_order_value,
    ROUND(SUM(order_value), 2) as total_revenue,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct_of_orders
FROM order_size
GROUP BY basket_size
ORDER BY
    CASE basket_size
        WHEN '1 item' THEN 1
        WHEN'2-3 items' THEN 2
        WHEN '4-5 items' THEN 3
        ELSE 4
    END


-- ============================================================
-- QUERY 15: State Performance Rankings
-- Purpose: Rank states by revenue and delivery performance simultaneously
-- Technique: Multiple RANK() window functions
-- ============================================================


SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(p.total_payment_value), 2) as total_revenue,
    ROUND(AVG(o.delivery_time_days), 1) as avg_delivery_days,
    RANK() OVER (ORDER BY SUM(p.total_payment_value) DESC) as revenue_rank,
    RANK() OVER (ORDER BY AVG(o.delivery_time_days) ASC) as delivery_rank
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.delivery_time_days IS NOT NULL
GROUP BY c.customer_state
ORDER BY revenue_rank

