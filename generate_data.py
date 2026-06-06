"""Script to generate a realistic retail dataset for the storytelling app."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────────
N_ROWS = 2000
START_DATE = datetime(2020, 1, 1)
END_DATE   = datetime(2023, 12, 31)

REGIONS = {
    "East":  [("New York","NY",40.71,-74.01),("Philadelphia","PA",39.95,-75.16),
               ("Boston","MA",42.36,-71.06),("Baltimore","MD",39.29,-76.61),
               ("Charlotte","NC",35.23,-80.84),("Jacksonville","FL",30.33,-81.65)],
    "West":  [("Los Angeles","CA",34.05,-118.24),("San Francisco","CA",37.77,-122.42),
               ("Seattle","WA",47.61,-122.33),("Denver","CO",39.74,-104.98),
               ("Phoenix","AZ",33.45,-112.07),("Las Vegas","NV",36.17,-115.14)],
    "Central":[("Chicago","IL",41.85,-87.65),("Dallas","TX",32.78,-96.80),
               ("Houston","TX",29.76,-95.37),("Minneapolis","MN",44.98,-93.27),
               ("Kansas City","MO",39.10,-94.58),("St. Louis","MO",38.63,-90.20)],
    "South": [("Atlanta","GA",33.75,-84.39),("Miami","FL",25.77,-80.19),
               ("Nashville","TN",36.17,-86.78),("Austin","TX",30.27,-97.74),
               ("New Orleans","LA",29.95,-90.07),("Memphis","TN",35.15,-90.05)],
}

CATEGORIES = {
    "Technology": ["Laptops","Smartphones","Tablets","Monitors","Printers",
                   "Keyboards","Mice","Headphones","Cameras","Smartwatches"],
    "Furniture":  ["Office Chairs","Desks","Bookshelves","Filing Cabinets",
                   "Sofas","Conference Tables","Standing Desks","Lamps","Rugs","Wardrobes"],
    "Office Supplies":["Pens","Notebooks","Staplers","Paper Reams","Binders",
                       "Sticky Notes","Scissors","Tape","Folders","Envelopes"],
}

SEGMENTS = ["Consumer","Corporate","Home Office"]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# ── Build rows ─────────────────────────────────────────────────────────────────
rows = []
order_counter = 10000

for _ in range(N_ROWS):
    region = random.choice(list(REGIONS.keys()))
    city_info = random.choice(REGIONS[region])
    city, state, lat, lon = city_info

    category = random.choice(list(CATEGORIES.keys()))
    product  = random.choice(CATEGORIES[category])
    segment  = random.choice(SEGMENTS)

    order_date = random_date(START_DATE, END_DATE)
    ship_date  = order_date + timedelta(days=random.randint(1, 7))

    quantity = random.randint(1, 20)
    base_price = {
        "Technology": random.uniform(50, 1500),
        "Furniture":  random.uniform(30, 800),
        "Office Supplies": random.uniform(5, 80),
    }[category]

    discount = random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50])
    unit_price = round(base_price, 2)
    sales = round(unit_price * quantity * (1 - discount), 2)

    base_margin = {"Technology": 0.22, "Furniture": 0.30, "Office Supplies": 0.40}[category]
    margin_noise = np.random.normal(0, 0.05)
    discount_drag = discount * 0.8
    profit_margin = base_margin + margin_noise - discount_drag
    profit = round(sales * profit_margin, 2)

    order_counter += random.randint(1, 5)
    order_id = f"ORD-{order_counter}"
    customer_id = f"CUST-{random.randint(10000,99999)}"

    rows.append({
        "order_id": order_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "ship_date": ship_date.strftime("%Y-%m-%d"),
        "customer_id": customer_id,
        "segment": segment,
        "city": city,
        "state": state,
        "region": region,
        "category": category,
        "product_name": product,
        "sales": sales,
        "quantity": quantity,
        "discount": discount,
        "profit": profit,
        "unit_price": unit_price,
        "latitude": round(lat + np.random.normal(0, 0.3), 4),
        "longitude": round(lon + np.random.normal(0, 0.3), 4),
    })

df = pd.DataFrame(rows)
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"]  = pd.to_datetime(df["ship_date"])
df["year"]   = df["order_date"].dt.year
df["month"]  = df["order_date"].dt.month
df["quarter"]= df["order_date"].dt.quarter
df["month_name"] = df["order_date"].dt.strftime("%b")
df["profit_margin"] = (df["profit"] / df["sales"]).round(4)

df.to_csv("data/dataset.csv", index=False)
print(f"✅  Dataset saved → data/dataset.csv  ({len(df)} rows × {len(df.columns)} cols)")
