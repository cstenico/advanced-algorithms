#JKP Puzzle

##Idea resolver um resta-um com janken inbutido.

Desenvolvimento:
    Aplicar um "DFS" em todas as posições do tabuleiro com peças
    Logo, constitui um brute-force de, pelo menos, O(n^2).

    Para cada peça, montar uma árvore de recursão, portanto, podemos
    iterar a cada jogada e determinar o número de possibilidades.

    Atenção com:
        1) Ilhas das peças: uma peça ficar isolada na situação:
            000
            010
            000
            onde 0 é empty (segundo o Asset)
        2) Parada da Recursão: Tabuleiro com uma única peça.
