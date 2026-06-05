https://zambia-retail-dashboard-app-wg8u4zhast9p9gjhz3cdvf.streamlit.app/
# 🇿🇲 Zambia National Retail Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-64FFDA?style=for-the-badge)

**A full-stack retail analytics dashboard for the Zambian market — featuring demand forecasting, customer segmentation, risk detection, and executive reporting, all powered by a synthetic 80,000-record dataset.**

[Features](#-features) · [Screenshots](#-screenshots) · [Installation](#-installation) · [Usage](#-usage) · [Architecture](#-architecture) · [Data Model](#-data-model) · [ML Models](#-ml-models) · [Roadmap](#-roadmap)

</div>

---

## 📌 Overview

The **Zambia National Retail Intelligence Platform** is an interactive business intelligence web application built with [Streamlit](https://streamlit.io). It simulates and analyses retail transaction data across Zambia's major cities and store chains from **2022 to 2024**, delivering actionable insights across six analytical modules:
https://zambia-retail-dashboard-app-wg8u4zhast9p9gjhz3cdvf.streamlit.app/

- Executive KPI dashboards with real-time filtering
- Exploratory data analysis with seasonality and promotion impact
- ML-powered demand forecasting (XGBoost & ARIMA)
- RFM-based customer segmentation using K-Means clustering
- Stockout and anomaly risk detection
- Interactive raw data explorer

> **Note:** All data in this application is **synthetically generated** for demonstration and analytical purposes. It does not represent real commercial data from any Zambian retailer.

---

## ✨ Features

### 📊 Executive Dashboard
- Seven headline KPI cards: Total Revenue, Gross Profit, Average Margin, Transactions, Customers, Stockout Rate, and Promotion Rate
- Revenue breakdown by city, month, category, product, and store type
- Year-on-year revenue comparison
- Gross margin analysis by product category

### 🔍 EDA & Trends
- Seasonality analysis — average revenue by month and day of week
- Promotion impact analysis: revenue lift %, margin trade-off comparison
- City and regional revenue breakdown with stacked bar charts
- Revenue treemap drill-down: City → Store

### 📈 Demand Forecasting
Two selectable forecasting models:

| Model | Description |
|---|---|
| **XGBoost Regressor** | Gradient-boosted tree model trained on 18 engineered features (lags, rolling averages, calendar flags). Falls back to scikit-learn's GradientBoostingRegressor if XGBoost is not installed. |
| **ARIMA(2,1,2)** | Classical time-series model on monthly aggregated revenue with 95% confidence intervals. |

Evaluation metrics reported: **MAE**, **RMSE**, **R²**, **MAPE**

### 🧠 Customer Segments
- RFM (Recency, Frequency, Monetary) feature engineering per customer
- K-Means clustering (k=4) with StandardScaler normalisation
- Auto-labelled segments: 💎 Champions, 😴 At-Risk, 🌱 New Customers, 🔄 Loyal Regulars
- Cluster profile table, RFM scatter plot, segment distribution pie chart
- Actionable strategic recommendations per segment

### 🚨 Risk Detection
- Stockout rate per product and city
- Z-score anomaly detection on daily revenue (|Z| > 2.5 flagged)
- Overstock risk identification (products with high average remaining stock)

### 📋 Data Explorer
- Filterable, searchable view of up to 500 raw transaction records
- Statistical summary (min, max, mean, std, percentiles) for key metrics
- Revenue and gross margin distribution histograms

---

## 🗂 Project Structure

```
zambia-retail-intelligence/
│
├── app.py                  # Main Streamlit application (single-file)
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .streamlit/
    └── config.toml         # Optional Streamlit theme configuration
```

> The entire application is contained in a **single Python file** (`app.py`) for easy deployment and portability.

---

## ⚙️ Installation

### Prerequisites

- Python 3.9 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/GIVEN-CHINYAMA/zambia-retail-intelligence.git
cd zambia-retail-intelligence
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📦 Dependencies

Create a `requirements.txt` with the following:

```txt
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scikit-learn>=1.3.0
xgboost>=2.0.0          # Optional — falls back to GradientBoostingRegressor
statsmodels>=0.14.0     # Required for ARIMA forecasting
```

Install everything at once:

```bash
pip install streamlit pandas numpy plotly scikit-learn xgboost statsmodels
```

---

## 🚀 Usage

### Sidebar Controls

Once the app is running, use the **left sidebar** to:

| Control | Options |
|---|---|
| **Navigate** | Switch between the 6 analytical pages |
| **Year** | Filter by 2022, 2023, and/or 2024 |
| **City** | Filter by one or more Zambian cities |
| **Category** | Filter by product category (Staples, Dairy, Protein, etc.) |

All filters apply globally across the active page in real time.

### Pages at a Glance

```
📊 Executive Dashboard  →  High-level KPIs and performance charts
🔍 EDA & Trends         →  Seasonality, promotions, and city analysis
📈 Demand Forecasting   →  XGBoost or ARIMA model selection and evaluation
🧠 Customer Segments    →  RFM analysis and K-Means clustering
🚨 Risk Detection       →  Stockout rates, anomalies, and overstock alerts
📋 Data Explorer        →  Raw transaction data and statistical summaries
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│  ┌───────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐  │
│  │ Sidebar   │  │  Pages   │  │ Charts │  │ Tables  │  │
│  │ (Filters) │  │ (Router) │  │(Plotly)│  │(Pandas) │  │
│  └───────────┘  └──────────┘  └────────┘  └─────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Cached Data Layer                       │
│  ┌──────────────────┐   ┌──────────────────────────┐    │
│  │  generate_data() │   │  build_daily_features()  │    │
│  │  @st.cache_data  │   │  @st.cache_data          │    │
│  └──────────────────┘   └──────────────────────────┘    │
│  ┌──────────────────┐                                    │
│  │   build_rfm()    │                                    │
│  │   @st.cache_data │                                    │
│  └──────────────────┘                                    │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   ML / Analytics Layer                   │
│  ┌───────────┐  ┌────────┐  ┌─────────┐  ┌──────────┐  │
│  │ XGBoost / │  │  ARIMA │  │ K-Means │  │ Z-Score  │  │
│  │  GBR      │  │(2,1,2) │  │  RFM    │  │ Anomaly  │  │
│  └───────────┘  └────────┘  └─────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Key design decisions:**

- `@st.cache_data` is used on all three data-building functions to avoid regenerating 80,000 rows on every user interaction.
- The app is **entirely stateless** — all data is regenerated from a fixed random seed (`SEED = 42`), ensuring reproducibility.
- Sidebar filters slice the cached `df_full` DataFrame into `df` before any page renders.

---

## 🗃 Data Model

The synthetic dataset contains **80,000 transaction records** spanning 2022–2024, with the following schema:

| Column | Type | Description |
|---|---|---|
| `transaction_id` | `str` | Unique identifier (e.g., `TXN482910`) |
| `date` | `datetime` | Transaction date |
| `year` / `month` / `day_of_week` | `int` / `str` | Calendar breakdowns |
| `city` | `str` | One of 7 Zambian cities |
| `region` | `str` | Geographic region (Southern, Copperbelt, etc.) |
| `store_name` | `str` | Retailer name (e.g., ShopRite, Choppies) |
| `store_type` | `str` | Large Supermarket, Medium Supermarket, etc. |
| `product_name` | `str` | One of 21 distinct products |
| `category` | `str` | Product category (Staples, Dairy, Protein, etc.) |
| `units_sold` | `int` | Poisson-distributed, seasonally adjusted |
| `unit_price_zmw` | `float` | List price, discounted during promotions |
| `unit_cost_zmw` | `float` | Cost of goods |
| `revenue_zmw` | `float` | `units_sold × unit_price_zmw` |
| `cogs_zmw` | `float` | `units_sold × unit_cost_zmw` |
| `gross_profit_zmw` | `float` | `revenue - cogs` |
| `gross_margin_pct` | `float` | `(gross_profit / revenue) × 100` |
| `is_promotion` | `int` | Binary flag (15% of transactions) |
| `discount_pct` | `float` | Discount applied (5–25% when on promotion) |
| `stock_before` | `int` | Simulated beginning stock level |
| `stock_after` | `int` | `stock_before - units_sold` |
| `stockout_risk` | `int` | 1 if `stock_after < 20`, else 0 |
| `customer_id` | `str` | Anonymised ID (pool of ~5,000 customers) |

### Cities & Weights

| City | Region | Transaction Weight |
|---|---|---|
| Lusaka | Southern | 38% |
| Kitwe | Copperbelt | 18% |
| Ndola | Copperbelt | 14% |
| Livingstone | Southern | 9% |
| Chipata | Eastern | 7% |
| Kabwe | Central | 7% |
| Solwezi | North-Western | 7% |

### Seasonality Profile

Revenue is multiplicatively adjusted by month to simulate real-world retail patterns:

| Month | Multiplier | Reason |
|---|---|---|
| January | 1.25 | Back-to-school peak |
| November | 1.10 | Pre-holiday build-up |
| December | 1.40 | Festive season peak |
| July–August | 0.88–0.92 | Mid-year lull |

---

## 🤖 ML Models

### XGBoost Demand Forecasting

**Features (18 total):**

```
Calendar:    day_of_week, month, quarter, year, day_of_year
Flags:       is_weekend, is_month_end, is_month_start, is_festive, is_back_to_school
Lag features: revenue_lag_7d, revenue_lag_14d, revenue_lag_30d
Rolling:     revenue_rolling_7d, revenue_rolling_30d, revenue_std_7d
Contextual:  promo_txns, stockout_flags
```

**Training split:** 80% train / 20% test (chronological, no data leakage)

**Hyperparameters:**
```python
XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
```

### ARIMA Forecasting

- **Model:** ARIMA(2, 1, 2) on monthly aggregated revenue
- **Train/test split:** Last 6 months held out as test set
- **Output:** 6-month forecast with 95% confidence interval band

### RFM Customer Segmentation

**Feature engineering:**

| Metric | Calculation |
|---|---|
| **Recency** | Days since the customer's last transaction (as of max date + 1 day) |
| **Frequency** | Total number of transactions |
| **Monetary** | Total revenue (ZMW) |

**Clustering:**
- StandardScaler normalisation applied before clustering
- K-Means with `k=4`, `n_init=10`, `random_state=42`
- Clusters auto-labelled based on centroid characteristics (highest Monetary → Champions, highest Recency → At-Risk, etc.)

### Anomaly Detection

- Z-score method on daily total revenue: `z = (x - μ) / σ`
- Days with `|z| > 2.5` are flagged as demand anomalies
- Visualised as scatter markers on the revenue time series

---

## 🎨 Design System

The app uses a custom dark-mode design with the following palette:

| Token | Hex | Usage |
|---|---|---|
| Teal Accent | `#64ffda` | KPI values, highlights, borders |
| Cyan | `#00bcd4` | Secondary charts and accents |
| Blue | `#4a90d9` | Tertiary charts, sub-labels |
| Dark Navy | `#0a0f1e` | App background |
| Card Navy | `#112240` | Card and sidebar backgrounds |
| Muted Text | `#8892b0` | Labels and descriptive text |
| Alert Red | `#e74c3c` | Risk indicators, anomalies |
| Warning Amber | `#f39c12` | Stockout and caution markers |

**Typography:** [Sora](https://fonts.google.com/specimen/Sora) (UI) + [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) (KPI values)

---

## 🗺 Roadmap

- [ ] Connect to a live PostgreSQL or BigQuery data source
- [ ] Add Prophet time-series forecasting as a third model option
- [ ] Export filtered data to CSV / Excel
- [ ] User authentication and role-based views
- [ ] Product-level demand forecasting (not just aggregate daily revenue)
- [ ] SMS/email alerting for stockout thresholds
- [ ] Docker containerisation for one-command deployment
- [ ] Automated unit tests for data generation and ML pipelines

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Given Chinyama**

- Built with ❤️ for Zambia's retail and data analytics community
- Data is entirely synthetic and generated for demonstration purposes only

---

<div align="center">
  <sub>🇿🇲 Zambia National Retail Intelligence Platform · 2026 · <em>Data is synthetic & generated for analytical demonstration purposes.</em></sub>
</div>


