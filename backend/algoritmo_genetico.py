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

if __name__ == "__main__":
    main()