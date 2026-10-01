import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_data, get_dataset_benchmarks
from utils.footer import render_footer

st.set_page_config(
    page_title="Executive KPIs & Performance | Bank Marketing",
    page_icon="📈",
    layout="wide"
)

# Custom High-End Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .kpi-container {
        background: #1E293B;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    .kpi-number {
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    
    .kpi-delta-pos {
        font-size: 0.85rem;
        font-weight: 600;
        color: #10B981;
    }
    
    .kpi-delta-neg {
        font-size: 0.85rem;
        font-weight: 600;
        color: #EF4444;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #06B6D4;
        padding-left: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

df = load_data()
benchmarks = get_dataset_benchmarks(df)

# Header
st.title("📈 Executive Marketing KPIs & Performance")
st.markdown("Slice and drill into customer segments with dynamic multi-dimensional filters to evaluate conversion drivers.")

# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------
st.sidebar.header("🎯 Segment Filter Controls")

# Reset button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# 1. Age Range
min_age = int(df['age'].min())
max_age = int(df['age'].max())
selected_age = st.sidebar.slider("Client Age Range:", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# 2. Job Professions
all_jobs = sorted(list(df['job'].unique()))
selected_jobs = st.sidebar.multiselect("Job Professions:", options=all_jobs, default=all_jobs, format_func=lambda x: x.title())

# 3. Education Levels (Simplified Human-Friendly Terms)
edu_map = {
    'tertiary': 'University Degree (Tertiary)',
    'secondary': 'High School (Secondary)',
    'primary': 'Elementary School (Primary)',
    'unknown': 'Not Specified'
}
all_edu = sorted(list(df['education'].unique()))
selected_edu = st.sidebar.multiselect(
    "Education Level:",
    options=all_edu,
    default=all_edu,
    format_func=lambda x: edu_map.get(x, x.title())
)

# 4. Marital Status
all_marital = sorted(list(df['marital'].unique()))
selected_marital = st.sidebar.multiselect("Marital Status:", options=all_marital, default=all_marital, format_func=lambda x: x.title())

# 5. Home Loan (Mortgage)
housing_filter = st.sidebar.radio("Home Mortgage Loan:", options=["All", "Yes", "No"], horizontal=True)

# 6. Personal Loan
loan_filter = st.sidebar.radio("Personal Loan:", options=["All", "Yes", "No"], horizontal=True)

# 7. Campaign Month
all_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
avail_months = [m for m in all_months if m in df['month'].unique()]
selected_months = st.sidebar.multiselect("Contact Months:", options=avail_months, default=avail_months)

# Apply Filters
filtered_df = df[
    (df['age'] >= selected_age[0]) & (df['age'] <= selected_age[1]) &
    (df['job'].isin(selected_jobs)) &
    (df['education'].isin(selected_edu)) &
    (df['marital'].isin(selected_marital)) &
    (df['month'].isin(selected_months))
]

if housing_filter != "All":
    filtered_df = filtered_df[filtered_df['housing'] == housing_filter.lower()]

if loan_filter != "All":
    filtered_df = filtered_df[filtered_df['loan'] == loan_filter.lower()]

# Check empty slice
if len(filtered_df) == 0:
    st.warning("⚠️ No records match the selected filter combination. Please broaden your filter criteria.")
    st.stop()

# ----------------------------------------------------
# COMPUTE FILTERED KPIS
# ----------------------------------------------------
n_filtered = len(filtered_df)
pct_of_total = (n_filtered / len(df)) * 100
sub_filtered = (filtered_df['y'] == 'yes').sum()
conv_rate_filtered = (sub_filtered / n_filtered * 100) if n_filtered > 0 else 0
delta_conv = conv_rate_filtered - benchmarks['conversion_rate']

avg_bal_filtered = filtered_df['balance'].mean()
delta_bal = avg_bal_filtered - benchmarks['avg_balance']

med_dur_filtered = filtered_df['duration'].median()
delta_dur = med_dur_filtered - benchmarks['median_duration']

avg_camp_filtered = filtered_df['campaign'].mean()
delta_camp = avg_camp_filtered - benchmarks['avg_campaign']

prior_filtered = filtered_df[filtered_df['pdays'] != -1]
prior_conv = (
    (prior_filtered['y'] == 'yes').sum() / len(prior_filtered) * 100
) if len(prior_filtered) > 0 else 0

# ----------------------------------------------------
# KPI CARDS ROW
# ----------------------------------------------------
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Selected Cohort</div>
        <div class="kpi-number">{n_filtered:,}</div>
        <div class="kpi-delta-pos">{pct_of_total:.1f}% of total base</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    delta_class = "kpi-delta-pos" if delta_conv >= 0 else "kpi-delta-neg"
    sign = "+" if delta_conv >= 0 else ""
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Conversion Rate</div>
        <div class="kpi-number">{conv_rate_filtered:.2f}%</div>
        <div class="{delta_class}">{sign}{delta_conv:.2f}% vs baseline</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    delta_class = "kpi-delta-pos" if delta_bal >= 0 else "kpi-delta-neg"
    sign = "+" if delta_bal >= 0 else ""
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Average Balance</div>
        <div class="kpi-number">€{avg_bal_filtered:,.0f}</div>
        <div class="{delta_class}">{sign}€{delta_bal:,.0f} vs baseline</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    delta_class = "kpi-delta-pos" if delta_dur >= 0 else "kpi-delta-neg"
    sign = "+" if delta_dur >= 0 else ""
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Median Call Length</div>
        <div class="kpi-number">{med_dur_filtered:.0f}s</div>
        <div class="{delta_class}">{sign}{delta_dur:.0f}s vs baseline</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Prior Success Rate</div>
        <div class="kpi-number">{prior_conv:.1f}%</div>
        <div class="kpi-delta-pos">{len(prior_filtered):,} warm leads</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------
# VISUAL ANALYTICS ROW 1
# ----------------------------------------------------
st.markdown('<div class="section-header">Customer Segment Response & Conversion Performance</div>', unsafe_allow_html=True)

v1, v2 = st.columns([1.2, 1.8])

with v1:
    # Gauge / Donut Conversion Chart
    sub_counts = filtered_df['y'].value_counts()
    fig_donut = px.pie(
        names=sub_counts.index,
        values=sub_counts.values,
        title='<b>Cohort Subscription Split</b>',
        color=sub_counts.index,
        color_discrete_map={'yes': '#00CC96', 'no': '#EF553B'},
        hole=0.55
    )
    fig_donut.update_traces(textinfo='percent+label', textfont_size=13, pull=[0.05, 0])
    fig_donut.update_layout(title_x=0.5, height=390, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_donut, use_container_width=True)

with v2:
    # Job Conversion Rate & Average Balance
    job_cohort = filtered_df.groupby('job', observed=False).agg(
        Total=('y', 'count'),
        Subscribed=('y', lambda x: (x == 'yes').sum()),
        Avg_Balance=('balance', 'mean')
    ).reset_index()
    job_cohort['Conversion_Rate_%'] = (job_cohort['Subscribed'] / job_cohort['Total'] * 100).round(2)
    job_cohort = job_cohort.sort_values(by='Conversion_Rate_%', ascending=True)

    fig_job = px.bar(
        job_cohort,
        x='Conversion_Rate_%',
        y='job',
        orientation='h',
        text='Conversion_Rate_%',
        title='<b>Conversion Rate (%) by Profession in Filtered Cohort</b>',
        labels={'Conversion_Rate_%': 'Conversion Rate (%)', 'job': 'Profession'},
        color='Conversion_Rate_%',
        color_continuous_scale='Tealgrn'
    )
    fig_job.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_job.update_layout(title_x=0.5, height=390, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_job, use_container_width=True)

# ----------------------------------------------------
# VISUAL ANALYTICS ROW 2
# ----------------------------------------------------
st.markdown('<div class="section-header">Campaign Efficiency & Marketing Fatigue Analysis</div>', unsafe_allow_html=True)

v3, v4 = st.columns(2)

with v3:
    # Fatigue curve
    camp_cohort = filtered_df.groupby('campaign')['y'].agg(
        Total='count',
        Subscribed=lambda x: (x == 'yes').sum()
    ).reset_index()
    camp_cohort['Conversion_Rate_%'] = (camp_cohort['Subscribed'] / camp_cohort['Total'] * 100).round(2)
    
    fig_camp = px.line(
        camp_cohort,
        x='campaign',
        y='Conversion_Rate_%',
        markers=True,
        text='Conversion_Rate_%',
        title='<b>Contact Frequency vs Conversion (Marketing Fatigue)</b>',
        labels={'campaign': 'Contacts During Campaign', 'Conversion_Rate_%': 'Conversion Rate (%)'},
        color_discrete_sequence=['#FF7F0E']
    )
    fig_camp.update_traces(textposition='top center')
    fig_camp.update_layout(title_x=0.5, height=380, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_camp, use_container_width=True)

with v4:
    # Call Duration Violin
    fig_dur = px.violin(
        filtered_df,
        x='y',
        y='duration',
        color='y',
        box=True,
        points=False,
        title='<b>Call Duration Distribution by Subscription Status (Seconds)</b>',
        labels={'y': 'Subscribed (y)', 'duration': 'Call Duration (sec)'},
        color_discrete_map={'yes': '#00CC96', 'no': '#FFA15A'}
    )
    fig_dur.update_layout(title_x=0.5, height=380, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig_dur, use_container_width=True)

# ----------------------------------------------------
# VISUAL ANALYTICS ROW 3: SEASONALITY
# ----------------------------------------------------
st.markdown('<div class="section-header">Monthly Campaign Seasonality Trend</div>', unsafe_allow_html=True)

month_stats = filtered_df.groupby('month', observed=False)['y'].agg(
    Total='count',
    Subscribed=lambda x: (x == 'yes').sum()
).reindex(all_months).dropna().reset_index()

month_stats['Conversion_Rate_%'] = (month_stats['Subscribed'] / month_stats['Total'] * 100).round(2)

fig_season = make_subplots(specs=[[{"secondary_y": True}]])

fig_season.add_trace(
    go.Bar(x=month_stats['month'], y=month_stats['Total'], name='Call Volume', marker_color='#64748B'),
    secondary_y=False
)

fig_season.add_trace(
    go.Scatter(x=month_stats['month'], y=month_stats['Conversion_Rate_%'], name='Conversion Rate (%)',
               mode='lines+markers+text', text=month_stats['Conversion_Rate_%'].round(1),
               textposition='top center', line=dict(color='#10B981', width=3)),
    secondary_y=True
)

fig_season.update_layout(
    title='<b>Monthly Call Volume vs Conversion Rate in Current Selection</b>',
    title_x=0.5,
    height=400,
    legend=dict(x=0.8, y=1.1, orientation='h'),
    margin=dict(l=10, r=10, t=50, b=10)
)
fig_season.update_yaxes(title_text="Total Contacts", secondary_y=False)
fig_season.update_yaxes(title_text="Conversion Rate (%)", secondary_y=True)
st.plotly_chart(fig_season, use_container_width=True)
