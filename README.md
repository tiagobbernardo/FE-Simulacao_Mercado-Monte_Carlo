# Dinâmica de Sistemas Estocásticos: Difusão Anómala e Fuga de Kramers via Movimento Browniano Fracionário

Este repositório explora a dinâmica de sistemas complexos através dos princípios da **Mecânica Estatística**, **Processos Estocásticos** e **Termodinâmica de Não-Equilíbrio**. 

Utilizando simulações numéricas de Monte Carlo paralelizadas, o projeto expande a difusão clássica para integrar a quebra do pressuposto de Markov (amnésia temporal). Através do **Movimento Browniano Fracionário (fBM)**, demonstra-se a transição entre regimes puramente difusivos, ambientes de alto atrito subdifusivo e estados de inércia superdifusiva, culminando na análise física do **Problema de Fuga de Kramers**.

## 1. Fundamentação Teórica: Equação de Langevin Generalizada

A evolução temporal da variável de estado do sistema $S_t$ é modelada por uma Equação Diferencial Estocástica (SDE) análoga à **Equação de Langevin**, introduzindo um processo de Wiener fracionário $W_t^H$:

$$
dS_t = \mu S_t dt + \sigma S_t dW_t^H
$$

onde:
- $\mu$ é o **Coeficiente de Advecção (Drift)**, representando a força determinística de crescimento ou deriva do sistema.
- $\sigma$ é o **Coeficiente de Difusão (Volatilidade/Temperatura)**, ditando a amplitude da agitação térmica.
- $dW_t^H$ é o incremento do ruído estocástico, governado pelo **Expoente de Hurst ($H$)**, introduzindo "memória" espacial na matriz de covariância.

A solução analítica da trajetória para a preservação de energia (martingala) no domínio fracionário é:

$$
S_t = S_0 \exp \left( \mu t - \frac{1}{2}\sigma^2 t^{2H} + \sigma W_t^H \right)
$$

## 2. Regimes Termodinâmicos e Dimensões Fractais ($H$)

O sistema é testado em três estados fundamentais, gerados via Fatorização de Cholesky da matriz de covariância exata, permitindo fixar a base de perturbação térmica para isolar as propriedades geométricas do espaço:

* **Subdifusão ($H = 0.25$):** Sistema com autocorrelação negativa (anti-persistência). Exerce forças elásticas de reversão à média. Para manter a dispersão térmica global, o espaço impõe uma elevada fricção cinética (micro-flutuações extremamente violentas), gerando trajetórias em "serrote" (*whipsaw*).
* **Difusão Normal ($H = 0.50$):** O passeio aleatório clássico sem memória (Processo de Markov). Ruído branco de Gauss puro, onde os incrementos temporais são ortogonais/independentes.
* **Superdifusão ($H = 0.75$):** Sistema com autocorrelação positiva. Domínio da inércia e do Efeito Manada. O atrito micro-estrutural é minimizado, permitindo que a força advectiva empurre as partículas em direções prolongadas de forma balística.

## 3. Transição de Fase: O Novo Tempo Crítico ($t^{\ast}$)

O colapso termodinâmico do sistema ocorre quando a força determinística supera o envelope de ruído imposto pela difusão. Definindo $\mu_{\text{efetivo}} = |\mu - 0.5\sigma^2|$:

- **Força Advectiva (Sinal):** $\text{Sinal}(t) = \mu_{\text{efetivo}} \cdot t$
- **Força Difusiva Fracionária (Ruído):** $\text{Ruído}(t) = \sigma t^H$

A **transição de regime** ocorre no **Tempo Crítico ($t^{\ast}$)**, cujo limite é exponencialmente sensível à geometria do espaço ($H$):

$$
\mu_{\text{efetivo}} \cdot t^{\ast} = \sigma (t^{\ast})^H \implies t^{\ast} = \left( \frac{\sigma}{\mu_{\text{efetivo}}} \right)^{\frac{1}{1-H}}
$$

Sistemas superdifusivos ($H > 0.5$) atrasam drasticamente o $t^{\ast}$, exigindo maiores horizontes temporais para que o sinal estrutural consiga anular o afastamento direcional criado pela inércia. Inversamente, a subdifusão antecipa este ponto crítico devido ao constante esmagamento espacial da mola limitadora.

## 4. O Paradoxo do Atrito Subdifusivo (Análise de Risco)

O senso comum sugere que um sistema em constante reversão à média (Subdifusão) apresenta menor risco direcional. Contudo, a simulação computacional prova o **Paradoxo do Atrito**: para atingir a mesma macro-volatilidade anual ($\sigma = 13\%$), a anulação contínua do movimento no espaço subdifusivo exige compensações diárias massivas.

Esta elevada fricção microscópica maximiza os micro-crashes e o risco intra-anual (**Drawdown**). A subdifusão protege contra desvios absolutos de longo prazo, mas fá-lo impelindo um atrito térmico extremo no curto prazo.

## 5. O Problema de Fuga de Kramers (Estados Absorventes)

Em sistemas com limites estritos (ex: fronteiras de absorção *Stop-Loss* a -20% e *Take-Profit* a +30%), o projeto modela a distribuição dos **Tempos de Primeira Passagem** (Taxa de Escape de Kramers):

- **Na Subdifusão:** A alta dissipação de energia inicial atira rapidamente as partículas contra as fronteiras, destruindo o sistema prematuramente e gerando a menor Taxa de Sobrevivência do ensamble.
- **Na Superdifusão:** A inércia suave do deslocamento balístico protege a trajetória do ruído de alta frequência, retendo a esmagadora maioria das partículas presas no poço de potencial termodinâmico durante todo o horizonte de observação.

## 6. Estrutura dos Parâmetros de Simulação

| Parâmetro | Significado Físico | Valor Simulado |
| :--- | :--- | :--- |
| $S_0$ | Posição Inicial do Sistema no Espaço de Estados | $171.32$ |
| $\mu$ | Coeficiente de Advecção (Deriva) | $0.097 \text{ / ano}$ |
| $\sigma$ | Coeficiente de Difusão (Agitação/Temperatura) | $0.130 \text{ / ano}$ |
| $H$ | Expoente de Hurst (Dimensão Fractal / Memória) | $0.25 \mid 0.50 \mid 0.75$ |
| $T$ | Horizonte Temporal de Observação | $1.0 \text{ ano}$ |
| $N_{\text{passos}}$ | Resolução Temporal ($dt = T / N$) | $252 \text{ iterações}$ |
| $N_{\text{simulações}}$ | Número de Trajetórias (Ensemble de Monte Carlo) | $5\,000$ |

## 7. Mapeamento das Visualizações Científicas

O motor numérico exporta automaticamente 12 gráficos analíticos para a pasta `Gráficos/` (paleta de cores: *Teal*):

1. **`Gráficos/01_trajetorias_mercado.png`**: Evolução temporal de um ensemble de trajetórias de difusão normal e cálculo do valor médio esperado.
2. **`Gráficos/02_distribuicao_final.png`**: Convergência empírica da densidade de probabilidade para a Curva Lognormal teórica em $T=1$.
3. **`Gráficos/03_distribuicao_retornos.png`**: Confirmação da simetria Gaussiana termodinâmica dos microestados do sistema.
4. **`Gráficos/04_drawdowns_maximos.png`**: Impacto da dimensão fractal no risco extremo (Paradoxo Subdifusivo nos Drawdowns).
5. **`Gráficos/05_probabilidade_lucro_tempo.png`**: O Paradoxo do Tempo e a evolução da probabilidade determinística $P(S_T > S_0)$.
6. **`Gráficos/06_sinal_vs_ruido.png`**: Análise em escala Log-Log ilustrando o Colapso Termodinâmico e o desvio matemático do Tempo Crítico ($t^*$).
7. **`Gráficos/07_difusao_fracionaria.png`**: Trajetória isolada da mesma partícula (mesma sequência exata de choques térmicos) em 3 geometrias espaciais diferentes.
8. **`Gráficos/08_fuga_kramers.png`**: Histogramas dos Tempos de Primeira Passagem modelando a resiliência à absorção fronteiriça.
9. **`Gráficos/09_destino_particulas.png`**: Gráfico de barras ilustrando a assimetria na dispersão de Kramers e a distribuição final (Profit vs. Loss vs. Presas no poço).
10. **`Gráficos/10_deslocamento_quadratico_medio.png`**: Variância do deslocamento estocástico ao longo do tempo, comparando os regimes de difusão em escala log-log e os seus expoentes teóricos.
11. **`Gráficos/11_autocorrelacao_microestados.png`**: Autocorrelação de lag 1 dos incrementos logarítmicos, comparando a antipersistência subdifusiva, a difusão normal e a persistência superdifusiva.
12. **`Gráficos/12_entropia_shannon.png`**: Evolução temporal da entropia de Shannon do ensemble de preços nos três regimes.