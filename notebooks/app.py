import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Queens Supermarket Analytics", layout="wide")
st.title("Queens Supermarket Sales Analytics Dashboard")
st.markdown("**Midroc Commerce | Data Warehouse**")

# Database Connection
@st.cache_resource
def get_engine():
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'queens_supermarket_dw')
    return create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

engine = get_engine()


@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

# Load dimension and fact data
dim_branch = load_data("SELECT * FROM dim_branch")
dim_product = load_data("SELECT * FROM dim_product")
dim_date = load_data("SELECT date_key, full_date, year, month_name FROM dim_date")

fact_query = """
SELECT 
    f.invoice_id, f.date_key, f.branch_key, f.product_key,
    f.customer_type_key, f.payment_key,
    f.quantity, f.unit_price, f.total, f.gross_income,
    f.gross_margin_percentage, f.rating, f.time_of_day,
    b.branch_name, b.city,
    p.product_line,
    d.full_date
FROM fact_sales f
JOIN dim_branch b ON f.branch_key = b.branch_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
"""

df = load_data(fact_query)
df['full_date'] = pd.to_datetime(df['full_date'])


# In[3]:


st.sidebar.header("Filters")

selected_branches = st.sidebar.multiselect(
    "Select Branches",
    options=dim_branch['branch_name'].unique(),
    default=dim_branch['branch_name'].unique()
)

selected_products = st.sidebar.multiselect(
    "Select Product Lines",
    options=dim_product['product_line'].unique(),
    default=dim_product['product_line'].unique()[:4]
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['full_date'].min(), df['full_date'].max()),
    min_value=df['full_date'].min(),
    max_value=df['full_date'].max()
)


# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

filtered_df = df[
    (df['branch_name'].isin(selected_branches)) &
    (df['product_line'].isin(selected_products)) &
    (df['full_date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

total_revenue = filtered_df['total'].sum()
total_transactions = len(filtered_df)
avg_transaction = filtered_df['total'].mean()
avg_margin = filtered_df['gross_margin_percentage'].mean()

col1.metric("Total Revenue", f"{total_revenue:,.0f} ETB")
col2.metric("Transactions", f"{total_transactions:,}")
col3.metric("Avg Transaction", f"{avg_transaction:,.0f} ETB")
col4.metric("Avg Gross Margin", f"{avg_margin:.1f}%")

# Visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Sales Overview", "Branch Performance", "Product Analysis", "Trends"])

with tab1:
    st.subheader("Monthly Sales Trend")
    monthly = filtered_df.groupby(filtered_df['full_date'].dt.to_period('M'))['total'].sum().reset_index()
    monthly['full_date'] = monthly['full_date'].astype(str)
    fig = px.line(monthly, x='full_date', y='total', title="Monthly Revenue Trend")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Performance by Branch")
    branch_perf = filtered_df.groupby('branch_name')['total'].sum().reset_index()
    fig = px.bar(branch_perf, x='branch_name', y='total', title="Revenue by Branch")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Top Product Lines")
    product_perf = filtered_df.groupby('product_line')['total'].sum().nlargest(8).reset_index()
    fig = px.bar(product_perf, x='total', y='product_line', orientation='h', title="Revenue by Product Line")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Payment Method Distribution")
    payment_dist = filtered_df['payment_key'].value_counts().reset_index()
    # You can map payment_key to actual names if needed
    fig = px.pie(payment_dist, names='payment_key', values='count', title="Payment Methods")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Developed by Aklilu Abera | Data Engineer Portfolio Project")
st.caption("Midroc Investment Group - Queens Supermarket Sales Analytics")




