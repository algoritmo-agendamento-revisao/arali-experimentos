import numpy as np
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
        self.__qtd_possiveis_estados__ = numero_repeticoes + 1
        self.__qtd_possiveis_efs__ = 16
        self.__utilitario_qlearning__ = UtilitarioQLearning()
        self.__gerenciador_card__: UtilitarioCard = UtilitarioCard()
        self.__gerenciador_estudo__: UtilitarioEstudo = UtilitarioEstudo()
        self.__taxa_aprendizado__ = .8  # a
        self.__fator_desconto__ = .10  # y
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
            self.__tabela_q_learning_ = np.zeros([self.__qtd_possiveis_estados__, self.__qtd_possiveis_efs__])
            #self.q_table[self.__qtd_possiveis_estados__ - 1, :] = 1 - Última Linha do q learning - Reccompensa 1
        else:
            self.__tabela_q_learning_ = tabela_q_learning

    # Atualiza tabela/s do Q-learning
    def atualizar_politica(self, recompensa, estudo: Estudo):
        estado = self.__utilitario_qlearning__.mapear_numero_repeticao_em_estado(estudo.numero_repeticao)
        card_ef = self.__gerenciador_card__.buscar_card(estudo.card_id).ef
        acao = self.__utilitario_qlearning__.mapear_ef_em_acao(card_ef)

        # Fórmula para atualizar QLearning com recompensas não determinísticas
        self.__tabela_q_learning_[estado, acao] = self.__tabela_q_learning_[estado, acao] + \
                                                  self.__taxa_aprendizado__ * (
                                                                     recompensa +
                                                                     self.__fator_desconto__ * np.max(self.__tabela_q_learning_[estado + 1, :]) -
                                                                     self.__tabela_q_learning_[estado, acao]
                                                )

    def atualizar_estudo(self, estudo: Estudo, acerto=False):
        if acerto is True:
            self.__atualizar_ef_card__(estudo)
            estudo = self.__calcular_proxima_repeticao__(estudo)
        else:
            self.__atualizar_ef_card__(estudo, resetar_ef_card=True)
            estudo = self.__calcular_proxima_repeticao__(estudo, resetar_estudo=True)

        self.__gerenciador_estudo__.atualizar_estudo(estudo)


    def atualizar_estudo_primeira_repeticao(self, estudo: Estudo, acerto=False):
        if acerto is True:
            self.__atualizar_ef_card__(estudo)
            estudo = self.__calcular_proxima_repeticao__(estudo)
        else:
            self.__atualizar_ef_card__(estudo, resetar_ef_card=True)
            estudo = self.__calcular_proxima_repeticao__(estudo, resetar_estudo=True)

        self.__gerenciador_estudo__.atualizar_estudo(estudo)


    # Ação do agente
    def __atualizar_ef_card__(self, estudo: Estudo, resetar_ef_card=None):
        card = self.__gerenciador_card__.buscar_card(estudo.card_id)
        ef_antigo = card.ef

        if resetar_ef_card is True:  # Reseta estudo caso o usuário erre a questão
            card.ef = 1.3
        else:
            estado = estudo.numero_repeticao - 1  # Recebe - 1 pois a recompensa será atribuída a ação passada
            # (1./(estado+1)) - E - Exloration vs Explotation rate
            acao = np.argmax(
                self.__tabela_q_learning_[estado, :] +
                np.random.randn(1, self.__qtd_possiveis_efs__) * (1./(estado+1))
            )
            card.ef = self.__utilitario_qlearning__.mapear_acao_em_ef(acao)  # O ef será resultante do atualizar política

        print(f'EF Novo: {card.ef} | EF Antigo: {ef_antigo}')
        self.__gerenciador_card__.atualizar_card(card)

    def __calcular_proxima_repeticao__(self, estudo: Estudo, resetar_estudo=False):
        card_corrente: Card = self.__gerenciador_card__.buscar_card(estudo.card_id)
        ef = card_corrente.ef

        if resetar_estudo is True:  # Caso o usuário erre a resposta
            estudo.numero_repeticao = 1
            estudo.data_primeira_repeticao = datetime.now() #  Será o tempo de agora pois ele será agendado para daqui a 5 dias depois de errar
            estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
            estudo.data_proxima_repeticao = estudo.data_ultima_repeticao + self.__calcular_oi__(ef, estudo.numero_repeticao)

        else:
            if estudo.numero_repeticao is 1:
                estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
                estudo.data_proxima_repeticao = estudo.data_primeira_repeticao + self.__calcular_oi__(ef,
                                                                                                      estudo.numero_repeticao)
            else:
                # Simulando que o tempo passou o tempo e que o card está sendo exibido na data estipulado
                estudo.data_ultima_repeticao = estudo.data_proxima_repeticao  # datetime.now()
                estudo.data_proxima_repeticao = estudo.data_ultima_repeticao + self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)

            estudo.numero_repeticao += 1

        return estudo

    def __calcular_intervalo_em_dias__(self, ef, repeticao):
        return (self.__calcular_oi__(ef, repeticao) - self.__calcular_oi__(ef, repeticao - 1))
