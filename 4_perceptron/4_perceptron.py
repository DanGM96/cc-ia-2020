# 8.3.2 - Perceptron - AND
from copy import deepcopy
import valores

def zeros(n):
    """ Cria um vetor de zeros """
    return [0 for i in range(n)]

def perceptron(dados):
    """ Regra de Perceptron para redes neurais """
    # Passo 0:
    # Inicialize os pesos e bias. Inicialize com o valor zero.
    # Inicialize a taxa de aprendizagem alpha (0 < alpha <= 1). Inicialize com o valor 1.
    n = len(dados[0][0]) - 1
    weight = zeros(n + 1)
    alpha = 1
    tetha = 0
    epoch = 0
    bias = zeros(4)

    # Passo 1: Enquanto a condição de parada for falsa, faça os passos 2 a 6.
    while True:
        print(f"> Época {epoch + 1}:")
        print(weight)
        # Passo 2: Para cada par de treinamento entrada(e_i)/saída(t), faça os passos 3 a 5.
        for i, dado in enumerate(dados):
            # Passo 3: Ajuste as ativações de entrada (x_i = e_i)
            x = dado[0] # Entradas
            t = dado[1] # Saída esperada

            # Passo 4: Calcule a saída.
            y = bias[i] # Bias
            for j in range(n):
                y += x[j] * weight[j]

            if y > tetha:
                y = 1
            elif -tetha <= y <= tetha:
                y = 0
            elif y < -tetha:
                y = -1

            # Passo 5: Atualize os pesos e o bias se houver erros para o padrão atual.
            weight_old = deepcopy(weight)
            if y != t:
                for k in range(n):
                    weight[k] += alpha * t * x[k]
                weight[n] += alpha * t # Bias é weight[n]
                bias[i] += alpha * t
            print(weight)

        # Passo 6: Teste a condição de parada:
        epoch += 1
        if weight_old == weight and epoch > 1:
            return False

if __name__ == "__main__":
    perceptron(valores.treinamento_and())
