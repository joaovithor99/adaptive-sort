# Relatório de Desempenho e Engenharia do Algoritmo Adaptativo

## 1. Tabela Comparativa de Cenários vs. Métodos
Tempo médio de execução medido em milissegundos ($ms$):

| Algoritmo | 1. Aleatório (Chaves Grandes) | 2. Faixa Estreita | 3. Quase Ordenado | 4. Lista Minúscula (n=30) |
| :--- | :--- | :--- | :--- | :--- |
| **Inserção** | N/A (> tempo) | 2708.53 ms | 7.77 ms | 0.02 ms |
| **Intercalação** | 15.34 ms | 35.09 ms | 10.43 ms | 0.04 ms |
| **Rápida (Pivô Aleat.)** | 11.42 ms | 5.21 ms | 9.47 ms | 0.03 ms |
| **Híbrida** | 10.58 ms | 17.83 ms | 6.21 ms | 0.02 ms |
| **Contagem** | N/A (memória) | **0.77 ms** | 2.33 ms | 0.02 ms |
| **Base (Radix)** | **5.67 ms** | 2.44 ms | 2.71 ms | **0.01 ms** |
| **`ordenar(v)` (Adaptativo)** | 12.24 ms | 1.54 ms | 8.15 ms | 0.02 ms |

---

## 2. Qual Venceu Cada Cenário e Por Quê

* **1. Aleatório (Chaves Grandes): Vencedor — Base (Radix Sort - 5.67 ms)**
  * **Por quê:** O Radix Sort processa dígitos individualmente em $O(d \cdot n)$ passadas lineares estáveis, sem realizar comparações par a par. A Ordenação por Contagem tornou-se inviável ($k > 10^7$, estourando memória e tempo de inicialização de contadores), e os métodos por comparação ficaram restritos ao piso $\Omega(n \log n)$.
* **2. Faixa Estreita ($k \le 50$, $n=10.000$): Vencedor — Contagem (Counting Sort - 0.77 ms)**
  * **Por quê:** Quando $k \ll n$, o custo de percorrer o vetor de contadores é irrelevante, fazendo com que o algoritmo opere estritamente em tempo linear $O(n + k) \approx O(n)$. Como os números servem como endereços de índice diretos, nenhuma comparação é feita, superando a Inserção em mais de 3.500 vezes ($2708.53\text{ ms}$ vs. $0.77\text{ ms}$).
* **3. Quase Ordenado: Vencedores — Métodos Lineares e Híbridos (2 a 6 ms)**
  * **Por quê:** A Inserção executou em $7.77\text{ ms}$ (contra os mais de $2700\text{ ms}$ do caso desordenado) porque a quantidade de inversões locais foi pequena, aproximando-se de $O(n)$. O método adaptativo garantiu execução em $8.15\text{ ms}$, eliminando o risco do pior caso.
* **4. Lista Minúscula ($n=30$): Vencedor — Base / Inserção / Híbrida (0.01 a 0.02 ms)**
  * **Por quê:** Para valores pequenos de $n$, os custos fixos de chamada recursiva, alocação de listas auxiliares e particionamento pesam mais que o trabalho útil. A Inserção e a chamada direta dispensam sobrecarga de pilha e intercala-se rapidamente.

---

## 3. Regras de Decisão do `escolher(v)` e Justificativa Teórica

As regras foram formuladas com base nas medições dos encontros da disciplina:

1. **Regra de Tamanho ($n \le 64$):**
   * *Decisão:* Despacha para **Inserção**.
   * *Origem:* Ponto de cruzamento assintótico demonstrado na Aula 3. Abaixo de $n=64$, o algoritmo $O(n^2)$ com constante pequena supera algoritmos $O(n \log n)$ com overhead de chamadas de função e divisão de vetores.
2. **Inspeção de Inversões por Amostra:**
   * *Decisão:* Se a amostra indicar quase ordenação ($inversões \le 1$), despacha para **Inserção**.
   * *Origem:* A Aula 11 provou que o melhor caso da Inserção é $O(n)$ quando a lista já possui poucos elementos fora de ordem.
3. **Cálculo da Faixa ($k = \max - \min$):**
   * *Decisão:* Se a faixa for estreita ($k \le 2n$ e $k \le 100.000$), despacha para **Contagem**.
   * *Origem:* A Aula 13 demonstrou que a Contagem degrada severamente se a faixa de valores for muito maior que $n$. A verificação protege a memória contra alocações astronômicas.
4. **Fallback Geral:**
   * *Decisão:* Despacha para **Rápida com Pivô Aleatório** ou **Híbrida**.
   * *Origem:* Pivô aleatório previne a degeneração para $O(n^2)$ de listas ordenadas, mantendo custo esperado $O(n \log n)$.

---

## 4. Custo do `escolher(v)`: Ele Compensa?

O `escolher(v)` executa em **tempo $O(n)$ com uma única passada** e espaço auxiliar **$O(1)$**:
* `len(v)` custa $O(1)$.
* O laço percorre a entrada uma única vez atualizando $\min$, $\max$ e verificando quebras de ordem em um passo amostral regular.

### O ganho compensa o custo da inspeção?
**Sim, com folga ampla.** 
No cenário de Faixa Estreita, inspecionar a lista custou frações de milissegundo, permitindo despachar para a Contagem e finalizar o trabalho total em $1.54\text{ ms}$. Se o algoritmo fixo escolhido fosse a Inserção, o programa levaria $2708.53\text{ ms}$; se fosse a Intercalação, levaria $35.09\text{ ms}$. Pagar uma varredura linear de inspeção é infinitesimal perto