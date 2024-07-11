import numpy as np
import matplotlib.pyplot as plt

def decimal_binario(decimal):
    """
    Converte um número decimal em uma string binária de 18 bits,
    incluindo um bit de sinal.

    Args:
        decimal (float): Número decimal a ser convertido.

    Returns:
        str: String binária de 18 bits representando o número.
    """
    # Multiplica o decimal por 10000 para lidar com a precisão e converte para inteiro
    decimal = int(decimal * 10000)

    if decimal > 0:
        # Converte o decimal positivo para binário, remove o prefixo '0b' e preenche com zeros até ter 17 bits
        binario = bin(decimal)[2:]
        binario = binario.zfill(17)
        # Adiciona o bit de sinal '0' indicando que o número é positivo
        binario = '0' + binario
    else:
        # Converte o decimal negativo para binário, remove o prefixo '-0b' e preenche com zeros até ter 17 bits
        binario = bin(decimal)[3:]
        binario = binario.zfill(17)
        # Adiciona o bit de sinal '1' indicando que o número é negativo
        binario = '1' + binario

    return binario

def binario_decimal(binario):
    """
    Converte uma string binária de 18 bits, incluindo um bit de sinal,
    em um número decimal.

    Args:
        binario (str): String binária de 18 bits a ser convertida.

    Returns:
        float: Número decimal representado pela string binária.
    """
    # Extrai o bit de sinal
    sinal = binario[0]
    # Extrai a magnitude (parte numérica sem o sinal)
    magnitude = binario[1:]

    # Converte a magnitude de binário para decimal e divide por 10000 para retornar à precisão original
    decimal = int(magnitude, 2) / 10000
    if sinal == '1':
        # Se o bit de sinal é '1', o número é negativo
        decimal *= -1
    
    return decimal

def decod_representacao(populacao):
    """
    Decodifica uma população de cromossomos binários em listas de valores decimais.

    Args:
        populacao (list of str): Lista de cromossomos binários, onde cada cromossomo
                                 é uma string binária representando valores x e y concatenados.

    Returns:
        tuple: Duas listas contendo os valores decodificados de x e y, respectivamente.
    """
    x_list = []
    y_list = []
    for cromossomo in populacao:
        # Divide o cromossomo em duas partes: x (primeiros 18 bits) e y (últimos 18 bits)
        x = cromossomo[:18]
        y = cromossomo[18:]

        # Converte as representações binárias de x e y para valores decimais
        x = binario_decimal(x)
        y = binario_decimal(y)

        # Adiciona os valores decodificados às listas correspondentes
        x_list.append(x)
        y_list.append(y)
        
    return x_list, y_list

def representacao(x_dom, y_dom):
    """
    Converte listas de valores decimais x e y em uma população de cromossomos binários.

    Args:
        x_dom (list of float): Lista de valores decimais para x.
        y_dom (list of float): Lista de valores decimais para y.

    Returns:
        list of str: Lista de cromossomos binários, onde cada cromossomo
                     é uma string binária representando valores x e y concatenados.
    """
    populacao = []
    for x, y in zip(x_dom, y_dom):
        # Converte os valores decimais de x e y para representações binárias
        xbin = decimal_binario(x)
        ybin = decimal_binario(y)

        # Concatena as representações binárias de x e y para formar o cromossomo
        populacao.append(xbin + ybin)
    
    return populacao


import numpy as np

def fitness(populacao):
    """
    Calcula o valor de fitness para cada cromossomo em uma população.

    Args:
        populacao (list): Lista de cromossomos, onde cada cromossomo é uma string binária de 36 bits.

    Returns:
        list of float: Lista contendo os valores de fitness para cada cromossomo na população.
    """
    lista_fitness = []
    for cromossomo in populacao:
        # Extrai os valores x e y do cromossomo e converte para decimal
        x = binario_decimal(cromossomo[:18])
        y = binario_decimal(cromossomo[18:])

        # Calcula o fitness com base na função F6(x, y)
        numerador = np.sin(np.sqrt(x**2 + y**2))**2 - 0.5
        denominador = (1 + 0.001 * (x**2 + y**2))**2
        fitness = 0.5 - numerador / denominador

        # Adiciona o valor de fitness à lista de fitness
        lista_fitness.append(fitness)
        
    return lista_fitness


def sorteio(population, fitness_populacao):
    """
    Seleciona dois pais de uma população com base em suas aptidões usando roleta viciada.

    Args:
        population (list): Lista de cromossomos representando a população.
        fitness_populacao (list of float): Lista de valores de aptidão para cada cromossomo na população.

    Returns:
        tuple: Dois cromossomos selecionados como pais.
    """
    # Verifica se a soma das aptidões é igual a 1; caso contrário, normaliza as aptidões
    if sum(fitness_populacao) != 1:
        fitness_populacao = np.array(fitness_populacao)
        fitness_populacao = fitness_populacao / np.sum(fitness_populacao)
    
    # Seleciona dois pais com base nas aptidões normalizadas
    pais = np.random.choice(population, p=fitness_populacao, size=2, replace=False)
    
    return pais[0], pais[1]

def cruzamento(pai1, pai2, taxa_cruzamento=0.85):
    """
    Realiza o cruzamento entre dois cromossomos pais para gerar um novo cromossomo filho.

    Args:
        pai1 (str): Cromossomo do primeiro pai.
        pai2 (str): Cromossomo do segundo pai.
        taxa_cruzamento (float, optional): Probabilidade de ocorrer o cruzamento. 
                                           O valor padrão é 0.85.

    Returns:
        str: Novo cromossomo filho gerado pelo cruzamento ou None se o cruzamento não ocorrer.
    """
    # Decide se o cruzamento ocorrerá com base na taxa de cruzamento
    cruza = np.random.choice([True, False], p=[taxa_cruzamento, 1 - taxa_cruzamento])
    if not cruza:
        return None
    
    # Comprimento dos cromossomos
    n = len(pai1)
    # Gera uma lista de índices de 0 a n
    indexes = np.linspace(0, n, n + 1, dtype=int)
    
    # Escolhe dois pontos de corte aleatórios
    ponto_corte = np.random.choice(indexes, 2, replace=False)
    ponto_corte.sort()
    
    # Gera o cromossomo filho combinando segmentos dos pais entre os pontos de corte
    filho = pai1[:ponto_corte[0]] + pai2[ponto_corte[0]:ponto_corte[1]] + pai1[ponto_corte[1]:]
    
    return filho

def mutacao(filho, taxa_mutacao=0.01):
    """
    Aplica mutação em um cromossomo filho, alterando aleatoriamente seus genes 
    com base na taxa de mutação.

    Args:
        filho (str): Cromossomo filho a ser mutado.
        taxa_mutacao (float, optional): Probabilidade de cada gene sofrer mutação.
                                        O valor padrão é 0.01.

    Returns:
        str: Novo cromossomo filho após a mutação.
    """
    novo_filho = []
    for gene in filho:
        # Decide se o gene sofrerá mutação com base na taxa de mutação
        if np.random.uniform() < taxa_mutacao:
            # Inverte o gene (0 vira 1 e 1 vira 0)
            novo_gene = '0' if gene == '1' else '1'
        else:
            # Mantém o gene original
            novo_gene = gene
        novo_filho.append(novo_gene)
    
    # Junta a lista de genes mutados em uma string
    return ''.join(novo_filho)


def selecao_aptos(population1, fitness1, population2, fitness2):
    """
    Seleciona os indivíduos mais aptos de duas populações combinadas com base em seus fitness.

    Args:
        population1 (list): Lista de cromossomos da primeira população.
        fitness1 (list of float): Lista de valores de fitness para a primeira população.
        population2 (list): Lista de cromossomos da segunda população.
        fitness2 (list of float): Lista de valores de fitness para a segunda população.

    Returns:
        list: Lista contendo os indivíduos mais aptos combinados das duas populações.
    """
    # Número de indivíduos na primeira população
    n = len(population1)

    # Combina as duas populações e seus respectivos fitness
    population1.extend(population2)
    fitness1.extend(fitness2)

    # Ordena os indivíduos combinados com base em seus fitness (do menor para o maior)
    # e seleciona os indivíduos mais aptos (os últimos n indivíduos da lista ordenada)
    population = [item for _, item in sorted(zip(fitness1, population1))]
    population = population[n:]

    return population


def plot_x_y(populacao, n):
    """
    Plota um gráfico de dispersão dos valores de X e Y decodificados de uma população de cromossomos.

    Args:
        population (list): Lista de cromossomos binários representando a população.

    Returns:
        None
    """
    # Decodifica a representação binária da população em valores de X e Y
    x_populacao, y_populacao = decod_representacao(populacao)
    
    plt.figure(figsize=(5.5, 5))
    # Plota o gráfico de dispersão
    plt.scatter(x_populacao, y_populacao)
    
    # Adiciona linhas de referência nos eixos x e y
    plt.axvline(0, 0, color='black')
    plt.axhline(0, 0, color='black')
    
    # Define os limites dos eixos x e y
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    
    # Configurações de tamanho das fontes nos eixos
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    
    # Rótulos dos eixos x e y
    plt.xlabel('X', fontsize=13)
    plt.ylabel('Y', fontsize=13, rotation=0)

    plt.grid()
    plt.title(f"Geração {n}")
    plt.savefig(f'images/geracao{n}.png', bbox_inches='tight')
    plt.show()
