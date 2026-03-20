import streamlit as st
import pandas as pd
import numpy as np

# --- Data ---
@st.cache_data
def load_data():
    rng = np.random.default_rng(seed=42)
    return pd.DataFrame({
        "month": pd.date_range("2024-01", periods=100, freq="D"),
        "sales": rng.integers(50, 500, 100),
        "category": rng.choice(["Electronics", "Clothing", "Food"], 100)
    })

df = load_data()

# --- Sidebar filter ---
st.title("Sales Dashboard")

categories = st.sidebar.multiselect(
    "Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# --- Filter ---
filtered = df[df["category"].isin(categories)]

# --- KPI cards ---
col1, col2 = st.columns(2)

col1.metric("Total Sales", f"${filtered['sales'].sum():,}")
col2.metric("Avg. Sale",   f"${filtered['sales'].mean():.0f}")

# --- Viz ---
st.bar_chart(filtered.groupby("category")["sales"].sum())
st.dataframe(filtered, use_container_width=True)