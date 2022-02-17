import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(layout="wide")

portfolio = pd.read_csv('quotes.csv')
portfolio = portfolio.sort_values(by=['Trade Date']).reset_index()
portfolio['Value'] = portfolio['Current Price'] * portfolio['Quantity']
portfolio['Purchase Value'] = portfolio['Purchase Price'] * portfolio['Quantity']
portfolio[portfolio['Symbol'] == 'ETH-USD']['Volume'] = 0
portfolio.drop(index=18, inplace=True)

padleft, col1, col2, padright = st.columns([1, 4, 4, 1])
with padleft:
    st.empty()
with padright:
    st.empty()

n = st.sidebar.selectbox(
    "How many datapoint?",
    (100, 200, 300)
)


c = alt.Chart(portfolio).mark_point().encode(
    x='Value',
    y='Purchase Value',
    size='Volume',
    tooltip='Symbol'
).properties(
    height=600
)

line = pd.DataFrame({
    'x': [0, 2e3],
    'y': [0, 2e3]
})

line_plot = alt.Chart(line).mark_line(color= 'red').encode(
    x= 'x',
    y= 'y')

with col1:
    st.altair_chart(c, use_container_width=True)

#==========================

with col2:
    live = st.empty()
import time

exp = 2


for i in range(n):
    df = pd.DataFrame({'x': range(i), 'y':np.arange(i)**exp})
    l = alt.Chart(df).mark_line().encode(x='x:Q', y='y:Q').properties(height=400)
    live.altair_chart(l, use_container_width=True)
    time.sleep(0.1)
