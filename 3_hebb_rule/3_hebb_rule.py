# 8.3.1 - Regra de Hebb - AND
import valores

def zeros(n):
    """ Cria um vetor de zeros """
    return [0 for i in range(n)]

def hebb_rule(dados):
    """ Regra de Hebb para redes neurais """
    # Passo 0: Inicializar todos os pesos
    n = len(dados[0][0]) - 1
    weight = zeros(n + 1)
    print(weight)

    # Passo 1: Para cada vetor de treinamento na entrada e par de objetivos na saída (e : s)
    for _, dado in enumerate(dados):
        # Passo 2: Ajuste as ativações para as unidades de entrada
        x = dado[0]
        # Passo 3: Ajuste a ativação para a unidade de saída
        y = dado[1]
        # Passo 4: Ajuste os pesos e o bias
        for j in range(n):
            weight[j] = weight[j] + x[j] * y
        weight[n] = weight[n] + y # Bias é weight[n]
        print(weight)

if __name__ == "__main__":
    hebb_rule(valores.treinamento_and())
