"""
app.py  —  Retail Data Storytelling Dashboard
==============================================
A production-grade Streamlit application that guides the user through a
5-step narrative journey: Introduction → EDA → Visual Storytelling →
Insights & Findings → Conclusion.

Author : Retail BI Team
Version: 1.0.0
Run    : streamlit run app.py
"""

from __future__ import annotations

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from pathlib import Path

import insights as ins  # local module

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Retail Story | BI Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
/* ── Google Fonts ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ─────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #1a1a2e;
}

/* ── Hero Sections ────────────────────────────── */
.hero-main {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-main::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-main h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem;
    line-height: 1.15;
}
.hero-main p { color: rgba(255,255,255,0.75); font-size: 1.1rem; margin: 0; }

.hero-section {
    background: linear-gradient(120deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.8rem;
    border-left: 5px solid #e94560;
}
.hero-section h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.4rem;
}
.hero-section p { color: rgba(255,255,255,0.7); margin: 0; font-size: 0.95rem; }

/* ── KPI Cards ────────────────────────────────── */
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.6rem 1.4rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-top: 4px solid;
    text-align: center;
    transition: transform 0.2s;
}
.kpi-card:hover { transform: translateY(-4px); }
.kpi-label { font-size: 0.78rem; font-weight: 500; text-transform: uppercase;
             letter-spacing: 0.08em; color: #6b7280; margin-bottom: 0.5rem; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 2rem;
             font-weight: 700; color: #1a1a2e; line-height: 1; }
.kpi-sub   { font-size: 0.78rem; color: #9ca3af; margin-top: 0.3rem; }

/* ── Insight Cards ────────────────────────────── */
.insight-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-left: 4px solid;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
}
.insight-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.12); }
.insight-title { font-family: 'Syne', sans-serif; font-weight: 700;
                 font-size: 0.95rem; margin-bottom: 0.25rem; }
.insight-value { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.2rem; }
.insight-desc  { font-size: 0.82rem; color: #6b7280; line-height: 1.4; }

/* ── Finding Cards ────────────────────────────── */
.finding-card {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid #e2e8f0;
    position: relative;
}
.finding-number {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #e2e8f0;
    position: absolute;
    top: 1rem; right: 1.5rem;
    line-height: 1;
}
.finding-title { font-family: 'Syne', sans-serif; font-size: 1.1rem;
                 font-weight: 700; color: #1a1a2e; margin-bottom: 0.5rem; }
.finding-detail { font-size: 0.88rem; color: #475569; line-height: 1.6; }
.badge-critical { background:#fee2e2; color:#dc2626; padding:2px 10px;
                  border-radius:20px; font-size:0.72rem; font-weight:600; }
.badge-high     { background:#fef3c7; color:#d97706; padding:2px 10px;
                  border-radius:20px; font-size:0.72rem; font-weight:600; }
.badge-medium   { background:#dbeafe; color:#2563eb; padding:2px 10px;
                  border-radius:20px; font-size:0.72rem; font-weight:600; }

/* ── Recommendation Cards ─────────────────────── */
.rec-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 3px 15px rgba(0,0,0,0.07);
    margin-bottom: 1.1rem;
    border-right: 4px solid #0f3460;
}
.rec-header { display:flex; justify-content:space-between; align-items:center;
               margin-bottom:0.5rem; }
.rec-num   { font-family:'Syne',sans-serif; font-weight:800; font-size:1.1rem;
              color:#0f3460; }
.rec-title { font-family:'Syne',sans-serif; font-weight:700; font-size:1rem;
              color:#1a1a2e; margin-bottom:0.4rem; }
.rec-detail{ font-size:0.85rem; color:#475569; line-height:1.6; }
.rec-meta  { font-size:0.75rem; color:#9ca3af; margin-top:0.4rem; }

/* ── Score Cards ──────────────────────────────── */
.score-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.score-grade { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800;
               width:3rem; text-align:center; }
.score-info  { flex:1; }
.score-name  { font-weight:600; font-size:0.92rem; color:#1a1a2e; }
.score-bar-wrap { background:#f1f5f9; border-radius:20px; height:8px;
                   margin-top:0.3rem; overflow:hidden; }
.score-bar   { height:8px; border-radius:20px; transition:width 0.6s; }
.score-num   { font-family:'Syne',sans-serif; font-weight:700; font-size:1.1rem;
                min-width:3rem; text-align:right; }

/* ── Section Dividers ─────────────────────────── */
.step-badge {
    display: inline-block;
    background: linear-gradient(90deg, #e94560, #0f3460);
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 16px;
    border-radius: 20px;
    margin-bottom: 0.6rem;
}

/* ── Sidebar ──────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: rgba(255,255,255,0.7) !important; font-size:0.82rem; }

/* ── DataFrames ───────────────────────────────── */
.dataframe { border-radius: 10px !important; }

/* ── Misc ─────────────────────────────────────── */
.divider { border:none; border-top:1px solid #e2e8f0; margin:2rem 0; }
h3 { font-family:'Syne',sans-serif; font-weight:700; color:#1a1a2e; }
.stTabs [data-baseweb="tab"] { font-family:'DM Sans',sans-serif; font-weight:500; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and preprocess the retail dataset."""
    data_path = Path("dataset.csv")
    if not data_path.exists():
        st.error("❌ Dataset not found at data/dataset.csv. Please run generate_data.py first.")
        st.stop()

    df = pd.read_csv(data_path, parse_dates=["order_date", "ship_date"])

    # Ensure derived columns exist
    if "profit_margin" not in df.columns:
        df["profit_margin"] = df["profit"] / df["sales"]
    if "year" not in df.columns:
        df["year"] = df["order_date"].dt.year
    if "month" not in df.columns:
        df["month"] = df["order_date"].dt.month
    if "quarter" not in df.columns:
        df["quarter"] = df["order_date"].dt.quarter
    if "month_name" not in df.columns:
        df["month_name"] = df["order_date"].dt.strftime("%b")

    return df


df_raw = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — FILTERS
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:2.8rem;'>🛍️</div>
        <div style='font-family:Syne,sans-serif; font-size:1.25rem; font-weight:800;
                    color:#fff; line-height:1.2;'>Retail Story</div>
        <div style='font-size:0.78rem; color:rgba(255,255,255,0.5); letter-spacing:0.1em;
                    text-transform:uppercase;'>BI Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔎 Filters")

    # Year
    all_years  = sorted(df_raw["year"].unique())
    sel_years  = st.multiselect("📅 Year", all_years, default=all_years, key="year_filter")

    # Region
    all_regions = sorted(df_raw["region"].unique())
    sel_regions = st.multiselect("🌍 Region", all_regions, default=all_regions, key="region_filter")

    # Category
    all_cats    = sorted(df_raw["category"].unique())
    sel_cats    = st.multiselect("📦 Category", all_cats, default=all_cats, key="cat_filter")

    # Apply filters
    df = df_raw.copy()
    if sel_years:
        df = df[df["year"].isin(sel_years)]
    if sel_regions:
        df = df[df["region"].isin(sel_regions)]
    if sel_cats:
        df = df[df["category"].isin(sel_cats)]

    st.markdown("---")
    st.caption(f"**{len(df):,}** records match filters")

    # Navigation
    st.markdown("### 📑 Navigate")
    STEPS = {
        "🏠 Introduction":        "intro",
        "🔬 Exploratory Analysis": "eda",
        "📊 Visual Storytelling":  "viz",
        "💡 Insights & Findings":  "insights",
        "🏁 Conclusion":           "conclusion",
    }
    step_label = st.radio("", list(STEPS.keys()), label_visibility="collapsed")
    active_step = STEPS[step_label]

# ══════════════════════════════════════════════════════════════════════════════
# COLOUR PALETTE  (consistent across charts)
# ══════════════════════════════════════════════════════════════════════════════

PALETTE = {
    "primary":   "#0f3460",
    "accent":    "#e94560",
    "positive":  "#10b981",
    "warning":   "#f59e0b",
    "cat":       px.colors.qualitative.Bold,
    "seq":       px.colors.sequential.Blues,
    "seq_r":     px.colors.sequential.Blues_r,
    "diverging": px.colors.diverging.RdYlGn,
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def fmt_currency(v: float) -> str:
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:.1f}K"
    return f"${v:.0f}"

def section_header(step_tag: str, title: str, subtitle: str = ""):
    st.markdown(f"<div class='step-badge'>{step_tag}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='hero-section'>
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def chart_defaults(fig: go.Figure, title: str = "", height: int = 420) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=16, color="#1a1a2e"),
                   x=0, xanchor="left"),
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        height=height,
        margin=dict(l=10, r=10, t=45, b=10),
        font=dict(family="DM Sans, sans-serif", size=12, color="#475569"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
    )
    fig.update_xaxes(gridcolor="#e2e8f0", linecolor="#e2e8f0")
    fig.update_yaxes(gridcolor="#e2e8f0", linecolor="#e2e8f0")
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# KPI DASHBOARD (shared component)
# ══════════════════════════════════════════════════════════════════════════════

def render_kpi_dashboard(df: pd.DataFrame):
    kpis = ins.compute_kpis(df)
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "Total Sales",    fmt_currency(kpis["total_sales"]),   "Revenue generated", "#0f3460"),
        (c2, "Total Profit",   fmt_currency(kpis["total_profit"]),  "Net profit earned",  "#10b981"),
        (c3, "Total Orders",   f"{kpis['total_orders']:,}",          "Unique orders",      "#e94560"),
        (c4, "Profit Margin",  f"{kpis['profit_margin']:.1f}%",     "Sales → profit rate","#f59e0b"),
    ]
    for col, label, value, sub, color in cards:
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='border-top-color:{color};'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{value}</div>
                <div class='kpi-sub'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ──────────────────────────────────────────────────────────────────────────────
# STEP A — INTRODUCTION
# ──────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

if active_step == "intro":
    st.markdown("""
    <div class='hero-main'>
        <h1>📖 The Retail Data Story</h1>
        <p>A five-chapter business intelligence narrative revealing what the numbers are really saying.</p>
    </div>
    """, unsafe_allow_html=True)

    # Story chapters overview
    cols = st.columns(5)
    chapters = [
        ("🏠","A. Introduction","Context, scope & dataset overview"),
        ("🔬","B. EDA","Statistical profiling & data quality audit"),
        ("📊","C. Visualisations","15 interactive charts & geographic maps"),
        ("💡","D. Insights","12 insights · 7 findings · 7 recommendations"),
        ("🏁","E. Conclusion","Scorecard, roadmap & executive summary"),
    ]
    for col, (icon, title, desc) in zip(cols, chapters):
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='border-top-color:#0f3460; text-align:left; padding:1.2rem;'>
                <div style='font-size:1.8rem;'>{icon}</div>
                <div style='font-family:Syne,sans-serif; font-weight:700; font-size:0.88rem;
                            color:#1a1a2e; margin:0.4rem 0 0.2rem;'>{title}</div>
                <div style='font-size:0.76rem; color:#6b7280; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Live KPIs
    st.markdown("<h3>📊 Live Dashboard KPIs</h3>", unsafe_allow_html=True)
    render_kpi_dashboard(df)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Dataset context
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("### 🗂️ About the Dataset")
        st.markdown("""
        This dataset simulates **four years of retail transactions** (2020–2023) across the United States,
        encompassing three product categories sold to three customer segments across four geographic regions.

        **Each record captures:**
        - 🏷️ Order ID, Customer ID, Segment
        - 📍 City, State, Region, Latitude/Longitude
        - 📦 Category, Product Name
        - 💰 Sales, Profit, Quantity, Discount, Unit Price
        - 📅 Order Date, Ship Date

        The data powers a complete storytelling pipeline — from raw numbers to strategic recommendations.
        """)

    with col_b:
        st.markdown("### 📐 Dataset Dimensions")
        dim_df = pd.DataFrame({
            "Metric": ["Total Records","Columns","Date Range","Categories","Regions","Segments","States"],
            "Value":  [
                f"{len(df_raw):,}",
                str(len(df_raw.columns)),
                f"{df_raw['year'].min()} – {df_raw['year'].max()}",
                str(df_raw["category"].nunique()),
                str(df_raw["region"].nunique()),
                str(df_raw["segment"].nunique()),
                str(df_raw["state"].nunique()),
            ]
        })
        st.dataframe(dim_df, hide_index=True, use_container_width=True)

    # Tiny sparkline per category
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📈 Sales Pulse (All Time)")
    monthly_agg = df_raw.groupby(["year","month"])["sales"].sum().reset_index()
    monthly_agg["period"] = pd.to_datetime(monthly_agg.assign(day=1)[["year","month","day"]])
    fig_pulse = px.area(monthly_agg, x="period", y="sales",
                        color_discrete_sequence=[PALETTE["primary"]])
    fig_pulse.update_traces(fillcolor="rgba(15,52,96,0.15)", line_color=PALETTE["primary"])
    chart_defaults(fig_pulse, "Monthly Sales Trend — Full Dataset", 280)
    fig_pulse.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig_pulse, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ──────────────────────────────────────────────────────────────────────────────
# STEP B — EDA
# ──────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

elif active_step == "eda":
    section_header("Step B", "🔬 Exploratory Data Analysis",
                   "Statistical profiling, data types, missing-value audit and distributions.")

    render_kpi_dashboard(df)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📐 Shape & Types", "❓ Missing Values", "📊 Summary Stats",
        "🏷️ Categorical", "📉 Numeric Dist.", "👁️ Sample Data", "🔗 Correlations"
    ])

    # ── Tab 1: Shape & Types ─────────────────────────────────────────────────
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Rows", f"{df.shape[0]:,}")
        with c2:
            st.metric("Columns", df.shape[1])
        with c3:
            st.metric("Memory", f"{df.memory_usage(deep=True).sum()/1024:.1f} KB")

        dtypes_df = pd.DataFrame({
            "Column": df.columns,
            "Dtype":  df.dtypes.astype(str).values,
            "Non-Null Count": df.count().values,
            "Null Count": df.isnull().sum().values,
            "Unique Values": df.nunique().values,
        })
        st.dataframe(dtypes_df, hide_index=True, use_container_width=True, height=420)

    # ── Tab 2: Missing Values ────────────────────────────────────────────────
    with tab2:
        null_counts = df.isnull().sum()
        null_pct    = (null_counts / len(df) * 100).round(2)
        missing_df  = pd.DataFrame({"Column": null_counts.index,
                                    "Missing Count": null_counts.values,
                                    "Missing %": null_pct.values})
        missing_df  = missing_df[missing_df["Missing Count"] > 0]

        if missing_df.empty:
            st.success("✅ Dataset is complete — no missing values detected.")
            fig_miss = go.Figure(go.Indicator(
                mode="number+delta",
                value=100,
                title={"text":"Data Completeness"},
                delta={"reference": 95},
                number={"suffix":"%"},
            ))
            st.plotly_chart(fig_miss, use_container_width=True)
        else:
            st.warning(f"⚠️ {len(missing_df)} columns have missing values.")
            fig_miss = px.bar(missing_df, x="Column", y="Missing %",
                              color="Missing %", color_continuous_scale="Reds",
                              title="Missing Value Percentage by Column")
            chart_defaults(fig_miss)
            st.plotly_chart(fig_miss, use_container_width=True)
            st.dataframe(missing_df, hide_index=True, use_container_width=True)

    # ── Tab 3: Summary Stats ─────────────────────────────────────────────────
    with tab3:
        num_cols = ["sales","profit","quantity","discount","unit_price","profit_margin"]
        num_cols = [c for c in num_cols if c in df.columns]
        stats    = df[num_cols].describe().T.round(2)
        stats.index.name = "Metric"
        st.dataframe(stats, use_container_width=True)

    # ── Tab 4: Categorical Distributions ─────────────────────────────────────
    with tab4:
        cat_cols = ["category","region","segment","state","city"]
        cat_cols = [c for c in cat_cols if c in df.columns]
        chosen   = st.selectbox("Select column", cat_cols)
        vc       = df[chosen].value_counts().reset_index()
        vc.columns = [chosen, "count"]
        vc["pct"]  = (vc["count"] / vc["count"].sum() * 100).round(1)

        col1, col2 = st.columns([3,2])
        with col1:
            fig_bar = px.bar(vc.head(20), x=chosen, y="count",
                             color="count", color_continuous_scale="Blues",
                             title=f"{chosen.title()} Distribution")
            chart_defaults(fig_bar)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            fig_pie = px.pie(vc.head(8), names=chosen, values="count",
                             color_discrete_sequence=PALETTE["cat"],
                             title=f"Top {min(8,len(vc))} {chosen.title()}")
            chart_defaults(fig_pie)
            st.plotly_chart(fig_pie, use_container_width=True)

    # ── Tab 5: Numeric Distributions ─────────────────────────────────────────
    with tab5:
        num_cols2 = ["sales","profit","quantity","discount","unit_price","profit_margin"]
        num_cols2 = [c for c in num_cols2 if c in df.columns]
        chosen_n  = st.selectbox("Select numeric column", num_cols2)

        col1, col2 = st.columns(2)
        with col1:
            fig_hist = px.histogram(df, x=chosen_n, nbins=50, marginal="box",
                                    color_discrete_sequence=[PALETTE["primary"]],
                                    title=f"{chosen_n.replace('_',' ').title()} Histogram")
            chart_defaults(fig_hist)
            st.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            fig_box = px.box(df, x="category", y=chosen_n,
                             color="category", color_discrete_sequence=PALETTE["cat"],
                             title=f"{chosen_n.replace('_',' ').title()} by Category")
            chart_defaults(fig_box)
            st.plotly_chart(fig_box, use_container_width=True)

    # ── Tab 6: Sample Data ───────────────────────────────────────────────────
    with tab6:
        n_rows = st.slider("Rows to preview", 5, 50, 10)
        display_cols = ["order_id","order_date","segment","region","category",
                        "product_name","sales","profit","quantity","discount"]
        display_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[display_cols].head(n_rows), hide_index=True, use_container_width=True)

    # ── Tab 7: Correlations ──────────────────────────────────────────────────
    with tab7:
        num_c = ["sales","profit","quantity","discount","unit_price","profit_margin"]
        num_c = [c for c in num_c if c in df.columns]
        corr_matrix = df[num_c].corr().round(2)

        fig_heat = go.Figure(go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 11},
            showscale=True,
        ))
        chart_defaults(fig_heat, "Correlation Heatmap — Numeric Features", 400)
        st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ──────────────────────────────────────────────────────────────────────────────
# STEP C — VISUAL STORYTELLING
# ──────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

elif active_step == "viz":
    section_header("Step C", "📊 Visual Storytelling",
                   "15 interactive visualisations across trends, categories, geography & correlations.")

    render_kpi_dashboard(df)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── C1: Monthly Trend ────────────────────────────────────────────────────
    st.markdown("### 1️⃣ Monthly Sales & Profit Trend")
    monthly = (df.groupby(["year","month"])
               .agg(sales=("sales","sum"), profit=("profit","sum"))
               .reset_index())
    monthly["period"] = pd.to_datetime(
        monthly.assign(day=1)[["year","month","day"]])

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(go.Bar(x=monthly["period"], y=monthly["sales"],
                                name="Sales", marker_color=PALETTE["primary"],
                                opacity=0.8), secondary_y=False)
    fig_trend.add_trace(go.Scatter(x=monthly["period"], y=monthly["profit"],
                                    name="Profit", line=dict(color=PALETTE["accent"], width=2.5),
                                    mode="lines+markers"), secondary_y=True)
    fig_trend.update_yaxes(title_text="Sales ($)", secondary_y=False,
                            tickprefix="$", tickformat=",.0f")
    fig_trend.update_yaxes(title_text="Profit ($)", secondary_y=True,
                            tickprefix="$", tickformat=",.0f")
    chart_defaults(fig_trend, "Monthly Sales (bars) vs Profit (line)", 400)
    st.plotly_chart(fig_trend, use_container_width=True)

    # ─── C2: YoY Comparison ──────────────────────────────────────────────────
    st.markdown("### 2️⃣ Year-over-Year Comparison")
    yoy = df.groupby("year").agg(sales=("sales","sum"), profit=("profit","sum"),
                                  orders=("order_id","nunique")).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig_yoy_s = px.bar(yoy, x="year", y="sales",
                            color="year", text_auto=".2s",
                            color_discrete_sequence=PALETTE["cat"])
        fig_yoy_s.update_traces(textposition="outside")
        chart_defaults(fig_yoy_s, "Annual Sales", 320)
        fig_yoy_s.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_yoy_s, use_container_width=True)
    with c2:
        fig_yoy_p = px.bar(yoy, x="year", y="profit",
                            color="year", text_auto=".2s",
                            color_discrete_sequence=PALETTE["cat"])
        fig_yoy_p.update_traces(textposition="outside")
        chart_defaults(fig_yoy_p, "Annual Profit", 320)
        fig_yoy_p.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_yoy_p, use_container_width=True)

    # ─── C3: Quarterly Trends ────────────────────────────────────────────────
    st.markdown("### 3️⃣ Quarterly Sales Trends")
    quarterly = df.groupby(["year","quarter"])["sales"].sum().reset_index()
    quarterly["label"] = "Q" + quarterly["quarter"].astype(str)

    fig_q = px.line(quarterly, x="label", y="sales", color="year",
                    color_discrete_sequence=PALETTE["cat"],
                    markers=True)
    chart_defaults(fig_q, "Sales by Quarter per Year", 360)
    fig_q.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── C4: Category Revenue ────────────────────────────────────────────────
    st.markdown("### 4️⃣ Category-wise Revenue Analysis")
    cat_agg = (df.groupby("category")
               .agg(sales=("sales","sum"), profit=("profit","sum"), orders=("order_id","nunique"))
               .reset_index())
    cat_agg["margin"] = cat_agg["profit"] / cat_agg["sales"] * 100

    c1, c2 = st.columns(2)
    with c1:
        fig_cat_bar = px.bar(cat_agg, x="category", y=["sales","profit"],
                              barmode="group", color_discrete_sequence=[PALETTE["primary"], PALETTE["positive"]])
        chart_defaults(fig_cat_bar, "Sales vs Profit by Category", 340)
        fig_cat_bar.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_cat_bar, use_container_width=True)
    with c2:
        fig_cat_pie = px.pie(cat_agg, names="category", values="sales",
                              color_discrete_sequence=PALETTE["cat"],
                              hole=0.45)
        chart_defaults(fig_cat_pie, "Revenue Share by Category", 340)
        st.plotly_chart(fig_cat_pie, use_container_width=True)

    # ─── C5: Segment Analysis ────────────────────────────────────────────────
    st.markdown("### 5️⃣ Segment-wise Sales Analysis")
    seg_agg = (df.groupby(["segment","category"])["sales"].sum().reset_index())

    fig_seg = px.bar(seg_agg, x="segment", y="sales", color="category",
                     barmode="stack", color_discrete_sequence=PALETTE["cat"])
    chart_defaults(fig_seg, "Sales by Segment & Category (stacked)", 360)
    fig_seg.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig_seg, use_container_width=True)

    # ─── C6: Top Products ────────────────────────────────────────────────────
    st.markdown("### 6️⃣ Top Products Analysis")
    top_n  = st.slider("Number of products", 5, 20, 10, key="top_prod_n")
    prod_agg = (df.groupby("product_name")
                .agg(sales=("sales","sum"), profit=("profit","sum"))
                .nlargest(top_n, "sales").reset_index())

    fig_prod = px.bar(prod_agg, x="sales", y="product_name",
                       orientation="h", color="profit",
                       color_continuous_scale="RdYlGn",
                       color_continuous_midpoint=0)
    chart_defaults(fig_prod, f"Top {top_n} Products by Sales", 400)
    fig_prod.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig_prod.update_layout(yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig_prod, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── C7: Sales vs Profit Scatter ─────────────────────────────────────────
    st.markdown("### 7️⃣ Sales vs Profit Correlation")
    fig_corr = px.scatter(df, x="sales", y="profit", color="category",
                           size="quantity", hover_data=["product_name","region"],
                           color_discrete_sequence=PALETTE["cat"],
                           opacity=0.65, trendline="ols")
    chart_defaults(fig_corr, "Sales vs Profit (size = Quantity)", 420)
    fig_corr.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig_corr.update_yaxes(tickprefix="$", tickformat=",.0f")
    st.plotly_chart(fig_corr, use_container_width=True)

    # ─── C8: Discount vs Margin ──────────────────────────────────────────────
    st.markdown("### 8️⃣ Discount vs Profit Margin Analysis")
    df_disc = df.copy()
    df_disc["disc_bin"] = pd.cut(df_disc["discount"],
                                  bins=[-0.01,0,0.1,0.2,0.3,1.0],
                                  labels=["0%","1–10%","11–20%","21–30%",">30%"])
    disc_agg = (df_disc.groupby("disc_bin", observed=True)["profit_margin"]
                .mean().reset_index())
    disc_agg["margin_pct"] = disc_agg["profit_margin"] * 100

    fig_disc = px.bar(disc_agg, x="disc_bin", y="margin_pct",
                       color="margin_pct",
                       color_continuous_scale="RdYlGn",
                       color_continuous_midpoint=0)
    chart_defaults(fig_disc, "Average Profit Margin by Discount Tier", 340)
    fig_disc.update_yaxes(ticksuffix="%")
    st.plotly_chart(fig_disc, use_container_width=True)

    # ─── C9: Correlation Heatmap ─────────────────────────────────────────────
    st.markdown("### 9️⃣ Correlation Heatmap")
    num_c = ["sales","profit","quantity","discount","unit_price","profit_margin"]
    num_c = [c for c in num_c if c in df.columns]
    corr_m = df[num_c].corr().round(2)

    fig_heat2 = go.Figure(go.Heatmap(
        z=corr_m.values,
        x=corr_m.columns.tolist(),
        y=corr_m.index.tolist(),
        colorscale="RdBu", zmid=0,
        text=corr_m.values.round(2),
        texttemplate="%{text}", textfont={"size": 12},
    ))
    chart_defaults(fig_heat2, "Feature Correlation Matrix", 400)
    st.plotly_chart(fig_heat2, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── C10: Sales Distribution ─────────────────────────────────────────────
    st.markdown("### 🔟 Sales Distribution Analysis")
    c1, c2 = st.columns(2)
    with c1:
        fig_violin = px.violin(df, x="category", y="sales",
                                color="category", box=True,
                                color_discrete_sequence=PALETTE["cat"])
        chart_defaults(fig_violin, "Sales Distribution by Category (violin)", 380)
        fig_violin.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_violin, use_container_width=True)
    with c2:
        fig_ecdf = px.ecdf(df, x="sales", color="category",
                            color_discrete_sequence=PALETTE["cat"])
        chart_defaults(fig_ecdf, "Cumulative Sales Distribution (ECDF)", 380)
        fig_ecdf.update_xaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_ecdf, use_container_width=True)

    # ─── C11 & C12: Geographic ───────────────────────────────────────────────
    st.markdown("### 1️⃣1️⃣ Geographic Sales Analysis")
    state_agg = (df.groupby("state")
                 .agg(sales=("sales","sum"), profit=("profit","sum"),
                      orders=("order_id","nunique"))
                 .reset_index())
    fig_choropleth = px.choropleth(
        state_agg,
        locations="state",
        locationmode="USA-states",
        color="sales",
        scope="usa",
        color_continuous_scale="Blues",
        hover_data=["profit","orders"],
    )
    chart_defaults(fig_choropleth, "State-wise Sales Choropleth", 480)
    fig_choropleth.update_layout(geo_bgcolor="#f8fafc")
    st.plotly_chart(fig_choropleth, use_container_width=True)

    # ─── C12: Region Performance ─────────────────────────────────────────────
    st.markdown("### 1️⃣2️⃣ Region Performance Analysis")
    reg_agg = (df.groupby("region")
               .agg(sales=("sales","sum"), profit=("profit","sum"),
                    orders=("order_id","nunique"))
               .reset_index())
    reg_agg["margin"] = reg_agg["profit"] / reg_agg["sales"] * 100

    c1, c2 = st.columns(2)
    with c1:
        fig_reg = px.bar(reg_agg, x="region", y="sales",
                          color="region", color_discrete_sequence=PALETTE["cat"],
                          text_auto=".2s")
        fig_reg.update_traces(textposition="outside")
        chart_defaults(fig_reg, "Total Sales by Region", 340)
        fig_reg.update_yaxes(tickprefix="$", tickformat=",.0f")
        st.plotly_chart(fig_reg, use_container_width=True)
    with c2:
        fig_reg_m = px.bar(reg_agg, x="region", y="margin",
                            color="region", color_discrete_sequence=PALETTE["cat"],
                            text_auto=".1f")
        fig_reg_m.update_traces(textposition="outside",
                                  texttemplate="%{y:.1f}%")
        chart_defaults(fig_reg_m, "Profit Margin % by Region", 340)
        fig_reg_m.update_yaxes(ticksuffix="%")
        st.plotly_chart(fig_reg_m, use_container_width=True)

    # ─── C13: Customer Segment ───────────────────────────────────────────────
    st.markdown("### 1️⃣3️⃣ Customer Segment Analysis")
    seg2 = (df.groupby("segment")
            .agg(sales=("sales","sum"), profit=("profit","sum"),
                 orders=("order_id","nunique"), customers=("customer_id","nunique"))
            .reset_index())
    seg2["aov"] = seg2["sales"] / seg2["orders"]

    fig_radar_vals = []
    categories_r   = ["Sales","Profit","Orders","Customers","AOV"]
    for _, row in seg2.iterrows():
        vals = [row["sales"], row["profit"], row["orders"], row["customers"], row["aov"]]
        norm = [v / max(seg2[col_].max(),1) for v, col_ in zip(vals,
                ["sales","profit","orders","customers","aov"])]
        fig_radar_vals.append((row["segment"], norm))

    fig_radar = go.Figure()
    for seg_name, vals in fig_radar_vals:
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories_r + [categories_r[0]],
            fill="toself", name=seg_name, opacity=0.6,
        ))
    chart_defaults(fig_radar, "Segment Comparison (normalised radar)", 420)
    st.plotly_chart(fig_radar, use_container_width=True)

    # ─── C14: State-wise Revenue ─────────────────────────────────────────────
    st.markdown("### 1️⃣4️⃣ State-wise Revenue Analysis")
    top_states = (df.groupby("state")["sales"].sum()
                  .nlargest(15).reset_index().sort_values("sales"))
    fig_state = px.bar(top_states, x="sales", y="state", orientation="h",
                        color="sales", color_continuous_scale="Blues")
    chart_defaults(fig_state, "Top 15 States by Revenue", 450)
    fig_state.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig_state.update_layout(yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig_state, use_container_width=True)

    # ─── C15: Geographic Bubble Map ──────────────────────────────────────────
    st.markdown("### 1️⃣5️⃣ Interactive Geographic Bubble Map")
    city_agg = (df.groupby(["city","state","region","latitude","longitude"])
                .agg(sales=("sales","sum"), profit=("profit","sum"),
                     orders=("order_id","nunique"))
                .reset_index())

    fig_bubble = px.scatter_mapbox(
        city_agg,
        lat="latitude", lon="longitude",
        size="sales", color="profit",
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        hover_name="city",
        hover_data={"state":True,"region":True,"orders":True,
                    "sales":":,.0f","profit":":,.0f",
                    "latitude":False,"longitude":False},
        size_max=40,
        zoom=3.5,
        center={"lat":38.0,"lon":-96.0},
        mapbox_style="carto-positron",
    )
    chart_defaults(fig_bubble, "City-level Sales & Profit Bubble Map", 520)
    st.plotly_chart(fig_bubble, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ──────────────────────────────────────────────────────────────────────────────
# STEP D — INSIGHTS & FINDINGS
# ──────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

elif active_step == "insights":
    section_header("Step D", "💡 Insights, Findings & Recommendations",
                   "Automatically generated intelligence from the filtered data.")

    render_kpi_dashboard(df)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    tab_i, tab_f, tab_r = st.tabs(["🔍 12 Key Insights","📋 7 Business Findings","🚀 7 Recommendations"])

    # ─── Key Insights ─────────────────────────────────────────────────────────
    with tab_i:
        st.markdown("#### Automatically derived from the current filter selection")
        insight_list = ins.generate_insights(df)
        if not insight_list:
            st.warning("No data matches the current filters.")
        else:
            cols = st.columns(3)
            for idx, item in enumerate(insight_list):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class='insight-card' style='border-left-color:{item["color"]};'>
                        <div class='insight-title'>{item["icon"]} {item["title"]}</div>
                        <div class='insight-value' style='color:{item["color"]};'>{item["value"]}</div>
                        <div class='insight-desc'>{item["description"]}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ─── Business Findings ────────────────────────────────────────────────────
    with tab_f:
        st.markdown("#### Data-driven business findings requiring leadership attention")
        findings = ins.generate_findings(df)
        if not findings:
            st.warning("Insufficient data for findings.")
        else:
            for f in findings:
                badge_class = {
                    "Critical": "badge-critical",
                    "High":     "badge-high",
                    "Medium":   "badge-medium",
                }.get(f["impact"], "badge-medium")
                st.markdown(f"""
                <div class='finding-card'>
                    <div class='finding-number'>{f["number"]}</div>
                    <div style='margin-bottom:0.35rem;'>
                        <span class='{badge_class}'>{f["impact"]} Impact</span>
                    </div>
                    <div class='finding-title'>{f["title"]}</div>
                    <div class='finding-detail'>{f["detail"]}</div>
                </div>
                """, unsafe_allow_html=True)

    # ─── Recommendations ──────────────────────────────────────────────────────
    with tab_r:
        st.markdown("#### Strategic actions ordered by priority")
        recs = ins.generate_recommendations(df)
        if not recs:
            st.warning("Insufficient data for recommendations.")
        else:
            for r in recs:
                st.markdown(f"""
                <div class='rec-card'>
                    <div class='rec-header'>
                        <span class='rec-num'>{r["number"]}</span>
                        <span>{r["priority"]}</span>
                    </div>
                    <div class='rec-title'>{r["title"]}</div>
                    <div class='rec-detail'>{r["detail"]}</div>
                    <div class='rec-meta'>⏱️ Timeline: {r["timeline"]}</div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ──────────────────────────────────────────────────────────────────────────────
# STEP E — CONCLUSION
# ──────────────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

elif active_step == "conclusion":
    section_header("Step E", "🏁 Conclusion",
                   "Executive summary, strategic roadmap and business health scorecard.")

    render_kpi_dashboard(df)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── Executive Summary ────────────────────────────────────────────────────
    st.markdown("### 📝 Executive Summary")
    kpis = ins.compute_kpis(df)
    cat_profit = df.groupby("category")["profit"].sum()
    best_cat   = cat_profit.idxmax() if not cat_profit.empty else "N/A"
    reg_sales  = df.groupby("region")["sales"].sum()
    best_reg   = reg_sales.idxmax() if not reg_sales.empty else "N/A"

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#f8fafc,#f1f5f9);
                border-radius:16px; padding:2rem; border:1px solid #e2e8f0;
                margin-bottom:1.5rem; line-height:1.8;'>
        <p style='font-size:1rem; color:#334155;'>
            The retail business generated <strong style='color:#0f3460;'>{fmt_currency(kpis["total_sales"])}</strong>
            in total revenue with a profit of <strong style='color:#10b981;'>{fmt_currency(kpis["total_profit"])}</strong>,
            translating to a <strong>{kpis["profit_margin"]:.1f}%</strong> overall profit margin across
            <strong>{kpis["total_orders"]:,}</strong> orders.
        </p>
        <p style='font-size:1rem; color:#334155;'>
            <strong>{best_cat}</strong> is the highest-profit category while the
            <strong>{best_reg}</strong> region drives the most revenue.
            The average discount of <strong>{kpis["avg_discount"]:.1f}%</strong> represents a
            significant margin lever — tightening discount governance alone could unlock
            meaningful EBIT upside.
        </p>
        <p style='font-size:1rem; color:#334155;'>
            Geographic concentration in top states and Q4 seasonality present both
            risk and growth opportunity. Sustainable value creation requires a balanced
            portfolio strategy: growing high-margin categories, deepening penetration in
            under-served geographies, and strengthening customer loyalty in the Corporate segment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Scorecard ────────────────────────────────────────────────────────────
    st.markdown("### 📊 Business Health Scorecard")
    scorecard = ins.compute_scorecard(df)

    col_s, col_radar = st.columns([2, 3])
    with col_s:
        for item in scorecard:
            st.markdown(f"""
            <div class='score-card'>
                <div class='score-grade' style='color:{item["color"]};'>{item["grade"]}</div>
                <div class='score-info'>
                    <div class='score-name'>{item["name"]}</div>
                    <div class='score-bar-wrap'>
                        <div class='score-bar'
                             style='width:{item["score"]}%;background:{item["color"]};'></div>
                    </div>
                    <div style='font-size:0.72rem;color:#9ca3af;margin-top:2px;'>{item["description"]}</div>
                </div>
                <div class='score-num' style='color:{item["color"]};'>{item["score"]}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_radar:
        if scorecard:
            fig_sc = go.Figure(go.Scatterpolar(
                r=[s["score"] for s in scorecard] + [scorecard[0]["score"]],
                theta=[s["name"] for s in scorecard] + [scorecard[0]["name"]],
                fill="toself",
                fillcolor="rgba(15,52,96,0.15)",
                line=dict(color=PALETTE["primary"], width=2),
                name="Score",
            ))
            chart_defaults(fig_sc, "Health Scorecard Radar", 400)
            fig_sc.update_layout(polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont_size=9),
                bgcolor="#f8fafc",
            ))
            st.plotly_chart(fig_sc, use_container_width=True)

    # ─── Strategic Roadmap ────────────────────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Strategic Roadmap")

    roadmap = [
        ("🔴","0–30 Days","Quick Wins",
         ["Enforce discount governance caps (20 % / 30 % thresholds)",
          "Flag and review all loss-making orders in CRM",
          "Launch weekly P&L report for regional managers"]),
        ("🟡","30–90 Days","Mid-Term",
         ["Category portfolio rebalancing — push high-margin SKUs",
          "Corporate segment loyalty programme launch",
          "Dynamic pricing pilot in top 5 cities"]),
        ("🟢","90–180 Days","Strategic",
         ["Geographic expansion into under-penetrated states",
          "Seasonal inventory demand-sensing model deployment",
          "Customer CLV model for at-risk account identification"]),
        ("🔵","180+ Days","Transformation",
         ["Full dynamic pricing engine go-live",
          "Data-driven sales incentive redesign",
          "Real-time BI dashboard rolled out to field sales teams"]),
    ]

    rm_cols = st.columns(4)
    for col, (dot, timeline, phase, actions) in zip(rm_cols, roadmap):
        with col:
            actions_html = "".join(f"<li style='margin-bottom:0.3rem;'>{a}</li>" for a in actions)
            st.markdown(f"""
            <div class='kpi-card' style='border-top-color:{{"🔴":"#dc2626","🟡":"#d97706",
                         "🟢":"#059669","🔵":"#2563eb"}}[dot]; text-align:left; padding:1.3rem;'>
                <div style='font-size:1.4rem; margin-bottom:0.3rem;'>{dot}</div>
                <div style='font-size:0.7rem; color:#9ca3af; text-transform:uppercase;
                            letter-spacing:0.08em;'>{timeline}</div>
                <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1rem;
                            color:#1a1a2e; margin:0.3rem 0 0.6rem;'>{phase}</div>
                <ul style='padding-left:1rem; margin:0; font-size:0.8rem;
                            color:#475569; line-height:1.5;'>{actions_html}</ul>
            </div>
            """.replace('{"🔴":"#dc2626","🟡":"#d97706","🟢":"#059669","🔵":"#2563eb"}[dot]',
                        {"🔴":"#dc2626","🟡":"#d97706","🟢":"#059669","🔵":"#2563eb"}[dot]),
            unsafe_allow_html=True)

    # ─── Future Enhancements ──────────────────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🚀 Future Enhancement Plan")
    enhancements = [
        ("🤖","ML Forecasting","Integrate ARIMA/Prophet for 90-day sales forecasting"),
        ("📱","Mobile App","React Native companion app for field sales teams"),
        ("🔗","ERP Integration","Live data sync from SAP/Oracle ERP via REST API"),
        ("🛡️","Anomaly Detection","Real-time ML flagging of unusual orders"),
        ("📧","Automated Reports","Scheduled PDF/email delivery of executive KPI digests"),
        ("🌐","Multi-currency","Support for international markets with FX normalisation"),
    ]
    enh_cols = st.columns(3)
    for idx, (icon, title, desc) in enumerate(enhancements):
        with enh_cols[idx % 3]:
            st.markdown(f"""
            <div class='insight-card' style='border-left-color:#0f3460;'>
                <div class='insight-title'>{icon} {title}</div>
                <div class='insight-desc' style='margin-top:0.3rem;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ─── Footer ───────────────────────────────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#9ca3af; font-size:0.82rem; padding:1rem 0 2rem;'>
        🛍️ <strong>Retail Data Storytelling Dashboard</strong> · Built with Streamlit, Pandas, NumPy & Plotly<br>
        © 2024 Retail BI Team · Production-Grade Business Intelligence
    </div>
    """, unsafe_allow_html=True)
