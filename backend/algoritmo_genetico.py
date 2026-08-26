TAMANHO_POPULACAO = 40
QUANTIDADE_FILHOS = 20
MAXIMO_GERACOES = 10_000

QUANTIDADE_BITS = 9
PONTO_CORTE = 4
TAXA_MUTACAO = 0.03

VALOR_MINIMO = 0
VALOR_MAXIMO = 511

def main():
    print("Algoritmo genético iniciado!")
    print("Tamanho da população:", TAMANHO_POPULACAO)
    print("Quantidade de filhos:", QUANTIDADE_FILHOS)
    print("Máximo de gerações:", MAXIMO_GERACOES)
    print("Quantidade de bits:", QUANTIDADE_BITS)
    print("Ponto de corte:", PONTO_CORTE)
    print("Taxa de mutação:", TAXA_MUTACAO)
    print("Domínio:", VALOR_MINIMO, "a", VALOR_MAXIMO)


if __name__ == "__main__":
    main()