```markdown
# Relatório de Desempenho e Engenharia do Algoritmo Adaptativo

## 1. Tabela Comparativa de Cenários vs. Métodos
Tempo médio de execução medido em milissegundos ($ms$):

| Algoritmo | 1. Aleatório (Chaves Grandes) | 2. Faixa Estreita | 3. Quase Ordenado | 4. Lista Minúscula ($n \le 64$) |
| :--- | :--- | :--- | :--- | :--- |
| **Inserção** | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |
| **Intercalação** | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |
| **Rápida (Pivô Aleat.)** | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |
| **Híbrida** | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |
| **Contagem** | *(estoura mem./lento)* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |
| **Base (Radix)** | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |
| **`ordenar(v)` (Adaptativo)** | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* | *[pendente benchmark]* |

---

## 2. Vencedores por Cenário e Fundamentação Teórica

* **Lista Minúscula ($n \le 64$):** Vence a **Inserção**. Em entradas pequenas, o fator constante de algoritmos $O(n \log n)$ (como chamadas recursivas e alocação de memória auxiliar) supera o custo quadrático da inserção, ficando abaixo do ponto de cruzamento assintótico[cite: 26, 460, 461, 463].
* **Faixa Estreita (ex.: $k \le 2n$):** Vence a **Contagem**. O algoritmo opera em $O(n + k)$ sem realizar comparações, utilizando o próprio valor da chave como endereço do contador[cite: 739, 741, 742].
* **Quase Ordenado:** Vence a **Inserção** (ou **Híbrida**). O número de inversões locais é muito baixo; os elementos realizam pouquíssimos deslocamentos e o custo aproxima-se do limite linear $O(n)$[cite: 85, 86, 107].
* **Aleatório com Chaves Grandes:** Vence a **Rápida com Pivô Aleatório** ou **Base (Radix)**. A Contagem é descartada devido ao risco de $O(n + k)$ inflar com $k$ gigantesco[cite: 741, 752, 753]; Quicksort oferece excelente localidade de referência de memória e quase nenhum overhead auxiliar[cite: 54, 55].

---

## 3. Regras de Decisão do `escolher(v)`

A função de despacho segue uma cascata de inspeções baratas:
1. **$n \le 64$:** Despacha para **Inserção**[cite: 461].
2. **Inspeção de Amostra/Ordenação Parcial (em $O(1)$ ou $O(m)$ amostral):** Se os elementos estiverem quase ordenados, despacha para **Inserção**.
3. **Cálculo da Faixa ($k = \max - \min$):** 
   - Se $k \le 2n$ e $\min \ge 0$, despacha para **Contagem** ($O(n+k)$ viável)[cite: 741, 742].
   - Se $k > 2n$ e chaves são inteiras não-negativas, despacha para **Base (Radix)** ou **Rápida (Pivô Aleatório)**[cite: 51, 769].
4. **Fallback Geral:** **Híbrida** ou **Rápida com Pivô Aleatório**[cite: 51, 57].

---

## 4. Custo Computacional do `escolher(v)` e Análise de Trade-off
O analisador **não pode** realizar duas passagens completas na lista sob risco de transformar um ganho assintótico em overhead inútil. A inspeção de tamanho `len(v)` é $O(1)$. A extração de $\min$ e $\max$ exige uma única varredura linear simultânea $O(n)$, amortizada pelo ganho substancial de trocar um algoritmo $O(n \log n)$ por um $O(n)$ linear (como a Contagem em faixas estreitas)[cite: 447, 742, 743].

---

## 5. Cenário de Falha da Heurística (Erro de Decisão)
* **Caso:** Vetor com $n$ grande composto quase inteiramente por zeros, mas com um único elemento anômalo (outlier) de valor $10^9$.
* **Impacto:** Uma regra ingênua baseada em $\max - \min$ concluiria que a amplitude é grande demais para métodos lineares e despacharia para divisão e conquista por comparação ($O(n \log n)$)[cite: 7, 33, 447], quando na verdade uma limpeza de outlier ou compressão permitiria resolução quase instantânea.