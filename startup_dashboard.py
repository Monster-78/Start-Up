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
tabs = st.tabs(["📊 EDA Visuals", "📈 Investment Trends", "💰 Funding Round Analysis", "👥 Investor Activity Insights", "📊 Investor-Focused Metrics", "🧠 Start-Up Prediction ","🌍 GEO Information"])

# Tab 1 - EDA Visuals
with tabs[0]:
    st.subheader("Top 15 Startup Categories by Investment Count")
    st.markdown("This bar chart shows which startup categories have received the most investment activity, helping us identify popular and high-interest sectors.")
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
    st.markdown("This visualization highlights countries that have secured the highest total funding amounts, indicating global hotspots for startup investments.")
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
    st.markdown("Here we identify cities that are leading in startup activity, useful for locating emerging entrepreneurial hubs.")
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
    st.markdown("Explore how funding amounts are distributed across the top 5 startup categories. The log scale helps visualize outliers effectively.")
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
    st.markdown("Understand the correlation between total and million-dollar funding metrics using this heatmap.")

    corr = df[['funding_total_usd', 'funding_million_usd']].corr()
    fig5 = px.imshow(corr, text_auto=True, color_continuous_scale='peach', title="Correlation Heatmap")
    st.plotly_chart(fig5, use_container_width=True)



# Tab 3 - Funding Round Analysis
with tabs[2]:
    st.subheader("💰 Funding Round Distribution")
    st.markdown("Displays how often investors participate in different funding rounds (Seed, Series A, B, etc.).")
    
    if 'funding_rounds' in df.columns:
        fig7 = px.histogram(df, x='funding_rounds', nbins=30, title='Distribution of Funding Rounds')
        st.plotly_chart(fig7, use_container_width=True)

    st.subheader("First and Last Funding Timeline")
    st.markdown("Shows which regions receive the most investment overall, indicating potential investment attractiveness.")

    if 'first_funding_at' in df.columns and 'last_funding_at' in df.columns:
        df['first_funding_at'] = pd.to_datetime(df['first_funding_at'], errors='coerce')
        df['last_funding_at'] = pd.to_datetime(df['last_funding_at'], errors='coerce')
        timeline_df = df[['first_funding_at', 'last_funding_at']].melt()
        fig8 = px.histogram(timeline_df, x='value', color='variable', barmode='overlay', title="Funding Timeline")
        st.plotly_chart(fig8, use_container_width=True)

# Tab 4 - Investor Activity Insights
with tabs[3]:
    st.subheader("👥 Investor Round Participation")
    st.markdown("Displays how often investors participate in different funding rounds (Seed, Series A, B, etc.).")
    st.markdown("Shows which regions receive the most investment overall, indicating potential investment attractiveness.")

    rounds = [col for col in df.columns if col.startswith('round_') and col[-1].isalpha()]
    round_df = df[rounds].sum().sort_values(ascending=False)
    fig9 = px.bar(x=round_df.index, y=round_df.values, labels={'x': 'Round Type', 'y': 'Number of Investments'}, title="Investor Participation by Round")
    st.plotly_chart(fig9, use_container_width=True)

    st.subheader("Investment by Region")
    if 'country_code' in df.columns:
        region_funding = df.groupby('country_code')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
        fig10 = px.bar(x=region_funding.index, y=region_funding.values, labels={'x': 'Region', 'y': 'Total Funding'}, title="Top Regions by Total Funding")
        st.plotly_chart(fig10, use_container_width=True)

# Tab 5- Investor Focused Metrics
with tabs[4]:
    st.subheader("📊 Average Investment Size")
    st.markdown("This histogram shows the average investment per startup by dividing total funding by number of rounds.")
    
    if 'funding_rounds' in df.columns:
        df['avg_investment'] = df['funding_total_usd'] / (df['funding_rounds'].replace(0, np.nan))
        fig11 = px.histogram(df, x='avg_investment', nbins=50, title='Distribution of Average Investment Size')
        st.plotly_chart(fig11, use_container_width=True)

    st.subheader("Stage Preference by Country")
    st.markdown("Explore the average stage-wise funding across countries to determine regional investor preferences.")
    
    country_stage = df.groupby('country_code')[rounds].mean().T
    fig12 = px.imshow(country_stage, title="Average Round Participation by Country", aspect="auto")
    st.plotly_chart(fig12, use_container_width=True)

    st.subheader("📈 Startup Funding Trends by Founded Year")
    st.markdown("Analyze funding activity by founding year using a dynamic slider for custom timeline filtering.")


# Clean and prepare the 'founded_at' column
    df['first_funding_at'] = pd.to_datetime(df['first_funding_at'], errors='coerce')
    df['last_funding_at'] = pd.to_datetime(df['last_funding_at'], errors='coerce')

# Get min and max dates as pandas Timestamps
    min_date = df['first_funding_at'].min()
    max_date = df['first_funding_at'].max()

# Convert to Python datetime objects for Streamlit slider
    min_date_dt = min_date.to_pydatetime()
    max_date_dt = max_date.to_pydatetime()

    selected_date_range = st.slider(
    "Select First Funding Date Range:",
       min_value=min_date_dt,
       max_value=max_date_dt,
       value=(min_date_dt, max_date_dt),
       format="YYYY-MM-DD"
    )  

# Filter by selected first funding date range
    filtered_df = df[
        (df['first_funding_at'] >= selected_date_range[0]) &
        (df['first_funding_at'] <= selected_date_range[1])
    ]

    # Aggregate funding total by year (from first_funding_at)
    filtered_df['funding_year'] = filtered_df['first_funding_at'].dt.year
    funding_by_year = filtered_df.groupby('funding_year')['funding_total_usd'].sum().reset_index()

    # Plot funding trend line
    fig = px.line(
        funding_by_year,
        x='funding_year',
        y='funding_total_usd',
        title="Funding Over Years (Filtered by First Funding Date)",
        labels={'funding_year': 'Year', 'funding_total_usd': 'Total Funding (USD)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 6 - Predictive Logic
with tabs[5]:
    st.subheader("🧠 Predictive Logic: High vs Low Funding")
    st.markdown("We label each startup as 'High' or 'Low' funded based on the median total funding. This classification helps with simple predictive modeling.")

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

# Tab 7 - GEO
with tabs[6]:
    st.subheader("🌍 Global Funding Distribution")
    st.markdown("This interactive choropleth map visualizes funding amounts across the world using country codes.")
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
            text="Funding Volume",
            font=dict(size=16)
        )
    )
)

    fig_geo.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Total: $%{z:,.0f}<extra></extra>"
    )

    st.plotly_chart(fig_geo, use_container_width=True)
