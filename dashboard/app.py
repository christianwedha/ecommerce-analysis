import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Custom CSS styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    
    .stMetric {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stMetric label {
        font-size: 0.9rem;
        color: #FAFAFA;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #FFFFFF;
    }
    
    h1 {
        color: #FFFFFF;
        padding-bottom: 1rem;
        border-bottom: 2px solid #FF4B4B;
    }
    
    h2 {
        color: #FAFAFA;
        padding: 1rem 0 0.5rem 0;
    }
    
    h3 {
        color: #E0E0E0;
        padding: 0.5rem 0;
    }
    
    .stPlotlyChart {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    div[data-testid="stDataFrame"] {
        background-color: #262730;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    .element-container {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Page config (keep this after CSS)
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
    
    # Top categories
    st.subheader("Top 10 Product Categories")

    top10_categories = categories_df.head(10)

    fig = px.bar(
        top10_categories,
        x='category',
        y='total_revenue',
        color='items_sold',
        title='Revenue and Volume by Category'
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Revenue (R$)",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category Performance Table")

        display_df = top10_categories[['category', 'total_orders', 'total_revenue', 'avg_item_price']].copy()
        display_df.columns = ['Category', 'Orders', 'Revenue', 'Avg Price']
        display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"R$ {x:,.2f}")
        display_df['Avg Price'] = display_df['Avg Price'].apply(lambda x:f"R$ {x:.2f}")

        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Freight Cost Analysis")

        high_freight = categories_df.nlargest(10, 'avg_freight_pct')

        fig = px.bar(
            high_freight,
            x='category',
            y='avg_freight_pct',
            title='Categories with Highest Freight % (Top 10)',
            color='avg_freight_pct',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Freight % of Price",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

    # Revenue concentration
    st.markdown("---")
    st.subheader("Revenue Concentration")
    
    top10_revenue = top10_categories['total_revenue'].sum()
    total_revenue = categories_df['total_revenue'].sum()
    concentration = (top10_revenue / total_revenue) * 100
    
    st.metric(
        "Top 10 Categories",
        f"{concentration:.1f}% of total revenue",
        help="Healthy if between 50-70%. Current: moderate concentration."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"""
        **Insight: Balanced Portfolio**  
        Top 10 categories represent {concentration:.1f}% of revenue.  
        Below 70% threshold indicates healthy diversification.
        """)
    
    with col2:
        st.info("""
        **Recommendation**  
        Focus inventory on top 10 categories while maintaining diversity.  
        Consider premium line for high AOV categories (Watches, Electronics).
        """)



elif page == "Delivery":
    st.header("Delivery Performance")
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    avg_delivery = delivery_df['avg_delivery_days'].mean()
    on_time_avg = delivery_df['on_time_pct'].mean()
    worst_state = delivery_df.loc[delivery_df['avg_delivery_days'].idxmax()]
    
    col1.metric("Avg Delivery Time", f"{avg_delivery:.1f} days")
    col2.metric("Avg On-Time Rate", f"{on_time_avg:.1f}%")
    col3.metric("Slowest State", f"{worst_state['customer_state']} ({worst_state['avg_delivery_days']:.0f} days)")
    
    st.markdown("---")
    
    # Delivery time by state
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Delivery Time by State")
        
        top15_slow = delivery_df.nlargest(15, 'avg_delivery_days')
        
        fig = px.bar(
            top15_slow,
            x='customer_state',
            y='avg_delivery_days',
            title='15 Slowest States',
            color='avg_delivery_days',
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_layout(
            xaxis_title="State",
            yaxis_title="Avg Delivery Days",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("On-Time Delivery Rate")
        
        worst_ontime = delivery_df.nsmallest(15, 'on_time_pct')
        
        fig = px.bar(
            worst_ontime,
            x='customer_state',
            y='on_time_pct',
            title='15 States with Lowest On-Time Rate',
            color='on_time_pct',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(
            xaxis_title="State",
            yaxis_title="On-Time Rate (%)",
            xaxis_tickangle=-45
        )
        fig.add_hline(y=80, line_dash="dash", line_color="red", 
                     annotation_text="80% Threshold")
        st.plotly_chart(fig, use_container_width=True)
    
    # Problem states
    st.markdown("---")
    st.subheader("Problem States (On-Time Rate < 80%)")
    
    problem_states = delivery_df[delivery_df['on_time_pct'] < 80].sort_values('on_time_pct')
    
    if len(problem_states) > 0:
        st.error(f"Found {len(problem_states)} state(s) below 80% on-time threshold")
        
        display_df = problem_states[['customer_state', 'total_orders', 'avg_delivery_days', 'on_time_pct']].copy()
        display_df.columns = ['State', 'Total Orders', 'Avg Delivery Days', 'On-Time Rate (%)']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        affected_orders = problem_states['total_orders'].sum()
        st.warning(f"""
        **Business Impact**  
        {affected_orders:,} orders affected by poor delivery performance.  
        Estimated monthly revenue at risk: R$ {affected_orders * 160:,.0f}
        """)
    else:
        st.success("All states meet 80% on-time delivery threshold")
    
    # Recommendations
    st.markdown("---")
    st.subheader("Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Northern States Strategy**  
        Accept 20-25 day delivery as reality for AM, AP, RR.  
        Set realistic expectations (25-30 days) instead of over-promising.  
        Improves customer satisfaction even with same delivery time.
        """)
    
    with col2:
        st.error("""
        **Critical: Fix Alagoas (AL)**  
        Only state below 80% threshold.  
        Partner with regional carrier or open fulfillment point.  
        Quick win opportunity.
        """)
elif page == "Customers":
    st.header("Customer Insights")
    
    # Customer segments
    st.subheader("Customer Segmentation")

    col1,col2 = st.columns(2)

    with col1:
        fig = px.pie(
            segments_df,
            values='customer_count',
            names='customer_segment',
            title='Customer Distribution by Segment'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            segments_df,
            x='customer_segment',
            y='avg_lifetime_value',
            titel='Average LTV by Segment',
            color='avg_lifetime_value',
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            xaxis_title="Segment",
            yaxis_title="Avg LTV (R$)"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Segment metrics
    st.markdown("---")
    st.subheader("Segment Performance")

    total_customers = segments_df['customer_count'].sum()
    total_revenue = segments_df['total_segment_revenue'].sum()

    display_segments = segments_df.copy()
    display_segments['pct_customers'] = (display_segments['customer_count'] / total_customers * 100).round(1)
    display_segments['pct_revenue'] = (display_segments['total_segment_revenue'] / total_revenue * 100).round(1)

    display_segments['avg_lifetime_value'] = display_segments['avg_lifetime_value'].apply(lambda x: f"R$ {x:,.2f}")
    display_segments['total_segment_revenue'] = display_segments['total_segment_revenue'].apply(lambda x: f"R$ {x:,.2f}")
    
    display_segments.columns = ['Segment', 'Customer Count', 'Avg LTV', 'Avg Orders', 'Total Revenue', '% Customers', '% Revenue']
    
    st.dataframe(display_segments, use_container_width=True, hide_index=True)
    
    # Critical finding
    onetime_pct = segments_df[segments_df['customer_segment'] == 'One-time']['customer_count'].values[0] / total_customers * 100
    
    st.error(f"""
    **CRITICAL FINDING: Retention Crisis**  
    {onetime_pct:.1f}% of customers make only ONE purchase.  
    
    **Impact:**  
    - No customer lifetime value (just transaction value)  
    - Every R$ 160 revenue requires NEW customer acquisition  
    - Competitors with 20% repeat rate will outlast us  
    
    **Opportunity:**  
    Moving just 10% from one-time to repeat = +R$ 1.26M annual revenue
    """)
    
    # Shopping patterns
    st.markdown("---")
    st.subheader("Shopping Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Orders by Day of Week")
        
        fig = px.bar(
            days_df,
            x='day_name',
            y='total_orders',
            title='Order Volume by Day'
        )
        fig.update_layout(
            xaxis_title="Day",
            yaxis_title="Orders"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        peak_day = days_df.loc[days_df['total_orders'].idxmax(), 'day_name']
        st.info(f"""
        **Peak Day: {peak_day}**  
        Weekday shopping preference indicates office/desk browsing.  
        Schedule flash sales Sunday evening for Monday morning traffic.
        """)
    
    with col2:
        st.subheader("Payment Methods")
        
        top_payments = payments_df.head(5)
        
        fig = px.bar(
            top_payments,
            x='payment_methods',
            y='total_orders',
            title='Top 5 Payment Methods'
        )
        fig.update_layout(
            xaxis_title="Payment Method",
            yaxis_title="Orders",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if len(top_payments[top_payments['payment_methods'] == 'credit_card']) > 0:
            credit_orders = top_payments[top_payments['payment_methods'] == 'credit_card']['total_orders'].values[0]
            credit_pct = (credit_orders / payments_df['total_orders'].sum() * 100)
            
            st.success(f"""
            **Credit Card Dominance: {credit_pct:.1f}%**  
            Average 3.5 installments = payment spreading behavior.  
            Gateway uptime is CRITICAL (99.9% requirement).
            """)
    
    # Recommendations
    st.markdown("---")
    st.subheader("Retention Strategy Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Immediate (Week 1-4)**  
        - Post-purchase email (Day 7, 14, 30)  
        - 20% discount on 2nd order  
        - Target: 5% conversion
        """)
    
    with col2:
        st.success("""
        **Short-term (Month 1-3)**  
        - Loyalty program (points system)  
        - Bundle recommendations  
        - Free shipping on 3+ items
        """)
    
    with col3:
        st.warning("""
        **Medium-term (Quarter 1-2)**  
        - Category-specific retention  
        - VIP program for repeat buyers  
        - Referral incentives
        """)

# Footer (add at the very end, after all elif blocks)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem 0; font-size: 0.9rem;'>
    <p style='margin: 0.5rem 0;'><strong>E-Commerce Sales Analysis Dashboard</strong></p>
    <p style='margin: 0.5rem 0;'>Built with Streamlit & Plotly | Data: 100,000+ orders (2016-2018)</p>
    <p style='margin: 0.5rem 0;'>
        <a href='https://github.com/christianwedha/ecommerce-analysis' style='color: #FF4B4B; text-decoration: none;'>GitHub</a> | 
        <a href='https://linkedin.com/in/christianwedha' style='color: #FF4B4B; text-decoration: none;'>LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)