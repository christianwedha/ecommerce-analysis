# E-Commerce Sales Analysis Dashboard

## Project Overview

End-to-end data analytics project analyzing 100,000+ Brazilian e-commerce orders to identify revenue drivers, operational bottlenecks, and customer retention opportunities.

**Business Impact:**
- Identified 3 states with 60% of late deliveries (average 5+ days delayed)
- Found top 10 product categories generating 70%+ of total revenue
- Discovered 97% one-time purchase rate - massive retention opportunity

---

## Tech Stack

**Languages & Database:**
- Python 3.11+
- SQL (SQLite)

**Data Analysis:**
- pandas - data manipulation and cleaning
- numpy - numerical computations
- matplotlib, seaborn - data visualization

**Database & Queries:**
- SQLite - normalized database (5 tables)
- 15 SQL queries (JOINs, CTEs, window functions)

**Tools:**
- Jupyter Notebook - exploratory analysis
- VS Code - development environment
- DBeaver - database management
- Git - version control

**Dashboards (Coming Week 2-3):**
- Streamlit - interactive web dashboard
- Tableau Public - executive dashboard

---

## Dataset

**Source:** [Olist Brazilian E-Commerce (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Size:**
- 100,000+ orders
- 9 CSV files
- Real company data from 2016-2018

**Tables:**
- orders (96,000+ delivered orders)
- customers (99,000+ customer records)
- products (33,000+ products)
- order_items (113,000+ line items)
- order_payments (99,000+ payment records)

---

## Project Structure
```
ecommerce-analysis/
├── data/
│   ├── raw/                    # Original 9 CSV files
│   └── processed/              # Cleaned data + SQLite database
│       ├── orders_clean.csv
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       ├── order_items_clean.csv
│       ├── order_payments_clean.csv
│       ├── master_dataset.csv
│       └── ecommerce.db        # SQLite database
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_merge_tables.ipynb
│   ├── 04_sql_queries.ipynb
│   └── 05_advanced_sql.ipynb
├── sql/
│   ├── initial_queries.sql     # First 3 test queries
│   ├── business_queries.sql    # 10 business analysis queries
│   └── advanced_queries.sql    # 5 advanced SQL queries
├── outputs/
│   └── charts/                 # Saved visualizations
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Key Findings

### 1. Revenue Analysis

**Monthly Revenue Trends:**
- Peak month: November 2017 (R$ 1,153,528)
- Clear Q4 seasonal pattern (30-40% higher than other quarters)
- Average monthly revenue: ~R$ 800,000

**Revenue by State:**
- São Paulo dominates: 42% of total revenue
- Top 3 states (SP, RJ, MG): 65% of revenue
- Bahia has highest AOV (R$ 181) despite lower volume

**Product Categories:**
- Top 10 categories: 62.4% of revenue (healthy diversification)
- Health & Beauty: Highest volume (8,836 orders)
- Watches & Gifts: Highest AOV (R$ 201)

### 2. Operational Challenges

**Delivery Performance:**
- Average delivery time: 12 days
- On-time delivery rate: 93%
- Northern states: 20-30 day delivery (infrastructure challenge)
- Only Alagoas (AL) below 80% on-time threshold

**Freight Costs:**
- 6 categories have freight >40% of product price
- DVDs/Blu-ray: 83% freight cost (severe problem)
- Electronics: 68% freight cost (high volume affected)

### 3. Customer Retention CRISIS

**Critical Finding:**
- 96.9% of customers make only ONE purchase
- Only 47 customers (0.05%) are "loyal" (4+ orders)
- One-time customers generate 95% of revenue

**Customer Value:**
- Loyal customers: R$ 789 average LTV (4.9x one-time)
- High-value segment: 0.27% of customers, 0.2% of revenue
- Moving 10% to repeat buyers: +R$ 1.26M annual revenue potential

### 4. Behavioral Insights

**Shopping Patterns:**
- Weekday preference (Monday-Wednesday peak)
- 70%+ single-item orders (cross-sell opportunity)
- Credit card: 76.5% of orders, 3.5 installments average

---

## SQL Skills Demonstrated

### Basic to Intermediate:
- Complex JOINs (3-4 table joins)
- Aggregations (SUM, COUNT, AVG, MIN, MAX)
- GROUP BY with multiple columns
- HAVING clause for post-aggregation filtering
- CASE statements for categorization
- Subqueries

### Advanced:
- **Window Functions:**
  - `SUM() OVER()` for running totals
  - `RANK()`, `DENSE_RANK()` for rankings
  - `PARTITION BY` for group-wise calculations
  
- **Common Table Expressions (CTEs):**
  - Multi-step query logic
  - Nested CTEs
  - Improves readability and maintainability

- **Date Manipulation:**
  - `strftime()` for date formatting
  - Cohort analysis using MIN() with GROUP BY

- **Percentage Calculations:**
  - Window functions for percentage of total
  - Month-over-month growth rates

---

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

**1. Clone repository:**
```bash
git clone https://github.com/[yourusername]/ecommerce-analysis.git
cd ecommerce-analysis
```

**2. Create virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Download dataset:**
- Go to [Kaggle dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Download `brazilian-ecommerce.zip`
- Extract all CSV files to `data/raw/` folder

**5. Run notebooks:**
```bash
# Open Jupyter
jupyter notebook

# Or use VS Code with Jupyter extension
code .
```

---

## Running SQL Queries

### Option 1: DBeaver (GUI)

1. Download [DBeaver Community Edition](https://dbeaver.io/download/)
2. Open DBeaver → New Connection → SQLite
3. Browse to `data/processed/ecommerce.db`
4. Open SQL Editor
5. Copy queries from `sql/` folder

### Option 2: Python (Jupyter)
```python
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('data/processed/ecommerce.db')

# Run query
query = """
SELECT 
    c.customer_state,
    COUNT(*) as total_orders,
    SUM(p.total_payment_value) as revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC
LIMIT 10
"""

result = pd.read_sql_query(query, conn)
print(result)
```

---

## Business Recommendations

### 1. IMMEDIATE ACTIONS (Week 1-4)

**Fix Alagoas (AL) Delivery Crisis:**
- 21.4% late delivery rate (only state >20%)
- Partner with regional carrier or open fulfillment point
- Potential revenue at risk: R$ 13,600/month

**Optimize Freight Costs:**
- DVDs/Blu-ray: Raise price 30%, absorb freight, market as "free shipping"
- Electronics: Bundle strategy ("Buy 2+, free shipping")
- Renegotiate carrier rates for high-volume categories

### 2. SHORT-TERM (Month 1-3)

**Launch Retention Program:**
- Post-purchase email sequence (Day 7, 14, 30)
- 20% discount on second purchase within 60 days
- Target: Move 10% from one-time to repeat (R$ 1.26M annual impact)

**Implement Cross-Sell Strategy:**
- Bundle recommendations at checkout
- "Customers also bought..." feature
- Free shipping threshold at 3+ items
- Target: Increase AOV by 15-20%

### 3. MEDIUM-TERM (Quarter 1-2)

**Geographic Expansion:**
- Double down on Bahia (high AOV, underpenetrated)
- Fix São Paulo profitability (reduce discounting)
- Consider Northern warehouse (Manaus/Belém)

**Category Management:**
- Focus inventory on top 10 categories (62% revenue)
- Improve furniture/decor mix (high volume, low AOV)
- Premium line for watches/gifts (already R$ 201 AOV)

---

## Next Steps (Week 2-4)

### Week 2: Streamlit Dashboard
- Interactive web app with filters
- 4 pages: Executive Summary, Products, Delivery, Customers
- Deploy to Streamlit Cloud

### Week 3: Tableau Public Dashboard
- Professional drag-and-drop visualization
- Executive-level presentation
- Published to Tableau Public

### Week 4: Executive Summary Report
- 2-3 page PDF document
- Business case with ROI calculations
- Implementation roadmap

---

## Author

Christian Wedha

Transitioning to data analytics with hands-on portfolio projects.

**Connect:**
- GitHub: christianwedha
- Email: christianwedha@gmail.com

---

## License

Dataset: CC BY-NC-SA 4.0 (Olist)  
Project Code: MIT License

---

## Acknowledgments

- Dataset provided by Olist via Kaggle
- Inspired by real-world e-commerce analytics challenges