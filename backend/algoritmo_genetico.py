import math
import random

TAMANHO_POPULACAO = 40
QUANTIDADE_FILHOS = 20
MAXIMO_GERACOES = 10_000

QUANTIDADE_BITS = 9
PONTO_CORTE = 4
TAXA_MUTACAO = 0.03

VALOR_MINIMO = 0
VALOR_MAXIMO = 511



def calcular_aptidao(x):
    return x * math.sin(x / 20) + 100



def criar_populacao_inicial():
    populacao = []

    for _ in range(TAMANHO_POPULACAO):
        valor_x = random.randint(VALOR_MINIMO, VALOR_MAXIMO)
        cromossomo = format(valor_x, f"0{QUANTIDADE_BITS}b")
        populacao.append(cromossomo)

    return populacao



def populacao_convergiu(populacao):
    if len(populacao) == 0:
        return False

    primeiro_cromossomo = populacao[0]

    for cromossomo in populacao:
        if cromossomo != primeiro_cromossomo:
            return False

    return True



def calcular_pesos_roleta(populacao):
    aptidoes = []

    for cromossomo in populacao:
        valor_x = int(cromossomo, 2)
        aptidao = calcular_aptidao(valor_x)
        aptidoes.append(aptidao)

    menor_aptidao = aptidoes[0]

    for aptidao in aptidoes:
        if aptidao < menor_aptidao:
            menor_aptidao = aptidao

    pesos = []

    for aptidao in aptidoes:
        peso = aptidao - menor_aptidao + 1
        pesos.append(peso)

    return pesos



def selecionar_pai_por_roleta(populacao, pesos):
    peso_total = 0

    for peso in pesos:
        peso_total += peso

    ponto_sorteado = random.random() * peso_total
    peso_acumulado = 0

    for indice in range(len(populacao)):
        peso_acumulado += pesos[indice]

        if peso_acumulado >= ponto_sorteado:
            return populacao[indice]

    return populacao[-1]



def cruzar(pai, mae):
    primeira_parte = pai[:PONTO_CORTE]
    segunda_parte = mae[PONTO_CORTE:]

    filho = primeira_parte + segunda_parte

    return filho



def gerar_filhos(populacao):
    pesos = calcular_pesos_roleta(populacao)
    filhos = []

    for _ in range(QUANTIDADE_FILHOS):
        pai = selecionar_pai_por_roleta(populacao, pesos)
        mae = selecionar_pai_por_roleta(populacao, pesos)

        filho = cruzar(pai, mae)
        filhos.append(filho)

    return filhos



def aplicar_mutacao(cromossomo, taxa_mutacao=TAXA_MUTACAO):
    bits = list(cromossomo)

    for indice in range(len(bits)):
        numero_sorteado = random.random()

        if numero_sorteado < taxa_mutacao:
            if bits[indice] == "0":
                bits[indice] = "1"
            else:
                bits[indice] = "0"

    cromossomo_mutado = "".join(bits)

    return cromossomo_mutado


def aplicar_mutacao_nos_filhos(filhos):
    filhos_mutados = []

    for filho in filhos:
        filho_mutado = aplicar_mutacao(filho)
        filhos_mutados.append(filho_mutado)

    return filhos_mutados



def ordenar_por_aptidao(individuos):
    individuos_ordenados = individuos.copy()
    quantidade = len(individuos_ordenados)

    for posicao_atual in range(quantidade - 1):
        indice_melhor = posicao_atual

        for indice in range(posicao_atual + 1, quantidade):
            cromossomo_atual = individuos_ordenados[indice]
            cromossomo_melhor = individuos_ordenados[indice_melhor]

            x_atual = int(cromossomo_atual, 2)
            x_melhor = int(cromossomo_melhor, 2)

            aptidao_atual = calcular_aptidao(x_atual)
            aptidao_melhor = calcular_aptidao(x_melhor)

            if aptidao_atual > aptidao_melhor:
                indice_melhor = indice

        temporario = individuos_ordenados[posicao_atual]

        individuos_ordenados[posicao_atual] = (
            individuos_ordenados[indice_melhor]
        )

        individuos_ordenados[indice_melhor] = temporario

    return individuos_ordenados



def selecionar_sobreviventes(populacao, filhos_mutados):
    candidatos = populacao + filhos_mutados

    candidatos_ordenados = ordenar_por_aptidao(candidatos)

    sobreviventes = []

    for indice in range(TAMANHO_POPULACAO):
        sobreviventes.append(candidatos_ordenados[indice])

    return sobreviventes



def executar_algoritmo_genetico():
    populacao = criar_populacao_inicial()
    populacao_inicial = populacao.copy()

    quantidade_geracoes = 0

    while (
        quantidade_geracoes < MAXIMO_GERACOES
        and not populacao_convergiu(populacao)
    ):
        filhos = gerar_filhos(populacao)

        filhos_mutados = aplicar_mutacao_nos_filhos(filhos)

        populacao = selecionar_sobreviventes(populacao, filhos_mutados)

        quantidade_geracoes += 1

    populacao_final = ordenar_por_aptidao(populacao)
    melhor_cromossomo = populacao_final[0]

    melhor_x = int(melhor_cromossomo, 2)
    melhor_aptidao = calcular_aptidao(melhor_x)

    resultado = {
        "geracoes": quantidade_geracoes,
        "melhor_individuo": melhor_cromossomo,
        "x": melhor_x,
        "aptidao": melhor_aptidao,
        "cromossomo_binario": melhor_cromossomo,
        "populacao_inicial": populacao_inicial,
        "populacao_final": populacao_final,
        "convergiu": populacao_convergiu(populacao_final),
    }

    return resultado



def main():
    print()
    print("Executando algoritmo genético...")

    resultado = executar_algoritmo_genetico()

    print()
    print("Resultado final:")
    print("Gerações executadas:", resultado["geracoes"])
    print("Melhor indivíduo:", resultado["melhor_individuo"])
    print("Valor de x:", resultado["x"])
    print("Valor de f(x):", resultado["aptidao"])
    print("Cromossomo:", resultado["cromossomo_binario"])
    print("Convergiu:", resultado["convergiu"])



if __name__ == "__main__":
    main()