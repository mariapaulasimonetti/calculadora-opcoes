import streamlit as st
import numpy as np
from scipy.stats import norm

# Black-Scholes (CALL)
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

# Volatilidade implícita com bisseção
def implied_vol_bissecao(S, K, T, r, market_price, tol=1e-6, max_iter=100):
    sigma_min = 0.0001
    sigma_max = 5.0
    for _ in range(max_iter):
        sigma_mid = (sigma_min + sigma_max) / 2
        price = black_scholes_call(S, K, T, r, sigma_mid)
        diff = price - market_price
        if abs(diff) < tol:
            return sigma_mid
        if diff > 0:
            sigma_max = sigma_mid
        else:
            sigma_min = sigma_mid
    return np.nan

st.title("Calculadora de Opções e Volatilidade Implícita")

tipo_opcao = st.selectbox("Tipo de opção", ["Europeia (Call)", "Americana (simples)", "Asiática (simples)"])
S = st.number_input("Preço do ativo (S)", value=100.0)
K = st.number_input("Strike (K)", value=100.0)
T = st.number_input("Tempo até vencimento (em anos)", value=0.5)
r = st.number_input("Taxa de juros (%)", value=5.0) / 100
preco_mercado = st.number_input("Preço de mercado da opção", value=7.0)

if st.button("Calcular"):
    if tipo_opcao == "Europeia (Call)":
        preco_teorico = black_scholes_call(S, K, T, r, 0.2)
        vol_impl = implied_vol_bissecao(S, K, T, r, preco_mercado)
        st.write(f"Preço teórico da CALL (vol=20%): {preco_teorico:.2f}")
        st.write(f"Volatilidade implícita: {vol_impl:.4f}")
    else:
        st.warning("Modelo para opções Americanas e Asiáticas ainda não implementado.")