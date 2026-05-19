'''
src/database/repositorios/aula_repo.py
responsabilidade: CRUD de aulas no banco SQLite.
'''

from database.conexao import get_conexao # abre conexao com o banco de dados


class AulaRepo:

    # buscar todas — retorna lista de aulas para exibir na tela
    def buscar_todas(self) -> list:
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aulas ORDER BY horario") # retorna a tabela aulas ordenada por horario
        rows = cursor.fetchall() # fetchall retorna todas as linhas como lista de sqlite3.row
        conn.close()
        return [dict(row) for row in rows] # converte cada sqlite3.row para dict puro e retorna a lista de dicionarios

    '''
     decrementar vaga — chamado quando aluno confirma presenca na aula
     retorna False se não há vagas disponíveis (regra de negócio)
     '''
    def decrementar_vaga(self, id_aula: int) -> bool:
        conn = get_conexao()
        cursor = conn.cursor()

        # primeiro verifica se ainda há vaga
        cursor.execute("SELECT vagas_disponiveis FROM aulas WHERE id = ?", (id_aula,)) # busca a quantidade de vagas disponiveis para a aula
        row = cursor.fetchone() #retorna apenas 1 linha (ou None se id_aula nao existe)

        if not row or row["vagas_disponiveis"] <= 0:
            conn.close()
            return False  # sem vagas —> aluno vai para fila de espera

        cursor.execute("""
            UPDATE aulas SET vagas_disponiveis = vagas_disponiveis - 1
            WHERE id = ?
        """, (id_aula,)) # decrementa 1 vaga disponivel para a aula
        conn.commit() # salva a alteração no banco
        conn.close()
        return True  # vaga garantida com sucesso
    
    '''
    incrementar vaga —> chamado quando aluno desiste da aula
    ao liberar vaga, o service vai chamar o primeiro da fila de espera
    '''
    def incrementar_vaga(self, id_aula: int):
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE aulas SET vagas_disponiveis = vagas_disponiveis + 1
            WHERE id = ?
        """, (id_aula,))
        conn.commit()
        conn.close()