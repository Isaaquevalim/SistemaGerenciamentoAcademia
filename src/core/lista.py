'''
Responsabilidade: estrutura de dados lista, armazena e manipula alunos
'''

class ListaAlunos:


    def __init__(self):
        self._dados = [] #lista interna vazia o _ mostra uso apenas dentro da classe

    # insercao O(1) -> append vai direto ao final, nao percorrendo nada
    def inserir(self, aluno: dict):
        self._dados.append(aluno) #adiciona o aluno ao final da lista

    # remocao O(n) -> percorre ate encontrar o id, depois reorganiza os indices
    def remover(self, id_aluno: int) -> bool:
        for i, aluno in enumerate(self._dados): # enumerate da o indice + o valor juntos
            if aluno["id"] == id_aluno: #confere se o aluno atual no loop e o procurad
                self._dados.pop(i) #remove pelo indice encontrado
                return True #se id encontrado e removido
        return False # caso id nao exista na lista
    
    # busca sequencial O(n): percorre do inicio ao fim 1 por 1 ate encontrar(usada sem ordenacao)
    def buscar_sequencial(self, nome: str) -> dict | None:
        nome_lower = nome.lower() # normaliza para ignorar maiusculas evitando erro
        for aluno in self._dados:
            if aluno["nome"].lower() == nome_lower:
                return aluno #retorna o dicionario do aluno que foi encontrado
        return None #se nao encontrado na lista
    
    '''
    busca binaria O(log n) -> divide a lista ao meio a cada passo
    pre condicao obrigatoria: a lista deve estar ordenada por nome
    '''
    def busca_binaria(self, nome: str) -> dict | None: 
        esquerda, direita = 0, len(self._dados) - 1
        nome_lower = nome.lower()
        
        #continua enquanto existir area de busca
        while esquerda <= direita:
            meio = (esquerda + direita) // 2 # calcula o indice central
            nome_meio = self._dados[meio]["nome"].lower()

            if nome_meio == nome_lower:
                return self._dados[meio] #achou diretamento no meio
            elif nome_lower < nome_meio:
                direita = meio - 1 # busca na metade esquerda
            else:
                esquerda = meio + 1 # busca na metade direita
        return None
    
    # exibir O(n) -> retorna uma copia da lista, nao expondo dados internos
    def exibir_todos(self) -> list:
        return list(self._dados) #cria a copia list da lista, para proteger de codigo externo
    
    # tamanho 0(1) -> py ja guarda o tamanho internamento, nao precisa contar
    def tamanho(self) -> int:
        return len(self._dados) #retorna a quantidade de alunos em int
        
    