import random

# Função a ser minimizada
def f(x):
    return x**3 - 6*x + 14

# Codificação binária de x
def codificar(x, bits=16):
    x_int = int((x + 10) * (2**(bits-1) / 20))
    return [int(b) for b in format(x_int, f'0{bits}b')]

def decodificar(binario, bits=16):
    x_int = int("".join(map(str, binario)), 2)
    return x_int * 20 / (2**(bits-1)) - 10

# Inicialização da população
def inicializar_populacao(tamanho, bits=16):
    return [codificar(random.uniform(-10, 10), bits) for _ in range(tamanho)]

# Seleção por torneio
def selecao_torneio(populacao, pontuacoes, k=3):
    selecionados = random.sample(list(zip(populacao, pontuacoes)), k)
    selecionados.sort(key=lambda x: x[1])
    return selecionados[0][0]

# Crossover de um ponto
def crossover(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

# Mutação
def mutacao(individuo, taxa_mutacao=0.01):
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]

# Algoritmo Genético
def algoritmo_genetico(f, geracoes=100, tamanho_populacao=10, taxa_mutacao=0.01, elitismo=True, tamanho_elite=0.1):
    bits = 16
    populacao = inicializar_populacao(tamanho_populacao, bits)
    melhor_individuo = None
    melhor_pontuacao = float('inf')

    for geracao in range(geracoes):
        pontuacoes = [f(decodificar(individuo, bits)) for individuo in populacao]
        melhor_geracao = min(pontuacoes)
        if melhor_geracao < melhor_pontuacao:
            melhor_pontuacao = melhor_geracao
            melhor_individuo = populacao[pontuacoes.index(melhor_geracao)]

        nova_populacao = []
        if elitismo:
            quantidade_elite = int(tamanho_elite * tamanho_populacao)
            indices_elite = sorted(range(len(pontuacoes)), key=lambda i: pontuacoes[i])[:quantidade_elite]
            nova_populacao.extend([populacao[i] for i in indices_elite])

        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, pontuacoes)
            pai2 = selecao_torneio(populacao, pontuacoes)
            filho1, filho2 = crossover(pai1, pai2)
            mutacao(filho1, taxa_mutacao)
            mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao[:tamanho_populacao]

    return decodificar(melhor_individuo, bits), melhor_pontuacao

melhor_x, melhor_f = algoritmo_genetico(f)
print(f"Melhor x: {melhor_x}, com valor mínimo da função: {melhor_f}")
