# ============================================================
# RetailPulse | Streamlit App
# Author: Naisha
# Date: June 2026
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="RetailPulse Analytics",
    page_icon="⚡",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    orders = pd.read_csv("Data/processed/orders_clean.csv",
                         parse_dates=['order_purchase_timestamp'])
    payments = pd.read_csv("Data/processed/payments_clean.csv")
    customers = pd.read_csv("Data/raw/olist_customers_dataset.csv")
    rfm = pd.read_csv("Data/processed/rfm_segments.csv")
    category_revenue = pd.read_csv("Data/processed/category_revenue.csv")
    return orders, payments, customers, rfm, category_revenue

orders, payments, customers, rfm, category_revenue = load_data()

# Merge for analysis
df = orders.merge(payments, on='order_id').merge(customers, on='customer_id')
df = df[df['order_status'] == 'delivered']

# ── Header ──────────────────────────────────────────────────
st.title("⚡ RetailPulse Analytics")
st.caption("E-Commerce Sales Analytics · Olist Brazil · 2016–2018")
st.divider()

# ── KPI Row ─────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"R${df['payment_value'].sum():,.0f}")
col2.metric("Total Orders", f"{df['order_id'].nunique():,}")
col3.metric("Avg Order Value", f"R${df['payment_value'].mean():,.2f}")
col4.metric("Repeat Purchase Rate", "3.12%", delta="-11.88% below target")

st.divider()

# ── Charts Row ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue Trend")
    df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly = df.groupby('month')['payment_value'].sum().reset_index()
    fig = px.line(monthly, x='month', y='payment_value',
                  title='', color_discrete_sequence=['#c084fc'])
    fig.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Categories by Revenue")
    fig2 = px.bar(category_revenue.sort_values('revenue'),
                  x='revenue', y='category', orientation='h',
                  color_discrete_sequence=['#c084fc'])
    fig2.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── RFM Segments ────────────────────────────────────────────
st.subheader("Customer Segments — RFM Analysis")
col1, col2 = st.columns(2)

with col1:
    segment_counts = rfm['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    fig3 = px.bar(segment_counts, x='segment', y='count',
                  color='segment',
                  color_discrete_sequence=['#c084fc', '#f87171',
                  '#fbbf24', '#22c55e', '#60a5fa', '#f97316'])
    fig3.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#1a1a2e',
        font_color='white',
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Segment Summary")
    segment_revenue = rfm.groupby('segment')['monetary'].agg(['sum', 'mean', 'count'])
    segment_revenue.columns = ['Total Revenue', 'Avg Revenue', 'Customers']
    segment_revenue['Total Revenue'] = segment_revenue['Total Revenue'].apply(
        lambda x: f"R${x:,.0f}")
    segment_revenue['Avg Revenue'] = segment_revenue['Avg Revenue'].apply(
        lambda x: f"R${x:,.0f}")
    st.dataframe(segment_revenue, use_container_width=True)

st.divider()

# ── Revenue by State ────────────────────────────────────────
st.subheader("Revenue by State")
state_revenue = df.groupby('customer_state')['payment_value'].sum().reset_index()
state_revenue.columns = ['state', 'revenue']
state_revenue = state_revenue.sort_values('revenue', ascending=False).head(10)

fig4 = px.bar(state_revenue, x='state', y='revenue',
              color_discrete_sequence=['#c084fc'])
fig4.update_layout(
    plot_bgcolor='#1a1a2e',
    paper_bgcolor='#1a1a2e',
    font_color='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)
st.plotly_chart(fig4, use_container_width=True)

# ── Footer ──────────────────────────────────────────────────
st.divider()
st.caption("Built by Naisha · RetailPulse Portfolio Project · 2026")
