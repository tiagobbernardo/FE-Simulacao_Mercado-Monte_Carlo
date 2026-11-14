# Dinâmica de Sistemas Estocásticos Fora do Equilíbrio: Difusão Anómala, Fuga de Kramers e Seta da Entropia via fBM

**Instituto Superior de Engenharia de Lisboa (ISEL)**  
**Licenciatura em Engenharia Física Aplicada (LEFA)**  
**Física Estatística — 2.º Trabalho Computacional**  
*Autores:* Tiago Bernardo (53117) & Gabriel Marques (53087)  
*Docente:* Prof. Doutor Pedro Patrício  

---

## 1. Visão Geral do Projeto

Este projeto investiga a evolução temporal de variáveis de estado estocásticas fora do equilíbrio termodinâmico, substituindo o postulado markoviano clássico (ausência de memória temporal) por processos que admitem correlações de longo alcance. Através do **Movimento Browniano Fracionário (fBM)** acoplado a um motor de simulação de Monte Carlo com fatorização exata de Cholesky, modela-se o comportamento de um *ensemble* de partículas submetido a diferentes geometrias espaciais e regimes difusivos.

A análise foca-se estritamente na mecânica estatística macroscópica e mesoscópica:
- Transição entre regimes difusivos governados pelo **Expoente de Hurst ($H$)** e **Dimensão Fractal ($D_f$)**;
- Validação estocástica através do **Deslocamento Quadrático Médio (MSD)** e autocorrelação de microestados;
- Resolução do **Problema de Fuga de Kramers** em poços de potencial com barreiras absorventes;
- Quantificação da **Seta do Tempo** mediante a evolução contínua da **Entropia de Shannon**.

---

## 2. Fundamentação Teórica e Formulação Matemática

### 2.1. Equação de Langevin Generalizada (fBM Multiplicativo)
A dinâmica contínua da variável macroscópica $S_t$ é formulada como uma Equação Diferencial Estocástica (SDE) multiplicativa:

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^H
$$

onde:
- $\mu$: **Coeficiente de Advecção (Drift)**, representativo da força determinística média atuante sobre o sistema ($\mu \approx 0.111338\text{ ano}^{-1}$).
- $\sigma$: **Coeficiente de Difusão (Temperatura do Banho Térmico)**, fixando a magnitude média das flutuações térmicas diárias ($\sigma \approx 0.137911\text{ ano}^{-1}$).
- $dW_t^H$: Incremento do processo fracionário de Wiener, governado pelo Expoente de Hurst $H \in ]0, 1[$.

No âmbito do cálculo estocástico fracionário, Hu & Øksendal (2003) deduziram a solução analítica martingala exata desta equação:

$$
S_t = S_0 \exp\left( \mu t - \frac{1}{2}\sigma^2 t^{2H} + \sigma W_t^H \right)
$$

### 2.2. Estrutura de Covariância e Fatorização de Cholesky
O ruído estocástico fracionário exibe uma função de covariância não-estacionária:

$$
\langle W_t^H W_s^H \rangle = \frac{1}{2} \left( t^{2H} + s^{2H} - |t - s|^{2H} \right)
$$

Para garantir a estrita reprodução da geometria espacial, as trajetórias do *ensemble* são sintetizadas através da fatorização de Cholesky da matriz de covariância discretizada $\mathbf{C} \in \mathbb{R}^{N \times N}$:

$$
\mathbf{C} = \mathbf{L}\mathbf{L}^\top, \quad \mathbf{W}^H = \mathbf{L}\mathbf{Z}
$$

onde $\mathbf{Z} \sim \mathcal{N}(0, \mathbf{I})$ representa ruído Gaussiano padrão independente, e aplica-se uma regularização diagonal $\epsilon = 10^{-8}\,\mathbf{I}$ para estabilidade numérica estrita.

---

## 3. Regimes Difusivos e Dimensões Fractais

A deformação geométrica do espaço e a memória temporal das trajetórias são caracterizadas pelo Expoente de Hurst ($H$) e pela Dimensão Fractal de Hausdorff-Besicovitch ($D_f = 2 - H$):

| Regime Difusivo | Expoente de Hurst ($H$) | Dimensão Fractal ($D_f$) | Propriedades Dinâmicas e Termodinâmicas |
| :--- | :---: | :---: | :--- |
| **Subdifusão** | $0.25$ | $1.75$ | Autocorrelação negativa (anti-persistência). Atrito térmico microscópico severo e força elástica de reversão à média. Trajetória com elevada rugosidade geométrica. |
| **Difusão Normal** | $0.50$ | $1.50$ | Movimento Browniano clássico (processo de Markov, ruído Gaussiano ortogonal). Dispersão linear de Einstein: $\langle \Delta x^2 \rangle \propto t$. |
| **Superdifusão** | $0.75$ | $1.25$ | Autocorrelação positiva (persistência temporal). Inércia balística e cooperação de microestados (efeito de arrasto/manada). Trajetória suave de baixa fricção. |

---

## 4. Fenomenologia Física e Resultados Numéricos

As simulações foram executadas para um *ensemble* de $N = 5\,000$ partículas durante um horizonte temporal de $T = 1.0\text{ ano}$ ($252$ passos temporais diários, $dt = 1/252$).

### 4.1. Assinatura do Deslocamento Quadrático Médio (MSD)
A componente puramente estocástica verifica a lei de potência $\text{MSD} = \langle (X_t - X_0)^2 \rangle \propto t^{\alpha}$, com declive teórico $\alpha = 2H$:
- **Subdifusão ($H=0.25$):** Declive experimental $\alpha \approx 0.50$.
- **Difusão Normal ($H=0.50$):** Declive experimental $\alpha \approx 1.00$.
- **Superdifusão ($H=0.75$):** Declive experimental $\alpha \approx 1.50$.

### 4.2. Paradoxo do Atrito e Análise de Risco (Drawdown)
Embora a reversão à média confine o sistema a longo prazo, para conservar a mesma dispersão anual ($\sigma \approx 13.8\%$), o espaço subdifusivo gera flutuações intra-anuais de alta amplitude:
- **Maximum Drawdown Médio:** $-23.0\%$ (Subdifusão) vs. $-11.9\%$ (Normal) vs. $-5.5\%$ (Superdifusão).
- **Autocorrelação $\text{Lag-1}$ dos Retornos:** $-0.292$ (Subdifusão) vs. $-0.004$ (Normal) vs. $+0.370$ (Superdifusão).

### 4.3. Problema de Fuga de Kramers (Fronteiras Absorventes)
Definindo barreiras de potencial em $+30\%$ (escape superior) e $-20\%$ (escape inferior) relativamente a $S_0$:
- **Subdifusão ($H=0.25$):** Taxa de sobrevivência no poço de **$53.0\%$** ($34.9\%$ escape superior, $12.1\%$ escape inferior). O atrito microscópico força colisões letais precoces com as fronteiras.
- **Difusão Normal ($H=0.50$):** Taxa de sobrevivência de **$79.5\%$** ($17.9\%$ escape superior, $2.6\%$ inferior).
- **Superdifusão ($H=0.75$):** Taxa de sobrevivência de **$86.6\%$** ($12.3\%$ escape superior, $1.1\%$ inferior). A inércia preserva as trajetórias no interior do poço.

### 4.4. A Seta do Tempo e Entropia de Shannon
A evolução da densidade espacial dos microestados $p_i(t)$ é avaliada através da Entropia de Shannon:

$$
S(t) = - \sum_{i=1}^{M} p_i(t) \log_2 p_i(t)
$$

Implementada sobre uma grelha espacial fixa ($M = 80$ intervalos), observa-se o crescimento estritamente monotónico de $S(t)$ (Seta do Tempo), convergindo assintoticamente para $S(T) \approx 5.22\text{–}5.23\text{ bits}$ em $T = 1.0\text{ ano}$ em todos os regimes difusivos.

---

## 5. Tabela de Parâmetros Calibrados

| Parâmetro | Significado Físico / Estatístico | Valor Calibrado |
| :---: | :--- | :---: |
| $S_0$ | Estado Inicial do Sistema | $171.32$ |
| $\mu$ | Coeficiente de Advecção (Drift / Força Determinística) | $0.111338\text{ ano}^{-1}$ ($11.13\%/\text{ano}$) |
| $\sigma$ | Coeficiente de Difusão (Temperatura do Banho / Volatilidade) | $0.137911\text{ ano}^{-1}$ ($13.79\%/\text{ano}$) |
| $H$ | Expoente de Hurst | $0.25 \mid 0.50 \mid 0.75$ |
| $D_f$ | Dimensão Fractal ($2 - H$) | $1.75 \mid 1.50 \mid 1.25$ |
| $T$ | Horizonte Temporal de Simulação | $1.0\text{ ano}$ |
| $N_{\text{passos}}$ | Resolução Temporal ($dt = 1/252$) | $252\text{ passos}$ |
| $N_{\text{simulações}}$ | Dimensão do *Ensemble* de Monte Carlo | $5\,000\text{ trajetórias}$ |

---

## 6. Visualizações Científicas Geradas

O simulador exporta 12 figuras a 300 DPI para o diretório `Gráficos/`:

1. `Gráficos/01_trajetorias_mercado.png`: Evolução temporal de 500 partículas no regime markoviano normal ($H=0.50$) e trajetória média analítica.
2. `Gráficos/02_distribuicao_final.png`: Distribuição de probabilidade terminal confrontada com a densidade teórica lognormal.
3. `Gráficos/03_distribuicao_retornos.png`: Densidade de probabilidade dos microestados diários e ajuste Gaussiano.
4. `Gráficos/04_drawdowns_maximos.png`: Distribuição comparativa dos desvios máximos (*Maximum Drawdown*) nos 3 regimes.
5. `Gráficos/05_probabilidade_lucro_tempo.png`: Evolução da probabilidade de deslocamento líquido positivo $P(S_t > S_0)$ no tempo.
6. `Gráficos/06_sinal_vs_ruido.png`: Análise da razão sinal-ruído e determinação do tempo crítico de crossover $t^{\ast}$.
7. `Gráficos/07_difusao_fracionaria.png`: Partícula com sequência idêntica de choques térmicos propagada nos 3 regimes de Hurst.
8. `Gráficos/08_fuga_kramers.png`: Distribuição empírica dos tempos de primeira passagem para barreiras em $+30\%$ e $-20\%$.
9. `Gráficos/09_destino_particulas.png`: Destino terminal das partículas no poço de Kramers (escapes assimétricos e confinamento).
10. `Gráficos/10_deslocamento_quadratico_medio.png`: Curvas de MSD em escala log-log validando os declives teóricos $\alpha = 2H$.
11. `Gráficos/11_autocorrelacao_microestados.png`: Função de autocorrelação $\text{Lag-1}$ dos incrementos estocásticos.
12. `Gráficos/12_entropia_shannon.png`: Crescimento monotónico da Entropia de Shannon (Seta do Tempo) em grelha fixa.

---

## 7. Estrutura do Repositório e Reprodução

### Estrutura de Ficheiros
```text
.
├── parameters.py            # Extração e calibração dos parâmetros termodinâmicos
├── simulacao_mercado.py     # Motor Monte Carlo, fatorização de Cholesky e exportação de gráficos
├── README.md                # Documentação técnica e científica do projeto
├── Gráficos/                # 12 figuras analíticas geradas a 300 DPI
│   ├── 01_trajetorias_mercado.png
│   └── ...
└── Relatório/               # Documentação académica em LaTeX
    ├── ISELlogo.png         # Emblema institucional
    ├── relatorio.tex        # Código-fonte LaTeX (XeLaTeX)
    └── relatorio.pdf        # Relatório final compilado (8 páginas)
```

### Reprodução da Simulação e Compilação
```bash
# 1. Executar a simulação numérica e gerar os 12 gráficos
python simulacao_mercado.py

# 2. Compilar o relatório académico em XeLaTeX (dupla compilação para resolver referências cruzadas)
cd Relatório
xelatex -interaction=nonstopmode relatorio.tex
xelatex -interaction=nonstopmode relatorio.tex
```

---

## 8. Referências Bibliográficas

1. **Patrício, P. (2026).** *Física Estatística Computacional*. Instituto Superior de Engenharia de Lisboa (ISEL).
2. **Metzler, R., Jeon, J.-H., Cherstvy, A. G., & Barkai, E. (2014).** *Anomalous diffusion models and their properties: non-stationarity, non-ergodicity, and ageing at the centenary of von Smoluchowski's theory*. Physical Chemistry Chemical Physics, 16(44), 24128–24164. DOI: [10.1039/C4CP03465A](https://doi.org/10.1039/C4CP03465A).
3. **Hu, Y., & Øksendal, B. (2003).** *Fractional white noise calculus and applications to finance*. Infinite Dimensional Analysis, Quantum Probability and Related Topics, 6(01), 1–32. DOI: [10.1142/S0219025703001110](https://doi.org/10.1142/S0219025703001110).
