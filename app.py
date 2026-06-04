"""
🇿🇲 Zambia National Retail Intelligence Platform
Author: Given Chinyama | Streamlit App Conversion
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import random
import math
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🇿🇲 Zambia Retail Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.main { background: #0a0f1e; }

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a0f1e 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #112240 100%);
    border-right: 1px solid #1e3a5f;
}
section[data-testid="stSidebar"] * { color: #cdd9e5 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label { color: #64ffda !important; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; }

/* Hero header */
.hero-header {
    background: linear-gradient(135deg, #0d1b2a, #112240, #0d1b2a);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(100,255,218,0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(0,188,212,0.06) 0%, transparent 60%);
}
.hero-title {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, #64ffda, #00bcd4, #64ffda);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; line-height: 1.2;
}
.hero-subtitle { color: #8892b0; font-size: 0.95rem; margin-top: 0.4rem; font-weight: 300; }

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #112240, #0d1b2a);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #64ffda, #00bcd4);
}
.kpi-label { color: #8892b0; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.kpi-value { color: #64ffda; font-size: 1.6rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
.kpi-sub { color: #4a90d9; font-size: 0.75rem; margin-top: 0.2rem; }

/* Section headers */
.section-header {
    color: #cdd9e5; font-size: 1.1rem; font-weight: 700;
    border-left: 3px solid #64ffda; padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
    letter-spacing: 0.02em;
}

/* Insight boxes */
.insight-box {
    background: rgba(100,255,218,0.05);
    border: 1px solid rgba(100,255,218,0.2);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    color: #a8b2d8;
    font-size: 0.88rem;
}
.insight-box strong { color: #64ffda; }

/* Plotly charts themed */
.stPlotlyChart { border-radius: 12px; overflow: hidden; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #0d1b2a; border-radius: 8px; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #8892b0;
    border-radius: 6px; padding: 0.5rem 1rem;
    font-weight: 600; font-size: 0.85rem;
}
.stTabs [aria-selected="true"] { background: #1e3a5f !important; color: #64ffda !important; }

/* Metric overrides */
[data-testid="stMetricValue"] { color: #64ffda !important; font-family: 'JetBrains Mono', monospace !important; }
[data-testid="stMetricLabel"] { color: #8892b0 !important; }

/* Dataframe */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* Spinner */
.stSpinner > div { border-top-color: #64ffda !important; }

div[data-testid="column"] > div { height: 100%; }

/* Progress bar */
.stProgress .st-bo { background-color: #64ffda; }
</style>
""", unsafe_allow_html=True)

# ── Constants & Config ───────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

PLOT_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(13,27,42,0)",
    plot_bgcolor="rgba(13,27,42,0)",
    font=dict(family="Sora, sans-serif", color="#cdd9e5"),
    colorway=["#64ffda", "#00bcd4", "#4a90d9", "#9b59b6", "#e74c3c", "#f39c12", "#2ecc71"],
)

CITIES = {
    "Lusaka":      {"weight": 0.38, "region": "Southern"},
    "Kitwe":       {"weight": 0.18, "region": "Copperbelt"},
    "Ndola":       {"weight": 0.14, "region": "Copperbelt"},
    "Livingstone": {"weight": 0.09, "region": "Southern"},
    "Chipata":     {"weight": 0.07, "region": "Eastern"},
    "Kabwe":       {"weight": 0.07, "region": "Central"},
    "Solwezi":     {"weight": 0.07, "region": "North-Western"},
}

STORES = {
    "ShopRite Zambia":   "Large Supermarket",
    "Pick n Pay":        "Large Supermarket",
    "Choppies":          "Medium Supermarket",
    "Melmart":           "Medium Supermarket",
    "Spar Zambia":       "Large Supermarket",
    "Mukuba Mall Store": "Department Store",
    "Local Kiosk":       "Informal Retail",
    "Shoppers Mart":     "Medium Supermarket",
}

PRODUCTS = {
    "Mealie Meal 25kg":       {"category": "Staples",    "price_zmw": 280, "cost_zmw": 190},
    "Cooking Oil 2L":         {"category": "Staples",    "price_zmw": 85,  "cost_zmw": 55},
    "Sugar 2kg":              {"category": "Staples",    "price_zmw": 75,  "cost_zmw": 48},
    "Noodles (Pack of 5)":    {"category": "Staples",    "price_zmw": 35,  "cost_zmw": 22},
    "Rice 5kg":               {"category": "Staples",    "price_zmw": 120, "cost_zmw": 78},
    "Fresh Milk 1L":          {"category": "Dairy",      "price_zmw": 28,  "cost_zmw": 18},
    "Yoghurt 500ml":          {"category": "Dairy",      "price_zmw": 22,  "cost_zmw": 14},
    "Kapenta (Dried) 500g":   {"category": "Protein",    "price_zmw": 95,  "cost_zmw": 62},
    "Beef Mince 1kg":         {"category": "Protein",    "price_zmw": 185, "cost_zmw": 130},
    "Eggs (Tray of 30)":      {"category": "Protein",    "price_zmw": 110, "cost_zmw": 72},
    "Tomatoes (1kg)":         {"category": "Produce",    "price_zmw": 18,  "cost_zmw": 10},
    "Onions (1kg)":           {"category": "Produce",    "price_zmw": 15,  "cost_zmw": 8},
    "Bathing Soap (3-pack)":  {"category": "HPC",        "price_zmw": 55,  "cost_zmw": 34},
    "Laundry Powder 1kg":     {"category": "HPC",        "price_zmw": 65,  "cost_zmw": 40},
    "Toothpaste 150ml":       {"category": "HPC",        "price_zmw": 42,  "cost_zmw": 26},
    "Airtime ZMW 20 Voucher": {"category": "Telecoms",   "price_zmw": 20,  "cost_zmw": 17},
    "Mobile Data Bundle":     {"category": "Telecoms",   "price_zmw": 45,  "cost_zmw": 38},
    "Soft Drink 2L":          {"category": "Beverages",  "price_zmw": 38,  "cost_zmw": 24},
    "Beer 330ml (6-pack)":    {"category": "Beverages",  "price_zmw": 115, "cost_zmw": 78},
    "Water 1.5L":             {"category": "Beverages",  "price_zmw": 16,  "cost_zmw": 9},
    "Nappies (Pack of 20)":   {"category": "Baby Care",  "price_zmw": 145, "cost_zmw": 98},
    "Baby Cereal 500g":       {"category": "Baby Care",  "price_zmw": 88,  "cost_zmw": 56},
    "Exercise Book (5-pk)":   {"category": "Stationery", "price_zmw": 45,  "cost_zmw": 28},
    "Pen Box (10-pk)":        {"category": "Stationery", "price_zmw": 32,  "cost_zmw": 18},
}


# ── Data generation (cached) ─────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_data(n_records: int = 80_000) -> pd.DataFrame:
    dates = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    seasonal = {1:1.25,2:1.00,3:0.95,4:1.10,5:1.00,6:0.90,
                7:0.88,8:0.92,9:0.95,10:1.00,11:1.10,12:1.40}

    city_names   = list(CITIES)
    city_weights = [CITIES[c]["weight"] for c in city_names]
    store_names  = list(STORES)
    product_names= list(PRODUCTS)
    records = []

    for _ in range(n_records):
        date    = random.choice(dates)
        city    = random.choices(city_names, weights=city_weights, k=1)[0]
        store   = random.choice(store_names)
        product = random.choice(product_names)
        p       = PRODUCTS[product]

        sm         = seasonal[date.month]
        units_sold = max(1, int(np.random.poisson(12) * sm * np.random.uniform(0.7, 1.3)))
        is_promo   = np.random.rand() < 0.15
        discount   = round(np.random.uniform(0.05, 0.25), 2) if is_promo else 0.0
        unit_price = round(p["price_zmw"] * (1 - discount), 2)
        revenue    = round(units_sold * unit_price, 2)
        cogs       = round(units_sold * p["cost_zmw"], 2)
        gp         = round(revenue - cogs, 2)
        sb         = max(units_sold, np.random.randint(units_sold, units_sold + 60))

        records.append({
            "transaction_id":   f"TXN{random.randint(100_000,999_999)}",
            "date":             date,
            "year":             date.year,
            "month":            date.month,
            "day_of_week":      date.day_name(),
            "city":             city,
            "region":           CITIES[city]["region"],
            "store_name":       store,
            "store_type":       STORES[store],
            "product_name":     product,
            "category":         p["category"],
            "units_sold":       units_sold,
            "unit_price_zmw":   unit_price,
            "unit_cost_zmw":    p["cost_zmw"],
            "revenue_zmw":      revenue,
            "cogs_zmw":         cogs,
            "gross_profit_zmw": gp,
            "gross_margin_pct": round((gp / revenue) * 100, 2) if revenue > 0 else 0,
            "is_promotion":     int(is_promo),
            "discount_pct":     round(discount * 100, 2),
            "stock_before":     sb,
            "stock_after":      sb - units_sold,
            "stockout_risk":    1 if (sb - units_sold) < 20 else 0,
            "customer_id":      f"CUS{random.randint(1000,6000):05d}",
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["revenue_zmw"] > 0].sort_values("date").reset_index(drop=True)
    return df


@st.cache_data(show_spinner=False)
def build_daily_features(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.groupby("date").agg(
        total_revenue  =("revenue_zmw",     "sum"),
        total_units    =("units_sold",      "sum"),
        total_txns     =("transaction_id",  "count"),
        avg_margin     =("gross_margin_pct","mean"),
        promo_txns     =("is_promotion",    "sum"),
        stockout_flags =("stockout_risk",   "sum"),
    ).reset_index().sort_values("date")

    daily["day_of_week"]      = daily["date"].dt.dayofweek
    daily["month"]            = daily["date"].dt.month
    daily["quarter"]          = daily["date"].dt.quarter
    daily["year"]             = daily["date"].dt.year
    daily["day_of_year"]      = daily["date"].dt.dayofyear
    daily["is_weekend"]       = (daily["day_of_week"] >= 5).astype(int)
    daily["is_month_end"]     = daily["date"].dt.is_month_end.astype(int)
    daily["is_month_start"]   = daily["date"].dt.is_month_start.astype(int)
    daily["is_festive"]       = daily["month"].isin([11, 12]).astype(int)
    daily["is_back_to_school"]= daily["month"].isin([1, 9]).astype(int)

    for lag in [7, 14, 30]:
        daily[f"revenue_lag_{lag}d"] = daily["total_revenue"].shift(lag)
    daily["revenue_rolling_7d"]  = daily["total_revenue"].rolling(7,  min_periods=1).mean()
    daily["revenue_rolling_30d"] = daily["total_revenue"].rolling(30, min_periods=1).mean()
    daily["revenue_std_7d"]      = daily["total_revenue"].rolling(7,  min_periods=1).std().fillna(0)
    daily.dropna(inplace=True)
    daily.reset_index(drop=True, inplace=True)
    return daily


@st.cache_data(show_spinner=False)
def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    snapshot = df["date"].max() + timedelta(days=1)
    rfm = df.groupby("customer_id").agg(
        Recency   =("date",           lambda x: (snapshot - x.max()).days),
        Frequency =("transaction_id", "count"),
        Monetary  =("revenue_zmw",    "sum"),
    ).reset_index()

    scaler     = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["Recency","Frequency","Monetary"]])
    kmeans     = KMeans(n_clusters=4, random_state=SEED, n_init=10)
    rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

    cp = rfm.groupby("Cluster").agg(
        Customers    =("customer_id","count"),
        Avg_Recency  =("Recency",    "mean"),
        Avg_Frequency=("Frequency",  "mean"),
        Avg_Monetary =("Monetary",   "mean"),
    ).round(1).reset_index()

    lm = {
        cp.loc[cp["Avg_Monetary"].idxmax(),   "Cluster"]: "💎 Champions",
        cp.loc[cp["Avg_Recency"].idxmax(),    "Cluster"]: "😴 At-Risk",
        cp.loc[cp["Avg_Frequency"].idxmin(),  "Cluster"]: "🌱 New Customers",
    }
    cp["Segment"] = cp["Cluster"].map(lm).fillna("🔄 Loyal Regulars")
    rfm["Segment"] = rfm["Cluster"].map(dict(zip(cp["Cluster"], cp["Segment"])))
    return rfm, cp


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇿🇲 Retail Intel")
    st.markdown("---")

    page = st.radio(
        "NAVIGATE",
        ["📊 Executive Dashboard",
         "🔍 EDA & Trends",
         "📈 Demand Forecasting",
         "🧠 Customer Segments",
         "🚨 Risk Detection",
         "📋 Data Explorer"],
        label_visibility="visible",
    )

    st.markdown("---")
    st.markdown("**FILTERS**")

    year_filter = st.multiselect(
        "Year", [2022, 2023, 2024], default=[2022, 2023, 2024]
    )
    city_filter = st.multiselect(
        "City", list(CITIES.keys()), default=list(CITIES.keys())
    )
    cat_filter = st.multiselect(
        "Category",
        list(set(v["category"] for v in PRODUCTS.values())),
        default=list(set(v["category"] for v in PRODUCTS.values())),
    )

    st.markdown("---")
    st.caption("Author: **Given Chinyama**")
    st.caption("Data: Synthetic | Period: 2022–2024")


# ── Load data ────────────────────────────────────────────────────────────────
with st.spinner("🔄 Generating Zambian retail dataset…"):
    df_full = generate_data(80_000)

# Apply filters
df = df_full[
    df_full["year"].isin(year_filter) &
    df_full["city"].isin(city_filter) &
    df_full["category"].isin(cat_filter)
].copy()

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar.")
    st.stop()


# ── Hero header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div class="hero-title">🛒 National Retail Intelligence Platform</div>
  <div class="hero-subtitle">Zambia · 2022–2024 · Analytics, Forecasting & Business Intelligence</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📊 Executive Dashboard":

    # KPIs
    total_rev    = df["revenue_zmw"].sum()
    total_profit = df["gross_profit_zmw"].sum()
    avg_margin   = df["gross_margin_pct"].mean()
    total_txns   = df["transaction_id"].nunique()
    total_cust   = df["customer_id"].nunique()
    stockout_rate= df["stockout_risk"].mean() * 100
    promo_rate   = df["is_promotion"].mean() * 100

    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
    kpis = [
        (c1, "Total Revenue",    f"ZMW {total_rev/1e6:.1f}M",     ""),
        (c2, "Gross Profit",     f"ZMW {total_profit/1e6:.1f}M",  ""),
        (c3, "Avg Margin",       f"{avg_margin:.1f}%",             ""),
        (c4, "Transactions",     f"{total_txns:,}",                ""),
        (c5, "Customers",        f"{total_cust:,}",                ""),
        (c6, "Stockout Rate",    f"{stockout_rate:.1f}%",          ""),
        (c7, "Promo Rate",       f"{promo_rate:.1f}%",             ""),
    ]
    for col, label, val, sub in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: Revenue by City + Monthly Trend
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="section-header">Revenue by City</div>', unsafe_allow_html=True)
        rc = df.groupby("city")["revenue_zmw"].sum().sort_values() / 1e6
        fig = px.bar(rc, orientation="h", labels={"value":"ZMW (M)","index":"City"},
                     color=rc.values, color_continuous_scale=["#1e3a5f","#64ffda"])
        fig.update_layout(**PLOT_THEME, height=280, margin=dict(l=0,r=10,t=10,b=0),
                          coloraxis_showscale=False, xaxis_title="ZMW Millions")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
        df["year_month"] = df["date"].dt.to_period("M").astype(str)
        monthly = df.groupby("year_month")["revenue_zmw"].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["year_month"], y=monthly["revenue_zmw"],
            mode="lines", fill="tozeroy",
            line=dict(color="#64ffda", width=2.5),
            fillcolor="rgba(100,255,218,0.08)",
        ))
        fig.update_layout(**PLOT_THEME, height=280, margin=dict(l=0,r=10,t=10,b=0),
                          xaxis_title="Month", yaxis_title="Revenue (ZMW)")
        st.plotly_chart(fig, use_container_width=True)

    # Row 2: Category share + Top Products + Store Type
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col1:
        st.markdown('<div class="section-header">Category Revenue Share</div>', unsafe_allow_html=True)
        cat_rev = df.groupby("category")["revenue_zmw"].sum()
        fig = go.Figure(go.Pie(
            labels=cat_rev.index, values=cat_rev.values, hole=0.42,
            textinfo="percent", textfont=dict(size=11),
            marker=dict(colors=["#64ffda","#00bcd4","#4a90d9","#9b59b6",
                                 "#e74c3c","#f39c12","#2ecc71","#1abc9c",
                                 "#e67e22","#27ae60"]),
        ))
        fig.update_layout(**PLOT_THEME, height=280, margin=dict(l=0,r=0,t=0,b=0),
                          legend=dict(font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
        tp = df.groupby("product_name")["revenue_zmw"].sum().sort_values(ascending=True).tail(10)
        fig = px.bar(tp, orientation="h", color=tp.values,
                     color_continuous_scale=["#1e3a5f","#64ffda"],
                     labels={"value":"ZMW","index":"Product"})
        fig.update_layout(**PLOT_THEME, height=280, margin=dict(l=0,r=10,t=10,b=0),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown('<div class="section-header">Revenue by Store Type</div>', unsafe_allow_html=True)
        st_rev = df.groupby("store_type")["revenue_zmw"].sum().sort_values()
        fig = px.bar(st_rev, orientation="h", color=st_rev.values,
                     color_continuous_scale=["#1e3a5f","#00bcd4"],
                     labels={"value":"ZMW","index":"Store"})
        fig.update_layout(**PLOT_THEME, height=280, margin=dict(l=0,r=10,t=10,b=0),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # Row 3: YoY + Margin by Category
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Year-on-Year Revenue</div>', unsafe_allow_html=True)
        yoy = df.groupby("year")["revenue_zmw"].sum()
        fig = px.bar(yoy, color=yoy.values, color_continuous_scale=["#1e3a5f","#64ffda"],
                     labels={"value":"Revenue (ZMW)","year":"Year"})
        fig.update_layout(**PLOT_THEME, height=250, margin=dict(l=0,r=10,t=10,b=0),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Gross Margin by Category (%)</div>', unsafe_allow_html=True)
        cm = df.groupby("category")["gross_margin_pct"].mean().sort_values()
        fig = px.bar(cm, orientation="h", color=cm.values,
                     color_continuous_scale=["#e74c3c","#f39c12","#64ffda"],
                     labels={"value":"Margin %","index":"Category"})
        fig.update_layout(**PLOT_THEME, height=250, margin=dict(l=0,r=10,t=10,b=0),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — EDA & TRENDS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 EDA & Trends":
    st.markdown('<div class="section-header">Seasonality & Temporal Patterns</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    with col1:
        monthly_avg = df.groupby("month")["revenue_zmw"].mean()
        fig = px.bar(x=month_labels, y=monthly_avg.values,
                     labels={"x":"Month","y":"Avg Revenue (ZMW)"},
                     title="Average Revenue by Month (Seasonality)",
                     color=monthly_avg.values,
                     color_continuous_scale=["#1e3a5f","#64ffda"])
        fig.update_layout(**PLOT_THEME, height=320, margin=dict(t=40),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow_avg = df.groupby("day_of_week")["revenue_zmw"].mean().reindex(dow_order)
        colors = ["#e74c3c" if d in ["Saturday","Sunday"] else "#4a90d9" for d in dow_order]
        fig = go.Figure(go.Bar(x=dow_order, y=dow_avg.values, marker_color=colors))
        fig.update_layout(**PLOT_THEME, height=320,
                          title="Average Revenue by Day of Week (Red = Weekend)",
                          xaxis_tickangle=-30, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Promotion Impact Analysis</div>', unsafe_allow_html=True)
    promo = df.groupby("is_promotion").agg(
        avg_units  =("units_sold",       "mean"),
        avg_revenue=("revenue_zmw",      "mean"),
        avg_margin =("gross_margin_pct", "mean"),
    ).reset_index()
    promo["label"] = promo["is_promotion"].map({0:"No Promotion", 1:"Promotion Active"})

    col1, col2, col3 = st.columns(3)
    metrics = [
        (col1, "avg_units",   "Avg Units Sold"),
        (col2, "avg_revenue", "Avg Revenue (ZMW)"),
        (col3, "avg_margin",  "Avg Gross Margin (%)"),
    ]
    for col, m, label in metrics:
        with col:
            fig = px.bar(promo, x="label", y=m, title=label,
                         color="label",
                         color_discrete_map={"No Promotion":"#4a90d9","Promotion Active":"#e74c3c"})
            fig.update_layout(**PLOT_THEME, height=280, showlegend=False,
                              margin=dict(t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

    lift = ((promo.loc[1,"avg_revenue"] - promo.loc[0,"avg_revenue"]) / promo.loc[0,"avg_revenue"]) * 100
    st.markdown(f"""
    <div class="insight-box">
      <strong>📢 Promotion Revenue Lift:</strong> {lift:+.1f}% &nbsp;|&nbsp;
      <strong>Margin Trade-off:</strong> {promo.loc[0,'avg_margin']:.1f}% (no promo)
      vs {promo.loc[1,'avg_margin']:.1f}% (with promo)
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">City & Regional Breakdown</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        city_cat = df.groupby(["city","category"])["revenue_zmw"].sum().reset_index()
        fig = px.bar(city_cat, x="city", y="revenue_zmw", color="category",
                     barmode="stack", title="Revenue by City & Category",
                     labels={"revenue_zmw":"Revenue (ZMW)","city":"City"})
        fig.update_layout(**PLOT_THEME, height=350, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        store_city = df.groupby(["store_name","city"])["revenue_zmw"].sum().reset_index()
        fig = px.treemap(store_city, path=["city","store_name"], values="revenue_zmw",
                         title="Revenue Treemap: City → Store",
                         color="revenue_zmw", color_continuous_scale=["#112240","#64ffda"])
        fig.update_layout(**PLOT_THEME, height=350, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DEMAND FORECASTING
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Demand Forecasting":
    with st.spinner("🔧 Building features & training models…"):
        daily = build_daily_features(df)

    st.markdown('<div class="section-header">Model Selection</div>', unsafe_allow_html=True)
    model_choice = st.radio("Choose model", ["XGBoost Regressor", "ARIMA (Monthly)"],
                            horizontal=True)

    if model_choice == "XGBoost Regressor":
        from sklearn.ensemble import GradientBoostingRegressor
        try:
            from xgboost import XGBRegressor
            use_xgb = True
        except ImportError:
            use_xgb = False

        features = [
            "day_of_week","month","quarter","year","day_of_year",
            "is_weekend","is_month_end","is_month_start",
            "is_festive","is_back_to_school",
            "revenue_lag_7d","revenue_lag_14d","revenue_lag_30d",
            "revenue_rolling_7d","revenue_rolling_30d","revenue_std_7d",
            "promo_txns","stockout_flags",
        ]
        X = daily[features]; y = daily["total_revenue"]
        split = int(len(daily) * 0.80)
        X_tr, X_te = X.iloc[:split], X.iloc[split:]
        y_tr, y_te = y.iloc[:split], y.iloc[split:]

        with st.spinner("Training model…"):
            if use_xgb:
                model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6,
                                     subsample=0.8, colsample_bytree=0.8,
                                     random_state=SEED, verbosity=0)
            else:
                model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05,
                                                  max_depth=5, random_state=SEED)
            model.fit(X_tr, y_tr)
            y_pred = model.predict(X_te)

        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        mae  = mean_absolute_error(y_te, y_pred)
        rmse = math.sqrt(mean_squared_error(y_te, y_pred))
        r2   = r2_score(y_te, y_pred)
        mape = np.mean(np.abs((y_te.values - y_pred) / y_te.values)) * 100

        c1,c2,c3,c4 = st.columns(4)
        for col, label, val in [(c1,"MAE",f"ZMW {mae:,.0f}"),
                                 (c2,"RMSE",f"ZMW {rmse:,.0f}"),
                                 (c3,"R²",f"{r2:.4f}"),
                                 (c4,"MAPE",f"{mape:.2f}%")]:
            with col:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
                            f'<div class="kpi-value" style="font-size:1.3rem">{val}</div></div>',
                            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        test_dates = daily["date"].iloc[split:]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=test_dates, y=y_te.values, mode="lines",
                                 name="Actual", line=dict(color="#2ecc71", width=2)))
        fig.add_trace(go.Scatter(x=test_dates, y=y_pred, mode="lines",
                                 name="Predicted", line=dict(color="#e74c3c", dash="dash", width=2)))
        fig.update_layout(**PLOT_THEME, height=380, title="Daily Revenue — Actual vs Predicted",
                          xaxis_title="Date", yaxis_title="Revenue (ZMW)")
        st.plotly_chart(fig, use_container_width=True)

        # Feature importance
        fi = pd.Series(model.feature_importances_, index=features).sort_values(ascending=True).tail(12)
        fig2 = px.bar(fi, orientation="h", title="Top Feature Importances",
                      color=fi.values, color_continuous_scale=["#1e3a5f","#64ffda"],
                      labels={"value":"Importance","index":"Feature"})
        fig2.update_layout(**PLOT_THEME, height=350, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    else:  # ARIMA
        try:
            from statsmodels.tsa.arima.model import ARIMA as _ARIMA
            from sklearn.metrics import mean_absolute_error, mean_squared_error

            monthly_ts = daily.set_index("date")["total_revenue"].resample("ME").sum()
            train_ts, test_ts = monthly_ts[:-6], monthly_ts[-6:]

            with st.spinner("Fitting ARIMA(2,1,2)…"):
                fit = _ARIMA(train_ts, order=(2,1,2)).fit()
                fc  = fit.forecast(steps=6)
                ci  = fit.get_forecast(steps=6).conf_int()

            mae  = mean_absolute_error(test_ts, fc)
            rmse = math.sqrt(mean_squared_error(test_ts, fc))
            mape = np.mean(np.abs((test_ts.values - fc.values) / test_ts.values)) * 100

            c1,c2,c3 = st.columns(3)
            for col, lbl, val in [(c1,"MAE",f"ZMW {mae:,.0f}"),
                                   (c2,"RMSE",f"ZMW {rmse:,.0f}"),
                                   (c3,"MAPE",f"{mape:.2f}%")]:
                with col:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">{lbl}</div>'
                                f'<div class="kpi-value" style="font-size:1.3rem">{val}</div></div>',
                                unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train_ts.index.astype(str), y=train_ts.values,
                                     mode="lines", name="Training", line=dict(color="#4a90d9")))
            fig.add_trace(go.Scatter(x=test_ts.index.astype(str), y=test_ts.values,
                                     mode="lines+markers", name="Actual",
                                     line=dict(color="#2ecc71", width=2)))
            fig.add_trace(go.Scatter(x=test_ts.index.astype(str), y=fc.values,
                                     mode="lines+markers", name="Forecast",
                                     line=dict(color="#e74c3c", dash="dash", width=2)))
            fig.add_trace(go.Scatter(
                x=list(test_ts.index.astype(str)) + list(test_ts.index.astype(str))[::-1],
                y=list(ci.iloc[:,1]) + list(ci.iloc[:,0])[::-1],
                fill="toself", fillcolor="rgba(231,76,60,0.1)",
                line=dict(color="rgba(255,255,255,0)"), name="95% CI",
            ))
            fig.update_layout(**PLOT_THEME, height=420,
                              title="ARIMA(2,1,2) — Monthly Revenue Forecast",
                              xaxis_title="Month", yaxis_title="Revenue (ZMW)")
            st.plotly_chart(fig, use_container_width=True)

        except ImportError:
            st.warning("statsmodels is not installed. Please add it to requirements.txt and restart.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CUSTOMER SEGMENTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 Customer Segments":
    with st.spinner("Running RFM analysis & K-Means clustering…"):
        rfm, cluster_profile = build_rfm(df)

    st.markdown('<div class="section-header">Customer Segment Profiles</div>', unsafe_allow_html=True)

    # Segment KPIs
    cols = st.columns(4)
    seg_counts = rfm["Segment"].value_counts()
    colors_seg = {"💎 Champions":"#f39c12","😴 At-Risk":"#e74c3c",
                  "🌱 New Customers":"#2ecc71","🔄 Loyal Regulars":"#4a90d9"}
    for i, (seg, cnt) in enumerate(seg_counts.items()):
        pct = cnt / len(rfm) * 100
        with cols[i % 4]:
            st.markdown(f"""<div class="kpi-card">
              <div class="kpi-label">{seg}</div>
              <div class="kpi-value" style="font-size:1.5rem">{cnt:,}</div>
              <div class="kpi-sub">{pct:.1f}% of customers</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        # Pie
        fig = go.Figure(go.Pie(
            labels=seg_counts.index, values=seg_counts.values, hole=0.42,
            textinfo="percent+label",
            marker=dict(colors=list(colors_seg.values())),
        ))
        fig.update_layout(**PLOT_THEME, height=340, title="Segment Distribution",
                          margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # RFM scatter
        sample = rfm.sample(min(2000, len(rfm)), random_state=SEED)
        fig = px.scatter(sample, x="Recency", y="Monetary", size="Frequency",
                         color="Segment",
                         color_discrete_map=colors_seg,
                         title="RFM Scatter (size = Frequency)",
                         labels={"Monetary":"Total Revenue (ZMW)","Recency":"Days Since Last Purchase"})
        fig.update_layout(**PLOT_THEME, height=340, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

    # Cluster profile table
    st.markdown('<div class="section-header">Cluster Profiles</div>', unsafe_allow_html=True)
    display_cp = cluster_profile[["Segment","Customers","Avg_Recency","Avg_Frequency","Avg_Monetary"]].copy()
    display_cp.columns = ["Segment","Customers","Avg Recency (days)","Avg Frequency","Avg Revenue (ZMW)"]
    st.dataframe(display_cp.set_index("Segment"), use_container_width=True)

    st.markdown('<div class="section-header">Strategic Recommendations by Segment</div>', unsafe_allow_html=True)
    recs = {
        "💎 Champions": "Launch VIP loyalty programme. Offer exclusive previews & bundle deals. Protect margin here.",
        "😴 At-Risk": "Run win-back campaigns with personalised discounts. Investigate reasons for churn.",
        "🌱 New Customers": "Onboard with welcome offers. Encourage second purchase within 30 days.",
        "🔄 Loyal Regulars": "Upsell higher-margin categories. Cross-sell complementary products.",
    }
    for seg, rec in recs.items():
        st.markdown(f'<div class="insight-box"><strong>{seg}:</strong> {rec}</div>',
                    unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RISK DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🚨 Risk Detection":
    with st.spinner("Analysing stockout & demand anomalies…"):
        daily = build_daily_features(df)

    st.markdown('<div class="section-header">Stockout Risk by Product</div>', unsafe_allow_html=True)

    so = df.groupby(["product_name","category"]).agg(
        total_txns      =("transaction_id","count"),
        stockout_events =("stockout_risk",  "sum"),
        avg_stock_after =("stock_after",    "mean"),
    ).reset_index()
    so["stockout_rate_pct"] = (so["stockout_events"] / so["total_txns"] * 100).round(2)
    so.sort_values("stockout_rate_pct", ascending=False, inplace=True)

    col1, col2 = st.columns([1.6, 1])
    with col1:
        top12 = so.head(12)
        fig = px.bar(top12, x="stockout_rate_pct", y="product_name", orientation="h",
                     color="stockout_rate_pct", color_continuous_scale=["#f39c12","#e74c3c"],
                     title="Top 12 Products by Stockout Rate (%)",
                     labels={"stockout_rate_pct":"Stockout Rate (%)","product_name":"Product"})
        fig.update_layout(**PLOT_THEME, height=400, margin=dict(t=40),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Stockout by City</div>', unsafe_allow_html=True)
        so_city = df.groupby("city")["stockout_risk"].mean() * 100
        fig = px.bar(so_city.sort_values(), orientation="h",
                     color=so_city.sort_values().values,
                     color_continuous_scale=["#f39c12","#e74c3c"],
                     labels={"value":"Stockout Rate (%)","index":"City"})
        fig.update_layout(**PLOT_THEME, height=300, margin=dict(t=10),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Demand Anomaly Detection (Z-Score Method)</div>',
                unsafe_allow_html=True)
    daily["z_score"] = (daily["total_revenue"] - daily["total_revenue"].mean()) / daily["total_revenue"].std()
    daily["anomaly"] = daily["z_score"].abs() > 2.5
    normal    = daily[~daily["anomaly"]]
    anomalies = daily[daily["anomaly"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=normal["date"], y=normal["total_revenue"],
                             mode="lines", name="Normal",
                             line=dict(color="#4a90d9", width=1.5)))
    fig.add_trace(go.Scatter(x=anomalies["date"], y=anomalies["total_revenue"],
                             mode="markers", name="⚠️ Anomaly",
                             marker=dict(color="#e74c3c", size=10, symbol="x")))
    fig.update_layout(**PLOT_THEME, height=360,
                      title="Daily Revenue with Anomaly Flags (|Z| > 2.5)",
                      xaxis_title="Date", yaxis_title="Revenue (ZMW)")
    st.plotly_chart(fig, use_container_width=True)

    n_anom = daily["anomaly"].sum()
    st.markdown(f"""<div class="insight-box">
      <strong>⚠️ {n_anom} anomalous days</strong> detected out of {len(daily)} trading days.
      These represent unusual demand spikes or drops — investigate for supply disruptions, promotions,
      or data quality issues.
    </div>""", unsafe_allow_html=True)

    # Overstock
    st.markdown('<div class="section-header">Overstock Risk (High Avg Stock After Sale)</div>',
                unsafe_allow_html=True)
    over = df.groupby("product_name")["stock_after"].mean().sort_values(ascending=False).head(10)
    fig = px.bar(over, title="Top 10 Products by Avg Remaining Stock (Overstock Risk)",
                 color=over.values, color_continuous_scale=["#64ffda","#f39c12"],
                 labels={"value":"Avg Stock After","index":"Product"})
    fig.update_layout(**PLOT_THEME, height=320, coloraxis_showscale=False,
                      xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — DATA EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Data Explorer":
    st.markdown('<div class="section-header">Raw Transaction Data</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Filtered Records", f"{len(df):,}")
    with col2:
        st.metric("Columns", f"{df.shape[1]}")

    search_col = st.selectbox("Filter by column value", ["(none)","city","category","store_name","product_name"])
    if search_col != "(none)":
        vals = df[search_col].unique().tolist()
        chosen = st.multiselect(f"Select {search_col}", vals, default=vals[:3])
        display_df = df[df[search_col].isin(chosen)]
    else:
        display_df = df

    st.dataframe(
        display_df[[
            "date","city","store_name","product_name","category",
            "units_sold","unit_price_zmw","revenue_zmw","gross_profit_zmw",
            "gross_margin_pct","is_promotion","stockout_risk","customer_id",
        ]].head(500),
        use_container_width=True, height=420,
    )

    st.markdown('<div class="section-header">Statistical Summary</div>', unsafe_allow_html=True)
    st.dataframe(
        df[["units_sold","unit_price_zmw","revenue_zmw","gross_profit_zmw","gross_margin_pct"]].describe().round(2),
        use_container_width=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x="revenue_zmw", nbins=60, title="Revenue Distribution",
                           color_discrete_sequence=["#64ffda"])
        fig.update_layout(**PLOT_THEME, height=300, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="gross_margin_pct", nbins=50, title="Gross Margin Distribution",
                           color_discrete_sequence=["#00bcd4"])
        fig.update_layout(**PLOT_THEME, height=300, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#4a5568; font-size:0.8rem;'>"
    "🇿🇲 Zambia National Retail Intelligence Platform · Given Chinyama · 2026 · "
    "Data is synthetic & generated for analytical demonstration purposes."
    "</p>",
    unsafe_allow_html=True,
)
