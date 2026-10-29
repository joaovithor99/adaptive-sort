import random
import time
import sys

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    meio = len(arr) // 2
    esq = merge_sort(arr[:meio])
    dir = merge_sort(arr[meio:])
    
    # Intercalação
    res = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            res.append(esq[i])
            i += 1
        else:
            res.append(dir[j])
            j += 1
    res.extend(esq[i:])
    res.extend(dir[j:])
    return res

def quicksort_random(arr):
    if len(arr) <= 1:
        return arr
    pivo = random.choice(arr)
    menores = [x for x in arr if x < pivo]
    iguais = [x for x in arr if x == pivo]
    maiores = [x for x in arr if x > pivo]
    return quicksort_random(menores) + iguais + quicksort_random(maiores)

def hybrid_sort(arr, limiar=32):
    if len(arr) <= limiar:
        return insertion_sort(arr)
    meio = len(arr) // 2
    esq = hybrid_sort(arr[:meio], limiar)
    dir = hybrid_sort(arr[meio:], limiar)
    
    res = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            res.append(esq[i])
            i += 1
        else:
            res.append(dir[j])
            j += 1
    res.extend(esq[i:])
    res.extend(dir[j:])
    return res

def counting_sort(arr):
    if not arr:
        return []
    menor = min(arr)
    maior = max(arr)
    faixa = maior - menor + 1
    contadores = [0] * faixa
    for x in arr:
        contadores[x - menor] += 1
    saida = []
    for idx, qtd in enumerate(contadores):
        saida.extend([idx + menor] * qtd)
    return saida

def radix_sort(arr):
    if not arr:
        return []
    menor = min(arr)
    # Suporte a negativos via deslocamento
    arr_shift = [x - menor for x in arr]
    maior = max(arr_shift)
    exp = 1
    while maior // exp > 0:
        baldes = [[] for _ in range(10)]
        for x in arr_shift:
            digito = (x // exp) % 10
            baldes[digito].append(x)
        arr_shift = [item for sub in baldes for item in sub]
        exp *= 10
    return [x + menor for x in arr_shift]

def escolher(v):
    n = len(v)
    if n <= 64:
        return insertion_sort
    
    # Inspeção rápida de faixa em uma única passada
    menor = maior = v[0]
    inversoes_amostra = 0
    passo = max(1, n // 50)
    for i in range(1, n):
        val = v[i]
        if val < menor:
            menor = val
        elif val > maior:
            maior = val
        if i % passo == 0 and v[i] < v[i - passo]:
            inversoes_amostra += 1
            
    # Quase ordenado detectado pela taxa de quebras
    if inversoes_amostra <= 1:
        return insertion_sort

    faixa = maior - menor
    # Proteção de memória para Contagem: faixa razoável proporcional a n
    if faixa <= 2 * n and faixa <= 100_000:
        return counting_sort
    
    return quicksort_random

def ordenar(v):
    if len(v) <= 1:
        return list(v)
    algoritmo = escolher(v)
    return algoritmo(v)

def rodar_testes_borda():
    casos = {
        "Vazia": [],
        "Um elemento": [42],
        "Todos iguais": [5, 5, 5, 5, 5],
        "Já ordenada": [1, 2, 3, 4, 5, 6, 7],
        "Invertida": [7, 6, 5, 4, 3, 2, 1],
        "Negativos": [-5, -1, -10, 0, 3, -2, 8]
    }
    for nome, dados in casos.items():
        esperado = sorted(dados)
        resultado = ordenar(dados)
        assert resultado == esperado, f"Falha no teste '{nome}': obteve {resultado}, esperava {esperado}"
    print("Todos os testes de borda passaram com sucesso!")

def benchmark_cenarios():
    import time
    
    # 4 Cenários solicitados
    cenarios = {
        "1. Aleatório (Chaves Grandes)": [random.randint(0, 10_000_000) for _ in range(5_000)],
        "2. Faixa Estreita": [random.randint(0, 50) for _ in range(10_000)],
        "3. Quase Ordenado": sorted([random.randint(0, 10_000) for _ in range(5_000)]),
        "4. Lista Minúscula (n=30)": [random.randint(0, 100) for _ in range(30)]
    }
    
    # Adiciona pequenas perturbações no cenário 'Quase Ordenado'
    for _ in range(25):
        i, j = random.randint(0, 4999), random.randint(0, 4999)
        cenarios["3. Quase Ordenado"][i], cenarios["3. Quase Ordenado"][j] = (
            cenarios["3. Quase Ordenado"][j], cenarios["3. Quase Ordenado"][i]
        )

    algoritmos = {
        "Inserção": insertion_sort,
        "Intercalação": merge_sort,
        "Rápida (Pivô Aleat.)": quicksort_random,
        "Híbrida": hybrid_sort,
        "Contagem": counting_sort,
        "Base (Radix)": radix_sort,
        "ordenar(v) (Adaptativo)": ordenar
    }

    print("\nExecutando benchmarks (aguarde alguns segundos)...")
    resultados = {alg: {} for alg in algoritmos}

    for nome_cenario, dados in cenarios.items():
        for nome_alg, func in algoritmos.items():
            # Evita estourar tempo ou memória da Inserção ou Contagem em casos extremos
            if nome_cenario == "1. Aleatório (Chaves Grandes)" and nome_alg == "Inserção":
                resultados[nome_alg][nome_cenario] = "N/A (> tempo)"
                continue
            if nome_cenario == "1. Aleatório (Chaves Grandes)" and nome_alg == "Contagem":
                resultados[nome_alg][nome_cenario] = "N/A (memória)"
                continue

            tempos = []
            repeticoes = 5 if "Minúscula" not in nome_cenario else 50
            for _ in range(repeticoes):
                amostra = list(dados)
                t0 = time.perf_counter()
                func(amostra)
                t1 = time.perf_counter()
                tempos.append((t1 - t0) * 1000)  # em ms
            
            media = sum(tempos) / len(tempos)
            resultados[nome_alg][nome_cenario] = f"{media:.2f} ms"

    # Imprime a tabela pronta em formato Markdown
    print("\n| Algoritmo | " + " | ".join(cenarios.keys()) + " |")
    print("| :--- | " + " | ".join([":---" for _ in cenarios]) + " |")
    for nome_alg in algoritmos:
        linha = [resultados[nome_alg].get(c, "N/A") for c in cenarios]
        print(f"| **{nome_alg}** | " + " | ".join(linha) + " |")

if __name__ == "__main__":
    if "--benchmark" in sys.argv:
        benchmark_cenarios()
    else:
        rodar_testes_borda()
        benchmark_cenarios()

if __name__ == "__main__":
    if "--test" in sys.argv:
        rodar_testes_borda()
    else:
        rodar_testes_borda()
        print("Ambiente inicial validado. Execute com os scripts de benchmark para preencher a tabela.")
