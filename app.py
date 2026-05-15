import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import report_generator

# --- REPORT HELPER ---
@st.cache_data(show_spinner=False)
def generate_cached_report(title, desc, _figures, dataframe=None):
    return report_generator.generate_pdf(title, desc, _figures, dataframe)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Global Data Dashboard", layout="wide")
st.title("Global Socio-Economic & Microfinance Dashboard")

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    # Load datasets
    df_country = pd.read_csv('country_profile_variables.csv')
    df_kiva = pd.read_csv('kiva_country_profile_variables.csv')
    
    # Clean '-99' and '...' which represent missing values, and '~0.0' for near zero
    for df in [df_country, df_kiva]:
        df.replace({'-99': np.nan, -99: np.nan, '...': np.nan}, inplace=True)
        df.replace({'~0.0': 0.0, '~0': 0, '-~0.0': 0.0}, inplace=True)
        
    # Ensure key columns used in plots are numeric
    numeric_cols = [
        'GDP growth rate (annual %, const. 2005 prices)',
        'Health: Total expenditure (% of GDP)',
        'Education: Government expenditure (% of GDP)',
        'Individuals using the Internet (per 100 inhabitants)',
        'Mobile-cellular subscriptions (per 100 inhabitants)',
        'GDP per capita (current US$)',
        'Employment: Agriculture (% of employed)',
        'Unemployment (% of labour force)',
        'Economy: Agriculture (% of GVA)',
        'Economy: Industry (% of GVA)',
        'Economy: Services and other activity (% of GVA)'
    ]
    
    for col in numeric_cols:
        if col in df_country.columns:
            df_country[col] = pd.to_numeric(df_country[col], errors='coerce')
        if col in df_kiva.columns:
            df_kiva[col] = pd.to_numeric(df_kiva[col], errors='coerce')
            
    return df_country, df_kiva

df_country, df_kiva = load_data()

# Clean up column names for easier access (optional but recommended)
gdp_col = 'GDP growth rate (annual %, const. 2005 prices)'
health_col = 'Health: Total expenditure (% of GDP)'
edu_col = 'Education: Government expenditure (% of GDP)'
internet_col = 'Individuals using the Internet (per 100 inhabitants)'
mobile_col = 'Mobile-cellular subscriptions (per 100 inhabitants)'

# --- SIDEBAR FOR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a View:", 
    ("Socio-Economic Correlations", "Microfinance Impact", "Country Comparison"))

# ==========================================
# PAGE 1: SOCIO-ECONOMIC CORRELATIONS
# ==========================================
if page == "Socio-Economic Correlations":
    st.header("1. Health & Education vs. GDP")
    st.write("Explore how government spending on health and education correlates with GDP growth.")
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Select X-Axis", [health_col, edu_col])
    with col2:
        y_axis = st.selectbox("Select Y-Axis", [gdp_col, 'GDP per capita (current US$)'])
        
    # Drop NaNs for a clean plot
    plot_data = df_country.dropna(subset=[x_axis, y_axis])
    
    fig = px.scatter(
        plot_data, x=x_axis, y=y_axis, 
        hover_name="country", color="Region",
        trendline="ols", # Adds a line of best fit
        title=f"Correlation: {x_axis} vs {y_axis}"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- REPORT GENERATION ---
    st.markdown("---")
    st.subheader("Export Findings")
    global_corr = plot_data[x_axis].corr(plot_data[y_axis])
    desc = [
        f"Analysis of {x_axis} vs {y_axis}.",
        f"Global Correlation (Pearson): {global_corr:.3f}",
        "The chart below shows the trendline across different regions."
    ]
    with st.spinner("Preparing Report..."):
        pdf_bytes = generate_cached_report("Socio-Economic Correlations Report", desc, [fig])
    st.download_button(label="📄 Download PDF Report", data=pdf_bytes, file_name="socio_economic_report.pdf", mime="application/pdf")

# ==========================================
# PAGE 2: MICROFINANCE IMPACT (Kiva Data)
# ==========================================
elif page == "Microfinance Impact":
    st.header("2. Technology Access and Microfinance")
    st.write("Does higher internet or mobile penetration correlate with Kiva metrics? (Using Kiva Country Profiles)")
    
    # We use df_kiva here. Since Kiva country profiles contain the same base columns 
    # as the UN dataset in this specific file, we will plot technology vs. a chosen economic metric.
    
    col1, col2 = st.columns(2)
    with col1:
        tech_metric = st.selectbox("Select Tech Metric", [internet_col, mobile_col])
    with col2:
        # Example metric: Unemployment or Employment in Agriculture (often a target for Kiva)
        impact_metric = st.selectbox("Select Impact Metric", 
            ['Employment: Agriculture (% of employed)', 'Unemployment (% of labour force)'])
            
    plot_data_kiva = df_kiva.dropna(subset=[tech_metric, impact_metric])
    
    fig2 = px.scatter(
        plot_data_kiva, x=tech_metric, y=impact_metric,
        hover_name="country", size="Population in thousands (2017)",
        color="Region",
        title=f"Kiva Countries: {tech_metric} vs {impact_metric}"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- REPORT GENERATION ---
    st.markdown("---")
    st.subheader("Export Findings")
    desc = [
        "Analysis of Microfinance Impact.",
        f"Comparing '{tech_metric}' vs '{impact_metric}' across Kiva countries."
    ]
    with st.spinner("Preparing Report..."):
        pdf_bytes = generate_cached_report("Microfinance Impact Report", desc, [fig2])
    st.download_button(label="📄 Download PDF Report", data=pdf_bytes, file_name="microfinance_impact_report.pdf", mime="application/pdf")

# ==========================================
# PAGE 3: COUNTRY COMPARISON
# ==========================================
elif page == "Country Comparison":
    st.header("3. Side-by-Side Country Comparison")
    
    countries = df_country['country'].dropna().unique()
    
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Select Country 1", countries, index=0)
    with col2:
        country2 = st.selectbox("Select Country 2", countries, index=1)
        
    # Filter data for selected countries
    c1_data = df_country[df_country['country'] == country1].iloc[0]
    c2_data = df_country[df_country['country'] == country2].iloc[0]
    
    # Display comparison metrics
    st.subheader("Key Metrics Comparison")
    
    metrics_to_compare = [
        'GDP per capita (current US$)',
        'Life expectancy at birth (females/males, years)',
        'Urban population (% of total population)',
        'Unemployment (% of labour force)'
    ]
    
    # Create an elegant table/dataframe for comparison
    comp_df = pd.DataFrame({
        "Metric": metrics_to_compare,
        country1: [c1_data[m] for m in metrics_to_compare],
        country2: [c2_data[m] for m in metrics_to_compare]
    })
    
    st.table(comp_df.set_index("Metric"))
    
    # Radar Chart for Economy Breakdown
    st.subheader("Economy Structure Comparison")
    categories = ['Economy: Agriculture (% of GVA)', 'Economy: Industry (% of GVA)', 'Economy: Services and other activity (% of GVA)']
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[c1_data[cat] for cat in categories],
        theta=['Agriculture', 'Industry', 'Services'],
        fill='toself',
        name=country1
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[c2_data[cat] for cat in categories],
        theta=['Agriculture', 'Industry', 'Services'],
        fill='toself',
        name=country2
    ))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(fig_radar)

    # --- REPORT GENERATION ---
    st.markdown("---")
    st.subheader("Export Findings")
    desc = [
        f"Country Comparison between {country1} and {country2}.",
        "The table provides key metrics comparison, and the radar chart shows the breakdown of the economy structure."
    ]
    with st.spinner("Preparing Report..."):
        # comp_df.set_index("Metric") gives a nice df where Metric is the index
        pdf_bytes = generate_cached_report("Country Comparison Report", desc, [fig_radar], dataframe=comp_df.set_index("Metric"))
    st.download_button(label="📄 Download PDF Report", data=pdf_bytes, file_name="country_comparison_report.pdf", mime="application/pdf")
