import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data, get_dataset_benchmarks
from utils.footer import render_footer

# Page Configuration
st.set_page_config(
    page_title="Bank Marketing Intelligence | Home",
    page_icon="🏦",
    layout="wide"
)

# Custom High-End Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F766E 100%);
        padding: 2.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        font-weight: 300;
        max-width: 850px;
        line-height: 1.6;
    }
    
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #06B6D4;
    }
    
    .metric-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #38BDF8;
        margin-bottom: 0.2rem;
    }
    
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8;
        font-weight: 600;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: rgba(6, 182, 212, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_data()
benchmarks = get_dataset_benchmarks(df)

# Hero Header
st.markdown("""
<div class="hero-container">
    <span class="badge">🚀 DIRECT TELEMARKETING INTELLIGENCE</span>
    <div class="hero-title">Bank Marketing Campaign Intelligence Hub</div>
    <div class="hero-subtitle">
        An interactive, end-to-end data analytics platform exploring customer deposit subscriptions from direct telemarketing campaigns. 
        Engineered with clean schemas, domain validation, strict outlier filtering, and interactive Plotly intelligence.
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# ESSAY SECTION: BACKGROUND, STORY & PROJECT AIM
# ----------------------------------------------------
with st.container():
    st.markdown("""
    ### 📖 The Story Behind the Data: Background, Business Challenge & Mission
    
    ##### 1. What is this dataset about?
    Imagine you are leading the retail marketing operations at a major bank. Your institution's goal is to encourage clients to invest their savings in a **Term Deposit** (a secure, fixed-term savings account that pays guaranteed interest). Because term deposits provide banks with dependable, long-term capital to fund loans and economic investments, growing this deposit base is a top priority.
    
    To win these deposits, the bank ran direct telemarketing campaigns where customer representatives contacted tens of thousands of individual account holders over the phone. For every customer contacted, the bank recorded detailed information across three key areas:
    * **Personal Profile:** Who is the customer? (Their age, job role, marital status, and education level—such as having a **University Degree**, **High School**, or **Elementary** education).
    * **Financial Health:** How much money do they keep in their account (**Average Yearly Balance**)? Do they already carry a **Home Mortgage Loan** or a **Personal Loan**?
    * **Call Engagement:** How long did the phone conversation last (**Call Duration**)? How many times was the customer called (**Contact Frequency**)? Did they respond positively to past promotions?
    * **The Result:** Did the customer agree to open the term deposit (**"Yes"**), or did they decline (**"No"**)?
    
    ---
    
    ##### 2. The Core Business Challenge
    Direct phone outreach is expensive and labor-intensive. If agents simply dial numbers at random:
    * Over **88% of calls result in rejection**, burning valuable agent hours and increasing marketing costs.
    * Calling prospects repeatedly leads to **"Marketing Fatigue"**, where frustrated clients reject offers they might otherwise have considered.
    * Marketing budget is wasted targeting individuals with zero disposable savings (e.g., those already struggling with heavy mortgage debt).
    
    ---
    
    ##### 3. The Aim of this Project & Analytics Dashboard
    The overarching aim of this project is to transform raw call logs into **actionable marketing strategy**:
    1. **Smarter Targeting:** Identify the ideal customer personas (for instance, university graduates and debt-free clients convert at more than double the rate of other groups).
    2. **Operational Efficiency:** Discover operational rules of thumb—such as the critical call duration threshold (conversations extending past 4 minutes are over **8 times more likely to convert**) and setting contact caps to prevent client burnout.
    3. **Executive Empowerment:** Provide a modern, interactive dashboard with easy-to-use filters and a bilingual AI assistant so business leaders can query data in plain language (English or Egyptian Arabic) and make data-driven decisions instantly.
    """)
    st.write("---")

# Top Metrics Row
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{benchmarks['total_clients']:,}</div>
        <div class="metric-label">Clean Customer Profiles</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{benchmarks['conversion_rate']:.2f}%</div>
        <div class="metric-label">Deposit Conversion Rate</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">€{df['balance'].sum():,.0f}</div>
        <div class="metric-label">Total Liquid Capital</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(df.columns)}</div>
        <div class="metric-label">Active Analytical Features</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Interactive Data Explorer", "📊 Dynamic Feature Peek", "🛠️ Data Engineering & Cleaning Audit"])

# TAB 1: Data Explorer
with tab1:
    st.subheader("Interactive Dataset Exploration")
    st.markdown("Filter, sort, search, and download the validated dataset records.")
    
    col_filter, row_filter = st.columns([3, 1])
    with col_filter:
        selected_cols = st.multiselect(
            "Select Columns to Display:",
            options=list(df.columns),
            default=['age', 'age_group', 'job', 'education', 'balance', 'housing', 'duration', 'campaign', 'poutcome', 'y']
        )
    with row_filter:
        n_rows = st.slider("Records to display:", min_value=10, max_value=200, value=25, step=10)
        
    st.dataframe(
        df[selected_cols].head(n_rows),
        use_container_width=True,
        hide_index=True
    )
    
    # Download Button
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=csv_bytes,
        file_name="cleaned_banking_marketing.csv",
        mime="text/csv",
        help="Download the complete 34,625 clean records with engineered features."
    )

# TAB 2: Dynamic Feature Peek
with tab2:
    st.subheader("Dynamic Feature Distribution Peek")
    st.markdown("Select any attribute from the dropdown to instantly render its interactive distribution.")
    
    col_feat, col_hue = st.columns(2)
    with col_feat:
        feature = st.selectbox(
            "Select Feature to Visualize:",
            options=[c for c in df.columns if c != 'y'],
            index=list(df.columns).index('age_group') if 'age_group' in df.columns else 0
        )
    with col_hue:
        hue = st.radio("Segment by Subscription Target (y)?", options=["Yes", "No"], horizontal=True)
        
    if pd.api.types.is_numeric_dtype(df[feature]) and df[feature].nunique() > 10:
        # Numeric Histogram / Box
        fig_feat = px.histogram(
            df,
            x=feature,
            color='y' if hue == 'Yes' else None,
            barmode='overlay',
            nbins=35,
            title=f"<b>Interactive Distribution of {feature.title()}</b>",
            color_discrete_map={'yes': '#00CC96', 'no': '#EF553B'} if hue == 'Yes' else None,
            opacity=0.75
        )
    else:
        # Categorical Bar Chart
        if hue == 'Yes':
            grouped_feat = df.groupby([feature, 'y'], observed=False).size().reset_index(name='Count')
            fig_feat = px.bar(
                grouped_feat,
                x=feature,
                y='Count',
                color='y',
                barmode='group',
                title=f"<b>Breakdown of {feature.title()} by Subscription (y)</b>",
                color_discrete_map={'yes': '#00CC96', 'no': '#EF553B'}
            )
        else:
            grouped_feat = df[feature].value_counts().reset_index()
            grouped_feat.columns = [feature, 'Count']
            fig_feat = px.bar(
                grouped_feat,
                x=feature,
                y='Count',
                title=f"<b>Frequency Distribution of {feature.title()}</b>",
                color='Count',
                color_continuous_scale='Blues'
            )
            
    fig_feat.update_layout(title_x=0.5, height=480)
    st.plotly_chart(fig_feat, use_container_width=True)

# TAB 3: Data Cleaning & Pipeline Audit
with tab3:
    st.subheader("Data Cleaning & Transformation Audit")
    
    audit_col1, audit_col2, audit_col3 = st.columns(3)
    with audit_col1:
        st.info("🎯 **Feature Pruning**\n\n• Dropped operational noise columns `day` and `contact`.\n• Retained demographic, financial, and campaign response metrics.")
    with audit_col2:
        st.success("✨ **Imputation Strategy**\n\n• Numerical nulls (`age`, `balance`, `duration`): Imputed with **Median**.\n• Categorical nulls (`job`, `education`, etc.): Imputed with **Mode**.")
    with audit_col3:
        st.warning("🛡️ **Strict Outlier Treatment**\n\n• Domain bounds: `18 <= age <= 100`, `campaign >= 1`.\n• Strict IQR row filtering applied on continuous features, preserving 76.6% clean data.")
        
    # Before vs After Comparison Summary Table
    comparison_data = pd.DataFrame({
        "Metric / Property": [
            "Total Records",
            "Columns Count",
            "Missing Values Remaining",
            "Duplicate Rows",
            "Age Format",
            "Balance Format",
            "Engineered Features"
        ],
        "Raw Dataset (banking.marketing.csv)": [
            "45,211",
            "17",
            "5,914 across 9 columns",
            "0",
            "Floats (e.g. 58.0) with errors (0, 150)",
            "Floats (e.g. 2143.0)",
            "None"
        ],
        "Cleaned Dataset (cleaned_banking_marketing.csv)": [
            "34,625",
            "17 (with engineered columns)",
            "0 (100% complete)",
            "0",
            "Clean Integers (18 to 70)",
            "Clean Integers (€)",
            "age_group, is_previously_contacted"
        ]
    })
    st.table(comparison_data)

# ── Footer ──
render_footer()
