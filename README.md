# 🏦 Bank Marketing Campaign Intelligence Hub

**Interactive Streamlit Dashboard + Bilingual AI Assistant**  
**Author:** Andrew Iskros  
**Project Type:** AI Diploma Capstone – Data Science & Machine Learning  
**Dataset:** UCI Bank Marketing Dataset (Portuguese banking institution)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Project Overview

This project transforms raw telemarketing call logs from a Portuguese bank into an **executive-grade interactive analytics platform**.

The bank ran phone campaigns to sell **Term Deposits**. Out of ~45,000 contacts, the conversion rate was only ~11%. The goal of this project is to answer:

> **Which customers should the bank call next, and how should agents talk to them to maximize subscriptions while minimizing cost and customer fatigue?**

### Key Deliverables
| Component | Description |
|-----------|-------------|
| **Cleaned Dataset** | 34,625 high-quality records after rigorous cleaning |
| **Jupyter Notebooks** | Full EDA + Data Engineering pipeline |
| **Streamlit Multi-Page App** | Professional dashboard with filters, KPIs & visualizations |
| **Bilingual AI Assistant** | Chat + Voice (English + Egyptian Arabic) that generates live Plotly charts |

---

## 🗂️ Repository Structure

---

## 🧹 Data Engineering Pipeline

### Raw → Clean Transformation

| Metric                        | Raw Dataset              | Cleaned Dataset              |
|-------------------------------|--------------------------|------------------------------|
| Total Records                 | 45,211                   | **34,625**                   |
| Columns                       | 17                       | 17 (with engineered features)|
| Missing Values                | 5,914 across 9 columns   | **0**                        |
| Duplicate Rows                | 0                        | 0                            |
| Age range                     | 0 – 150 (errors)         | **18 – 70**                  |
| Engineered Features           | None                     | `age_group`, `is_previously_contacted` |

### Cleaning Steps Applied
1. **Feature Pruning** → Dropped `day` and `contact` (operational noise)
2. **Imputation**
   - Numerical (`age`, `balance`, `duration`) → **Median**
   - Categorical (`job`, `education`, etc.) → **Mode**
3. **Domain Validation**
   - Age between 18–100
   - Campaign contacts ≥ 1
4. **Strict IQR Outlier Filtering** on continuous features
5. **Feature Engineering**
   - `age_group`: `<30 | 30-39 | 40-49 | 50-59 | 60+`
   - `is_previously_contacted`: binary flag from `pdays`

---

## Streamlit Application Features

### 1. Home & Data Overview (`1_Home.py`)
- Beautiful hero section explaining the business problem
- Top-level KPIs (Total clients, Conversion Rate, Total Liquid Capital)
- Interactive Data Explorer with column selector & download
- Dynamic Feature Distribution Peek
- Full Data Cleaning Audit table

### 2. Executive KPIs & Analytics (`2_Base_KPIs.py`)
**Sidebar Filters:**
- Age range
- Job professions
- Education level
- Marital status
- Housing loan / Personal loan
- Campaign months

**Live Metrics (with delta vs baseline):**
- Selected Cohort size
- Conversion Rate
- Average Balance
- Median Call Duration
- Prior Success Rate (warm leads)

**Visualizations:**
- Subscription donut chart
- Conversion Rate by Profession (horizontal bar)
- Marketing Fatigue curve (Contact Frequency vs Conversion)
- Call Duration Violin plot by Subscription
- Monthly Seasonality (Call Volume + Conversion Rate)

### 3. AI Marketing Intelligence Assistant (`3_AI_Assistant.py`)
- **Bilingual** support: English + Egyptian Arabic
- **Voice input** via microphone (Google Speech Recognition)
- Smart ambiguity detection → asks clarifying questions
- Generates **live interactive Plotly charts** for:
  - Call duration impact
  - Job / Profession conversion
  - Age cohorts
  - Housing & Personal loans
  - Previous campaign outcome (`poutcome`)
  - Marketing fatigue
  - Education level

---

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/iskrosandrew-ai/Bank-Marketing-Campaign-Analysis.git
cd Bank-Marketing-Campaign-Analysis
