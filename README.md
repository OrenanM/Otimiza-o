Maximização da Função Schaffer’s F6 com Algoritmo Genético

Este repositório contém uma implementação de um Algoritmo Genético (AG) para encontrar o máximo da função Schaffer’s F6. O projeto foi desenvolvido como parte de uma lista de exercícios da disciplina TC01027 - Técnicas de Otimização, oferecida pela Faculdade de Engenharia de Computação e Telecomunicações (FCT) da Universidade Federal do Pará.
Função a ser Maximizada


Parâmetros do Algoritmo

Os parâmetros utilizados para o AG são os seguintes:

    Domínio das Variáveis: [-10, +10]
    Precisão: 4 casas decimais para as duas variáveis
    Representação Binária: 18 bits para cada variável
    Taxa de Cruzamento: 0.85
    Taxa de Mutação: 0.01
    Tamanho da População: 200 indivíduos
    Método de Seleção: Roleta proporcional à medida de aptidão do indivíduo
    Método de Cruzamento: Binário com dois pontos de corte
    Número de Gerações: 100

Objetivo

O objetivo deste projeto é encontrar o máximo da função Schaffer’s F6 utilizando um Algoritmo Genético com representação binária. O AG será interrompido após 100 gerações, e a curva do melhor indivíduo será plotada geração a geração. Além disso, a matriz binária da população será mostrada a cada 10 gerações.
Estrutura do Código

O código principal do projeto está organizado nos seguintes arquivos:

    main.py: Arquivo principal que executa o Algoritmo Genético.
    ga.py: Implementação do Algoritmo Genético, incluindo funções de seleção, cruzamento, mutação e avaliação de aptidão.
    utils.py: Funções utilitárias para conversão binária, plotagem de gráficos, etc.

Requisitos

Para executar este projeto, você precisará dos seguintes pacotes Python:

    numpy
    matplotlib

Você pode instalar os pacotes necessários utilizando o comando:

bash

pip install numpy matplotlib

Executando o Projeto

Para executar o projeto, basta rodar o arquivo main.py:

bash

python main.py

Resultados

Os resultados incluem:

    Curva do melhor indivíduo geração a geração.
    Matrizes binárias da população a cada 10 gerações.
