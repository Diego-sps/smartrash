import streamlit as st
import matplotlib.pyplot as plt
from numpy.random import default_rng as rng
import pandas as pd

st.title("Dashboard Mensal")

plt.figure(figsize=(10, 6))
df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])
st.line_chart(df)