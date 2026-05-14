''' 
Responsabilidade -> estrutura FIFO (primeiro que entra, primeiro que sai)
Aplicacao -> fila de atendimento e fila da espera por aula
'''

class Fila:

    def __init__(self, nome: str):
        self._dados = [] # lista interna que representa a fila/cria uma lista vazia
        self.nome = nome # identifica a fila (ex: Recepcao, Spinning, etc)

    #enfileirar O(1) -> adiciona no final da fila
    def enqueue(self, aluno: dict):
        self._dados.append(aluno) #append que faz a funcao de adicionar ao final da fila

    #desenfileirar O(n) -> remove o primeiro elemento e os demais andam uma posicao            
    def dequeue(self) -> dict | None: #dict > se houver alguem na fila | None > se nao houver alguem na fila
        if self.esta_vazia():    # verifica antes de remover se esta vazia
            return None          #fila vazia: ninguem a ser atendido (evita erro)
        return self.dados_pop(0) #remove o elenento da posicao 0 e retorna o primeiro da fila

    #espiar O(1) -> espia o proximo sem remover > usado para exibir o proximo da fila
    def peek(self) -> dict | None:
        if self.esta_vazia():
            return None
        return self._dados[0] #retorna o elemento na posicao 0
    
    #esta vazia O() -> verifica o tamanho interno
    def esta_vazia(self) -> bool:
        return len(self._dados) == 0 #len pega o tamanho da lista, se lista = 0, retorna true
    
    #tamanho O(1) -> retorna quantos elementos na fila
    def tamanho(self) -> int:
        return len(self._dados) #len le a fila e retorna o tamanho em inteiro
    
    #exibir O(n) -> retorna uma copia para nao expor dados internos
    def exibir(self) -> list:
        return list(self._dados) #cria a copia list da lista, para proteger de codigo externo