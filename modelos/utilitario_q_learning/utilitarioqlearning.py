from tabulate import tabulate
import numpy as np

class UtilitarioQLearning:

    __qlearning_salvo__ = None

    def __init__(self):
        pass

    def mapear_numero_repeticao_em_estado(self, repeticao: int):
        # tirado 2, pois tratamos de atualizar a tabela para ação de determinar o ef passado e - 1 do indice do array
        # EX: repetição 2 - Recompensa do EF 1, tira-se 1 por causa do índice do array, então ficaria linha 0 na tabela
        return repeticao - 2

    def mapear_estado_em_numero_de_repeticao(self):
        pass

    def mapear_ef_em_acao(self, ef):
        # Mapeia ef de 1.3 a 2.8 em 0 até 15 #TODO:verificar se vai até 15 mesmo
        return int((ef - 1.3) * 10)

    def mapear_acao_em_ef(self, acao):
        #Mapeia acao de 0 a 15 em ef de 1.3 a 2.8
        return acao * 0.1 + 1.3

    def imprimir_tabela_formatada(self, tabela):
        coluna_indice = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9]])
        nova_tabela = np.append(coluna_indice, tabela[:,1:], axis=1)
        headers = ['1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9',
                   '2.0', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7']
        return nova_tabela
        #print(tabulate(nova_tabela, headers=headers, tablefmt='orgtbl'))

    def salvar_tabela(self, tabela):
        self.__qlearning_salvo__ = tabela

    def retornar_tabela_salva(self):
        return self.__qlearning_salvo__
