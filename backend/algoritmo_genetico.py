import math

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

if __name__ == "__main__":
    main()