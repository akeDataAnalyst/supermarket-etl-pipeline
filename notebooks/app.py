import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Queens Supermarket Analytics",
    layout="wide",
    page_icon="🛒"
)

st.title("Queens Supermarket Sales Analytics")
st.markdown("**Midroc Commerce | Data Warehouse Dashboard**")

# ====================== LOAD DATA FROM FILE ======================
@st.cache_data
def load_data():
    data_path = "data/silver/queens_supermarket_sales_silver.parquet"
    if os.path.exists(data_path):
        if data_path.endswith('.parquet'):
            df = pd.read_parquet(data_path)
        else:
            df = pd.read_csv(data_path)
        return df
    else:
        st.error(f"Data file not found at: {data_path}")
        st.stop()

df = load_data()

# Convert date column
df['date'] = pd.to_datetime(df['date'])
df['full_date'] = df['date']

# ====================== SIDEBAR FILTERS ======================
st.sidebar.header("🔍 Filters")

selected_branches = st.sidebar.multiselect(
    "Select Branches",
    options=sorted(df['branch_name'].unique()),
    default=sorted(df['branch_name'].unique())
)

selected_products = st.sidebar.multiselect(
    "Select Product Lines",
    options=sorted(df['product_line'].unique()),
    default=sorted(df['product_line'].unique())[:5]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['full_date'].min().date(), df['full_date'].max().date()),
    min_value=df['full_date'].min().date(),
    max_value=df['full_date'].max().date()
)

# Filter the dataframe
filtered_df = df[
    (df['branch_name'].isin(selected_branches)) &
    (df['product_line'].isin(selected_products)) &
    (df['full_date'].dt.date.between(date_range[0], date_range[1]))
]

# ====================== KPI METRICS ======================
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['total'].sum()
total_transactions = len(filtered_df)
avg_transaction = filtered_df['total'].mean()
avg_margin = filtered_df['gross_margin_percentage'].mean()

col1.metric("Total Revenue", f"{total_revenue:,.0f} ETB")
col2.metric("Transactions", f"{total_transactions:,}")
col3.metric("Avg Transaction", f"{avg_transaction:,.0f} ETB")
col4.metric("Avg Gross Margin", f"{avg_margin:.1f}%")

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Sales Overview", 
    "🏬 Branch Performance", 
    "📦 Product Analysis", 
    "👥 Customer Insights"
])

with tab1:
    st.subheader("Monthly Sales Trend")
    monthly = filtered_df.groupby(filtered_df['full_date'].dt.to_period('M'))['total'].sum().reset_index()
    monthly['full_date'] = monthly['full_date'].astype(str)
    fig = px.line(monthly, x='full_date', y='total', title="Monthly Revenue Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Revenue by Branch")
    branch_perf = filtered_df.groupby('branch_name')['total'].sum().reset_index()
    fig = px.bar(branch_perf, x='branch_name', y='total', title="Total Revenue by Branch")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Top Product Lines by Revenue")
    product_perf = filtered_df.groupby('product_line')['total'].sum().nlargest(8).reset_index()
    fig = px.bar(product_perf, x='total', y='product_line', orientation='h', 
                 title="Revenue by Product Line", color='total')
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Payment Method Distribution")
    payment_dist = filtered_df['payment'].value_counts().reset_index()
    payment_dist.columns = ['Payment Method', 'Count']
    fig = px.pie(payment_dist, names='Payment Method', values='Count', 
                 title="Payment Methods Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ====================== FOOTER ======================
st.markdown("---")
st.caption("Developed by **Aklilu Abera** | Data Engineer")
st.caption("Queens Supermarket Sales ETL Pipeline | Midroc Commerce Portfolio Project")
st.caption(f"Last Updated: {datetime.now().strftime('%B %d, %Y')}")
