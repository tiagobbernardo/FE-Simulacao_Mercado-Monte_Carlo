import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import entropy

print("\nA INICIAR SIMULAÇÃO ...\n")

# Cores
base = "#17B0B0"
claro = "#97F2F2"
escuro = "#083F3F"
negro = "#031717"
branco = "#E8FCFC"

# ==========================================
# 1. PARÂMETROS GLOBAIS DO MERCADO
# ==========================================
S0 = 171.32                     # Preço inicial do ativo
mu = 0.097                      # Tendência de crescimento (drift)
sigma = 0.130                   # Volatilidade (temperatura/agitação)
T = 1                           # Horizonte temporal
dias_uteis = 252                # Dias úteis do mercado financeiro
N_passos = int(dias_uteis*T)    # Resolução
N_simulacoes = 5000             # Número de cenários a simular 

dt = T / N_passos

# Regimes Termodinâmicos (Expoentes de Hurst)
H_sub = 0.25  # Subdifusão (Reversão à Média)
H_norm = 0.50 # Difusão Normal (Browniano Clássico)
H_sup = 0.75  # Superdifusão (Inércia/Manada)

# ==========================================
# 2. MOTOR DE MONTE CARLO (3 REGIMES - CHOLESKY)
# ==========================================
print(f"[1/13] A processar Motor de Monte Carlo (3 Regimes x {N_simulacoes} trajetórias)...")

rng = np.random.RandomState(42)
Z = rng.standard_normal((N_passos, N_simulacoes))
Z[0, :] = 0

def gerar_universos_fbm(H, S0, mu, sigma, T, N_passos, Z):
    t = np.linspace(0, T, N_passos)
    t_power = t**(2*H)
    Cov = 0.5 * (
        t_power[:, np.newaxis]
        + t_power[np.newaxis, :]
        - np.abs(t[:, np.newaxis] - t[np.newaxis, :])**(2*H)
    )
    Cov += np.eye(N_passos) * 1e-8 # Estabilidade numérica
    L = np.linalg.cholesky(Cov)

    W_H = np.dot(L, Z).T
    
    t_matrix = t.reshape(1, -1)
    precos = S0 * np.exp(mu * t_matrix - 0.5 * (sigma**2) * (t_matrix**(2*H)) + sigma * W_H)
    return t, precos

tempos, precos_sub  = gerar_universos_fbm(H_sub, S0, mu, sigma, T, N_passos, Z)
_, precos_norm = gerar_universos_fbm(H_norm, S0, mu, sigma, T, N_passos, Z)
_, precos_sup  = gerar_universos_fbm(H_sup, S0, mu, sigma, T, N_passos, Z)

# O modelo normal abastece os gráficos clássicos
precos = precos_norm 
print("      -> Concluído.\n")

# ==========================================
# 3. VISUALIZAÇÃO 1: CENÁRIOS DE MERCADO
# ==========================================
print("[2/13] A gerar Gráfico 1 (Cenários de Mercado)...")
plt.figure(figsize=(10, 6))
plt.plot(tempos, precos[:min(500, N_simulacoes), :].T, lw=1, alpha=0.08, color=base)

plt.xlim(0, T)
preco_medio = np.mean(precos, axis=0)
plt.plot(tempos, preco_medio, lw=2.5, color=escuro, label='Trajetória Média Esperada')

plt.title('Simulação de Monte Carlo: Movimento Browniano Geométrico')
plt.xlabel('Tempo (Anos)')
plt.ylabel('Preço do Ativo')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('Gráficos/01_trajetorias_mercado.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '01_trajetorias_mercado.png'.\n")

# ==========================================
# 4. VISUALIZAÇÃO 2: DISTRIBUIÇÃO LOGNORMAL (PREÇOS)
# ==========================================
print("[3/13] A gerar Gráfico 2 (Distribuição Lognormal)...")
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
plt.savefig('Gráficos/02_distribuicao_final.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '02_distribuicao_final.png'.\n")

# ==========================================
# 5. ANÁLISE DE MICROESTADOS: RETORNOS LOGARÍTMICOS
# ==========================================
print("[4/13] A gerar Gráfico 3 (Termodinâmica e Retornos)...")
retornos_diarios = np.log(precos[:, 1:] / precos[:, :-1])
todos_retornos = retornos_diarios.ravel()

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
plt.savefig('Gráficos/03_distribuicao_retornos.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '03_distribuicao_retornos.png'.\n")

# ==========================================
# 6. ANÁLISE DE RISCO: MAXIMUM DRAWDOWN (OS 3 REGIMES)
# ==========================================
print("[5/13] A gerar Gráfico 4 (Maximum Drawdown Comparativo)...")
def calcular_drawdowns(matriz):
    picos = np.maximum.accumulate(matriz, axis=1)
    dds = (matriz - picos) / picos
    return np.min(dds, axis=1) * 100 

dd_sub = calcular_drawdowns(precos_sub)
dd_norm = calcular_drawdowns(precos_norm)
dd_sup = calcular_drawdowns(precos_sup)

plt.figure(figsize=(10, 6))
plt.hist(dd_sub, bins=50, density=True, histtype='step', lw=2.5, color=claro, label=f'Subdifusão (Méd: {np.mean(dd_sub):.1f}%)')
plt.hist(dd_norm, bins=50, density=True, histtype='step', lw=2.5, color=base, label=f'Normal (Méd: {np.mean(dd_norm):.1f}%)')
plt.hist(dd_sup, bins=50, density=True, histtype='step', lw=2.5, color=escuro, label=f'Superdifusão (Méd: {np.mean(dd_sup):.1f}%)')

plt.title('Impacto da Memória no Risco: Distribuição dos Drawdowns Máximos')
plt.xlabel('Drawdown Máximo (%)')
plt.ylabel('Densidade')
plt.legend(loc='upper left')
plt.grid(alpha=0.3)
plt.savefig('Gráficos/04_drawdowns_maximos.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '04_drawdowns_maximos.png'.\n")

# ==========================================
# 7. A CURVA DO TEMPO: 0 DIAS vs 20 ANOS
# ==========================================
print("[6/13] A gerar Gráfico 5 (Probabilidade no Tempo)...")
T_dias = np.arange(0, 20 * 252 + 1)
T_anos = T_dias / 252

drift_efetivo = mu - 0.5 * sigma**2
probabilidades_tempo = norm.cdf((drift_efetivo * np.sqrt(T_anos)) / sigma) * 100

plt.figure(figsize=(10, 6))
plt.plot(T_anos, probabilidades_tempo, color='teal', lw=2.5, label='Probabilidade Teórica de Lucro P(S_T > S_0)')
plt.axhline(50, color='black', linestyle='--', alpha=0.7, label='Ruído Estocástico (50%)')

milestones = {
    '1 Dia': 1, '1 Semana': 5, '1 Mês': 21,
    '1 Ano': 252, '10 Anos': 252*10, '20 Anos': 252*20
}

cores_milestones = [branco, claro, base, "#108888", "#054243", negro]

for (label, dias), cor in zip(milestones.items(), cores_milestones):
    idx = min(dias, len(T_anos) - 1) 
    prob = probabilidades_tempo[idx]
    tempo = T_anos[idx]
    plt.scatter(tempo, prob, color=cor, s=30, zorder=5, edgecolor=negro, lw=0.6, label=f'{label}: {prob:.1f}%')

plt.xlim(-0.8, 20.8)
plt.ylim(bottom=48, top=102)

plt.title('O Paradoxo do Day Trading: Probabilidade de Lucro vs Horizonte Temporal')
plt.xlabel('Horizonte Temporal $T$ (Anos)')
plt.ylabel('Probabilidade de Lucro (%)')
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.savefig('Gráficos/05_probabilidade_lucro_tempo.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '05_probabilidade_lucro_tempo.png'.\n")

# ==========================================
# 8. A ESCALA MICROSCÓPICA: SINAL VS RUÍDO (3 REGIMES)
# ==========================================
print("[7/13] A gerar Gráfico 6 (Colapso Termodinâmico: Sinal vs Ruído)...")
minutos_por_ano = 252 * 6.5 * 60
t_minutos = np.logspace(0, np.log10(10 * minutos_por_ano), 500)
t_anos_array = t_minutos / minutos_por_ano

drift_efetivo = np.abs(mu - 0.5 * sigma**2)
magnitude_sinal = drift_efetivo * t_anos_array

ruido_sub = sigma * (t_anos_array**H_sub)
ruido_norm = sigma * (t_anos_array**H_norm)
ruido_sup = sigma * (t_anos_array**H_sup)

plt.figure(figsize=(10, 6))

plt.plot(t_anos_array, magnitude_sinal, color=negro, lw=2.5, label=r'Sinal Advectivo ($\mu t$)')
plt.plot(t_anos_array, ruido_sub, color=claro, lw=2.5, linestyle='--', label=r'Ruído Subdifusivo ($\sigma t^{0.25}$)')
plt.plot(t_anos_array, ruido_norm, color=base, lw=2.5, linestyle='--', label=r'Ruído Normal ($\sigma t^{0.50}$)')
plt.plot(t_anos_array, ruido_sup, color=escuro, lw=2.5, linestyle='--', label=r'Ruído Superdifusivo ($\sigma t^{0.75}$)')

plt.xscale('log')
plt.yscale('log')
plt.xlim(left=t_anos_array[0] * 0.5, right=t_anos_array[-1] * 1.5)

# NOVOS CONTROLOS DE POSIÇÃO
# Valores < 1 movem o texto para a esquerda da linha pontilhada, > 1 movem para a direita
desvios_x = [0.75, 1.15, 1.15] 
# Mantém todos os textos exatamente na mesma altura relativa
alturas_y = [0.10, 0.10, 0.10] 

# Tempos Críticos com ajuste individual de posição
for H, cor, nome, dev_x, alt_y in zip([H_sub, H_norm, H_sup], [claro, base, escuro], ["Sub", "Norm", "Sup"], desvios_x, alturas_y):
    t_critico = (sigma / drift_efetivo)**(1 / (1 - H))
    mag_critica = drift_efetivo * t_critico
    
    plt.scatter(t_critico, mag_critica, color=cor, s=30, edgecolor='darkslategray', zorder=5, alpha=0.8)
    plt.axvline(t_critico, color=cor, linestyle=':', alpha=0.8)
    
    # Aplicamos o dev_x e alt_y calculados
    plt.text(t_critico * dev_x, mag_critica * alt_y, f'$t^*$ {nome}: {t_critico:.1f} Anos', 
             color=cor, weight='bold', rotation=90, va='top')

plt.title('Colapso Termodinâmico do Day Trading: Sinal vs Ruído')
plt.xlabel('Horizonte Temporal (Escala Logarítmica de Anos)')
plt.ylabel('Magnitude da Força no Preço')
plt.legend(loc='upper left')
plt.grid(alpha=0.2, which='both')
plt.savefig('Gráficos/06_sinal_vs_ruido.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '06_sinal_vs_ruido.png'.\n")

# ==========================================
# 9. A ESCALA MACROSCÓPICA: TRAJETÓRIA COMPARATIVA
# ==========================================
print("[8/13] A gerar Gráfico 7 (Trajetória de Partícula Única)...")
plt.figure(figsize=(10, 6))

plt.plot(tempos, precos_sub[0, :], color=claro, lw=2.5, label='Subdifusão: Reversão / Mola')
plt.plot(tempos, precos_norm[0, :], color=base, lw=2.0, alpha=0.8, linestyle='--', label='Normal: Difusão Padrão')
plt.plot(tempos, precos_sup[0, :], color=escuro, lw=2.5, linestyle=':', label='Superdifusão: Tendência / Inércia')

plt.xlim(0, T)
plt.title('Dinâmica Fora do Equilíbrio: A Mesma Partícula em 3 Regimes')
plt.xlabel('Tempo (Anos)')
plt.ylabel('Preço do Ativo ($S_t$)')
plt.legend(loc='upper left')
plt.grid(alpha=0.3)
plt.savefig('Gráficos/07_difusao_fracionaria.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '07_difusao_fracionaria.png'.\n")

# ==========================================
# 10. A ESCALA DE KRAMERS: TEMPOS DE PRIMEIRA PASSAGEM
# ==========================================
print("[9/13] A gerar Gráfico 8 (Tempos de Primeira Passagem / Fuga de Kramers)...")

# Definir os limites do "Poço de Potencial" (Fronteiras Absorventes)
limite_sup = S0 * 1.30  # +30% (Take-Profit / Escape Superior)
limite_inf = S0 * 0.80  # -20% (Stop-Loss / Escape Inferior)

def analisar_primeiras_colisoes(matriz_precos, tempos_array):
    colisoes = (matriz_precos >= limite_sup) | (matriz_precos <= limite_inf)
    colidiu = np.any(colisoes, axis=1)
    indices_fuga = np.argmax(colisoes, axis=1)
    indices_colisoes = np.flatnonzero(colidiu)

    tempos_fuga = tempos_array[indices_fuga[colidiu]]
    precos_fuga = matriz_precos[indices_colisoes, indices_fuga[colidiu]]
    taxa_lucro = np.count_nonzero(precos_fuga >= limite_sup) / len(matriz_precos) * 100
    taxa_ruina = np.count_nonzero(precos_fuga <= limite_inf) / len(matriz_precos) * 100
    taxa_sobrevivencia = 100 - (np.sum(colidiu) / len(matriz_precos) * 100)

    return tempos_fuga, taxa_sobrevivencia, taxa_lucro, taxa_ruina

fuga_sub, surv_sub, l_sub, r_sub = analisar_primeiras_colisoes(precos_sub, tempos)
fuga_norm, surv_norm, l_norm, r_norm = analisar_primeiras_colisoes(precos_norm, tempos)
fuga_sup, surv_sup, l_sup, r_sup = analisar_primeiras_colisoes(precos_sup, tempos)
s_sub = 100 - (l_sub + r_sub)
s_norm = 100 - (l_norm + r_norm)
s_sup = 100 - (l_sup + r_sup)

plt.figure(figsize=(10, 6))

plt.hist(fuga_sub, bins=50, density=True, histtype='step', lw=2.5, color=claro, 
         label=f'Subdifusão (Presas no poço: {surv_sub:.1f}%)')
plt.hist(fuga_norm, bins=50, density=True, histtype='step', lw=2.5, color=base, 
         label=f'Normal (Presas no poço: {surv_norm:.1f}%)')
plt.hist(fuga_sup, bins=50, density=True, histtype='step', lw=2.5, color=escuro, 
         label=f'Superdifusão (Presas no poço: {surv_sup:.1f}%)')

plt.axvline(np.mean(fuga_sub) if len(fuga_sub) > 0 else 0, color=claro, linestyle=':', alpha=0.8)
plt.axvline(np.mean(fuga_norm) if len(fuga_norm) > 0 else 0, color=base, linestyle=':', alpha=0.8)
plt.axvline(np.mean(fuga_sup) if len(fuga_sup) > 0 else 0, color=escuro, linestyle=':', alpha=0.8)

plt.title('Problema de Fuga de Kramers: Tempos de Primeira Passagem')
plt.xlabel('Tempo Estocástico de Fuga (Anos)')
plt.ylabel('Densidade de Colisões (Taxa de Escape)')
plt.legend(loc='upper right')
plt.grid(alpha=0.3)
plt.xlim(0, T)

plt.savefig('Gráficos/08_fuga_kramers.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '08_fuga_kramers.png'.\n")

# ==========================================
# 11. O DESTINO DAS PARTÍCULAS (PROFIT VS LOSS)
# ==========================================
print("[10/13] A gerar Gráfico 9 (Análise de Destino: Profit vs Loss)...")

plt.figure(figsize=(10, 6))

regimes = ['Subdifusão\n(Alta Fricção)', 'Difusão Normal\n(Padrão)', 'Superdifusão\n(Inércia)']
lucros = [l_sub, l_norm, l_sup]
ruinas = [r_sub, r_norm, r_sup]
sobrev = [s_sub, s_norm, s_sup]

largura = 0.55

# Construção das Barras Empilhadas
plt.bar(regimes, lucros, largura, label='Escape Superior (+30% Profit)', color=escuro, edgecolor=negro)
plt.bar(regimes, ruinas, largura, bottom=lucros, label='Escape Inferior (-20% Loss)', color=base, edgecolor=negro)
plt.bar(regimes, sobrev, largura, bottom=np.array(lucros)+np.array(ruinas), label='Sobrevivência (Presas)', color=branco, edgecolor=negro)

# Inserção das legendas numéricas dinâmicas
for i in range(3):
    # 1. Label de Profit (Barra inferior escura)
    if lucros[i] > 0.5:
        plt.text(i, lucros[i]/2, f"{lucros[i]:.1f}%", ha='center', va='center', color=branco, weight='bold')
    
    # 2. Label de Loss (Barra do meio clara)
    if ruinas[i] >= 5:
        # Se for grande o suficiente, imprime ao centro (ex: Subdifusão)
        plt.text(i, lucros[i] + ruinas[i]/2, f"{ruinas[i]:.1f}%", ha='center', va='center', color=negro, weight='bold')
    elif ruinas[i] > 0:
        # Se for fina demais, desenha uma linha vertical para cima, ligeiramente desviada à direita
        plt.annotate(f"{ruinas[i]:.1f}%", 
                     xy=(i + 0.18, lucros[i] + ruinas[i]/2),           # Base da linha (na barra fina)
                     xytext=(i + 0.18, lucros[i] + ruinas[i] + 1),     # Topo da linha (1% acima, na barra branca)
                     ha='center', va='bottom', color=negro, weight='bold',
                     arrowprops=dict(arrowstyle="-", color=negro, lw=1))
                     
    # 3. Label de Sobrevivência (Barra superior branca)
    if sobrev[i] > 0.5:
        plt.text(i, lucros[i] + ruinas[i] + sobrev[i]/2, f"{sobrev[i]:.1f}%", ha='center', va='center', color=negro, weight='bold')

plt.title(f'Assimetria de Fuga: Distribuição do Destino Termodinâmico ($T={T}$)')
plt.ylabel('Percentagem do Ensamble (%)')

# Com a anotação para cima, podemos voltar a encostar a legenda ao gráfico
plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))
plt.grid(alpha=0.2, axis='y')

plt.savefig('Gráficos/09_destino_particulas.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '09_destino_particulas.png'.\n")

# ==========================================
# 12. FÍSICA ESTATÍSTICA: DESLOCAMENTO QUADRÁTICO MÉDIO (MSD)
# ==========================================
print("[11/13] A gerar Gráfico 10 (Deslocamento Quadrático Médio - MSD)...")

# Isolamos a componente puramente estocástica (retirando o drift determinístico)
X_sub = np.log(precos_sub / S0) - (mu - 0.5 * sigma**2) * tempos
X_norm = np.log(precos_norm / S0) - (mu - 0.5 * sigma**2) * tempos
X_sup = np.log(precos_sup / S0) - (mu - 0.5 * sigma**2) * tempos

# A variância espacial em cada instante de tempo (MSD)
msd_sub = np.var(X_sub, axis=0)
msd_norm = np.var(X_norm, axis=0)
msd_sup = np.var(X_sup, axis=0)

plt.figure(figsize=(10, 6))

# Ignoramos t=0 para evitar log(0)
t_msd = tempos[1:]
plt.plot(t_msd, msd_sub[1:], color=claro, lw=2.5, label=rf'Subdifusão (Declive Teórico $\sim t^{{{2*H_sub}}})$')
plt.plot(t_msd, msd_norm[1:], color=base, lw=2.5, label=rf'Difusão Normal (Declive Teórico $\sim t^{{{2*H_norm}}})$')
plt.plot(t_msd, msd_sup[1:], color=escuro, lw=2.5, label=rf'Superdifusão (Declive Teórico $\sim t^{{{2*H_sup}}})$')

plt.xscale('log')
plt.yscale('log')
plt.title('Dispersão Espacial: Deslocamento Quadrático Médio (MSD)')
plt.xlabel('Tempo (Anos) - Escala Logarítmica')
plt.ylabel(r'Variância Estocástica $\langle x^2(t) \rangle$ - Escala Log')
plt.legend(loc='upper left')
plt.grid(alpha=0.3, which='both')

plt.savefig('Gráficos/10_deslocamento_quadratico_medio.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '10_deslocamento_quadratico_medio.png'.\n")


# ==========================================
# 13. FÍSICA ESTATÍSTICA: AUTOCORRELAÇÃO DOS MICROESTADOS (fGn)
# ==========================================
print("[12/13] A gerar Gráfico 11 (Autocorrelação e Memória)...")

def calcular_autocorrelacao_lag1(matriz_precos):
    # Calcula os incrementos (retornos logarítmicos) de todas as trajetórias
    incrementos = np.log(matriz_precos[:, 1:] / matriz_precos[:, :-1])
    correlacoes = []
    # Correlação entre o incremento t e o incremento t+1 para cada trajetória
    for i in range(len(incrementos)):
        if np.std(incrementos[i, :-1]) > 0 and np.std(incrementos[i, 1:]) > 0:
            corr = np.corrcoef(incrementos[i, :-1], incrementos[i, 1:])[0, 1]
            correlacoes.append(corr)
    return np.mean(correlacoes)

corr_sub = calcular_autocorrelacao_lag1(precos_sub)
corr_norm = calcular_autocorrelacao_lag1(precos_norm)
corr_sup = calcular_autocorrelacao_lag1(precos_sup)

plt.figure(figsize=(10, 6))
barras = plt.bar(['Subdifusão\n(Fricção/Mola)', 'Difusão Normal\n(Markov)', 'Superdifusão\n(Inércia)'], 
                 [corr_sub, corr_norm, corr_sup], 
                 color=[claro, base, escuro], edgecolor=negro, width=0.5)

plt.axhline(0, color=negro, lw=1)

# Adicionar os valores exatos em cima/baixo das barras
for bar in barras:
    yval = bar.get_height()
    pos = yval + 0.02 if yval > 0 else yval - 0.03
    plt.text(bar.get_x() + bar.get_width()/2, pos, f"{yval:.3f}", ha='center', va='center', weight='bold', color=negro)

plt.title('Memória Microscópica: Autocorrelação de Incrementos (Lag-1)')
plt.ylabel('Coeficiente de Autocorrelação (Pearson)')
plt.ylim(-0.5, 0.5)
plt.grid(alpha=0.2, axis='y')

plt.savefig('Gráficos/11_autocorrelacao_microestados.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '11_autocorrelacao_microestados.png'.\n")


# ==========================================
# 14. TERMODINÂMICA DA INFORMAÇÃO: ENTROPIA DE SHANNON
# ==========================================
print("[13/13] A gerar Gráfico 12 (Evolução da Entropia de Shannon)...")

def entropia_temporal(matriz_precos):
    entropias = []
    # Calculamos a entropia do ensamble a cada 5 passos de tempo para fluidez
    passos = range(1, matriz_precos.shape[1], 5)
    for t_idx in passos:
        counts, _ = np.histogram(matriz_precos[:, t_idx], bins=50, density=True)
        counts = counts[counts > 0] # Evitar log(0)
        entropias.append(entropy(counts, base=2))
    return tempos[list(passos)], np.array(entropias)

t_ent, ent_sub = entropia_temporal(precos_sub)
_, ent_norm = entropia_temporal(precos_norm)
_, ent_sup = entropia_temporal(precos_sup)

plt.figure(figsize=(10, 6))

plt.plot(t_ent, ent_sub, color=claro, lw=2.5, label='Subdifusão')
plt.plot(t_ent, ent_norm, color=base, lw=2.5, label='Difusão Normal')
plt.plot(t_ent, ent_sup, color=escuro, lw=2.5, label='Superdifusão')

plt.title('A Seta do Tempo: Evolução da Entropia de Shannon no Ensamble')
plt.xlabel('Tempo (Anos)')
plt.ylabel('Entropia (Bits de Informação)')
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.xlim(0, T)

plt.savefig('Gráficos/12_entropia_shannon.png', dpi=300, bbox_inches='tight')
plt.close()
print("      -> Exportado como '12_entropia_shannon.png'.\n")

print("Simulação Concluída")