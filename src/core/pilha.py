'''
Responsabilidade: estrutura LIFO -> ultima acao realizada e a primeira a ser desfeita
Usada para historico de acoes com funcao desfazer
'''

LIMITE = 10 # constante -> maximo de acoes armazenadas (evita o uso excessivo de memoria)

class Pilha:

    def __init__(self):
        self._dados = [] # topo da pilha = ultimo elemento da lista

    '''
    push O(1) -> empilha no topo (final da lista)
    se ja atingiu o limite, descarta a acao mais antiga (indice 0) antes de empilhar
    '''
    def push(self, acao: str):
        if len(self._dados) >= LIMITE: # se for maior que o limite
            self._dados.pop(0)         # remove a acao mais antiga para abrir espaco
        self._dados.append(acao) # empilha a nova acao no topo

    # pop O(1) -> desempilha do topo (ultima acao = ultima posicao)
    def pop(self) -> str | None:
        if self._esta_vazia():
            return None          #pilha vazia: nada para fazer
        return self._dados.pop() #pop() sem argumento remove e retorna o ultimo
    
    # peek O(1) -> vizualiza o topo sem remover (util para mostrar a ultima acao)
    def peek(self) -> str | None:
        if self.esta_vazia():
            return None
        return self._dados[-1] # indice -1 acessa o ultimo elemento diretamente
    
    # esta vazia O(1)
    def esta_vazia(self) -> bool:
        return len(self._dados) == 0 # se a pilha for = 0 (vazia) retorna true
    
    # tamanho O(1)
    def tamanho(self) -> int:
        return len(self._dados)
    
    # exibir O(n) -> retorna copia na ordem do topo para a base (o mais recente primeiro)
    def exibir(self) -> list:
        return list(reversed(self._dados)) # reversed nao altera os dados internos
