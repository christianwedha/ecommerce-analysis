# DAY 2 CLEANING - SIMPLIFIED AND BULLETPROOF
import pandas as pd
import numpy as np
import os

print("="*70)
print("DAY 2: DATA CLEANING")
print("="*70)

# Load data
print("\n📦 Loading data...")
customers = pd.read_csv('data/raw/olist_customers_dataset.csv')
orders = pd.read_csv('data/raw/olist_orders_dataset.csv')
print(f"Customers: {customers.shape}")
print(f"Orders: {orders.shape}")

# Convert datetime
print("\nConverting datetime columns...")
datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date',
                 'order_estimated_delivery_date']

for col in datetime_cols:
    orders[col] = pd.to_datetime(orders[col], errors='coerce')
print("Done")

# Create derived columns
print("\nCreating derived columns...")
orders['delivery_time_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
orders['delivery_delay_days'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days
orders['on_time_delivery'] = (orders['delivery_delay_days'] <= 0).astype(int)
orders['order_year'] = orders['order_purchase_timestamp'].dt.year
orders['order_month'] = orders['order_purchase_timestamp'].dt.month
orders['order_day_of_week'] = orders['order_purchase_timestamp'].dt.dayofweek
orders['order_hour'] = orders['order_purchase_timestamp'].dt.hour
print("Created 7 columns")

# Filter delivered orders
print("\nFiltering delivered orders...")
orders_delivered = orders[orders['order_status'] == 'delivered'].copy()
print(f"Kept: {len(orders_delivered):,} delivered orders")

# Stats
print("\nDELIVERY STATS:")
delivered_with_data = orders_delivered[orders_delivered['delivery_time_days'].notna()]
print(f"Average delivery: {delivered_with_data['delivery_time_days'].mean():.1f} days")
print(f"On-time rate: {delivered_with_data['on_time_delivery'].mean()*100:.1f}%")

# Customer stats
print("\nCUSTOMER STATS:")
print(f"Total customers: {customers['customer_unique_id'].nunique():,}")
print(f"States: {customers['customer_state'].nunique()}")
print(f"Top state: {customers['customer_state'].value_counts().index[0]}")

# Merge and analyze
print("\nAnalyzing by state...")
merged = orders_delivered.merge(customers, on='customer_id')
state_analysis = merged.groupby('customer_state').agg({
    'order_id': 'count',
    'delivery_delay_days': 'mean',
    'on_time_delivery': 'mean'
}).round(2)

state_analysis.columns = ['orders', 'avg_delay', 'on_time_rate']
state_analysis['late_rate'] = (1 - state_analysis['on_time_rate']) * 100
state_analysis = state_analysis.sort_values('late_rate', ascending=False)

print("\nTop 5 worst states for late delivery:")
print(state_analysis.head(5))

worst = state_analysis[state_analysis['late_rate'] > 20].head(3)
print(f"\nKEY INSIGHT: {len(worst)} states have >20% late delivery!")
for state, row in worst.iterrows():
    print(f"   {state}: {row['late_rate']:.1f}% late ({row['orders']:.0f} orders)")

# Save
print("\nSaving files...")
os.makedirs('data/processed', exist_ok=True)
orders_delivered.to_csv('data/processed/orders_clean.csv', index=False)
customers.to_csv('data/processed/customers_clean.csv', index=False)
print(f"Saved to data/processed/")