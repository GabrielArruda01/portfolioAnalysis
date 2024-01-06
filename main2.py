import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

st.title('Portfolio Dashboard')

assets = st.text_input('Digite seus ativos (separado por vírgula', 'AAPL, GOOGL, TSLA, MSFT')
assets_list = assets.split(', ')

# Entrada dos pesos como porcentagens
weights_str = st.text_input('Digite os pesos para cada ativo em porcentagem (separado por vírgula, soma deve ser 100)', '25, 25, 25, 25')

weights_list = [float(x)/100 for x in weights_str.split(', ')]

if sum(weights_list) != 1:
    st.error('A soma dos pesos deve ser igual a 100%.')
else:

    start = st.date_input('Escolha a data de inicio para a análise', value=pd.to_datetime('2020-01-01'))

    data = yf.download(assets, start=start)['Adj Close']

    returns = data.pct_change()
    cumulative_returns = (returns+1).cumprod() - 1
    pf_cumulative_returns = (cumulative_returns*weights_list).sum(axis=1) #calcula a soma ao longo das colunas para cada linha. Isso agrega os retornos ponderados de todas as ações em cada ponto do tempo, resultando no retorno cumulativo do portfólio inteiro.

    benchmark = yf.download('^GSPC', start=start)['Adj Close']
    benchmark_returns = benchmark.pct_change()
    bench_cumulative_returns = (benchmark_returns+1).cumprod() - 1

    Weight = np.array(weights_list)
    Portfolio_std = (Weight.dot(returns.cov()).dot(Weight)) ** (1/2) #desvio padrao do portfolio(risco)

    st.subheader('Portfolio vs Index')

    tog = pd.concat([bench_cumulative_returns, pf_cumulative_returns],axis=1)
    tog.columns=['S&P 500 Performance', 'Portfolio Performance']

    st.line_chart(tog)

    st.subheader('Portfolio Risk:')
    st.write(Portfolio_std)

    st.subheader('Benchmark Risk:')
    bench_risk = benchmark_returns.std()
    st.write(bench_risk)

    st.subheader('Portfolio Composition:')
    fig, ax = plt.subplots(facecolor='#121212')
    ax.pie(Weight, labels=data.columns, autopct='%1.1f',textprops={'color': 'white'})
    st.pyplot(fig)