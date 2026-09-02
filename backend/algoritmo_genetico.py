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
    cadidatos = populacao + filhos_mutados

    candidatos_ordenados = ordenar_por_aptidao(cadidatos)

    sobreviventes = []

    for indice in range(TAMANHO_POPULACAO):
        sobreviventes.append(candidatos_ordenados[indice])

    return sobreviventes




def main():
    print()
    print("Algoritmo genético iniciado!")
    print("Tamanho da população:", TAMANHO_POPULACAO)
    print("Quantidade de filhos:", QUANTIDADE_FILHOS)
    print("Máximo de gerações:", MAXIMO_GERACOES)
    print("Quantidade de bits:", QUANTIDADE_BITS)
    print("Ponto de corte:", PONTO_CORTE)
    print("Taxa de mutação:", TAXA_MUTACAO)
    print("Domínio:", VALOR_MINIMO, "a", VALOR_MAXIMO)

    print()
    print("Teste da função de aptidão:")
    print("f(0) =", calcular_aptidao(0))
    print("f(20) =", calcular_aptidao(20))
    print("f(100) =", calcular_aptidao(100))

    populacao = criar_populacao_inicial()

    print()
    print("População inicial:")

    for indice, cromossomo in enumerate(populacao):
        valor_x = int(cromossomo, 2)
        aptidao = calcular_aptidao(valor_x)

        print(
            indice,
            "Cromossomo:", 
            cromossomo,
            "- x",
            valor_x,
            "- Aptidão:",
            aptidao,
        )

    assert len(populacao) == TAMANHO_POPULACAO

    for cromossomo in populacao:
        assert len(cromossomo) == QUANTIDADE_BITS
        assert set(cromossomo).issubset({"0", "1"})

        valor_x = int(cromossomo, 2)
        assert VALOR_MINIMO <= valor_x <= VALOR_MAXIMO

    populacao_igual = [
        "111111111",
        "111111111",
        "111111111",
    ]

    populacao_diferente = [
        "111111111",
        "000000000",
        "101010101",
    ]

    assert populacao_convergiu(populacao_igual)
    assert not populacao_convergiu(populacao_diferente)

    print()
    print("População inicial convergiu:", populacao_convergiu(populacao))
    print("Testes de convergência concluídos com sucesso!")

    pesos = calcular_pesos_roleta(populacao)

    assert len(pesos) == len(populacao)

    for peso in pesos:
        assert peso > 0

    print()
    print("Teste de seleção por roleta:")

    for numero_selecao in range(10):
        pai_selecionado = selecionar_pai_por_roleta(populacao, pesos)

        assert pai_selecionado in populacao

        valor_x = int(pai_selecionado, 2)
        aptidao = calcular_aptidao(valor_x)

        print(
            "Seleção",
            numero_selecao + 1,
            "- Pai:",
            pai_selecionado,
            "- x:",
            valor_x,
            "- Aptidão:",
            aptidao,
        )

    print()
    print("Teste de cruzamento:")

    pai_teste = "101001101"
    mae_teste = "001111000"

    filho_teste = cruzar(pai_teste, mae_teste)

    print("Pai: ", pai_teste)
    print("Mãe: ", mae_teste)
    print("Filho:", filho_teste)

    assert filho_teste == "101011000"

    filhos = gerar_filhos(populacao)

    assert len(filhos) == QUANTIDADE_FILHOS

    for filho in filhos:
        assert len(filho) == QUANTIDADE_BITS
        assert set(filho).issubset({"0", "1"})

    print()
    print("Filhos gerados:")

    for indice, filho in enumerate(filhos):
        valor_x = int(filho, 2)
        aptidao = calcular_aptidao(valor_x)

        print(
            indice,
            "- Cromossomo:",
            filho,
            "- x:",
            valor_x,
            "- Aptidão:",
            aptidao,
        )

    cromossomo_teste = "101001101"

    sem_mutacao = aplicar_mutacao(
        cromossomo_teste, 
        taxa_mutacao=0
    )

    mutacao_total = aplicar_mutacao(
        cromossomo_teste, 
        taxa_mutacao=1
    )

    assert sem_mutacao == "101001101"
    assert mutacao_total == "010110010"

    print()
    print("Teste controlado de mutação:")
    print("Original: ", cromossomo_teste)
    print("Taxa 0%: ", sem_mutacao)
    print("Taxa 100%: ", mutacao_total)

    filhos_mutados = aplicar_mutacao_nos_filhos(filhos)

    assert len(filhos_mutados) == QUANTIDADE_FILHOS

    for filho in filhos_mutados:
        assert len(filho) == QUANTIDADE_BITS
        assert set(filho).issubset({"0", "1"})

    print()
    print("Filhos após mutação:")

    for indice in range(len(filhos)):
        print(
            indice,
            "- Antes:",
            filhos[indice],
            "- Depois:",
            filhos_mutados[indice]
        )

    candidatos = populacao + filhos_mutados
    nova_populacao = selecionar_sobreviventes(
        populacao,
        filhos_mutados
    )

    assert len(candidatos) == 60
    assert len(nova_populacao) == TAMANHO_POPULACAO

    for indice in range(len(nova_populacao) - 1):
        x_atual = int(nova_populacao[indice], 2)
        x_seguinte = int(nova_populacao[indice + 1], 2)

        aptidao_atual = calcular_aptidao(x_atual)
        aptidao_seguinte = calcular_aptidao(x_seguinte)

        assert aptidao_atual >= aptidao_seguinte

    print()
    print("Nova população com os 40 sobreviventes:")

    for indice, cromossomo in enumerate(nova_populacao):
        valor_x = int(cromossomo, 2)
        aptidao = calcular_aptidao(valor_x)

        print(
            indice,
            "- Cromossomo:",
            cromossomo,
            "- x:",
            valor_x,
            "- Aptidão:",
            aptidao
        )



if __name__ == "__main__":
    main()