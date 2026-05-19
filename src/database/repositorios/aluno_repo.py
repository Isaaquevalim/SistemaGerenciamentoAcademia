'''
src/database/repositorios/aluno_repo.py
responsabilidade: realizar o CRUD de alunos no banco de dados
essa classe so fala SQL
'''

# imporrta a funcao para obter conexao com o banco de dados
from database.conexao import get_conexao


class AlunoRepo:

    '''
    inserir -> grava um novo aluno no banco de dados
    retorna o id gerado automaticamente pelo banco
    '''

    def inserir(self, nome: str, cpf: str, telefone: str,
                email: str, plano_id: int) -> int:
        conn = get_conexao()
        cursor = conn.cursor()  # cursor e o executor de comandos SQL

        '''
         ? sao placeholders -> o SQL e quem substitui pelos valores em ordem
         NUNCA MONTAR SQL com f-string: risco de SQL injection
        '''
        cursor.execute("""
            INSERT INTO alunos (nome, cpf, telefone, email, plano_id)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cpf, telefone, email, plano_id))  # envia esse SQL para o SQLite

        conn.commit()  # salva no arquivo .db
        novo_id = cursor.lastrowid  # id gerado pelo AUTOINCREMENT
        conn.close()  # fecha a conexao para liberar recursos
        return novo_id  # retorna o id do aluno inserido

    # buscar por id -> retorta o aluno com o id especificado ou None se nao encontrado

    def buscar_por_id(self, id_aluno: int) -> dict | None:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_aluno,))
        row = cursor.fetchone()  # fetchone retorna apenas 1 linha (ou None)
        conn.close()
        # converte sqlite3.row para dict puro
        return dict(row) if row else None

    '''
    buscar todos -> retorna a lista de todos os alunos
    usada para carregar a ListaAlunos em memoria ao iniciar o sistema
    '''

    def buscar_todos(self) -> list:
        conn = get_conexao()
        cursor = conn.cursor()
        # ordena por nome para facilitar exibicao
        cursor.execute("SELECT * FROM alunos ORDER BY nome")
        rows = cursor.fetchall()  # fetchall retorna todas as linhas como lista de sqlite3.row
        conn.close()
        # converte cada sqlite3.row para dict puro e retorna a lista de dicionarios
        return [dict(row) for row in rows]

    # atualizar -> edita os dados de um aluno ja existente
    def atualizar(self, id_aluno: int, nome: str, telefone: str,
                  email: str, status: str, plano_id: int) -> bool:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alunos
            SET nome=?, telefone=?, email=?, status=?, plano_id=?
            WHERE id=?
        """, (nome, telefone, email, status, plano_id, id_aluno))
        conn.commit()
        # rowcount retorna quantas linhas foram afetadas pelo UPDATE
        afetados = cursor.rowcount
        conn.close()
        return afetados > 0  # True se pelo menos 1 linha foi atualizada, False se id nao existe

    # remover -> deleta um aluno do banco de dados pelo id, retorna True se removido ou False se id nao existe
    def remover(self, id_aluno: int) -> bool:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
        conn.commit()
        afetados = cursor.rowcount
        conn.close()
        return afetados > 0

    '''
    buscar planos -> retorna a lista de todos os planos disponiveis
    usada para exibir as opcoes de plano no cadastro/edicao de aluno
    '''
    def buscar_planos(self) -> list:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planos")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
