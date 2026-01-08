import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="E-commerce Analytics",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    monthly = pd.read_csv('../dashboard/data/monthly_revenue.csv')
    states = pd.read_csv('../dashboard/data/state_revenue.csv')
    categories = pd.read_csv('../dashboard/data/category_performance.csv')
    delivery = pd.read_csv('../dashboard/data/delivery_performance.csv')
    segments = pd.read_csv('../dashboard/data/customer_segments.csv')
    days = pd.read_csv('../dashboard/data/day_patterns.csv')
    payments = pd.read_csv('../dashboard/data/payment_methods.csv')

    return monthly, states, categories, delivery, segments, days, payments

monthly_df, states_df, categories_df, delivery_df, segments_df, days_df, payments_df = load_data()

# Title
st.title("E-commerce Sales Analysis Dashboard")
st.markdown("---")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select Page",
    ["Executive Summary", "Products", "Delivery", "Customers"]
)

#Page routing
if page == "Executive Summary":
    st.header("Executive Summary")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = monthly_df['total_revenue'].sum()
    total_orders = monthly_df['total_orders'].sum()
    avg_order_value = total_revenue / total_orders
    on_time_rate = delivery_df['on_time_pct'].mean()

    col1.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Avg Order Value", f"R$ {avg_order_value:,.2f}")
    col4.metric("On-Time Rate", f"{on_time_rate:.1f}")

    st.markdown("---")

    # Monthly revenue trend
    st.subheader("Monthly Revenue Trend")

    monthly_df['date'] = pd.to_datetime(
        monthly_df['order_year'].astype(str) + '-' +
        monthly_df['order_month'].astype(str).str.zfill(2)
    )

    fig = px.line(
        monthly_df,
        x='date',
        y='total_revenue',
        title='Monthly Revenue Over Time'
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (R$)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Products":
    st.header("Product Analytics")
    st.write("Coming soon...")

elif page == "Delivery":
    st.header("Delivery Performance")
    st.write("Coming soon...")

elif page == "Customers":
    st.header("Customer Insights")
    st.write("Coming soon...")