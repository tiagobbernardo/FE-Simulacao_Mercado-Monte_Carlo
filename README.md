# Dinâmica de Sistemas Estocásticos: Simulação de Monte Carlo e Transição de Regime num Movimento Browniano Geométrico

Este repositório explora a dinâmica de sistemas complexos através dos princípios da **Mecânica Estatística**, **Processos Estocásticos** e **Termodinâmica Fora do Equilíbrio**. 

Utilizando simulações numéricas de Monte Carlo aplicadas ao Movimento Browniano Geométrico (GBM), o projeto demonstra a transição entre um **regime puramente difusivo (dominado por flutuações estocásticas/ruído)** a escalas temporais microscópicas e um **regime advectivo/balístico (dominado por drift/sinal)** a escalas temporais macroscópicas.

## 1. Fundamentação Teórica e Equação de Langevin

A evolução temporal da variável de estado do sistema $S_t$ é modelada por uma Equação Diferencial Estocástica (SDE) multiplicativa, estruturalmente equivalente à **Equação de Langevin** na física de partículas:

$$
dS_t = \mu S_t dt + \sigma S_t dW_t
$$

onde:
* $\mu$ é o **Coeficiente de Advecção (Drift)**, representando a força determinística de crescimento ou deriva do sistema.
* $\sigma$ é o **Coeficiente de Difusão (Volatilidade)**, análogo à intensidade da agitação térmica num meio fluido.
* $dW_t \sim \mathcal{N}(0, dt)$ é o incremento de um Processo de Wiener (Ruído Branco de Gauss).

Aplicando o **Lema de Itô**, obtém-se a solução analítica exata para a trajetória do sistema:

$$
S_t = S_0 \exp \left( \left( \mu - \frac{1}{2}\sigma^2 \right) t + \sigma W_t \right)
$$

O parâmetro $\mu_{\text{efetivo}} = \mu - \frac{1}{2}\sigma^2$ dita a taxa efetiva de variação determinística da densidade de probabilidade no espaço de estados.

## 2. Microestados, Macroestados e Termodinâmica Estatística

A análise estatística do sistema desdobra-se em duas escalas fundamentais:

### Microestados (Incrementos Logarítmicos)
As flutuações discretas em intervalos $\Delta t$, dadas por $\Delta x = \ln(S_{t+\Delta t} / S_t)$, correspondem aos microestados de colisão (ex: num gás ideal). A sua densidade de probabilidade segue rigorosamente uma **Distribuição Gaussiana (Normal)**:

$$
P(\Delta x) = \frac{1}{\sigma \sqrt{2\pi \Delta t}} \exp \left( -\frac{(\Delta x - \mu_{\text{efetivo}}\Delta t)^2}{2\sigma^2 \Delta t} \right)
$$

### Macroestados (Distribuição de Posições Finais $S_T$)
Devido à natureza multiplicativa do processo estocástico, a integração temporal dos microestados gaussianos resulta numa **Distribuição Lognormal** para os macroestados finais $S_T$. Esta distribuição apresenta uma forte assimetria positiva, onde o valor médio do ensemble excede a sua mediana.

## 3. Transição de Fase: O Tempo Crítico ($t^{*}$)

O comportamento do sistema é determinado pelo confronto entre duas forças em escalas temporais distintas:

* **Força Advectiva / Sinal Linear:** $\text{Sinal}(t) = \mu_{\text{efetivo}} \cdot t$
* **Força Difusiva / Ruído por Raiz Quadrada:** $\text{Ruído}(t) = \sigma \sqrt{t}$

No limite microscópico ($t \to 0^{+}$), a taxa de variação da componente difusiva domina completamente a componente advectiva:

$$
\lim_{t \to 0^{+}} \frac{\text{Ruído}(t)}{\text{Sinal}(t)} = \lim_{t \to 0^{+}} \frac{\sigma \sqrt{t}}{\mu_{\text{efetivo}} t} = \infty
$$

### Cálculo do Ponto de Equilíbrio

A **transição de regime** (onde a magnitude do sinal advectivo iguala a amplitude do ruído difusivo) ocorre no **Tempo Crítico ($t^{*}$)**:

$$
\mu_{\text{efetivo}} \cdot t^{*} = \sigma \sqrt{t^{*}} \implies t^{*} = \left( \frac{\sigma}{\mu_{\text{efetivo}}} \right)^{2}
$$

* **Para $t < t^{*}$:** O sistema encontra-se num estado termodinâmico de elevada entropia relativa, indistinguível de puro ruído térmico.
* **Para $t > t^{*}$:** A componente advectiva rompe a barreira estocástica, elevando a probabilidade de deslocamento positivo rumo aos 100%.

## 4. Análise de Risco e Estados Absorventes

Em sistemas limitados inferiormente, a presença de uma barreira atuará como um **Estado Absorvente** (ruína do sistema) no contexto da Equação de Fokker-Planck. 

A simulação avalia distribuições extremas (Drawdowns Máximos), demonstrando que a alta difusão inicial (antes de atingir $t^*$) garante uma probabilidade não nula de o sistema colidir com fronteiras absorventes, independentemente de possuir um $\mu_{\text{efetivo}} > 0$ a longo prazo.

## 5. Estrutura dos Parâmetros de Simulação

| Parâmetro | Significado Físico | Valor Simulado |
| :--- | :--- | :--- |
| $S_0$ | Posição Inicial do Sistema no Espaço de Estados | $171.32$ |
| $\mu$ | Coeficiente de Advecção (Deriva) | $0.097 \text{ / ano}$ |
| $\sigma$ | Coeficiente de Difusão (Agitação/Temperatura) | $0.130 \text{ / ano}$ |
| $T$ | Horizonte Temporal de Observação | $1.0 \text{ ano}$ |
| $N_{\text{passos}}$ | Resolução Temporal ($dt = T / N$) | $252 \text{ iterações}$ |
| $N_{\text{simulações}}$ | Número de Trajetórias (Ensemble de Monte Carlo) | $5\,000$ |

## 6. Mapeamento das Visualizações Científicas

O motor numérico exporta automaticamente 6 outputs analíticos:

1. **`01_trajetorias_mercado.png`**: Evolução temporal de um ensemble de trajetórias e cálculo do valor médio esperado.
2. **`02_distribuicao_final.png`**: Convergência empírica da densidade de probabilidade para a Curva Lognormal teórica.
3. **`03_distribuicao_retornos.png`**: Confirmação da simetria Gaussiana nos microestados do sistema.
4. **`04_drawdowns_maximos.png`**: Distribuição de quedas extremas e probabilidade de impacto com estados absorventes.
5. **`05_probabilidade_lucro_tempo.png`**: Curva de evolução da probabilidade determinística no tempo $P(S_T > S_0)$.
6. **`06_sinal_vs_ruido.png`**: Análise em escala Log-Log ilustrando o Colapso Termodinâmico e o ponto de intersecção exato do Tempo Crítico ($t^*$).