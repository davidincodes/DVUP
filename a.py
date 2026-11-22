"""
====================================================================================
ENTERPRISE NETFLIX GLOBAL ANALYTICS & PREDICTIVE DASHBOARD
====================================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="Netflix Global Analytics Engine",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. EXECUTIVE CSS STYLING
# ==========================================
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #0b0b0f;
        color: #e0e0e0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0b0b0f; }
    ::-webkit-scrollbar-thumb { background: #E50914; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #ff0f1a; }

    /* Metric Cards Hover Effect */
    div[data-testid="metric-container"] {
        background-color: #141418;
        border: 1px solid #26262e;
        padding: 18px;
        border-radius: 6px;
        transition: all 0.25s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        border-color: #E50914;
        box-shadow: 0 6px 12px rgba(229, 9, 20, 0.15);
    }

    /* Section Headers */
    .section-header {
        font-size: 20px;
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #ffffff;
        border-bottom: 1px solid #26262e;
        padding-bottom: 8px;
        margin-top: 35px;
        margin-bottom: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CLEAN ENTERPRISE HEADER
# ==========================================
st.title("🎥 Netflix Global Content & Financial Operations Dashboard")
st.markdown("<p style='color: #888; font-size: 14px;'>Global catalog metrics, regional performance, and financial modeling.</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 4. DATA ENGINE
# ==========================================
@st.cache_data
def load_enterprise_data():
    np.random.seed(101)
    n_rows = 5000

    types = np.random.choice(['Movie', 'TV Show'], n_rows, p=[0.70, 0.30])
    years = np.random.randint(2010, 2024, n_rows)
    months = np.random.randint(1, 13, n_rows)

    countries = np.random.choice(
        ['United States', 'India', 'United Kingdom', 'Japan', 'South Korea', 'Canada', 'Spain', 'France', 'Mexico', 'Australia', 'Brazil', 'Germany'],
        n_rows, p=[0.35, 0.15, 0.08, 0.08, 0.06, 0.05, 0.05, 0.04, 0.04, 0.04, 0.03, 0.03]
    )

    genres = np.random.choice(
        ['Drama', 'Comedy', 'Action', 'Thriller', 'Sci-Fi', 'Documentary', 'Horror', 'Anime', 'Romance'],
        n_rows
    )
    ratings = np.random.choice(['TV-MA', 'TV-14', 'PG-13', 'R', 'TV-PG', 'G'], n_rows)

    base_budget = np.random.uniform(1_000_000, 50_000_000, n_rows)
    engagement = np.random.normal(65, 15, n_rows).clip(0, 100)

    revenue = base_budget * (engagement / 40) * np.random.uniform(0.8, 1.5, n_rows)
    global_views = (revenue / 5) * np.random.uniform(0.5, 2.0, n_rows)

    coords = {
        'United States': (37.09, -95.71), 'India': (20.59, 78.96), 'United Kingdom': (55.37, -3.43),
        'Japan': (36.20, 138.25), 'South Korea': (35.90, 127.76), 'Canada': (56.13, -106.34),
        'Spain': (40.46, -3.74), 'France': (46.22, 2.21), 'Mexico': (23.63, -102.55),
        'Australia': (-25.27, 133.77), 'Brazil': (-14.23, -51.92), 'Germany': (51.16, 10.45)
    }

    df = pd.DataFrame({
        'Content_ID': [f'NX-{10000 + i}' for i in range(n_rows)],
        'Type': types,
        'Release_Year': years,
        'Release_Month': months,
        'Country': countries,
        'Genre': genres,
        'Maturity_Rating': ratings,
        'Budget_USD': base_budget,
        'Revenue_USD': revenue,
        'Global_Views': global_views,
        'Engagement_Score': engagement
    })

    df['Latitude'] = df['Country'].map(lambda x: coords[x][0])
    df['Longitude'] = df['Country'].map(lambda x: coords[x][1])

    return df

df = load_enterprise_data()

# ==========================================
# 5. ENTERPRISE CONTROL PANEL
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.markdown("### 🎛️ Data Filters")

selected_types = st.sidebar.multiselect("Content Format", options=df['Type'].unique(), default=df['Type'].unique())
year_range = st.sidebar.slider("Release Window", int(df['Release_Year'].min()), int(df['Release_Year'].max()), (2018, 2023))

all_countries = sorted(df['Country'].unique())
selected_countries = st.sidebar.multiselect("Target Markets", options=all_countries, default=all_countries[:6])

selected_genres = st.sidebar.multiselect("Genre Spectrum", options=df['Genre'].unique(), default=df['Genre'].unique()[:5])

min_budget = st.sidebar.number_input("Min Production Budget ($)", min_value=0, value=0, step=1000000)

mask = (
    (df['Type'].isin(selected_types)) &
    (df['Release_Year'] >= year_range[0]) &
    (df['Release_Year'] <= year_range[1]) &
    (df['Country'].isin(selected_countries)) &
    (df['Genre'].isin(selected_genres)) &
    (df['Budget_USD'] >= min_budget)
)
filtered_df = df[mask]

# ==========================================
# 6. EXECUTIVE KPIs
# ==========================================
if filtered_df.empty:
    st.warning("⚠️ No records match the applied filters.")
    st.stop()

st.markdown("<div class='section-header'>1. Operational & Financial Overview</div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_revenue = filtered_df['Revenue_USD'].sum() / 1e9
avg_engagement = filtered_df['Engagement_Score'].mean()
total_views = filtered_df['Global_Views'].sum() / 1e6
roi = ((filtered_df['Revenue_USD'].sum() - filtered_df['Budget_USD'].sum()) / filtered_df['Budget_USD'].sum()) * 100

kpi1.metric("Catalog Size", f"{len(filtered_df):,}", "Active Titles")
kpi2.metric("Gross Revenue", f"${total_revenue:.2f} B", "+8.4% YoY")
kpi3.metric("Total Viewership", f"{total_views:.1f} M", "+12.1% YoY")
kpi4.metric("Engagement Index", f"{avg_engagement:.1f} / 100", "Stable", delta_color="off")
kpi5.metric("Catalog ROI", f"{roi:.1f}%", "Profitable")

# ==========================================
# 7. GEOSPATIAL ANALYSIS
# ==========================================
st.markdown("<div class='section-header'>2. Global Reach & Spatial Distribution</div>", unsafe_allow_html=True)

map_col, gauge_col = st.columns([7, 3])

with map_col:
    map_df = filtered_df.groupby(['Country', 'Latitude', 'Longitude']).agg({
        'Content_ID': 'count',
        'Revenue_USD': 'sum',
        'Global_Views': 'sum'
    }).reset_index()

    fig_map = px.scatter_geo(
        map_df,
        lat='Latitude', lon='Longitude',
        color="Revenue_USD",
        size="Global_Views",
        hover_name="Country",
        hover_data={"Content_ID": True, "Latitude": False, "Longitude": False, "Revenue_USD": ':$,.0f'},
        title="Global Market Penetration & Revenue Map",
        size_max=45,
        template="plotly_dark",
        color_continuous_scale="Reds"
    )
    fig_map.update_geos(
        showcoastlines=True, coastlinecolor="#333",
        showland=True, landcolor="#111",
        showocean=True, oceancolor="#050505",
        projection_type="natural earth"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=480)
    st.plotly_chart(fig_map, use_container_width=True)

with gauge_col:
    st.markdown("<br>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = avg_engagement,
        title = {'text': "Retention Quality Score", 'font': {'size': 18, 'color': 'white'}},
        delta = {'reference': 60, 'increasing': {'color': "#00ff00"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#E50914"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 40], 'color': '#2a0204'},
                {'range': [40, 75], 'color': '#66040a'},
                {'range': [75, 100], 'color': '#b30711'}],
        }
    ))
    fig_gauge.update_layout(template='plotly_dark', height=380, margin={"r":10,"t":40,"l":10,"b":10})
    st.plotly_chart(fig_gauge, use_container_width=True)

# ==========================================
# 8. TIME SERIES & CONVERSION
# ==========================================
st.markdown("<div class='section-header'>3. Production Metrics & Conversion Modeling</div>", unsafe_allow_html=True)

ts_col1, ts_col2 = st.columns([6, 4])

with ts_col1:
    yearly_stats = filtered_df.groupby(['Release_Year', 'Type']).agg({
        'Content_ID': 'count',
        'Revenue_USD': 'sum'
    }).reset_index()

    fig_area = px.area(
        yearly_stats, x='Release_Year', y='Content_ID', color='Type',
        title="Annual Production Output Trend",
        color_discrete_map={'Movie': '#E50914', 'TV Show': '#555555'},
        template='plotly_dark', markers=True
    )
    fig_area.update_layout(hovermode="x unified", height=380)
    st.plotly_chart(fig_area, use_container_width=True)

with ts_col2:
    funnel_data = pd.DataFrame({
        'Stage': ['Impressions', 'Trailer Plays', 'Started (10m)', 'Completed Title', 'Re-watched'],
        'Count': [total_views * 5, total_views * 2, total_views, total_views * 0.4, total_views * 0.15]
    })
    fig_funnel = px.funnel(
        funnel_data, x='Count', y='Stage',
        title="Viewer Engagement Funnel",
        template='plotly_dark',
        color_discrete_sequence=['#E50914']
    )
    fig_funnel.update_layout(height=380)
    st.plotly_chart(fig_funnel, use_container_width=True)

# ==========================================
# 9. FINANCIAL CORRELATIONS & GENRE PERFORMANCE
# ==========================================
st.markdown("<div class='section-header'>4. Financial Modeling & Genre Performance</div>", unsafe_allow_html=True)

ml_col1, ml_col2 = st.columns(2)

with ml_col1:
    fig_scatter = px.scatter(
        filtered_df, x="Budget_USD", y="Revenue_USD", color="Type",
        size="Engagement_Score", hover_name="Content_ID",
        title="Production Cost vs Revenue Return Distribution",
        template="plotly_dark",
        color_discrete_map={'Movie': '#E50914', 'TV Show': '#888888'},
        labels={"Budget_USD": "Production Budget ($)", "Revenue_USD": "Generated Revenue ($)"}
    )
    fig_scatter.update_layout(height=420)
    st.plotly_chart(fig_scatter, use_container_width=True)

with ml_col2:
    # Replaced complex Treemap with a clean, easy-to-explain Genre Bar Chart
    genre_rev = filtered_df.groupby('Genre')['Revenue_USD'].sum().reset_index().sort_values(by='Revenue_USD', ascending=True)
    fig_genre = px.bar(
        genre_rev, x='Revenue_USD', y='Genre', orientation='h',
        title="Total Revenue Generated by Genre",
        template="plotly_dark",
        color='Revenue_USD', color_continuous_scale='Reds',
        labels={"Revenue_USD": "Total Revenue ($)", "Genre": "Content Genre"}
    )
    fig_genre.update_layout(height=420, showlegend=False)
    st.plotly_chart(fig_genre, use_container_width=True)

# ==========================================
# 10. RAW DATA EXPLORER
# ==========================================
st.markdown("<div class='section-header'>5. Enterprise Database Extract</div>", unsafe_allow_html=True)

with st.expander("📂 Access Data Warehouse Extract (Filtered View)", expanded=False):
    st.dataframe(
        filtered_df.style.format({
            "Budget_USD": "${:,.0f}",
            "Revenue_USD": "${:,.0f}",
            "Global_Views": "{:,.0f}",
            "Engagement_Score": "{:.1f}"
        }),
        height=380,
        use_container_width=True
    )

    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Data to CSV",
        data=csv_data,
        file_name=f'netflix_data_extract_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #555; font-size: 11px;'>"
    "NETFLIX DATA ANALYTICS & BUSINESS INTELLIGENCE PLATFORM<br>"
    "Internal Operations View — Powered by Python & Streamlit Engine</p>",
    unsafe_allow_html=True
)
