# retail-storytelling
# 🛍️ Retail Data Storytelling Dashboard

> A production-grade, five-chapter Business Intelligence narrative built with **Streamlit**, **Pandas**, **NumPy**, and **Plotly** — turning raw retail transaction data into executive-ready strategic insights.

---

## 📖 Project Overview

Most dashboards show numbers. This application **tells a story**.

Following a structured five-step narrative framework, the dashboard guides the user from raw data exploration through visual analysis to automated insights and strategic recommendations — mimicking the workflow of a professional data storytelling presentation.

```
A. Introduction  →  B. EDA  →  C. Visual Storytelling  →  D. Insights  →  E. Conclusion
```

---

## ✨ Features

| Category | Details |
|---|---|
| **Storytelling** | 5-step guided narrative (Introduction → Conclusion) |
| **KPI Dashboard** | Total Sales, Profit, Orders, Margin — live & filtered |
| **Sidebar Filters** | Year · Region · Category — all charts update dynamically |
| **EDA** | Shape, types, missing values, stats, distributions, sample data, correlations |
| **Visualisations** | 15 interactive Plotly charts including bubble maps & choropleth |
| **Auto-Insights** | 12 key insights, 7 findings, 7 recommendations — all data-driven |
| **Conclusion** | Health scorecard, strategic roadmap, executive summary |
| **Design** | Gradient heroes, card UI, Syne + DM Sans typography, dark sidebar |

---

## 📁 Repository Structure

```
retail_storytelling/
│
├── app.py                  # Main Streamlit application (5-step narrative)
├── insights.py             # BI engine: KPIs, insights, findings, recommendations
├── generate_data.py        # Synthetic dataset generator (run once)
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── data/
│   └── dataset.csv         # 2 000-row retail transactions (2020–2023)
│
└── assets/
    └── output.png          # Dashboard screenshot
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone / download the project
git clone https://github.com/your-org/retail-storytelling.git
cd retail-storytelling

# 2. Create & activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the dataset (if data/dataset.csv is missing)
python generate_data.py

# 5. Launch the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 🧭 Usage Guide

| Sidebar Control | Effect |
|---|---|
| **Year filter** | Restrict data to one or more years (2020–2023) |
| **Region filter** | Focus on East · West · Central · South |
| **Category filter** | Technology · Furniture · Office Supplies |
| **Navigation radio** | Jump directly to any of the 5 story steps |

All charts, KPI cards, and automated insights update instantly when filters change.

---

## 📊 Dataset Information

| Attribute | Value |
|---|---|
| **Source** | Synthetically generated (see `generate_data.py`) |
| **Rows** | 2 000 |
| **Columns** | 22 |
| **Date range** | 2020-01-01 → 2023-12-31 |
| **Regions** | East, West, Central, South |
| **Categories** | Technology, Furniture, Office Supplies |
| **Segments** | Consumer, Corporate, Home Office |
| **Cities** | 24 major US cities |

### Key columns

| Column | Type | Description |
|---|---|---|
| `order_id` | str | Unique order identifier |
| `order_date` | date | Transaction date |
| `segment` | str | Customer segment |
| `region` | str | Geographic region |
| `category` | str | Product category |
| `product_name` | str | Product |
| `sales` | float | Revenue (post-discount) |
| `profit` | float | Net profit |
| `quantity` | int | Units sold |
| `discount` | float | Discount rate (0–1) |
| `profit_margin` | float | Profit / Sales ratio |
| `latitude` | float | City latitude (jittered) |
| `longitude` | float | City longitude (jittered) |

---

## 🚀 Deployment

### Streamlit Community Cloud (free)

1. Push the repo to GitHub (include `data/dataset.csv`).
2. Visit [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set `app.py` as the entry point.
4. Click **Deploy** — the app is live in ~2 minutes.

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t retail-story .
docker run -p 8501:8501 retail-story
```

### Heroku / Railway / Render

Add a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## 🔮 Future Enhancements

| Priority | Enhancement |
|---|---|
| 🔴 High | **ML Forecasting** — ARIMA/Prophet 90-day sales prediction |
| 🔴 High | **Anomaly Detection** — real-time flagging of unusual orders |
| 🟡 Medium | **ERP Integration** — live SAP/Oracle sync via REST API |
| 🟡 Medium | **Automated PDF Reports** — scheduled executive digests |
| 🟢 Low | **Mobile App** — React Native companion for field sales |
| 🟢 Low | **Multi-currency** — international market support |

---

## 🛠️ Tech Stack

| Library | Version | Role |
|---|---|---|
| Streamlit | ≥ 1.32 | Web UI framework |
| Pandas | ≥ 2.0 | Data manipulation |
| NumPy | ≥ 1.26 | Numerical operations |
| Plotly | ≥ 5.19 | Interactive visualisations |
| Statsmodels | ≥ 0.14 | OLS trendlines in scatter plots |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

Inspired by professional BI storytelling frameworks used in management consulting and corporate strategy teams. Data is entirely synthetic and does not represent any real company.

---

*Built with ❤️ using Python · Streamlit · Pandas · NumPy · Plotly*
