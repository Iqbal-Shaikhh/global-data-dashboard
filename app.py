import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import report_generator

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Global Data Dashboard", layout="wide")
st.title("Global Socio-Economic & Microfinance Dashboard")

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    df_country = pd.read_csv('country_profile_variables.csv')
    df_kiva = pd.read_csv('kiva_country_profile_variables.csv')
    
    # Clean '-99' which represent missing values
    df_country = df_country.replace([-99, '-99', -99.0], np.nan)
    df_kiva = df_kiva.replace([-99, '-99', -99.0], np.nan)
    
    return df_country, df_kiva

df_country, df_kiva = load_data()

# Column Variables
gdp_col = 'GDP growth rate (annual %, const. 2005 prices)'
health_col = 'Health: Total expenditure (% of GDP)'
edu_col = 'Education: Government expenditure (% of GDP)'
internet_col = 'Individuals using the Internet (per 100 inhabitants)'
mobile_col = 'Mobile-cellular subscriptions (per 100 inhabitants)'

# --- REPORT HELPER ---
@st.cache_data(show_spinner=False)
def generate_cached_report(title, desc, _figures, dataframe=None):
    return report_generator.generate_pdf(title, desc, _figures, dataframe)

# --- SIDEBAR FOR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a View:", 
    ("Socio-Economic Correlations", "Microfinance Impact", "Country Comparison"))

# ==========================================
# PAGE 1: SOCIO-ECONOMIC CORRELATIONS
# ==========================================
if page == "Socio-Economic Correlations":
    st.header("1. Health & Education vs. GDP")
    st.write("Explore how government spending correlates with GDP growth.")
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Select X-Axis", [health_col, edu_col])
    with col2:
        y_axis = st.selectbox("Select Y-Axis", [gdp_col, 'GDP per capita (current US$)'])
        
    plot_data = df_country.dropna(subset=[x_axis, y_axis])
    
    # Styled Scatter Plot
    fig = px.scatter(
        plot_data, x=x_axis, y=y_axis, 
        hover_name="country", color="Region",
        color_discrete_sequence=px.colors.qualitative.Bold,
        trendline="ols", 
        template="plotly_white",
        title=f"Correlation: {x_axis} vs {y_axis}"
    )
    
    # Thicken markers and trendline for better visibility
    fig.update_traces(
        marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')),
        selector=dict(mode='markers')
    )
    fig.update_traces(
        line=dict(dash="dash", width=2, color="black"),
        selector=dict(mode='lines')
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Correlation Heatmap")
    
    # Styled Heatmap
    metrics = [gdp_col, health_col, edu_col, internet_col, 'Life expectancy at birth (females/males, years)']
    numeric_df = df_country[metrics].apply(pd.to_numeric, errors='coerce')
    corr_matrix = numeric_df.corr()
    
    fig_corr = px.imshow(
        corr_matrix, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        template="plotly_white", title="Socio-Economic Correlation Matrix"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # PDF Report Generation Button
    st.markdown("---")
    st.subheader("Export Findings")
    if st.button("Generate PDF Report"):
        with st.spinner("Preparing Report... This takes a few seconds..."):
            desc = [
                f"This report explores the relationship between {x_axis} and {y_axis}.",
                "The correlation matrix highlights how macro-indicators interact globally."
            ]
            pdf_bytes = generate_cached_report("Socio-Economic Report", desc, [fig, fig_corr])
            
            st.download_button(
                label="📄 Download PDF Report", 
                data=pdf_bytes, 
                file_name="socio_economic_report.pdf", 
                mime="application/pdf"
            )

# ==========================================
# PAGE 2: MICROFINANCE IMPACT
# ==========================================
elif page == "Microfinance Impact":
    st.header("2. Technology Access and Microfinance")
    st.write("Explore how internet or mobile penetration correlates with employment metrics.")
    
    col1, col2 = st.columns(2)
    with col1:
        tech_metric = st.selectbox("Select Tech Metric", [internet_col, mobile_col])
    with col2:
        impact_metric = st.selectbox("Select Impact Metric", 
            ['Employment: Agriculture (% of employed)', 'Unemployment (% of labour force)'])
            
    plot_data_kiva = df_kiva.dropna(subset=[tech_metric, impact_metric])
    
    fig2 = px.scatter(
        plot_data_kiva, x=tech_metric, y=impact_metric,
        hover_name="country", size="Population in thousands (2017)",
        color="Region", color_discrete_sequence=px.colors.qualitative.Prism,
        template="plotly_white",
        title=f"Kiva Countries: {tech_metric} vs {impact_metric}"
    )
    fig2.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    st.plotly_chart(fig2, use_container_width=True)

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
        country2 = st.selectbox("Select Country 2", countries, index=min(1, len(countries)-1))
        
    c1_data = df_country[df_country['country'] == country1].iloc[0]
    c2_data = df_country[df_country['country'] == country2].iloc[0]
    
    st.subheader("Key Metrics Comparison")
    metrics_to_compare = [
        'GDP per capita (current US$)',
        'Life expectancy at birth (females/males, years)',
        'Urban population (% of total population)',
        'Unemployment (% of labour force)'
    ]
    
    comp_df = pd.DataFrame({
        "Metric": metrics_to_compare,
        country1: [c1_data[m] for m in metrics_to_compare],
        country2: [c2_data[m] for m in metrics_to_compare]
    })
    st.table(comp_df.set_index("Metric"))
    
    st.subheader("Economy Structure Comparison")
    categories = ['Economy: Agriculture (% of GVA)', 'Economy: Industry (% of GVA)', 'Economy: Services and other activity (% of GVA)']
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[c1_data[cat] for cat in categories], theta=['Agriculture', 'Industry', 'Services'], fill='toself', name=country1))
    fig_radar.add_trace(go.Scatterpolar(r=[c2_data[cat] for cat in categories], theta=['Agriculture', 'Industry', 'Services'], fill='toself', name=country2))
    
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, template="plotly_white")
    st.plotly_chart(fig_radar, use_container_width=True)
