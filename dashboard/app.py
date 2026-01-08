import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    monthly = pd.read_csv('data/monthly_revenue.csv')
    states = pd.read_csv('data/state_revenue.csv')
    categories = pd.read_csv('data/category_performance.csv')
    delivery = pd.read_csv('data/delivery_performance.csv')
    segments = pd.read_csv('data/customer_segments.csv')
    days = pd.read_csv('data/day_patterns.csv')
    payments = pd.read_csv('data/payment_methods.csv')
    
    # Create date column immediately after loading
    monthly['date'] = pd.to_datetime(
        monthly['order_year'].astype(str) + '-' + 
        monthly['order_month'].astype(str).str.zfill(2)
    )
    
    return monthly, states, categories, delivery, segments, days, payments

monthly_df, states_df, categories_df, delivery_df, segments_df, days_df, payments_df = load_data()

# Title
st.title("E-Commerce Sales Analysis Dashboard")
st.markdown("---")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select Page",
    ["Executive Summary", "Products", "Delivery", "Customers"]
)

# Filters in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

# Date range filter
min_date = monthly_df['date'].min()
max_date = monthly_df['date'].max()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# State filter
all_states = ['All'] + sorted(states_df['customer_state'].unique().tolist())
selected_state = st.sidebar.selectbox("State", all_states)

# Apply filters
if selected_state != 'All':
    states_df = states_df[states_df['customer_state'] == selected_state]
    delivery_df = delivery_df[delivery_df['customer_state'] == selected_state]

# Filter by date
if len(date_range) == 2:
    monthly_df = monthly_df[
        (monthly_df['date'] >= pd.Timestamp(date_range[0])) &
        (monthly_df['date'] <= pd.Timestamp(date_range[1]))
    ]

# Page routing
if page == "Executive Summary":
    st.header("Executive Summary")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = monthly_df['total_revenue'].sum()
    total_orders = monthly_df['total_orders'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    on_time_rate = delivery_df['on_time_pct'].mean() if len(delivery_df) > 0 else 0
    
    col1.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Avg Order Value", f"R$ {avg_order_value:.2f}")
    col4.metric("On-Time Rate", f"{on_time_rate:.1f}%")
    
    st.markdown("---")
    
    # Key Insights
    st.subheader("Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Revenue Peak**  
        November 2017 generated highest revenue (R$ 1.15M).  
        Q4 shows 30-40% higher revenue than other quarters.
        """)
    
    with col2:
        st.warning("""
        **Retention Crisis**  
        97% of customers make only ONE purchase.  
        Potential: R$ 1.26M annual revenue if 10% become repeat buyers.
        """)
    
    with col3:
        st.error("""
        **Delivery Issues**  
        3 states have 60% of late deliveries.  
        Average delay: 5+ days beyond estimate.
        """)
    
    st.markdown("---")
    
    # Monthly revenue trend
    st.subheader("Monthly Revenue Trend")
    
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
    
    # Revenue by state
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 States by Revenue")
        
        top10_states = states_df.head(10)
        
        fig = px.bar(
            top10_states,
            x='customer_state',
            y='total_revenue',
            title='Revenue by State'
        )
        fig.update_layout(
            xaxis_title="State",
            yaxis_title="Revenue (R$)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Distribution")
        
        fig = px.pie(
            top10_states,
            values='total_revenue',
            names='customer_state',
            title='Revenue Share (Top 10 States)'
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Products":
    st.header("Product Analytics")
    st.write("Coming in Day 9...")

elif page == "Delivery":
    st.header("Delivery Performance")
    st.write("Coming in Day 9...")

elif page == "Customers":
    st.header("Customer Insights")
    st.write("Coming in Day 10...")