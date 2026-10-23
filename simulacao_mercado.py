import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.colors import LinearSegmentedColormap

print("A INICIAR SIMULAÇÃO ...")

# Cores
base = "#17B0B0"
claro = "#97F2F2"
escuro = "#083F3F"
negro = "#031717"
branco = "#E8FCFC"

# ==========================================
# 1. PARÂMETROS GLOBAIS DO MERCADO
# ==========================================
S0 = 171.32           # Preço inicial do ativo
mu = 0.097            # Tendência de crescimento (drift)
sigma = 0.130          # Volatilidade (temperatura/agitação)
T = 1.0              # Horizonte temporal (1 ano)
N_passos = 252       # Resolução (252 dias úteis de trading)
N_simulacoes = 5000  # Número de cenários a simular 

dt = T / N_passos
tempos = np.linspace(0, T, N_passos)

# ==========================================
# 2. MOTOR DE MONTE CARLO (EVOLUÇÃO DO PREÇO)
# ==========================================
print(f"[1/7] A processar Motor de Monte Carlo ({N_simulacoes} trajetórias)...")
precos = np.zeros((N_simulacoes, N_passos))
precos[:, 0] = S0

for t in range(1, N_passos):
    Z = np.random.standard_normal(N_simulacoes)
    precos[:, t] = precos[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
print("      -> Concluído.\n")

# ==========================================
# 3. VISUALIZAÇÃO 1: CENÁRIOS DE MERCADO
# ==========================================
print("[2/7] A gerar Gráfico 1 (Cenários de Mercado)...")
plt.figure(figsize=(10, 6))
for i in range(min(500, N_simulacoes)):
    plt.plot(tempos, precos[i, :], lw=1, alpha=0.08, color=base)

preco_medio = np.mean(precos, axis=0)
plt.plot(tempos, preco_medio, lw=2.5, color=escuro, label='Trajetória Média Esperada')

plt.title('Simulação de Monte Carlo: Movimento Browniano Geométrico')
plt.xlabel('Tempo (Anos)')
plt.ylabel('Preço do Ativo')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('01_trajetorias_mercado.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '01_trajetorias_mercado.png'.\n")

# ==========================================
# 4. VISUALIZAÇÃO 2: DISTRIBUIÇÃO LOGNORMAL (PREÇOS)
# ==========================================
print("[3/7] A gerar Gráfico 2 (Distribuição Lognormal)...")
precos_finais = precos[:, -1] 

plt.figure(figsize=(10, 6))
plt.hist(precos_finais, bins=60, density=True, alpha=0.6, color=base, edgecolor=escuro, label='Simulação Empírica')

x = np.linspace(np.min(precos_finais), np.max(precos_finais), 200)
mu_norm = np.log(S0) + (mu - 0.5 * sigma**2) * T
pdf_lognormal = (1 / (x * sigma * np.sqrt(T * 2 * np.pi))) * np.exp(- (np.log(x) - mu_norm)**2 / (2 * sigma**2 * T))

plt.plot(x, pdf_lognormal, color=negro, lw=2.5, label='Curva Teórica Lognormal')
plt.axvline(S0, color='black', linestyle='--', alpha=0.7, label=f'Preço Inicial (S0 = {S0})')

plt.title('Distribuição Estatística dos Preços Finais')
plt.xlabel('Preço Final do Ativo')
plt.ylabel('Densidade de Probabilidade')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('02_distribuicao_final.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '02_distribuicao_final.png'.\n")

# ==========================================
# 5. ANÁLISE DE MICROESTADOS: RETORNOS LOGARÍTMICOS
# ==========================================
print("[4/7] A gerar Gráfico 3 (Termodinâmica e Retornos)...")
retornos_diarios = np.log(precos[:, 1:] / precos[:, :-1])
todos_retornos = retornos_diarios.flatten() 

plt.figure(figsize=(10, 6))
plt.hist(todos_retornos, bins=100, density=True, alpha=0.6, color=base, edgecolor=escuro, label='Retornos Diários Simulados')

mu_ret = (mu - 0.5 * sigma**2) * dt
sigma_ret = sigma * np.sqrt(dt)
x_ret = np.linspace(np.min(todos_retornos), np.max(todos_retornos), 200)
pdf_normal = (1 / (sigma_ret * np.sqrt(2 * np.pi))) * np.exp(- (x_ret - mu_ret)**2 / (2 * sigma_ret**2))

plt.plot(x_ret, pdf_normal, color=negro, lw=2.5, label='Curva Teórica Normal (Gaussiana)')

plt.title('Termodinâmica do Mercado: Distribuição de Retornos (O Ruído)')
plt.xlabel('Retorno Logarítmico Diário')
plt.ylabel('Densidade')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('03_distribuicao_retornos.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '03_distribuicao_retornos.png'.\n")

# ==========================================
# 6. ANÁLISE DE RISCO: MAXIMUM DRAWDOWN
# ==========================================
print("[5/7] A gerar Gráfico 4 (Maximum Drawdown)...")
picos_acumulados = np.maximum.accumulate(precos, axis=1)
drawdowns = (precos - picos_acumulados) / picos_acumulados
drawdowns_maximos = np.min(drawdowns, axis=1) * 100 

plt.figure(figsize=(10, 6))
plt.hist(drawdowns_maximos, bins=50, density=True, alpha=0.6, color=base, edgecolor=escuro, label='Drawdown Máximo por Cenário')
plt.axvline(np.mean(drawdowns_maximos), color=negro, linestyle='--', lw=2, label=f'Drawdown Médio: {np.mean(drawdowns_maximos):.1f}%')

plt.title('Risco Extremo: Distribuição dos Drawdowns Máximos a 1 Ano')
plt.xlabel('Drawdown Máximo (%)')
plt.ylabel('Densidade')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('04_drawdowns_maximos.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '04_drawdowns_maximos.png'.\n")

# ==========================================
# 7. A CURVA DO TEMPO: 0 DIAS vs 20 ANOS
# ==========================================
print("[6/7] A gerar Gráfico 5 (Probabilidade no Tempo)...")
dias_por_ano = 252
T_dias = np.arange(0, 20 * dias_por_ano + 1)
T_anos = T_dias / dias_por_ano

drift_efetivo = mu - 0.5 * sigma**2
probabilidades_tempo = norm.cdf((drift_efetivo * np.sqrt(T_anos)) / sigma) * 100

plt.figure(figsize=(10, 6))
plt.plot(T_anos, probabilidades_tempo, color='teal', lw=2.5, label='Probabilidade Teórica de Lucro P(S_T > S_0)')
plt.axhline(50, color='black', linestyle='--', alpha=0.7, label='Ruído Estocástico (50%)')

milestones = {
    '1 Dia': 1,
    '1 Semana': 5,
    '1 Mês': 21,
    '1 Ano': 252,
    '10 Anos': 252*10,
    '20 Anos': 252*20
}

# Gradiente contínuo na escala Teal (do turquesa claro ao azul-petróleo escuro)
cores_milestones = [branco, claro, base, "#108888", "#054243", negro]

for (label, dias), cor in zip(milestones.items(), cores_milestones):
    idx = min(dias, len(T_anos) - 1) 
    prob = probabilidades_tempo[idx]
    tempo = T_anos[idx]
    
    # Repara no color=cor aqui em baixo:
    plt.scatter(tempo, prob, color=cor, s=30, zorder=5, edgecolor=negro, lw=0.6, label=f'{label}: {prob:.1f}%')

plt.xlim(-0.8, 20.8)
plt.ylim(bottom=48, top=102)

plt.title('O Paradoxo do Day Trading: Probabilidade de Lucro vs Horizonte Temporal')
plt.xlabel('Horizonte Temporal $T$ (Anos)')
plt.ylabel('Probabilidade de Lucro (%)')
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.savefig('05_probabilidade_lucro_tempo.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '05_probabilidade_lucro_tempo.png'.\n")

# ==========================================
# 8. A ESCALA MICROSCÓPICA: SINAL VS RUÍDO
# ==========================================
print("[7/7] A gerar Gráfico 6 (Colapso Termodinâmico: Sinal vs Ruído)...")
minutos_por_ano = 252 * 6.5 * 60
t_minutos = np.logspace(0, np.log10(10 * minutos_por_ano), 500)
t_anos_array = t_minutos / minutos_por_ano

drift_efetivo = np.abs(mu - 0.5 * sigma**2)
magnitude_sinal = drift_efetivo * t_anos_array
magnitude_ruido = sigma * np.sqrt(t_anos_array)

plt.figure(figsize=(10, 6))

# Sinal em Teal Escuro e Ruído em Teal Claro (Turquesa) para criar contraste direto
plt.plot(t_anos_array, magnitude_sinal, color=escuro, lw=2.5, label=r'Sinal Económico ($\mu t$) - Crescimento Linear')
plt.plot(t_anos_array, magnitude_ruido, color=claro, lw=2.5, label=r'Ruído Estocástico ($\sigma \sqrt{t}$) - Raiz Quadrada')

plt.xscale('log')
plt.yscale('log')

# Ponto de Transição de Regime (Tempo Crítico) em destaque vibrante
tempo_critico = (sigma / drift_efetivo)**2
magnitude_critica = sigma * np.sqrt(tempo_critico)
plt.scatter(tempo_critico, magnitude_critica, color=escuro, s=30, zorder=5, alpha=0.8, label=f'Tempo Crítico ($t^*$ = {tempo_critico:.2f} Anos)')
plt.axvline(tempo_critico, color='darkslategray', linestyle=':', alpha=0.8)

marcos = {
    '1 Minuto': 1 / minutos_por_ano,
    '1 Dia': 1 / 252,
    '1 Ano': 1,
    '10 Anos': 10
}

for label, t_val in marcos.items():
    plt.axvline(t_val, color='gray', linestyle='--', alpha=0.4)
    plt.text(t_val * 1.1, np.min(magnitude_sinal), label, rotation=90, verticalalignment='bottom', color='black', alpha=0.8)

plt.title('Colapso Termodinâmico do Day Trading: Sinal vs Ruído')
plt.xlabel('Horizonte Temporal (Escala Logarítmica de Anos)')
plt.ylabel('Magnitude da Força no Preço')
plt.legend(loc='upper left')
plt.grid(alpha=0.2, which='both')
plt.savefig('06_sinal_vs_ruido.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '06_sinal_vs_ruido.png'.\n")
print("Simulação Concluída.\n")