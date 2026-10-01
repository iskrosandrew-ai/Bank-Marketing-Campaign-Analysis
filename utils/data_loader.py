import pandas as pd
import numpy as np
import streamlit as st

DATA_PATH = "cleaned_banking_marketing.csv"

@st.cache_data(show_spinner=False)
def load_data():
    """Load and prepare the cleaned banking marketing dataset."""
    df = pd.read_csv(DATA_PATH)
    
    # Ensure correct categorical datatypes
    cat_cols = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'month', 'poutcome', 'y', 'age_group']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
            
    # Ensure correct integer datatypes
    int_cols = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous', 'is_previously_contacted']
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype('int64')
            
    return df

@st.cache_data(show_spinner=False)
def get_dataset_benchmarks(df):
    """Compute overall baseline metrics for delta comparisons."""
    total_clients = len(df)
    subscribed_count = (df['y'] == 'yes').sum()
    conversion_rate = (subscribed_count / total_clients * 100) if total_clients > 0 else 0
    avg_balance = df['balance'].mean()
    median_duration = df['duration'].median()
    avg_campaign = df['campaign'].mean()
    
    prior_clients = df[df['pdays'] != -1]
    prior_success_rate = (
        (prior_clients['y'] == 'yes').sum() / len(prior_clients) * 100
    ) if len(prior_clients) > 0 else 0
    
    return {
        'total_clients': total_clients,
        'subscribed_count': subscribed_count,
        'conversion_rate': conversion_rate,
        'avg_balance': avg_balance,
        'median_duration': median_duration,
        'avg_campaign': avg_campaign,
        'prior_success_rate': prior_success_rate
    }
