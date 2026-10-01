import streamlit as st

st.set_page_config(
    page_title="Bank Marketing Intelligence Hub",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Bank Marketing Campaign Intelligence Hub")
st.markdown("""
Welcome to the **Bank Marketing Campaign Analysis** dashboard.

Use the sidebar on the left to navigate between the pages:

- **Home** → Data overview & cleaning audit  
- **Base KPIs** → Interactive filters and performance metrics  
- **AI Assistant** → Bilingual AI chat (English + Egyptian Arabic)
""")

st.info("👈 Select a page from the sidebar to get started.")