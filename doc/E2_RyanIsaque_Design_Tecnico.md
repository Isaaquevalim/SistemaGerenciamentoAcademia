# Design Técnico e MVP — E2
**Estrutura de Dados**
**Prazo:** 14/05 | **Peso na nota:** 25% da nota final

---

## Identificação do Grupo

| Campo | Preenchimento |
|-------|---------------|
| Nome do projeto | Sistema de Gerenciamento de Academia |
| Repositório GitHub | https://github.com/Isaaquevalim/SistemaGerenciamentoAcademia |
| Integrante 1 | Ryan Catão de Paula — RA 42651786 |
| Integrante 2 | Isaque Rodrigues Valim — RA 43992960 |

---

## 1. Escolha e Justificativa das Estruturas de Dados

---

### Estrutura 1 — Lista Sequencial

**Nome completo e categoria:**
Lista Sequencial Linear — estrutura de dados linear que armazena elementos em posições contíguas, acessíveis por índice.

**Complexidade das operações principais:**

| Operação | Tempo | Espaço | Observação |
|----------|-------|--------|------------|
| Inserção (final) | O(1) | O(1) | Append direto ao final — Python conhece a posição sem percorrer |
| Remoção (por ID) | O(n) | O(1) | Percorre até encontrar o ID, depois reorganiza índices internos |
| Busca sequencial | O(n) | O(1) | Percorre todos os elementos no pior caso (lista desordenada) |
| Busca binária | O(log n) | O(1) | Divide o conjunto ao meio a cada passo (exige lista ordenada) |
| Acesso por índice | O(1) | O(1) | Acesso direto via posição sem necessidade de percurso |

**Justificativa de escolha:**
No domínio de uma academia, a Lista é a estrutura ideal para catalogar os cadastros permanentes de alunos. Ela permite percorrer sequencialmente todos os registros durante auditorias de planos ativos e inativos, possibilita o acesso direto a um aluno por índice e suporta tanto a busca sequencial (quando desordenada) quanto a busca binária (após ordenação por Merge Sort). Essa dualidade de buscas com complexidades diferentes — O(n) vs O(log n) — é o principal argumento técnico para o uso desta estrutura, pois torna observável na prática o impacto da ordenação prévia no desempenho das consultas.

**Alternativa descartada:**
Dicionário Python (`dict`) — descartado porque, apesar de oferecer busca em O(1) amortizado por chave, não permite aplicar algoritmos de ordenação manual (Bubble Sort, Merge Sort) sobre os dados, que é exigência explícita da disciplina. Além disso, não evidencia a diferença entre busca sequencial e binária, tornando o objetivo pedagógico do projeto impossível de ser demonstrado.

**Limitações conhecidas:**
A remoção de elementos no meio da lista tem custo O(n) devido à reorganização dos índices internos. Com volumes muito grandes de cadastros (acima de 100 mil alunos), a busca sequencial se tornaria um gargalo severo de desempenho, sendo necessária a migração para uma árvore de busca binária ou índice hash complementar.

**Referência bibliográfica:**
CORMEN, Thomas H. et al. **Algoritmos: teoria e prática**. 3. ed. Rio de Janeiro: Elsevier, 2012. Cap. 10, p. 238–256.

---

### Estrutura 2 — Fila (FIFO)

**Nome completo e categoria:**
Fila Linear FIFO (First In, First Out) — estrutura de dados linear restrita em que o primeiro elemento inserido é o primeiro a ser removido.

**Complexidade das operações principais:**

| Operação | Tempo | Espaço | Observação |
|----------|-------|--------|------------|
| Enqueue (inserção) | O(1) | O(1) | Inserção sempre no final da fila |
| Dequeue (remoção) | O(n) | O(1) | Remoção no início com reorganização dos índices (implementação manual) |
| Peek (frente) | O(1) | O(1) | Acesso direto ao índice 0 sem remoção |
| Acesso | O(n) | O(1) | Acesso a elemento específico exige percurso |

**Justificativa de escolha:**
O atendimento em uma academia respeita naturalmente a ordem de chegada — o primeiro aluno a chegar deve ser o primeiro atendido. A Fila FIFO modela exatamente esse comportamento. O sistema utiliza duas filas independentes: uma para o atendimento geral na recepção e filas exclusivas por aula, ativadas quando a lotação máxima é atingida. Quando um aluno desiste de uma aula, o sistema chama automaticamente o primeiro da fila de espera daquela aula, garantindo justiça no processo.

**Alternativa descartada:**
Lista ordenada por horário de chegada — descartada porque exigiria reordenação a cada nova inserção (O(n log n) por Merge Sort), tornando cada enfileiramento mais custoso. A Fila garante O(1) na inserção e preserva a ordem sem custo adicional, sendo a estrutura semanticamente correta para o problema.

**Limitações conhecidas:**
A implementação manual sobre lista Python resulta em Dequeue O(n) em vez de O(1). A solução de produção usaria `collections.deque` para obter O(1), mas a implementação manual foi mantida para tornar o custo computacional observável e pedagogicamente relevante, evidenciando o impacto da escolha de implementação no Big O real.

**Referência bibliográfica:**
GOODRICH, Michael T.; TAMASSIA, Roberto; GOLDWASSER, Michael H. **Estruturas de dados e algoritmos em Python**. Porto Alegre: Bookman, 2013. Cap. 6, p. 230–248.

---

### Estrutura 3 — Pilha (LIFO)

**Nome completo e categoria:**
Pilha Linear LIFO (Last In, First Out) — estrutura de dados linear restrita em que o último elemento inserido é o primeiro a ser removido.

**Complexidade das operações principais:**

| Operação | Tempo | Espaço | Observação |
|----------|-------|--------|------------|
| Push (inserção) | O(1) | O(1) | Inserção sempre no topo (final da lista interna) |
| Pop (remoção) | O(1) | O(1) | Remoção sempre do topo sem necessidade de percurso |
| Peek (topo) | O(1) | O(1) | Acesso direto ao índice -1 sem remoção |
| Acesso | O(n) | O(1) | Acesso a elemento específico exige percurso |

**Justificativa de escolha:**
O histórico de ações do sistema segue naturalmente o comportamento LIFO: a última ação realizada deve ser a primeira a poder ser desfeita. A Pilha modela esse mecanismo com precisão — cada operação de cadastro, edição ou remoção de aluno é empilhada automaticamente, e o recepcionista pode desfazer ações recentes em ordem inversa. A limitação de 10 ações foi definida para evitar consumo excessivo de memória, conforme documentado no RFC do projeto.

**Alternativa descartada:**
Lista com ponteiro manual de topo — descartada pois exigiria controle explícito de um índice `topo` pelo programador, aumentando o risco de erros de implementação (ex.: acesso fora dos limites). A Pilha encapsula essa lógica internamente, tornando o código mais seguro e deixando a semântica LIFO explícita e verificável.

**Limitações conhecidas:**
A pilha armazena apenas as últimas 10 ações da sessão atual — ações anteriores são descartadas automaticamente. O histórico não persiste entre sessões: ao fechar o sistema, a pilha é esvaziada. Para persistência do histórico seria necessário gravar cada ação no banco de dados, funcionalidade marcada como Out-of-Scope nesta entrega.

**Referência bibliográfica:**
CORMEN, Thomas H. et al. **Algoritmos: teoria e prática**. 3. ed. Rio de Janeiro: Elsevier, 2012. Cap. 10, p. 225–232.

---

## 2. Arquitetura em Camadas

**Diagrama:**

```
┌──────────────────────────────────────────────────────────────┐
│                  CAMADA UI  (src/ui/)                        │
│   main.py · tela_alunos.py · tela_fila.py                    │
│   tela_historico.py · tela_performance.py                    │
│                  Interface gráfica Tkinter                   │
└───────────────────────┬──────────────────────────────────────┘
                        │ chama academia_service
┌───────────────────────▼──────────────────────────────────────┐
│               CAMADA SERVICE  (src/service/)                 │
│         academia_service.py · telemetria.py                  │
│      Regras de negócio, validações e orquestração            │
└──────────────┬───────────────────────┬───────────────────────┘
               │ persiste/lê           │ opera em memória
┌──────────────▼────────────┐  ┌───────▼───────────────────────┐
│  CAMADA DATABASE          │  │   CAMADA CORE  (src/core/)    │
│  (src/database/)          │  │                               │
│  conexao.py               │  │  lista.py    fila.py          │
│  aluno_repo.py            │  │  pilha.py    ordenacao.py     │
│  aula_repo.py             │  │                               │
│  schema.sql               │  │  Estruturas de dados puras    │
└──────────────┬────────────┘  └───────────────────────────────┘
               │
        ┌──────▼──────┐
        │ data/        │
        │ academia.db  │
        │  (SQLite)    │
        └─────────────┘
```

**Descrição das camadas:**

| Camada | Nome no projeto | Responsabilidade |
|--------|-----------------|-----------------|
| Apresentação (UI) | `src/ui/` | Interface gráfica Tkinter — janelas, botões, formulários, exibição de resultados e mensagens de erro ao usuário |
| Aplicação (Service) | `src/service/` | Orquestração das operações, validação das regras de negócio (CPF único, vaga disponível, plano válido) e medição de telemetria |
| Persistência (Database) | `src/database/` | Comunicação com o banco SQLite — leitura e escrita persistente de alunos e aulas entre sessões |
| Domínio (Core) | `src/core/` | Implementação pura das estruturas de dados (Lista, Fila, Pilha) e algoritmos de ordenação (Bubble Sort, Merge Sort) |

**Como as camadas se comunicam:**
A UI captura a ação do usuário (ex.: clique em "Cadastrar") e chama o método correspondente no `academia_service`. O Service valida as regras de negócio — verifica CPF duplicado, e-mail único, plano válido — e, se aprovado, chama o `aluno_repo` para gravar no banco SQLite (Database). Em seguida, o Service chama `lista.inserir()` para carregar o aluno em memória (Core) e `pilha.push()` para registrar a ação no histórico (Core). O Service retorna o resultado ao UI, que atualiza a tabela de alunos na tela em tempo real.

---

## 3. Estrutura de Diretórios

```
academia-gym/
│
├── src/
│   ├── core/                        # Estruturas de dados puras
│   │   ├── lista.py                 # Lista sequencial — busca sequencial e binária
│   │   ├── fila.py                  # Fila FIFO — atendimento e espera por aula
│   │   ├── pilha.py                 # Pilha LIFO — histórico e desfazer
│   │   └── ordenacao.py             # Bubble Sort O(n²) e Merge Sort O(n log n)
│   │
│   ├── database/                    # Camada de persistência SQLite
│   │   ├── conexao.py               # Abre conexão e inicializa o banco
│   │   ├── schema.sql               # Script de criação das tabelas
│   │   └── repositorios/
│   │       ├── __init__.py
│   │       ├── aluno_repo.py        # CRUD de alunos
│   │       └── aula_repo.py         # CRUD de aulas e controle de vagas
│   │
│   ├── service/                     # Regras de negócio e orquestração
│   │   ├── academia_service.py      # Conecta banco + estruturas de dados
│   │   └── telemetria.py            # Medição de tempos reais de execução
│   │
│   └── ui/                          # Interface gráfica Tkinter
│       ├── main.py                  # Janela principal e dashboard
│       └── telas/
│           ├── __init__.py
│           ├── tela_alunos.py       # Lista, cadastro, busca e ordenação
│           ├── tela_fila.py         # Fila de atendimento e fila de espera
│           ├── tela_historico.py    # Pilha LIFO e função desfazer
│           └── tela_performance.py  # Dashboard de Big O com métricas reais
│
├── data/
│   └── academia.db                  # Banco SQLite (gerado automaticamente)
│
├── tests/
│   ├── test_lista.py
│   ├── test_fila.py
│   └── test_pilha.py
│
├── doc/
│   └── E2_RyanIsaque_Design_Tecnico.md
│
├── .gitignore
└── README.md
```

**Justificativa de desvios:**
Foi adicionada a camada `src/database/` (não presente no modelo sugerido) para separar a responsabilidade de persistência das regras de negócio. Isso evita que o `service/` acesse o banco diretamente, tornando o código mais organizado e testável. A camada `database/` segue o padrão Repository — cada entidade do banco tem seu próprio arquivo de repositório, isolando os comandos SQL do restante do sistema.

---

## 4. Backlog do Projeto

### In-Scope — O que será implementado

---

**Item 1:** Cadastro de aluno com validação

Critério de aceite:
> **Dado** um formulário preenchido com nome, CPF, e-mail e plano válidos,
> **quando** o recepcionista confirmar o cadastro,
> **então** o sistema insere o aluno na lista em memória em O(1), grava no banco SQLite e registra a ação na pilha de histórico, exibindo o novo estado da lista na tela.

---

**Item 2:** Busca de aluno por nome (sequencial e binária)

Critério de aceite:
> **Dado** uma lista de alunos cadastrados,
> **quando** o recepcionista informar um nome e escolher o modo de busca (sequencial ou binária),
> **então** o sistema executa a busca em O(n) ou O(log n) respectivamente, exibe o aluno encontrado com seus dados ou mensagem de erro caso não exista, e registra o tempo de execução real no dashboard de performance.

---

**Item 3:** Ordenação da lista por nome (Bubble Sort e Merge Sort)

Critério de aceite:
> **Dado** uma lista com múltiplos alunos cadastrados,
> **quando** o recepcionista acionar a ordenação e escolher o algoritmo (Bubble Sort ou Merge Sort),
> **então** o sistema ordena a lista alfabeticamente, exibe o resultado na tela e mostra o tempo de execução de cada algoritmo separadamente, evidenciando a diferença entre O(n²) e O(n log n).

---

**Item 4:** Fila de atendimento na recepção (FIFO)

Critério de aceite:
> **Dado** que há alunos na fila de atendimento,
> **quando** o recepcionista acionar "Chamar próximo",
> **então** o sistema executa Dequeue no primeiro da fila, exibe o nome do aluno chamado na tela, atualiza o estado atual da fila em tempo real e exibe mensagem de erro caso a fila esteja vazia.

---

**Item 5:** Fila de espera por aula com vaga liberada

Critério de aceite:
> **Dado** uma aula com todas as vagas preenchidas e alunos na fila de espera,
> **quando** um aluno desistir da aula,
> **então** o sistema incrementa a vaga disponível no banco, executa Dequeue na fila de espera da aula em questão e exibe na tela o nome do próximo aluno que assumiu a vaga automaticamente.

---

**Item 6:** Histórico de ações com função desfazer (LIFO)

Critério de aceite:
> **Dado** que o recepcionista realizou ao menos uma ação (cadastro, edição ou remoção),
> **quando** acionar o botão "Desfazer",
> **então** o sistema executa Pop na pilha em O(1), reverte a última ação realizada, exibe o novo topo da pilha e mostra mensagem de erro caso a pilha esteja vazia, respeitando o limite de 10 ações armazenadas.

---

**Item 7:** Dashboard de performance com telemetria real

Critério de aceite:
> **Dado** que operações foram executadas durante a sessão,
> **quando** o recepcionista acessar o dashboard de performance,
> **então** o sistema exibe os tempos reais medidos de busca sequencial vs binária, tamanho atual da fila, número de ações na pilha e comparativo entre Bubble Sort e Merge Sort, confirmando na prática as complexidades teóricas declaradas no RFC.

---

**Item 8:** Remoção de aluno com registro no histórico

Critério de aceite:
> **Dado** um aluno cadastrado no sistema,
> **quando** o recepcionista confirmar a remoção,
> **então** o sistema remove o aluno da lista em memória em O(n), deleta do banco SQLite, empilha a ação no histórico e exibe o estado atualizado da lista na tela.

---

### Out-of-Scope — O que não será implementado

| Funcionalidade | Motivo de exclusão |
|----------------|--------------------|
| Controle financeiro e emissão de boletos | Exige integração com sistemas de pagamento externos, aumentando complexidade sem agregar à demonstração das estruturas de dados. Fora do escopo da disciplina. |
| Gerenciamento de professores e grades horárias | Funcionalidade de negócio que não demonstra nenhuma estrutura de dados adicional além das já implementadas. |
| Persistência do histórico de ações entre sessões | A pilha é volátil por natureza neste projeto. Gravar cada ação no banco exigiria modelo de dados adicional e desviaria o foco da demonstração do comportamento LIFO em memória. |
| Autenticação de usuários (login/senha) | Aumenta a complexidade da interface sem contribuir para a demonstração das estruturas de dados. Fora do escopo da disciplina. |
| Relatórios e exportação de dados (PDF, Excel) | Depende de bibliotecas externas e lógica de formatação sem relação com o conteúdo de Estruturas de Dados I. |

---

## 5. Repositório GitHub

**Link do repositório:** https://github.com/Isaaquevalim/SistemaGerenciamentoAcademia

**Checklist do repositório:**

- [x] Repositório público com nome descritivo
- [x] `.gitignore` configurado para Python
- [x] `README.md` com nome, descrição e instruções de execução
- [x] Mínimo de 5 commits com prefixos semânticos (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`)

**O que não sobe no repositório (`.gitignore`):**
```
__pycache__/
*.pyc
*.pyo
data/academia.db
.env
.env.local
venv/
.DS_Store
Thumbs.db
*.log
```

**Como executar o projeto:**
```bash
# 1. Clone o repositório
git clone https://github.com/Isaaquevalim/SistemaGerenciamentoAcademia

# 2. Acesse a pasta
cd SistemaGerenciamentoAcademia

# 3. Nenhuma instalação adicional necessária
#    Tkinter e sqlite3 já estão incluídos no Python padrão

# 4. Execute o sistema
python src/ui/main.py
```

---

## 6. Implementação do Núcleo

### 6.1 Estrutura implementada: Lista Sequencial

**Linguagem:** Python 3.11

**Localização no repositório:** `src/core/lista.py`

**Operações implementadas:**

| Operação | Implementada? | Observação |
|----------|---------------|------------|
| `inserir` | ✅ | Inserção no final — O(1) |
| `remover` | ✅ | Busca por ID + remoção — O(n) |
| `buscar_sequencial` | ✅ | Percurso completo — O(n) |
| `buscar_binaria` | ✅ | Divisão ao meio — O(log n), exige lista ordenada |
| `exibir_todos` | ✅ | Retorna cópia da lista — O(n) |
| `tamanho` | ✅ | Retorno direto — O(1) |

**Trecho representativo do código** (busca binária — operação que evidencia o Big O):

```python
def buscar_binaria(self, nome: str) -> dict | None:
    # PRÉ-CONDIÇÃO: lista deve estar ordenada por nome
    esquerda, direita = 0, len(self._dados) - 1
    nome_lower = nome.lower()

    while esquerda <= direita:
        meio = (esquerda + direita) // 2          # índice do elemento central
        nome_meio = self._dados[meio]["nome"].lower()

        if nome_meio == nome_lower:
            return self._dados[meio]              # achou
        elif nome_lower < nome_meio:
            direita = meio - 1                    # descarta metade direita
        else:
            esquerda = meio + 1                   # descarta metade esquerda
    return None                                   # não encontrado
```

**Leitura de arquivo:**
O sistema utiliza banco de dados SQLite (`data/academia.db`) como fonte de dados persistente. Na inicialização, o `academia_service.py` chama `aluno_repo.buscar_todos()`, que executa `SELECT * FROM alunos ORDER BY nome` e retorna uma lista de dicionários. Cada dicionário é então inserido na `ListaAlunos` em memória via `lista.inserir()`, tornando os dados disponíveis para as operações de busca e ordenação.

Exemplo do conteúdo retornado pelo banco (equivalente ao arquivo de entrada):
```json
[
  {"id": 1, "nome": "Ana Souza",   "cpf": "111.111.111-11", "email": "ana@email.com",    "status": "ativo",   "plano_id": 3},
  {"id": 2, "nome": "Bruno Lima",  "cpf": "222.222.222-22", "email": "bruno@email.com",  "status": "ativo",   "plano_id": 1},
  {"id": 3, "nome": "Carlos Melo", "cpf": "333.333.333-33", "email": "carlos@email.com", "status": "inativo", "plano_id": 2}
]
```

---

### 6.2 Estrutura implementada: Fila FIFO

**Linguagem:** Python 3.11

**Localização no repositório:** `src/core/fila.py`

**Operações implementadas:**

| Operação | Implementada? | Observação |
|----------|---------------|------------|
| `enqueue` | ✅ | Inserção no final — O(1) |
| `dequeue` | ✅ | Remoção no início — O(n) implementação manual |
| `peek` | ✅ | Acesso ao índice 0 sem remoção — O(1) |
| `esta_vazia` | ✅ | Verificação de tamanho — O(1) |
| `tamanho` | ✅ | Retorno direto — O(1) |
| `exibir` | ✅ | Retorna cópia da fila — O(n) |

**Trecho representativo do código** (dequeue — operação principal da Fila):

```python
def dequeue(self) -> dict | None:
    if self.esta_vazia():
        return None           # fila vazia: retorna None sem lançar exceção
    return self._dados.pop(0) # remove e retorna o primeiro elemento — O(n)
    # pop(0) é O(n) pois todos os elementos seguintes
    # precisam ser deslocados uma posição para a esquerda
```

---

### 6.3 Estrutura implementada: Pilha LIFO

**Linguagem:** Python 3.11

**Localização no repositório:** `src/core/pilha.py`

**Operações implementadas:**

| Operação | Implementada? | Observação |
|----------|---------------|------------|
| `push` | ✅ | Empilha no topo com controle de limite — O(1) |
| `pop` | ✅ | Remove do topo — O(1) |
| `peek` | ✅ | Acesso ao índice -1 sem remoção — O(1) |
| `esta_vazia` | ✅ | Verificação de tamanho — O(1) |
| `tamanho` | ✅ | Retorno direto — O(1) |
| `exibir` | ✅ | Retorna cópia invertida (topo primeiro) — O(n) |

**Trecho representativo do código** (push com controle de limite):

```python
LIMITE = 10  # máximo de ações armazenadas

def push(self, acao: str):
    if len(self._dados) >= LIMITE:
        self._dados.pop(0)    # descarta a ação mais antiga para abrir espaço
    self._dados.append(acao)  # empilha a nova ação no topo — O(1)
```

---

## 7. MVP — Mínimo Produto Viável

### 7.1 Tipo de interface

- [ ] CLI (linha de comando)
- [x] GUI desktop (Tkinter)
- [ ] Web

---

### 7.2 Tela 1 — Boas-vindas / Menu Principal

**Descrição:** Ao iniciar o sistema, o recepcionista vê o dashboard principal com o nome do sistema, totalizadores em tempo real (alunos ativos, tamanho da fila) e botões de acesso a cada módulo.

**Representação textual:**
```
╔══════════════════════════════════════════════════════╗
║        SISTEMA DE GERENCIAMENTO DE ACADEMIA          ║
╠══════════════════════════════════════════════════════╣
║  Alunos ativos: 42        Fila de atendimento: 3     ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   [ 👤 Gerenciar Alunos    ]  [ 🏃 Fila Atendimento ]║
║                                                      ║
║   [ 📋 Histórico / Desfazer]  [ 📊 Performance      ]║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║                        [ Sair ]                      ║
╚══════════════════════════════════════════════════════╝
```

**Comportamentos implementados nesta tela:**
- [x] Nome do sistema exibido
- [x] Lista de operações disponíveis (4 módulos)
- [x] Opção de sair
- [x] Totalizadores atualizados em tempo real

---

### 7.3 Tela 2 — Entrada de Dados (Tela de Alunos)

**Descrição:** O recepcionista cadastra um novo aluno preenchendo o formulário, ou busca um aluno existente pelo nome escolhendo o modo de busca.

**Representação textual:**
```
╔══════════════════════════════════════════════════════╗
║                  GERENCIAR ALUNOS                    ║
╠══════════════════════════════════════════════════════╣
║  CADASTRAR NOVO ALUNO                                ║
║  Nome:     [________________________]                ║
║  CPF:      [________________________]                ║
║  Email:    [________________________]                ║
║  Telefone: [________________________]                ║
║  Plano:    [ Mensal ▼ ]                              ║
║                          [ Confirmar Cadastro ]      ║
╠══════════════════════════════════════════════════════╣
║  BUSCAR ALUNO                                        ║
║  Nome: [____________________]                        ║
║  Modo: ( ) Sequencial O(n)  (•) Binária O(log n)     ║
║                                    [ Buscar ]        ║
╠══════════════════════════════════════════════════════╣
║  ORDENAR LISTA                                       ║
║  [ Bubble Sort O(n²) ]     [ Merge Sort O(n log n) ] ║
╚══════════════════════════════════════════════════════╝
```

**Comportamentos implementados nesta tela:**
- [x] Campo de formulário para inserir dados do aluno
- [x] Dropdown para seleção de plano (carregado do banco)
- [x] Seleção do modo de busca (sequencial ou binária)
- [x] Botões de ordenação com algoritmos distintos
- [x] Confirmação da ação antes de executar

---

### 7.4 Tela 3 — Resultado (Tabela de Alunos e Feedback)

**Descrição:** Após qualquer operação, o estado atual da lista é exibido em tabela e uma mensagem de resultado ou erro aparece ao usuário.

**Representação textual:**
```
╔══════════════════════════════════════════════════════╗
║  ✅ Aluno "Bruno Lima" cadastrado com sucesso!        ║
║  Busca binária: 0.0003ms | Lista ordenada: Sim        ║
╠══════════════════════════════════════════════════════╣
║  ESTADO ATUAL DA LISTA (42 alunos)                   ║
╠══════════════════════════════════════════════════════╣
║  ID  │ Nome          │ Plano       │ Status           ║
║  ────┼───────────────┼─────────────┼──────────        ║
║   1  │ Ana Souza     │ Anual       │ ativo            ║
║   2  │ Bruno Lima    │ Mensal      │ ativo            ║
║   3  │ Carlos Melo   │ Trimestral  │ inativo          ║
║   …  │ …             │ …           │ …                ║
╠══════════════════════════════════════════════════════╣
║  ❌ ERRO: CPF já cadastrado no sistema.               ║
╚══════════════════════════════════════════════════════╝
```

**Comportamentos implementados nesta tela:**
- [x] Resultado da operação executada (mensagem de sucesso ou erro)
- [x] Estado atual completo da estrutura (tabela com todos os alunos)
- [x] Mensagem de erro clara para operações inválidas
- [x] Tempo de execução da operação exibido (telemetria)

---

### 7.5 Fluxo completo demonstrado

**Cenário:** Recepcionista cadastra um aluno, ordena a lista, busca o aluno por nome usando busca binária e desfaz o cadastro.

```
[INÍCIO DO SISTEMA]
→ Banco SQLite carregado: 5 alunos encontrados
→ ListaAlunos populada em memória: 5 elementos
→ Dashboard exibido: Alunos ativos: 5 | Fila: 0

[TELA DE ALUNOS]
→ Recepcionista preenche formulário:
  Nome: Diana Rocha | CPF: 444.444.444-44 | Plano: Anual
→ Clica em "Confirmar Cadastro"
→ Service valida: CPF e e-mail únicos ✅
→ aluno_repo.inserir() → gravado no banco (id=6)
→ lista.inserir() → O(1) | tamanho: 6
→ pilha.push("Cadastro: Diana Rocha") → topo da pilha
→ ✅ "Aluno Diana Rocha cadastrado com sucesso!"
→ Tabela atualizada: 6 alunos exibidos

[ORDENAÇÃO]
→ Recepcionista clica em "Merge Sort O(n log n)"
→ merge_sort() executado → lista ordenada alfabeticamente
→ Tempo: 0.0021ms para 6 elementos
→ Lista reordenada exibida na tabela

[BUSCA BINÁRIA]
→ Recepcionista digita "Diana Rocha" e seleciona "Binária O(log n)"
→ buscar_binaria() executado: 3 comparações (log₂6 ≈ 2.6)
→ Tempo: 0.0004ms
→ ✅ Aluno encontrado: Diana Rocha | Plano: Anual | Status: ativo

[DESFAZER]
→ Recepcionista clica em "Desfazer"
→ pilha.pop() → O(1) | retorna "Cadastro: Diana Rocha"
→ Service reverte: aluno_repo.remover(6) + lista.remover(6)
→ ✅ "Ação desfeita: cadastro de Diana Rocha revertido"
→ Tabela atualizada: 5 alunos

[FIM DO CENÁRIO]
```

---

## 8. Testes Unitários

**Framework de testes utilizado:** pytest

**Localização:** `tests/`

---

### Estrutura testada: Lista Sequencial (`tests/test_lista.py`)

---

**Teste 1 — Caso base**

Descrição: Insere um aluno e verifica que `tamanho()` retorna 1 e `buscar_sequencial()` encontra o elemento pelo nome correto.

```python
def test_inserir_e_buscar_sequencial():
    lista = ListaAlunos()
    aluno = {"id": 1, "nome": "Ana Souza", "status": "ativo"}
    lista.inserir(aluno)

    assert lista.tamanho() == 1
    resultado = lista.buscar_sequencial("Ana Souza")
    assert resultado is not None
    assert resultado["nome"] == "Ana Souza"
```

Resultado: ✅ Passando

---

**Teste 2 — Caso vazio**

Descrição: Chama `buscar_sequencial()` em lista vazia e verifica que retorna `None` sem lançar exceção.

```python
def test_busca_sequencial_lista_vazia():
    lista = ListaAlunos()

    resultado = lista.buscar_sequencial("Carlos")
    assert resultado is None
    assert lista.tamanho() == 0
```

Resultado: ✅ Passando

---

**Teste 3 — Caso com múltiplos elementos**

Descrição: Insere 5 alunos, ordena com `merge_sort` e verifica que `buscar_binaria()` encontra o elemento correto.

```python
def test_busca_binaria_apos_merge_sort():
    from core.ordenacao import merge_sort

    lista = ListaAlunos()
    nomes = ["Carlos", "Ana", "Eduardo", "Bruno", "Diana"]
    for i, nome in enumerate(nomes):
        lista.inserir({"id": i+1, "nome": nome, "status": "ativo"})

    ordenados = merge_sort(lista.exibir_todos())
    lista2 = ListaAlunos()
    for aluno in ordenados:
        lista2.inserir(aluno)

    resultado = lista2.buscar_binaria("Eduardo")
    assert resultado is not None
    assert resultado["nome"] == "Eduardo"
```

Resultado: ✅ Passando

---

### Estrutura testada: Fila FIFO (`tests/test_fila.py`)

---

**Teste 1 — Caso base**

Descrição: Enqueue de um aluno e verifica que `peek()` retorna o mesmo aluno e `tamanho()` retorna 1.

```python
def test_enqueue_e_peek():
    fila = Fila("Recepção")
    aluno = {"id": 1, "nome": "Ana Souza"}
    fila.enqueue(aluno)

    assert fila.tamanho() == 1
    assert fila.peek()["nome"] == "Ana Souza"
```

Resultado: ✅ Passando

---

**Teste 2 — Caso vazio**

Descrição: Chama `dequeue()` em fila vazia e verifica que retorna `None` sem lançar exceção.

```python
def test_dequeue_fila_vazia():
    fila = Fila("Recepção")

    resultado = fila.dequeue()
    assert resultado is None
    assert fila.esta_vazia() is True
```

Resultado: ✅ Passando

---

**Teste 3 — Caso com múltiplos elementos**

Descrição: Enqueue de 3 alunos, Dequeue 2 vezes e verifica que o terceiro aluno é o novo `peek()` (FIFO preservado).

```python
def test_fifo_multiplos_elementos():
    fila = Fila("Recepção")
    fila.enqueue({"id": 1, "nome": "Ana"})
    fila.enqueue({"id": 2, "nome": "Bruno"})
    fila.enqueue({"id": 3, "nome": "Carlos"})

    assert fila.dequeue()["nome"] == "Ana"    # primeiro a entrar, primeiro a sair
    assert fila.dequeue()["nome"] == "Bruno"
    assert fila.peek()["nome"] == "Carlos"    # terceiro agora é o primeiro
    assert fila.tamanho() == 1
```

Resultado: ✅ Passando

---

### Estrutura testada: Pilha LIFO (`tests/test_pilha.py`)

---

**Teste 1 — Caso base**

Descrição: Push de uma ação e verifica que `peek()` retorna a mesma ação e `tamanho()` retorna 1.

```python
def test_push_e_peek():
    pilha = Pilha()
    pilha.push("Cadastro: Ana Souza")

    assert pilha.tamanho() == 1
    assert pilha.peek() == "Cadastro: Ana Souza"
```

Resultado: ✅ Passando

---

**Teste 2 — Caso vazio**

Descrição: Chama `pop()` em pilha vazia e verifica que retorna `None` sem lançar exceção.

```python
def test_pop_pilha_vazia():
    pilha = Pilha()

    resultado = pilha.pop()
    assert resultado is None
    assert pilha.esta_vazia() is True
```

Resultado: ✅ Passando

---

**Teste 3 — Caso com múltiplos elementos (limite de 10)**

Descrição: Push de 12 ações e verifica que a pilha mantém no máximo 10 elementos e que a ação mais recente está no topo.

```python
def test_limite_de_dez_acoes():
    pilha = Pilha()
    for i in range(12):
        pilha.push(f"Acao {i+1}")

    assert pilha.tamanho() == 10                    # limite respeitado
    assert pilha.peek() == "Acao 12"                # ação mais recente no topo
    assert "Acao 1" not in pilha.exibir()           # ação mais antiga descartada
    assert "Acao 2" not in pilha.exibir()           # segunda mais antiga descartada
```

Resultado: ✅ Passando

---

## Checklist de Autoavaliação

**Seção 1 — Estruturas**
- [x] Big-O preenchido para inserção, remoção, busca e acesso de cada estrutura
- [x] Pelo menos 1 alternativa descartada com justificativa técnica
- [x] Limitações conhecidas descritas
- [x] Referência bibliográfica fornecida

**Seção 2 — Arquitetura**
- [x] Diagrama com as 3 camadas visíveis (4 camadas implementadas)
- [x] Fluxo de comunicação entre camadas descrito

**Seção 3 — Diretórios**
- [x] Árvore de diretórios presente
- [x] Desvios do modelo justificados (camada database/ adicionada)

**Seção 4 — Backlog**
- [x] 8 itens In-Scope com critério de aceite no formato Dado/Quando/Então
- [x] 5 itens Out-of-Scope com justificativa

**Seção 5 — Repositório**
- [x] Link do repositório público informado
- [x] README.md com instruções de execução
- [x] Mínimo de 5 commits semânticos

**Seção 6 — Núcleo**
- [x] 3 estruturas completamente implementadas (Lista, Fila, Pilha)
- [x] Leitura de dados via banco SQLite funcionando
- [x] Trecho de código representativo incluído para cada estrutura

**Seção 7 — MVP**
- [x] 3 telas documentadas com representação textual
- [x] Fluxo completo de ponta a ponta demonstrado
- [x] Mensagem de erro para operação inválida implementada
- [x] Loop de menu funcionando (programa não encerra após 1 operação)

**Seção 8 — Testes**
- [x] 3 testes por estrutura documentados (9 testes no total)
- [x] Resultado de cada teste indicado (✅ Passando)

---

## Referências

CORMEN, Thomas H. et al. **Algoritmos: teoria e prática**. 3. ed. Rio de Janeiro: Elsevier, 2012.

GOODRICH, Michael T.; TAMASSIA, Roberto; GOLDWASSER, Michael H. **Estruturas de dados e algoritmos em Python**. Porto Alegre: Bookman, 2013.

PYTHON SOFTWARE FOUNDATION. **Python Documentation**. Disponível em: https://docs.python.org/3/. Acesso em: 14 mai. 2026.

---

*Nome do arquivo de entrega: `E2_RyanIsaque_Design_Tecnico.md`*
*Este arquivo está na pasta `/doc` do repositório.*
