# 🏋️‍♂️ Sistema de Gerenciamento de Academia

Um sistema de gerenciamento desenvolvido em **Python** para otimizar o controle de alunos, professores e planos em uma academia em crescimento. 

Este projeto foi desenvolvido como requisito para a disciplina de **Estruturas de Dados 1** (3º semestre de Ciência da Computação) e foca na aplicação prática de estruturas de dados lineares e algoritmos de ordenação e busca para garantir alta performance.

# Colaboradores do Projeto

Isaque Rodrigues Valim | Ryan Catão de Paula | Yago Heideky Tadaguma
---

## 🚀 O Problema Resolvido
Academias lidam com um volume crescente de dados. Com o aumento do número de alunos, buscas manuais ou em listas desordenadas geram lentidão no atendimento na recepção e perda de eficiência. Este sistema resolve esse gargalo implementando algoritmos eficientes que reduzem drasticamente o tempo de busca e ordenação dos cadastros.

## 🛠️ Tecnologias e Estruturas de Dados
* **Linguagem:** Python
* **Estrutura Principal:** Listas dinâmicas contendo dicionários (para representar os registros de alunos, planos e professores).
* **Algoritmos de Ordenação:** * **Quick Sort:** Utilizado como motor principal de ordenação devido à sua eficiência $O(n \log n)$, ideal para grandes volumes de dados.
    * **Bubble/Insertion Sort:** Implementados para cenários de validação ou pequenas inserções.
* **Algoritmos de Busca:**
    * **Busca Binária:** Aplicada após a ordenação para localizar cadastros em tempo logarítmico $O(\log n)$.
    * **Busca Sequencial:** Para pesquisas em bases não ordenadas com custo $O(n)$.

## ⚙️ Funcionalidades
- [x] Cadastrar novos alunos (Nome, CPF, Plano, Status)
- [x] Buscar alunos por CPF ou Nome (Busca Binária e Sequencial)
- [x] Remover registros de alunos
- [x] Listar todos os alunos matriculados
- [x] Ordenar a base de dados em ordem alfabética (Quick Sort)

## 💻 Como Executar o Projeto

1. Clone este repositório para a sua máquina:
   ```bash
   git clone [https://github.com/seu-usuario/gerenciamento-academia.git](https://github.com/seu-usuario/gerenciamento-academia.git)
