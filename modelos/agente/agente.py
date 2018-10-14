import numpy as np
import pandas as pd
from datetime import timedelta
from datetime import datetime

from modelos.utilitario_q_learning.utilitarioqlearning import UtilitarioQLearning
from modelos.cards.card import Card
from modelos.cards.utilitariocard import UtilitarioCard
from modelos.estudo.estudo import Estudo
from modelos.estudo.utilitarioestudo import UtilitarioEstudo


class Agente:

    def __init__(self, numero_repeticoes):
        # Contrói uma tabela com uma linha a mais por causa da ultima repetição
        self.__qtd_repeticoes__ = numero_repeticoes + 1
        self.__qtd_efs__ = 16
        self.__utilitario_qlearning__ = UtilitarioQLearning()
        self.__gerenciador_card__: UtilitarioCard = UtilitarioCard()
        self.__gerenciador_estudo__: UtilitarioEstudo = UtilitarioEstudo()
        self.__tabela_q_learning_ = []

    def obter_tabela_q_learing(self):
        return self.__tabela_q_learning_

    def __calcular_oi__(self, ef, repeticao):
        if repeticao is 1:
            return timedelta(days=5)

        part1 = self.__calcular_oi__(ef, repeticao - 1)
        part2 = ef - 0.1 + np.power(np.e, (-2.3 * repeticao + 5))
        oi = part1 * part2
        return timedelta(days=oi.days)

    def __inicializar_tabela_qlearning__(self, tabela_q_learning=None):
        if tabela_q_learning is None:
            self.__tabela_q_learning_ = np.zeros([self.__qtd_repeticoes__, self.__qtd_efs__])
            #self.q_table[self.__qtd_possiveis_estados__ - 1, :] = 1 - Última Linha do q learning - Reccompensa 1
        else:
            self.__tabela_q_learning_ = tabela_q_learning

    # Atualiza tabela/s do Q-learning
    def atualizar_politica(self, recompensa, estudo: Estudo):
        fator_desconto = 0.1  # y
        taxa_aprendizagem = 0.8  # a - learning rate
        s = self.__utilitario_qlearning__.mapear_numero_repeticao_em_estado(estudo.numero_repeticao)
        card_ef = self.__gerenciador_card__.buscar_card(estudo.card_id).ef
        a = self.__utilitario_qlearning__.mapear_ef_em_acao(card_ef)
        
        q_atual = self.__tabela_q_learning_[s, a]
        q_proxima_acao = self.__tabela_q_learning_[s + 1, :]

        self.__tabela_q_learning_[s,a] += taxa_aprendizagem * (recompensa + fator_desconto * np.max(q_proxima_acao) - q_atual)


    def atualizar_estudo(self, estudo: Estudo, questao_respondida_corretamente=False):
        if questao_respondida_corretamente:
            self.__atualizar_ef_card__(estudo)
            estudo = self.__calcular_proxima_repeticao__(estudo)
        else:
            self.__atualizar_ef_card__(estudo, resetar_ef_card=True)
            estudo = self.__calcular_proxima_repeticao__(estudo, resetar_estudo=True)

        self.__gerenciador_estudo__.atualizar_estudo(estudo)


    def atualizar_estudo_primeira_repeticao(self, estudo: Estudo, questao_respondida_corretamente=False):
        if questao_respondida_corretamente:
            self.__atualizar_ef_card__(estudo)
            estudo = self.__calcular_proxima_repeticao__(estudo)
        else:
            self.__atualizar_ef_card__(estudo, resetar_ef_card=True)
            estudo = self.__calcular_proxima_repeticao__(estudo, resetar_estudo=True)

        self.__gerenciador_estudo__.atualizar_estudo(estudo)


    # Ação do agente
    def __atualizar_ef_card__(self, estudo:Estudo, resetar_ef_card=False):
        card = self.__gerenciador_card__.buscar_card(estudo.card_id)

        if resetar_ef_card is True:  # Reseta estudo caso o usuário erre a questão
            card.ef = 1.3
        else:
            s = estudo.numero_repeticao - 1  # Recompensa será atribuída a ação passada
            q_atual = self.__tabela_q_learning_[s, :]
            taxa_exploration_explotation = (1. / (s + 1))

            acao = np.argmax(q_atual + np.random.randn(1, self.__qtd_efs__) * taxa_exploration_explotation)
            card.ef = self.__utilitario_qlearning__.mapear_acao_em_ef(acao)

        self.__gerenciador_card__.atualizar_card(card)

    def __calcular_proxima_repeticao__(self, estudo: Estudo, resetar_estudo=False):
        card_corrente: Card = self.__gerenciador_card__.buscar_card(estudo.card_id)
        ef = card_corrente.ef

        # TODO: Arranjar aqui o esquema de resetar e manter a data da primeira repetição!
        # TODO: Olhar o teamworks
        if resetar_estudo is True:  # Caso o usuário erre a resposta
            estudo.numero_repeticao = 1
            estudo.data_primeira_repeticao = datetime.now()  # Será o tempo de agora pois ele será agendado para daqui a 5 dias depois de errar
            estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
            diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao, primeira_repeticao=True)
            estudo.data_proxima_repeticao = estudo.data_ultima_repeticao + diferenca_em_dias

        else:
            if estudo.numero_repeticao is 1:
                estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
                diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao, primeira_repeticao=True)
                estudo.data_proxima_repeticao = estudo.data_primeira_repeticao + diferenca_em_dias
            else:
                # Simulando que o tempo passou o tempo e que o card está sendo exibido na data estipulado
                estudo.data_ultima_repeticao = estudo.data_proxima_repeticao  # datetime.now()
                diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)
                estudo.data_proxima_repeticao += diferenca_em_dias

            estudo.numero_repeticao += 1

        return estudo

    def __calcular_intervalo_em_dias__(self, ef: float, repeticao: int, primeira_repeticao=False):
        if primeira_repeticao is True:
            return self.__calcular_oi__(ef, repeticao)
        else:
            return (self.__calcular_oi__(ef, repeticao) - self.__calcular_oi__(ef, repeticao - 1))
