import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

st.title('Portfolio Dashboard')

assets = st.text_input('Digite seus ativos (separado por vírgula', 'AAPL, GOOGL, TSLA, MSFT')

start = st.date_input('Escolha a data de inicio para a análise', value=pd.to_datetime('2020-01-01'))

data = yf.download(assets, start=start)['Adj Close']

returns = data.pct_change()
cumulative_returns = (returns+1).cumprod() - 1
pf_cumulative_returns = cumulative_returns.mean(axis=1) #usa o eixo das colunas para fazer a média dos ativos com pesos iguais

benchmark = yf.download('^GSPC', start=start)['Adj Close']
benchmark_returns = benchmark.pct_change()
bench_cumulative_returns = (benchmark_returns+1).cumprod() - 1

Weight = (np.ones(len(returns.cov())) / len(returns.cov()))
Portfolio_std = (Weight.dot(returns.cov()).dot(Weight)) ** (1/2) #desvio padrao do portfolio(risco)

st.subheader('Portfolio vs Index')

tog = pd.concat([bench_cumulative_returns, pf_cumulative_returns],axis=1)
tog.columns=['S&P 500 Performance', 'Portfolio Performance']

st.line_chart(tog)

st.subheader('Portfolio Risk:')
Portfolio_std

st.subheader('Benchmark Risk:')
bench_risk = benchmark_returns.std()
bench_risk

st.subheader('Portfolio Composition:')
fig, ax = plt.subplots(facecolor='#121212')
ax.pie(Weight, labels=data.columns, autopct='%1.1f',textprops={'color': 'white'})
st.pyplot(fig)