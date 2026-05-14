'''
src/database/conexao.py
responsabilidade: abrir/fechar conexao com o banco de dados
'''

import sqlite3 # biblioteca nativa do python para trabalhar com bancos de dados sqlite
import os # para montar caminhos de arquivos de forma segura

'''
Monta o caminho absoluto para o banco de dados e o arquivo SQL, garantindo que funcione em qualquer ambiente
__file__ e o caminho de 'conexao.py'
Sobe 3 niveis para chegar na raiz do projeto, depois entra em data e pega o academia.db (database > src > data > academia.db)
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #vira a raiz do projeto, junta os pedacos do caminho (os.path ...)
DB_path = os.path.join(BASE_DIR, "data", "academia.db")
SQL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

def get_conexao() -> sqlite3.Connection: # abra o banco academia.db se nao existir o cria
    '''
    Abre ou cria o arquivo academia.db e retorna a conexao com o banco de dadoss
    check_same_thread=False: necessario para uso com o Tkinter (que roda em thread diferente do principal)
    '''
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    '''
    row_factory faz cada linha retornar como dicionario {coluna: valor}
    sem isso o SQLite retorna tuplas ex: (1, Ana, ativo)
    com isso: (id: 1, nome: Ana, status: ativo)
    '''
    conn.row_factory = sqlite3.Row

    return conn

def inicializar_banco():
    '''
    le o schema.sql e executa todos os CREATE TABLE e INSERT iniciais
    ele e chamado uma vez quando o sistema inicia, garantindo que o banco esteja pronto para uso
    '''
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) # cria a pasta data se nao existir, evitando erro de pasta inexistente

    with open(SQL_PATH, "r", enconding="utf-8") as f: # abre o arquivo schema.sql para leitura, garantindo que seja lido como texto e nao binario
        sql = f.read() # le todo o arquivo SQL

    conn = get.conexao()
    conn.executescript(sql) # executa todo o script SQL, criando as tabelas e inserindo os dados iniciais
    conn.commit() # salva as mudancas no banco de dados
    conn.close() # fecha a conexao
