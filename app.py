import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text, URL


USER = "readonly_user.tyxjmbptftftcqgozyfc"
PASSWORD = "your_secure_password"
HOST = "aws-1-us-east-1.pooler.supabase.com"
PORT = "6543"
DBNAME = "postgres"

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# --- Data ---
@st.cache_data
def load_country_data():
    q2 = """
    SELECT billing_country AS country,
           COUNT(*)          AS invoice_count,
           ROUND(SUM(total)::numeric, 2) AS total_spent
    FROM invoice
    GROUP BY billing_country
    ORDER BY total_spent DESC
    LIMIT 15
    """
    return pd.read_sql(q2, con=engine)

df_countries = load_country_data()


# --- Sidebar filter ---
st.title("Sales Dashboard")

countries = st.sidebar.multiselect(
    "Country",
    options=df_countries["country"].unique(),
    default=df_countries["country"].unique()
)

# --- Filter ---
filtered = df_countries[df_countries["country"].isin(countries)]

g = sns.catplot(
    data    = filtered,
    x       = 'total_spent',
    y       = 'country',
    kind    = 'bar',
    palette = 'viridis',
    height  = 6,
    aspect  = 1.4
)

st.pyplot(g)