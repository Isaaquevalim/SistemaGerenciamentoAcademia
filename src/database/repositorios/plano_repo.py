'''
src/database/repositorios/plano_repo.py
responsabilidade: operações de leitura dos planos no banco SQLite.
planos são dados fixos —> não há cadastro ou remoção de planos pelo sistema.
'''

from database.conexao import get_conexao # conexao com o banco de dados


class PlanoRepo:

    '''
    buscar todos —> retorna lista de todos os planos disponíveis
    usado para popular o dropdown de planos no formulário de cadastro
    '''
    def buscar_todos(self) -> list:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planos ORDER BY preco")  # ordena do mais barato ao mais caro
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    '''
    buscar por id —> retorna um plano específico pelo id
    usado para exibir o nome do plano junto aos dados do aluno
    '''
    def buscar_por_id(self, id_plano: int) -> dict | None:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planos WHERE id = ?", (id_plano,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    '''
    buscar por nome —> retorna plano pelo nome exato
    usado para validar se o plano escolhido pelo recepcionista existe
    '''
    def buscar_por_nome(self, nome: str) -> dict | None:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planos WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None