'''
src/service/academia_service.py
responsabilidade: orquestrar todas as operações do sistema.
e a unica camada que conhece tanto o banco quanto as estruturas de dados.
e UI nunca acessa o banco diretamente —> tudo passa por aqui.
'''

# importa as classes de repositório para acessar o banco de dados
from core.lista import ListaAlunos
from core.fila import Fila
from core.pilha import Pilha
from core.ordenacao import bubble_sort, merge_sort
from database.repositorios.aluno_repo import AlunoRepo
from database.repositorios.aula_repo import AulaRepo
from database.repositorios.plano_repo import PlanoRepo
from database.conexao import inicializar_banco


class AcademiaService:

    def __init__(self):
        # inicializa o banco na primeira execução (cria academia.db e tabelas)
        inicializar_banco()

        # instancia os repositórios — cada um cuida de uma tabela do banco
        self._aluno_repo = AlunoRepo()
        self._aula_repo  = AulaRepo()
        self._plano_repo = PlanoRepo()

        # instancia as estruturas de dados em memória
        self._lista   = ListaAlunos()         # armazena alunos durante a sessão
        self._pilha   = Pilha()               # histórico de ações (max 10)
        
        '''
        dicionario de filas: cada aula tem sua própria fila de espera
        chave = id da aula (int), valor = objeto Fila
        ex: {1: Fila("Spinning 07:00"), 2: Fila("Yoga 09:00")}
         '''
        self._filas_espera = {}

        # fila unica de atendimento geral da recepção
        self._fila_atendimento = Fila("Recepção")

        # carrega os dados do banco para as estruturas em memória
        self._carregar_dados()

    '''
     ─────────────────────────────────────────────
     INICIALIZAÇÃO
     ─────────────────────────────────────────────
    '''
    def _carregar_dados(self):
        # le todos os alunos do banco e popula a lista em memoria
        # chamado apenas uma vez na inicializacao do sistema
        alunos = self._aluno_repo.buscar_todos()  # SELECT * FROM alunos
        for aluno in alunos:
            self._lista.inserir(aluno)            # O(1) por inserção

        # Cria uma fila de espera vazia para cada aula cadastrada
        aulas = self._aula_repo.buscar_todas()
        for aula in aulas:
            nome_fila = f"{aula['nome']} {aula['horario']}"
            self._filas_espera[aula["id"]] = Fila(nome_fila)

    '''
     ─────────────────────────────────────────────
     MÓDULO ALUNOS
     ─────────────────────────────────────────────
    '''
    def cadastrar_aluno(self, nome: str, cpf: str, telefone: str,
                        email: str, plano_id: int) -> dict:
        # regra 1: CPF deve ser único no sistema
        todos = self._aluno_repo.buscar_todos()
        for aluno in todos:
            if aluno["cpf"] == cpf:
                return {"sucesso": False, "mensagem": "CPF já cadastrado no sistema."}

        # regra 2: e-mail deve ser unico no sistema
        for aluno in todos:
            if aluno["email"] == email:
                return {"sucesso": False, "mensagem": "E-mail já cadastrado no sistema."}

        # regra 3: plano informado deve existir no banco
        plano = self._plano_repo.buscar_por_id(plano_id)
        if not plano:
            return {"sucesso": False, "mensagem": "Plano inválido."}

        # todas as regras passaram — grava no banco
        novo_id = self._aluno_repo.inserir(nome, cpf, telefone, email, plano_id)

        # monta o dicionário do novo aluno para inserir na lista
        novo_aluno = {
            "id": novo_id,
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email,
            "status": "ativo",
            "plano_id": plano_id
        }

        self._lista.inserir(novo_aluno)                          # O(1) na lista
        self._pilha.push(f"Cadastro: {nome} (ID {novo_id})")    # registra no historico

        return {"sucesso": True, "mensagem": f"Aluno {nome} cadastrado com sucesso!", "aluno": novo_aluno}

    def remover_aluno(self, id_aluno: int) -> dict:
        # verifica se o aluno existe antes de remover
        aluno = self._aluno_repo.buscar_por_id(id_aluno)
        if not aluno:
            return {"sucesso": False, "mensagem": "Aluno não encontrado."}

        nome = aluno["nome"]

        # remove do banco e da lista em memória
        self._aluno_repo.remover(id_aluno)   # DELETE no banco
        self._lista.remover(id_aluno)        # O(n) na lista

        self._pilha.push(f"Remoção: {nome} (ID {id_aluno})")  # registra no histórico

        return {"sucesso": True, "mensagem": f"Aluno {nome} removido com sucesso."}

    def buscar_aluno_sequencial(self, nome: str) -> dict:
        # cusca O(n) — nao exige lista ordenada
        resultado = self._lista.buscar_sequencial(nome)
        if resultado:
            return {"sucesso": True, "aluno": resultado}
        return {"sucesso": False, "mensagem": f"Aluno '{nome}' não encontrado."}

    def buscar_aluno_binario(self, nome: str) -> dict:
        # busca O(log n) — EXIGE lista ordenada
        # ordena com Merge Sort antes de buscar para garantir a pre-condição
        dados_ordenados = merge_sort(self._lista.exibir_todos())

        # reconstroi a lista interna com os dados ordenados
        self._lista = ListaAlunos()
        for aluno in dados_ordenados:
            self._lista.inserir(aluno)

        resultado = self._lista.buscar_binaria(nome)
        if resultado:
            return {"sucesso": True, "aluno": resultado}
        return {"sucesso": False, "mensagem": f"Aluno '{nome}' não encontrado."}

    def ordenar_lista(self, algoritmo: str) -> dict:
        # algoritmo: "bubble" ou "merge"
        dados = self._lista.exibir_todos()

        if algoritmo == "bubble":
            ordenados = bubble_sort(dados)      # O(n²)
            nome_algoritmo = "Bubble Sort"
        else:
            ordenados = merge_sort(dados)       # O(n log n)
            nome_algoritmo = "Merge Sort"

        # reconstroi a lista interna com os dados ordenados
        self._lista = ListaAlunos()
        for aluno in ordenados:
            self._lista.inserir(aluno)

        return {
            "sucesso": True,
            "mensagem": f"Lista ordenada com {nome_algoritmo}.",
            "alunos": self._lista.exibir_todos()
        }

    def listar_alunos(self) -> list:
        # retorna todos os alunos da lista em memoria — O(n)
        return self._lista.exibir_todos()

    def buscar_planos(self) -> list:
        # retorna todos os planos para popular dropdown na UI
        return self._plano_repo.buscar_todos()

    '''
     ─────────────────────────────────────────────
     MÓDULO FILA DE ATENDIMENTO
     ─────────────────────────────────────────────
    '''

    def entrar_fila_atendimento(self, nome_aluno: str) -> dict:
        # enfileira o aluno na fila de atendimento geral — O(1)
        self._fila_atendimento.enqueue({"nome": nome_aluno})
        posicao = self._fila_atendimento.tamanho()
        return {
            "sucesso": True,
            "mensagem": f"{nome_aluno} entrou na fila. Posição: {posicao}",
            "fila": self._fila_atendimento.exibir()
        }

    def chamar_proximo_atendimento(self) -> dict:
        # desenfileira o primeiro da fila — O(n)
        proximo = self._fila_atendimento.dequeue()
        if not proximo:
            return {"sucesso": False, "mensagem": "Fila de atendimento vazia."}

        self._pilha.push(f"Atendimento: {proximo['nome']}")  # registra no historico
        return {
            "sucesso": True,
            "mensagem": f"Chamando: {proximo['nome']}",
            "proximo": proximo,
            "fila": self._fila_atendimento.exibir()
        }

    def ver_proximo_atendimento(self) -> dict:
        # espia o primeiro sem remover — O(1)
        proximo = self._fila_atendimento.peek()
        if not proximo:
            return {"sucesso": False, "mensagem": "Fila de atendimento vazia."}
        return {"sucesso": True, "proximo": proximo}

    def estado_fila_atendimento(self) -> dict:
        return {
            "fila": self._fila_atendimento.exibir(),
            "tamanho": self._fila_atendimento.tamanho()
        }
    
    '''
     ─────────────────────────────────────────────
     MÓDULO FILA DE ESPERA POR AULA
     ─────────────────────────────────────────────
    '''
    def listar_aulas(self) -> list:
        return self._aula_repo.buscar_todas()

    def entrar_fila_espera_aula(self, id_aula: int, nome_aluno: str) -> dict:
        # verifica se a aula existe
        aulas = self._aula_repo.buscar_todas()
        aula = next((a for a in aulas if a["id"] == id_aula), None) # devolve a primeira aula que tiver id igual a id_aula ou None se nao encontrar
        if not aula:
            return {"sucesso": False, "mensagem": "Aula não encontrada."}

        # regra: so entra na fila de espera se a aula estiver realmente cheia
        if aula["vagas_disponiveis"] > 0:
            return {"sucesso": False, "mensagem": f"Ainda há {aula['vagas_disponiveis']} vaga(s) disponível(is). Não é necessário entrar na fila."}

        # garante que a fila da aula existe no dicionário
        if id_aula not in self._filas_espera:
            self._filas_espera[id_aula] = Fila(aula["nome"])

        self._filas_espera[id_aula].enqueue({"nome": nome_aluno})
        posicao = self._filas_espera[id_aula].tamanho()

        return {
            "sucesso": True,
            "mensagem": f"{nome_aluno} entrou na fila de espera. Posição: {posicao}",
            "fila": self._filas_espera[id_aula].exibir()
        }

    def liberar_vaga_aula(self, id_aula: int) -> dict:
        # chamado quando um aluno desiste de uma aula
        # regra: incrementa vaga no banco e chama o proximo da fila de espera
        self._aula_repo.incrementar_vaga(id_aula)

        fila = self._filas_espera.get(id_aula)
        if not fila or fila.esta_vazia():
            return {
                "sucesso": True,
                "mensagem": "Vaga liberada. Nenhum aluno na fila de espera.",
                "proximo": None
            }

        # chama o primeiro da fila de espera — dequeue O(n)
        proximo = fila.dequeue()
        # decrementa a vaga que acabou de ser liberada para o próximo
        self._aula_repo.decrementar_vaga(id_aula)

        self._pilha.push(f"Vaga liberada: {proximo['nome']} assumiu vaga na aula {id_aula}")

        return {
            "sucesso": True,
            "mensagem": f"Vaga assumida por: {proximo['nome']}",
            "proximo": proximo,
            "fila": fila.exibir()
        }

    def estado_fila_espera(self, id_aula: int) -> dict:
        fila = self._filas_espera.get(id_aula)
        if not fila:
            return {"fila": [], "tamanho": 0}
        return {
            "fila": fila.exibir(),
            "tamanho": fila.tamanho()
        }
    '''
     ─────────────────────────────────────────────
     MÓDULO HISTÓRICO / PILHA
     ─────────────────────────────────────────────
    '''
    def desfazer_ultima_acao(self) -> dict:
        acao = self._pilha.pop()  # O(1)
        if not acao:
            return {"sucesso": False, "mensagem": "Nenhuma ação para desfazer."}
        return {
            "sucesso": True,
            "mensagem": f"Ação desfeita: {acao}",
            "historico": self._pilha.exibir()
        }

    def ver_topo_historico(self) -> dict:
        topo = self._pilha.peek()  # O(1)
        if not topo:
            return {"sucesso": False, "mensagem": "Histórico vazio."}
        return {"sucesso": True, "topo": topo}

    def estado_historico(self) -> dict:
        return {
            "historico": self._pilha.exibir(),   # do mais recente ao mais antigo
            "tamanho": self._pilha.tamanho()
        }

    '''
     ─────────────────────────────────────────────
     MÓDULO DASHBOARD / TOTALIZADORES
     ─────────────────────────────────────────────
    '''

    def totalizadores(self) -> dict:
        # dados exibidos no dashboard principal em tempo real
        alunos = self._lista.exibir_todos()
        ativos   = sum(1 for a in alunos if a["status"] == "ativo")
        inativos = sum(1 for a in alunos if a["status"] == "inativo")

        return {
            "total_alunos"       : self._lista.tamanho(),
            "alunos_ativos"      : ativos,
            "alunos_inativos"    : inativos,
            "fila_atendimento"   : self._fila_atendimento.tamanho(),
            "acoes_historico"    : self._pilha.tamanho()
        }