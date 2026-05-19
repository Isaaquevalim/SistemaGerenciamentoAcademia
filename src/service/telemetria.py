'''
src/service/telemetria.py
responsabilidade: medir o tempo real de execução das operações.
usado pelo dashboard de performance para evidenciar o Big O na prática.
'''

import time  # biblioteca nativa —> não precisa instalar


class Telemetria:

    def __init__(self):
        # dicionario que acumula os registros de tempo por operação
        # chave = nome da operação, valor = lista de tempos em ms
        self._registros: dict[str, list[float]] = {}

    def medir(self, nome_operacao: str, funcao, *args):
        # executa a função e mede o tempo em milissegundos
        # *args repassa qualquer argumento para a função medida
        inicio = time.perf_counter()    # contador de alta precisão
        resultado = funcao(*args)       # executa a operação real
        fim = time.perf_counter()

        tempo_ms = (fim - inicio) * 1000  # converte para milissegundos

        # acumula o tempo no historico da operação
        if nome_operacao not in self._registros:
            self._registros[nome_operacao] = []
        self._registros[nome_operacao].append(round(tempo_ms, 4))

        return resultado, tempo_ms  # retorna o resultado E o tempo medido

    def media(self, nome_operacao: str) -> float:
        # calcula o tempo médio de uma operação especifica
        tempos = self._registros.get(nome_operacao, [])
        if not tempos:
            return 0.0
        return round(sum(tempos) / len(tempos), 4)

    def ultimo_tempo(self, nome_operacao: str) -> float:
        # retorna o tempo da execucao mais recente
        tempos = self._registros.get(nome_operacao, [])
        if not tempos:
            return 0.0
        return tempos[-1]

    def relatorio(self) -> dict:
        # retorna todos os dados para o dashboard de performance
        return {
            operacao: {
                "ultimo_ms" : self.ultimo_tempo(operacao),
                "media_ms"  : self.media(operacao),
                "execucoes" : len(tempos)
            }
            for operacao, tempos in self._registros.items()
        }

    def limpar(self):
        # reseta todos os registros — útil para testes
        self._registros = {}