import streamlit as st

# Main Application Entrypoint with Multi-Page Navigation
home_page = st.Page("pages/1_Home.py", title="Home & Data Overview", icon="🏠", default=True)
kpis_page = st.Page("pages/2_Base_KPIs.py", title="Base KPIs & Analytics", icon="📈")
assistant_page = st.Page("pages/3_AI_Assistant.py", title="AI Marketing Assistant", icon="🤖")

pg = st.navigation({
    "Navigation": [home_page, kpis_page, assistant_page]
})

pg.run()
