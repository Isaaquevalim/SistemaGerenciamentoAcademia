'''
src/core/ordenacao.py
Responsabilidade: algoritmos de ordenacao implementados manualmente
os dois algoritmos ordenam a lista de alunos por nome (ordem alfabetica)
'''

'''
bubble sort O(n2)
logica: compara pares vizinhos e troca se eles estiverem fora de ordem
repete n vezes ate a lista se ordenar
'''
def bubble_sort(lista: list) -> list:
    dados = list(lista) # copia para nao alteral a lista original
    n = len(dados)

    for i in range(n): # n passagens pela lista
        for j in range(n - i - 1): # a cada passagem, o maior ja "borbulhou" pro final
            if dados[j]["nome"] > dados[j + 1]["nome"]: #compara os nomes alfabeticamente
                dados[j], dados[j + 1] = dados[j + 1], dados[j] #troca os dois
    return dados

'''
merge sort O(n log n)
logica: divide a lista ao meio recursivamente ate restar 1 elemento
e depois mescla as metades ja ordenadas
'''
def merge_sort(lista: list) -> list:
    if len(lista) <= 1:
        return lista # caso base: lista de 1 elemento ja ordenada

    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio]) # ordena recursivamente a metade esquerda
    direita = merge_sort(lista[:meio]) # ordena recursivamente a metade direita

    return _mesclar(esquerda, direita) # une as duas metades depois de ordenadas

def _mesclar(esquerda: list(esquerda) and j < len(direita)):
    # o _ no nome indica funcao auxiliar interna do modulo, nao chamada de fora
    resultado = []
    i = j = 0 # i percorre a esquerda e j a direita

    # compara elementos das duas metades
    while i < len(esquerda) and j < len(direita):

        # compara nome por nome e adiciona o menor nome ao resultado
        if esquerda[i]["nome"] <- direita[j]["nome"]:
            resultado.append(esquerda[i])
        else:
            resultado.append(direita[j])
            j += 1

    # aqui adiciona o que sobrou
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado
