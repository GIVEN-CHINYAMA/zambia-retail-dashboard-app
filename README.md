# 🇿🇲 Zambia National Retail Intelligence Dashboard App

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-orange?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge)

**A fully deployed, interactive Streamlit web application for retail analytics across Zambia.**  
Demand forecasting · Customer segmentation · Stockout risk detection · Executive BI dashboard.

[🚀 Live Demo](#) · [📓 Notebook Repo](https://github.com/GIVEN-CHINYAMA/zambia-retail-intelligence-platform) · [💼 LinkedIn](https://www.linkedin.com/in/given-chinyama-data)

</div>

---

## 📌 Project Overview

Zambia's retail sector is growing rapidly, driven by urbanisation across cities like **Lusaka, Kitwe, Ndola, and Livingstone** — yet most retailers still operate without data-driven insights. This application provides a **National Retail Intelligence Platform** built entirely in Python and deployed as a live web app.

The platform simulates a realistic **80,000-record multi-city Zambian retail dataset** and delivers actionable intelligence through six analytical modules — covering everything from executive KPI dashboards to machine learning demand forecasts and customer loyalty segmentation.

> **This project demonstrates a full data science-to-deployment pipeline:** data engineering → EDA → ML modelling → interactive web application → cloud deployment.

---

## 🖥️ Application Pages

The app is organised into **six interactive pages**, accessible via the sidebar:

### 📊 1. Executive Dashboard
The top-level command centre for retail decision-makers. Includes:
- **7 live KPI cards** — Total Revenue, Gross Profit, Avg Margin, Transactions, Customers, Stockout Rate, Promotion Rate
- Revenue breakdown by **city, product category, and store type**
- **Monthly revenue trend** (2022–2024) with area fill
- **Top 10 products** by revenue
- **Year-on-Year (YoY) revenue** comparison
- **Gross margin by category** ranked bar chart

### 🔍 2. EDA & Trends
Deep exploratory analysis of Zambia-specific retail patterns:
- **Monthly seasonality** — visualises demand peaks (December festive, January back-to-school)
- **Day-of-week revenue patterns** — highlights weekend uplift
- **Promotion impact analysis** — compares avg units sold, revenue, and margin between promotional and non-promotional transactions
- **Revenue by city × category** stacked bar chart
- **Revenue treemap** — City → Store drill-down

### 📈 3. Demand Forecasting
Two production-grade forecasting models with full performance metrics:

| Model | Type | Best For |
|---|---|---|
| **XGBoost Regressor** | ML (gradient boosting) | High-accuracy daily forecasting |
| **ARIMA(2,1,2)** | Statistical time-series | Trend + seasonality interpretation |

- Metrics displayed: **MAE, RMSE, R², MAPE**
- **Actual vs Predicted** line chart on held-out test data
- **Top 10 feature importances** (XGBoost)
- **95% Confidence Interval** bands (ARIMA)

### 🧠 4. Customer Segmentation
RFM analysis combined with unsupervised machine learning:
- **RFM scoring** — Recency, Frequency, Monetary value per customer
- **K-Means clustering (K=4)** on StandardScaler-normalised RFM features
- Four named segments: `💎 Champions` · `🔄 Loyal Regulars` · `🌱 New Customers` · `😴 At-Risk`
- **Segment KPI cards** with customer counts and percentages
- **RFM scatter plot** (size = Frequency, colour = Segment)
- **Cluster profile table** with avg Recency, Frequency, and Monetary per segment
- **Strategic recommendations** per segment for targeted marketing

### 🚨 5. Risk Detection
Automated inventory and demand risk flagging:
- **Stockout risk rate** by product — ranks all 24 SKUs by stockout frequency
- **Stockout risk by city** — identifies underserved markets
- **Demand anomaly detection** using Z-score method (|Z| > 2.5 threshold) on daily revenue
- **Overstock risk** — flags products with excess average remaining stock after sales

### 📋 6. Data Explorer
Interactive access to the underlying dataset:
- Filter by city, category, store name, or product name
- Paginated table view (up to 500 rows)
- **Statistical summary** (mean, std, percentiles) for all key numeric columns
- **Revenue distribution histogram**
- **Gross margin distribution histogram**

---

## 🗂️ Repository Structure

```
zambia-retail-dashboard-app/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

> All data is **generated programmatically at runtime** — no external data files required. The synthetic dataset is cached using `@st.cache_data` for fast performance.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Web Framework** | Streamlit 1.35+ |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Time Series** | Statsmodels (ARIMA) |
| **Visualisation** | Plotly Express & Graph Objects |
| **Deployment** | Streamlit Community Cloud |
| **Language** | Python 3.10+ |

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/GIVEN-CHINYAMA/zambia-retail-dashboard-app.git
cd zambia-retail-dashboard-app
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Launch the app**
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

This app is designed for **zero-cost deployment** on Streamlit Community Cloud.

1. **Fork or push** this repository to your GitHub account (must be public)
2. Visit [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **"New app"**
4. Set the following:
   - **Repository:** `your-username/zambia-retail-dashboard-app`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy** — your app will be live in approximately 2 minutes ✅

Your app will receive a public URL in the format:
`https://GIVEN-CHINYAMA/zambia-retail-dashboard-app-xxxx.streamlit.app`

---

## 📊 Dataset Details

The app generates a **synthetic but realistic** retail dataset grounded in Zambian market conditions:

| Attribute | Detail |
|---|---|
| **Records** | 80,000 transactions |
| **Period** | January 2022 – December 2024 |
| **Cities** | Lusaka, Kitwe, Ndola, Livingstone, Chipata, Kabwe, Solwezi |
| **Stores** | ShopRite, Pick n Pay, Choppies, Spar, Melmart, Local Kiosk + more |
| **Products** | 24 SKUs across Staples, Dairy, Protein, HPC, Beverages, Baby Care, Stationery, Telecoms |
| **Currency** | Zambian Kwacha (ZMW) |
| **Seasonality** | December festive peak (+40%), January back-to-school (+25%), dry/rainy season effects |
| **Customers** | ~5,000 simulated repeat customers |

All prices, costs, and demand volumes are calibrated to reflect realistic Zambian retail market conditions.

---

## 🔑 Key Insights Delivered

- Lusaka contributes approximately **38% of national retail revenue**, making it the priority market for distribution and promotions
- **December revenue spikes ~40% above baseline** — requiring proactive stock pre-positioning by October
- **Staples (Mealie Meal, Cooking Oil)** are the highest-revenue categories but carry thin margins — bulk procurement is essential
- Promotions deliver a measurable **revenue lift** while compressing gross margins — selective deployment is recommended
- Approximately **25% of SKUs** carry elevated stockout risk — automated reorder triggers are advised
- **Champions** and **Loyal Regulars** segments account for the majority of customer lifetime value
- **Weekends outperform weekdays** — promotional timing should prioritise Friday–Saturday windows

---

## 🛠️ Features at a Glance

- ✅ Fully interactive sidebar filters (Year, City, Category)
- ✅ All charts update dynamically based on filter selection
- ✅ Dark-themed professional UI with custom CSS
- ✅ Cached data generation for fast load times
- ✅ Graceful fallback if XGBoost is unavailable (uses GradientBoostingRegressor)
- ✅ Zero external data dependencies — fully self-contained

---

## 🔭 Future Enhancements

- [ ] Integrate **real-time POS data** via REST API
- [ ] Add **geospatial heatmaps** using Zambia district shapefiles (Folium / Kepler.gl)
- [ ] Connect to **ZRA or ZamStats** open data APIs for live price benchmarking
- [ ] Incorporate **mobile money transaction signals** (Airtel Money, MTN MoMo) as demand proxies
- [ ] Implement **LSTM deep learning** for longer-horizon demand forecasting
- [ ] Add **user authentication** for multi-retailer access via Streamlit Authenticator

---

## 👤 Author

**Given Chinyama**
Data Scientist | Python · Machine Learning · Business Intelligence

- 🔗 [LinkedIn](https://www.linkedin.com/in/given-chinyama-data)
- 💻 [GitHub](https://github.com/GIVEN-CHINYAMA)
- 📓 [Original Notebook Repository](https://github.com/GIVEN-CHINYAMA/zambia-retail-intelligence-platform)

---

## 📄 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute this code with attribution.

---

<div align="center">

*Built with Python · Deployed on Streamlit Community Cloud · 🇿🇲 Made for Zambia*

</div>


