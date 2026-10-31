import yfinance as yf
import numpy as np

# 1. Extrair os dados do Yahoo Finance (ex: S&P 500 ETF, últimos 5 anos)
ticker = "VWCE.DE"
dados = yf.download(ticker, period="5y")
precos_fecho = dados['Close'].values

# 2. Calcular os microestados (retornos logarítmicos diários)
retornos = np.log(precos_fecho[1:] / precos_fecho[:-1])

# 3. Calcular a Termodinâmica Anualizada (252 dias úteis)
sigma_diario = np.std(retornos)
mu_diario = np.mean(retornos)

# Escalar para o macroestado anual
sigma_anual = sigma_diario * np.sqrt(252)
mu_anual = (mu_diario + 0.5 * sigma_diario**2) * 252 # Drift de Itô

print(f"Ativo: {ticker}")
print(f"Advecção / Drift (\u03bc): {mu_anual:.6f} ({mu_anual*100:.2f}% ao ano)")
print(f"Volatilidade (\u03c3): {sigma_anual:.6f} ({sigma_anual*100:.2f}% ao ano)")