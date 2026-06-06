"""
insights.py
===========
Automated business intelligence engine for the Retail Storytelling App.
Generates KPIs, key insights, business findings, and strategic recommendations
from a filtered pandas DataFrame.

Author : Retail BI Team
Version: 1.0.0
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ══════════════════════════════════════════════════════════════════════════════
# 1. KPI CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════

def compute_kpis(df: pd.DataFrame) -> dict:
    """Return a dictionary of top-level KPI values for the dashboard."""
    if df.empty:
        return {
            "total_sales": 0, "total_profit": 0,
            "total_orders": 0, "profit_margin": 0,
            "avg_order_value": 0, "avg_discount": 0,
            "total_quantity": 0, "unique_customers": 0,
        }

    total_sales    = df["sales"].sum()
    total_profit   = df["profit"].sum()
    total_orders   = df["order_id"].nunique()
    profit_margin  = (total_profit / total_sales * 100) if total_sales else 0
    avg_order_val  = total_sales / total_orders if total_orders else 0
    avg_discount   = df["discount"].mean() * 100
    total_quantity = int(df["quantity"].sum())
    unique_customers = df["customer_id"].nunique()

    return {
        "total_sales":       round(total_sales, 2),
        "total_profit":      round(total_profit, 2),
        "total_orders":      total_orders,
        "profit_margin":     round(profit_margin, 2),
        "avg_order_value":   round(avg_order_val, 2),
        "avg_discount":      round(avg_discount, 2),
        "total_quantity":    total_quantity,
        "unique_customers":  unique_customers,
    }


# ══════════════════════════════════════════════════════════════════════════════
# 2. KEY INSIGHTS  (12)
# ══════════════════════════════════════════════════════════════════════════════

def generate_insights(df: pd.DataFrame) -> list[dict]:
    """
    Automatically derive 12 data-driven insights from the filtered DataFrame.
    Each insight is a dict with keys: title, value, description, icon, color.
    """
    if df.empty:
        return []

    insights = []

    # ── I1: Best-performing category ────────────────────────────────────────
    cat_profit = df.groupby("category")["profit"].sum()
    best_cat   = cat_profit.idxmax()
    best_cat_pct = cat_profit[best_cat] / cat_profit.sum() * 100
    insights.append({
        "title":       "Top Revenue Category",
        "value":       best_cat,
        "description": f"contributes {best_cat_pct:.1f}% of total profit — the undisputed revenue engine.",
        "icon":        "🏆",
        "color":       "#4CAF50",
    })

    # ── I2: Best region ─────────────────────────────────────────────────────
    reg_sales  = df.groupby("region")["sales"].sum()
    best_reg   = reg_sales.idxmax()
    best_reg_v = reg_sales[best_reg]
    insights.append({
        "title":       "Dominant Region",
        "value":       best_reg,
        "description": f"leads with ${best_reg_v:,.0f} in sales — a key growth market.",
        "icon":        "🌍",
        "color":       "#2196F3",
    })

    # ── I3: Discount impact ─────────────────────────────────────────────────
    corr = df[["discount", "profit_margin"]].corr().iloc[0, 1]
    insights.append({
        "title":       "Discount–Margin Correlation",
        "value":       f"{corr:.2f}",
        "description": (
            "Strong negative correlation — each 10 % discount erodes margin significantly."
            if corr < -0.3 else
            "Moderate relationship — discounting strategy has mixed profit impact."
        ),
        "icon":        "📉",
        "color":       "#F44336" if corr < -0.3 else "#FF9800",
    })

    # ── I4: Best month ──────────────────────────────────────────────────────
    monthly = df.groupby("month")["sales"].sum()
    best_mo  = monthly.idxmax()
    month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    insights.append({
        "title":       "Peak Sales Month",
        "value":       month_names.get(best_mo, str(best_mo)),
        "description": f"records ${monthly[best_mo]:,.0f} in sales — seasonal demand peaks here.",
        "icon":        "📅",
        "color":       "#9C27B0",
    })

    # ── I5: Top customer segment ─────────────────────────────────────────────
    seg_sales = df.groupby("segment")["sales"].sum()
    top_seg   = seg_sales.idxmax()
    seg_pct   = seg_sales[top_seg] / seg_sales.sum() * 100
    insights.append({
        "title":       "Leading Customer Segment",
        "value":       top_seg,
        "description": f"accounts for {seg_pct:.1f}% of revenue — retention here is mission-critical.",
        "icon":        "👥",
        "color":       "#00BCD4",
    })

    # ── I6: Avg order value ──────────────────────────────────────────────────
    aov = df["sales"].sum() / df["order_id"].nunique()
    insights.append({
        "title":       "Average Order Value",
        "value":       f"${aov:,.2f}",
        "description": "Average revenue per unique order — upsell opportunities exist above this threshold.",
        "icon":        "🛒",
        "color":       "#FF5722",
    })

    # ── I7: Profitability red-zone (high discount, negative profit) ──────────
    red_zone = df[(df["discount"] >= 0.30) & (df["profit"] < 0)]
    red_pct  = len(red_zone) / len(df) * 100
    insights.append({
        "title":       "Loss-Making Orders",
        "value":       f"{red_pct:.1f}%",
        "description": f"{len(red_zone)} orders with ≥30% discount are unprofitable — a margin leak.",
        "icon":        "⚠️",
        "color":       "#F44336",
    })

    # ── I8: YoY growth ──────────────────────────────────────────────────────
    yearly = df.groupby("year")["sales"].sum().sort_index()
    if len(yearly) >= 2:
        yoy = (yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2] * 100
        yoy_str = f"{yoy:+.1f}%"
        color = "#4CAF50" if yoy > 0 else "#F44336"
        desc  = "year-over-year growth — positive momentum." if yoy > 0 else "year-over-year decline — needs strategic attention."
    else:
        yoy_str, color, desc = "N/A", "#9E9E9E", "Insufficient years for YoY comparison."
    insights.append({
        "title":       "YoY Sales Growth",
        "value":       yoy_str,
        "description": desc,
        "icon":        "📈",
        "color":       color,
    })

    # ── I9: Top state ───────────────────────────────────────────────────────
    state_sales = df.groupby("state")["sales"].sum()
    top_state   = state_sales.idxmax()
    insights.append({
        "title":       "Top State by Revenue",
        "value":       top_state,
        "description": f"${state_sales[top_state]:,.0f} in sales — geographic concentration risk and opportunity.",
        "icon":        "📍",
        "color":       "#3F51B5",
    })

    # ── I10: High-volume, low-profit products ────────────────────────────────
    prod_df = df.groupby("product_name").agg(qty=("quantity","sum"), profit=("profit","sum"))
    if len(prod_df) > 1:
        low_margin_prod = prod_df[prod_df["profit"] < prod_df["profit"].median()].nlargest(1,"qty")
        if not low_margin_prod.empty:
            lmp = low_margin_prod.index[0]
            insights.append({
                "title":       "High Volume, Low Margin Product",
                "value":       lmp,
                "description": f"sells {int(low_margin_prod['qty'].iloc[0]):,} units but delivers below-median profit — pricing review needed.",
                "icon":        "📦",
                "color":       "#FF9800",
            })
        else:
            insights.append({"title":"Product Mix","value":"Balanced","description":"No single product dominates volume without decent margin.","icon":"📦","color":"#4CAF50"})
    else:
        insights.append({"title":"Product Mix","value":"Single Product","description":"Limited product diversity in current filter.","icon":"📦","color":"#9E9E9E"})

    # ── I11: Q4 effect ──────────────────────────────────────────────────────
    q_sales = df.groupby("quarter")["sales"].sum()
    if 4 in q_sales.index:
        q4_pct = q_sales[4] / q_sales.sum() * 100
        insights.append({
            "title":       "Q4 Revenue Share",
            "value":       f"{q4_pct:.1f}%",
            "description": "Holiday-quarter contribution — strong Q4 = healthy annual pipeline.",
            "icon":        "🎯",
            "color":       "#E91E63",
        })
    else:
        insights.append({"title":"Q4 Data","value":"N/A","description":"Q4 not in current filtered range.","icon":"🎯","color":"#9E9E9E"})

    # ── I12: Profit-positive rate ────────────────────────────────────────────
    pos_rate = (df["profit"] > 0).mean() * 100
    insights.append({
        "title":       "Profitable Order Rate",
        "value":       f"{pos_rate:.1f}%",
        "description": f"{pos_rate:.1f}% of all orders generate positive profit — operational health indicator.",
        "icon":        "✅",
        "color":       "#4CAF50" if pos_rate > 75 else "#FF9800",
    })

    return insights[:12]


# ══════════════════════════════════════════════════════════════════════════════
# 3. BUSINESS FINDINGS  (7)
# ══════════════════════════════════════════════════════════════════════════════

def generate_findings(df: pd.DataFrame) -> list[dict]:
    """Return 7 structured business findings derived from the data."""
    if df.empty:
        return []

    findings = []

    # F1
    cat_margin = df.groupby("category")["profit_margin"].mean() * 100
    best_c  = cat_margin.idxmax()
    worst_c = cat_margin.idxmin()
    findings.append({
        "number": "01",
        "title":  "Category Profitability Divergence",
        "detail": (
            f"'{best_c}' averages {cat_margin[best_c]:.1f}% margin vs. "
            f"'{worst_c}' at {cat_margin[worst_c]:.1f}%. "
            "Product-mix optimisation toward high-margin categories can lift overall EBIT by 3–5 pp."
        ),
        "impact": "High",
    })

    # F2
    disc_bins = pd.cut(df["discount"], bins=[-0.01,0,0.1,0.2,0.3,1.0],
                       labels=["No Disc","1–10%","11–20%","21–30%",">30%"])
    disc_profit = df.groupby(disc_bins, observed=True)["profit_margin"].mean() * 100
    findings.append({
        "number": "02",
        "title":  "Discount Threshold Effect",
        "detail": (
            f"Orders with >30% discount show {disc_profit.get('>30%',0):.1f}% avg margin — "
            f"vs. {disc_profit.get('No Disc',0):.1f}% for undiscounted orders. "
            "A hard cap at 20% could protect margin without material volume loss."
        ),
        "impact": "Critical",
    })

    # F3
    reg_perf = df.groupby("region").agg(sales=("sales","sum"), profit=("profit","sum"))
    reg_perf["margin"] = reg_perf["profit"] / reg_perf["sales"] * 100
    top_r  = reg_perf["margin"].idxmax()
    low_r  = reg_perf["margin"].idxmin()
    findings.append({
        "number": "03",
        "title":  "Regional Profitability Gap",
        "detail": (
            f"'{top_r}' leads with {reg_perf.loc[top_r,'margin']:.1f}% margin; "
            f"'{low_r}' lags at {reg_perf.loc[low_r,'margin']:.1f}%. "
            "Localised pricing and cost-reduction initiatives in lagging regions can close this gap."
        ),
        "impact": "Medium",
    })

    # F4
    seg_aov = df.groupby("segment")["sales"].sum() / df.groupby("segment")["order_id"].nunique()
    top_seg = seg_aov.idxmax()
    findings.append({
        "number": "04",
        "title":  "Segment AOV Leadership",
        "detail": (
            f"'{top_seg}' segment delivers the highest average order value (${seg_aov[top_seg]:,.0f}). "
            "Targeted account-based marketing and volume incentives for this segment offer the fastest AOV upside."
        ),
        "impact": "High",
    })

    # F5
    monthly_cv = df.groupby("month")["sales"].sum().std() / df.groupby("month")["sales"].sum().mean() * 100
    findings.append({
        "number": "05",
        "title":  "Seasonal Demand Volatility",
        "detail": (
            f"Monthly sales coefficient of variation is {monthly_cv:.1f}%. "
            + ("High volatility signals strong seasonality — inventory and staffing must flex accordingly."
               if monthly_cv > 20 else
               "Relatively stable monthly demand — operational planning is predictable.")
        ),
        "impact": "Medium",
    })

    # F6
    top5_states = df.groupby("state")["sales"].sum().nlargest(5)
    top5_pct = top5_states.sum() / df["sales"].sum() * 100
    findings.append({
        "number": "06",
        "title":  "Geographic Revenue Concentration",
        "detail": (
            f"Top 5 states contribute {top5_pct:.1f}% of total sales "
            f"({', '.join(top5_states.index.tolist())}). "
            "Geographic concentration is a risk; expansion to mid-tier states presents upside."
        ),
        "impact": "Medium",
    })

    # F7
    repeat_city = df.groupby("city")["order_id"].nunique().sort_values(ascending=False)
    top_city = repeat_city.index[0]
    findings.append({
        "number": "07",
        "title":  "Urban Market Density",
        "detail": (
            f"'{top_city}' generates the most orders ({repeat_city.iloc[0]:,}), indicating dense urban demand. "
            "City-specific loyalty programmes and same-day delivery pilots here could materially lift NPS and repeat-purchase rate."
        ),
        "impact": "High",
    })

    return findings


# ══════════════════════════════════════════════════════════════════════════════
# 4. STRATEGIC RECOMMENDATIONS  (7)
# ══════════════════════════════════════════════════════════════════════════════

def generate_recommendations(df: pd.DataFrame) -> list[dict]:
    """Return 7 actionable strategic recommendations."""
    if df.empty:
        return []

    kpis = compute_kpis(df)
    margin = kpis["profit_margin"]
    avg_disc = kpis["avg_discount"]

    recs = [
        {
            "number":   "R1",
            "title":    "Enforce Discount Governance Framework",
            "priority": "🔴 Critical",
            "timeline": "0–30 days",
            "detail":   (
                f"Current average discount is {avg_disc:.1f}%. "
                "Implement a tiered approval system: discounts >20% require manager sign-off, "
                ">30% require VP approval. Automate enforcement via CRM rules. "
                "Expected margin uplift: 2–4 percentage points within one quarter."
            ),
        },
        {
            "number":   "R2",
            "title":    "Category Portfolio Rebalancing",
            "priority": "🔴 Critical",
            "timeline": "30–60 days",
            "detail":   (
                "Shift sales-mix toward high-margin categories (Technology & Furniture). "
                "Bundle low-margin Office Supplies with high-margin items to protect AOV. "
                "Review SKU rationalisation — discontinue the bottom 20% of margin contributors."
            ),
        },
        {
            "number":   "R3",
            "title":    "Regional Expansion & Investment Plan",
            "priority": "🟡 High",
            "timeline": "60–90 days",
            "detail":   (
                "Allocate incremental marketing budget to under-penetrated regions. "
                "Establish regional distribution hubs to reduce fulfilment cost. "
                "Set region-level P&L accountability to surface hidden cost drivers."
            ),
        },
        {
            "number":   "R4",
            "title":    "Customer Segment Loyalty Programme",
            "priority": "🟡 High",
            "timeline": "60–90 days",
            "detail":   (
                "Launch tiered loyalty rewards for the Corporate segment (highest AOV). "
                "Introduce annual volume-rebate contracts to lock in recurring revenue. "
                "Use predictive CLV models to identify at-risk high-value accounts."
            ),
        },
        {
            "number":   "R5",
            "title":    "Dynamic Pricing Engine",
            "priority": "🟡 High",
            "timeline": "90–120 days",
            "detail":   (
                f"Current profit margin is {margin:.1f}%. "
                "Implement a rules-based dynamic pricing model that adjusts unit price by "
                "demand signal, inventory level, and competitor price. "
                "Target: +1.5 pp margin improvement without volume loss."
            ),
        },
        {
            "number":   "R6",
            "title":    "Seasonal Inventory Optimisation",
            "priority": "🟢 Medium",
            "timeline": "90–180 days",
            "detail":   (
                "Use historical monthly seasonality indices to build a demand-sensing model. "
                "Pre-position inventory 6–8 weeks before peak months to reduce stock-outs. "
                "Implement vendor-managed inventory (VMI) for top 10 SKUs by volume."
            ),
        },
        {
            "number":   "R7",
            "title":    "Geographic Market Penetration",
            "priority": "🟢 Medium",
            "timeline": "180+ days",
            "detail":   (
                "Identify the top 10 states by population where current sales density is low. "
                "Run geo-targeted digital campaigns and appoint regional sales partners. "
                "Track market-share growth per state quarterly against a pre-defined KPI scorecard."
            ),
        },
    ]
    return recs


# ══════════════════════════════════════════════════════════════════════════════
# 5. SCORECARD METRICS (for Conclusion section)
# ══════════════════════════════════════════════════════════════════════════════

def compute_scorecard(df: pd.DataFrame) -> list[dict]:
    """Return a business health scorecard with scores and grades."""
    if df.empty:
        return []

    kpis = compute_kpis(df)

    def grade(score):
        if score >= 85: return "A", "#4CAF50"
        if score >= 70: return "B", "#8BC34A"
        if score >= 55: return "C", "#FF9800"
        if score >= 40: return "D", "#FF5722"
        return "F", "#F44336"

    # Profitability score  (0–100 scale: 0% margin=0, 30%+ margin=100)
    prof_score = min(100, max(0, kpis["profit_margin"] / 30 * 100))
    # Discount discipline  (0% disc=100, 50%+ disc=0)
    disc_score = min(100, max(0, (50 - kpis["avg_discount"]) / 50 * 100))
    # Order volume         (proxy: log scale normalised)
    vol_score  = min(100, max(0, np.log1p(kpis["total_orders"]) / np.log1p(5000) * 100))
    # AOV health           (target AOV $500 = 100)
    aov_score  = min(100, max(0, kpis["avg_order_value"] / 500 * 100))
    # Customer breadth
    cust_score = min(100, max(0, np.log1p(kpis["unique_customers"]) / np.log1p(2000) * 100))

    items = [
        ("Profitability",      prof_score, "Profit margin relative to 30% benchmark"),
        ("Discount Discipline",disc_score, "Avg discount gap from 50% worst-case"),
        ("Order Volume",       vol_score,  "Logarithmic order count normalised to 5 000 orders"),
        ("Avg Order Value",    aov_score,  "AOV relative to $500 benchmark"),
        ("Customer Breadth",   cust_score, "Unique customer count depth"),
    ]

    scorecard = []
    for name, score, desc in items:
        g, color = grade(score)
        scorecard.append({"name": name, "score": round(score), "grade": g, "color": color, "description": desc})

    return scorecard
