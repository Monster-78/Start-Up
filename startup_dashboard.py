# startup_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

#### DASHBOARD ####
st.set_page_config(page_title="Startup Investment Dashboard", layout="wide")
df = pd.read_csv("clean.csv", dtype={'column': 'float'}, keep_default_na=True)

# Layout

st.title("🚀 Startup Investment Insights Dashboard")

# Tabs for navigation
tabs = st.tabs(["📊 EDA Visuals", "📈 Investment Trends", "🧠 Start-Up Prediction ","🌍 GEO Information"])

# Tab 1 - EDA Visuals
with tabs[0]:
    st.subheader("Top 15 Startup Categories by Investment Count")
    top_categories = df['main_category'].value_counts().head(15)
    fig1 = px.bar(
        x=top_categories.values,
        y=top_categories.index,
        orientation='h',
        labels={'x': 'Number of Investments', 'y': 'Startup Category'},
        color=top_categories.values,
        color_continuous_scale='plasma',
        title="Top 15 Categories"
    )
    fig1.update_traces(marker=dict(line=dict(color='black', width=2)))
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Top 10 Countries by Total Funding")
    top_countries = df.groupby('country_code')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
    fig2 = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        orientation='h',
        labels={'x': 'Total Funding (USD)', 'y': 'Country'},
        color=top_countries.values,
        color_continuous_scale='viridis',
        title="Top Funded Countries"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 10 Cities with Most Startups")
    top_cities = df['city'].value_counts().head(10)
    fig3 = px.bar(
        x=top_cities.index,
        y=top_cities.values,
        labels={'x': 'City', 'y': 'Startup Count'},
        color=top_cities.values,
        color_continuous_scale='thermal',
        title="Cities with Most Startups"
    )
    st.plotly_chart(fig3, use_container_width=True)

# Tab 2 - Investment Distribution
with tabs[1]:
    st.subheader("Funding Distribution by Category")
    top5_cat = df['main_category'].value_counts().head(5).index
    df_top5 = df[df['main_category'].isin(top5_cat)]
    fig4 = px.box(
        df_top5,
        x='main_category',
        y='funding_million_usd',
        log_y=True,
        points='outliers',
        color='main_category',
        labels={'funding_million_usd': 'Funding (Million USD)', 'main_category': 'Category'},
        title="Funding Distribution (Log Scale)"
        
        
    )
    
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Correlation Heatmap")
    corr = df[['funding_total_usd', 'funding_million_usd']].corr()
    fig5 = px.imshow(corr, text_auto=True, color_continuous_scale='peach', title="Correlation Heatmap")
    st.plotly_chart(fig5, use_container_width=True)

# Tab 3 - Predictive Logic
with tabs[2]:
    st.subheader("🧠 Predictive Logic: High vs Low Funding")
    threshold = df['funding_total_usd'].median()
    df['funding_label'] = df['funding_total_usd'].apply(lambda x: 'High' if x > threshold else 'Low')
    label_count = df['funding_label'].value_counts()
    fig6 = px.pie(values=label_count.values, names=label_count.index, title="High vs Low Funding Startups")
    fig6.update_traces(marker=dict(line=dict(color='black', width=3)))
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
        **Logic**: 
        - If `funding_total_usd` > median → High
        - Else → Low
    """)

with tabs[3]:
    st.subheader("🌍 Global Funding Distribution")

    country_funding = df.groupby('country_code')['funding_total_usd'].sum().reset_index()

    fig_geo = px.choropleth(
        country_funding,
        locations='country_code',
        locationmode='ISO-3',
        color='funding_total_usd',
        hover_name='country_code',
        color_continuous_scale='Reds',
        title="Funding Distribution by Country"
    )

   
    fig_geo.update_layout(
      coloraxis_colorbar=dict(
         title=dict(
            text="Your Legend Title",
            font=dict(size=16)
        )
    )
)


    fig_geo.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Total: $%{z:,.0f}<extra></extra>"
    )

    st.plotly_chart(fig_geo, use_container_width=True)
