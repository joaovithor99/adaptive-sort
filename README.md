# Ordenação Adaptativa (Meta-Sort) — Estruturas de Dados Avançadas

Implementação de um algoritmo de ordenação adaptativo (`ordenar(v)`) capaz de inspecionar as características da entrada através da função `escolher(v)` e despachar a execução para o algoritmo mais eficiente em tempo de execução.

## Algoritmos Integrados
1. **Inserção (Insertion Sort)**
2. **Intercalação (Merge Sort)**
3. **Rápida com Pivô Aleatório (Quicksort)**
4. **Híbrida (Timsort simplificado: Merge Sort com Insertion Sort para partições pequenas)**
5. **Contagem (Counting Sort)**
6. **Base (Radix Sort)**

## Estrutura do Projeto
- `main.py`: Implementação dos algoritmos, do motor de decisão `escolher(v)`, `ordenar(v)`, suíte de testes de borda e benchmarks.
- `RELATORIO.md`: Análise comparativa, justificativas teóricas, métricas de desempenho e discussão de erros de heurística.

## Como Executar e Reproduzir as Medições

### Pré-requisitos
- Python 3.10 ou superior.

### Execução dos Testes de Borda
```bash
python main.py --test