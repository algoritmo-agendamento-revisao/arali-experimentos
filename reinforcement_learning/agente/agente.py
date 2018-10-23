import numpy as np
from datetime import timedelta
from datetime import datetime

from reinforcement_learning.agente.utilitarioqlearning import UtilitarioQLearning
from modelos.estudo.estudo import Estudo
from modelos_matematicos.formula_repeticao.formula_repeticao import calcular_oi


class Agente:

    def __init__(self, numero_repeticoes):
        # Contrói uma tabela com uma linha a mais por causa da ultima repetição
        self.__qtd_repeticoes__ = numero_repeticoes + 1
        self.__qtd_efs__ = 16  # 1.3 - 2.8
        self.__utilitario_qlearning__ = UtilitarioQLearning()
        self.__tabela_q_learning__ = []

    def obter_tabela_q_learing(self):
        return self.__tabela_q_learning__

    def __inicializar_tabela_qlearning__(self, tabela_q_learning=None):
        if tabela_q_learning is None:
            self.__tabela_q_learning__ = np.zeros([self.__qtd_repeticoes__, self.__qtd_efs__])
        else:
            self.__tabela_q_learning__ = tabela_q_learning

    def tomar_acao(self, recompensa: float, estudo: Estudo):
        if estudo.numero_repeticao is not 1:
            self.__atualizar_politica__(recompensa, estudo)
        estudo.card.ef = self.__calcular_ef_card__(estudo)
        estudo_atualizado = self.__atualizar_info_estudo__(estudo)
        estudo_atualizado.concluido = self.__verificar_estudo_concluido__(estudo_atualizado)
        return estudo_atualizado

    def __atualizar_politica__(self, recompensa: float, estudo: Estudo):
        fator_desconto = 0.1  # y
        taxa_aprendizagem = 0.1  # a - learning rate - O quão rápido converge

        s = self.__utilitario_qlearning__.mapear_numero_repeticao_em_estado(estudo.numero_repeticao)
        a = self.__utilitario_qlearning__.mapear_ef_em_acao(estudo.card.ef)

        q_atual = self.__tabela_q_learning__[s, a]
        q_proxima_acao = self.__tabela_q_learning__[s + 1, :]

        self.__tabela_q_learning__[s, a] = q_atual + taxa_aprendizagem * (
                    recompensa + (fator_desconto * np.max(q_proxima_acao)) - q_atual)


    def __calcular_ef_card__(self, estudo: Estudo):
        if estudo.acerto_ultima_repeticao is False:  # Reseta estudo caso o usuário erre a questão
            return 1.3
        else:
            s = estudo.numero_repeticao - 1  # Recompensa será atribuída a ação passada
            q_atual = self.__tabela_q_learning__[s, :]
            taxa_exploracao = 0.9
            # taxa_exploracao = (1. / (s + 1))

            acao = np.argmax(q_atual + np.random.randn(1, self.__qtd_efs__) * taxa_exploracao)
            return self.__utilitario_qlearning__.mapear_acao_em_ef(acao)


    def __atualizar_info_estudo__(self, estudo: Estudo):
        if estudo.acerto_ultima_repeticao is False:  # Caso o usuário tenha errado a pergunta
            estudo.numero_repeticao = 1
            estudo.data_primeira_repeticao = datetime.utcfromtimestamp(0) #datetime.now()
            estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
            # A próxima repetição será agendada para o próximo dia
            estudo.data_proxima_repeticao = estudo.data_ultima_repeticao + timedelta(days=1)

        else:
            ef = estudo.card.ef  # O ef não é alterado, é apenas utilizado para ser passado de parâmetro
            if estudo.numero_repeticao is 1:
                estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
                diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)
                estudo.data_proxima_repeticao = estudo.data_primeira_repeticao + diferenca_em_dias
            else:
                # Simulando que o tempo passou o tempo e que o card está sendo exibido na data estipulado
                try:
                    estudo.data_ultima_repeticao = estudo.data_proxima_repeticao
                    diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)
                    estudo.data_proxima_repeticao += diferenca_em_dias
                except Exception:
                    print(f"Algo deu errado com o intervalo : {diferenca_em_dias}" + {estudo.data_proxima_repeticao})

            estudo.__qtd_repeticoes__ +=1
            estudo.numero_repeticao += 1

        return estudo

    def __verificar_estudo_concluido__(self, estudo: Estudo):
        finalizou_por_repeticao = estudo.numero_repeticao >= 36
        finalizou_por_intervalo = (estudo.data_proxima_repeticao - estudo.data_ultima_repeticao).days >= 1100
        return finalizou_por_repeticao or finalizou_por_intervalo

    def __calcular_intervalo_em_dias__(self, ef: float, repeticao: int):
        if repeticao is 1:
            return calcular_oi(ef, repeticao)
        else:
            return calcular_oi(ef, repeticao) - calcular_oi(ef, repeticao - 1)
