# Libraries
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
import random

from modelos.cards.card import Card
from modelos.resposta_usuario.respostausuario import RespostaUsuario
from modelos.estudo.estudo import Estudo
from modelos.cards.gerenciadorcard import GerenciadorCard
from modelos.estudo.gerenciadorestudo import GerenciadorEstudo


class Agente:
    __qtd_possiveis_estados__ = 8
    __qtd_possiveis_efs__ = 10
    lr = .8
    y = .95

    __gerenciador_card__: GerenciadorCard = GerenciadorCard()
    __gerenciador_estudo__: GerenciadorEstudo = GerenciadorEstudo()
    q_table = []

    def __calcular_oi__(self, ef, repeticao):
        if repeticao is 1:
            return timedelta(days=5)

        part1 = self.__calcular_oi__(ef, repeticao - 1)
        part2 = ef - 0.1 + np.power(np.e, (-2.3 * repeticao + 5))
        oi = part1 * part2
        return timedelta(days=oi.days)

    def __inicializar_tabela_qlearning__(self):
        self.q_table = np.zeros([self.__qtd_possiveis_estados__, self.__qtd_possiveis_efs__])

    # Atualiza tabela/s do Q-learning
    def atualizar_politica(self, recompensa, estudo: Estudo):
        # tirado 2, pois tratamos de atualizar a tabela para ação de determinar o ef passado e - 1 do indice do array
        # EX: repetição 2 - Recompensa do EF 1, tira-se 1 por causa do índice do array, então ficaria linha 0 na tabela
        ultima_repeticao = estudo.numero_repeticao - 2
        estado = ultima_repeticao
        card_ef = int( (self.__gerenciador_card__.buscar_card(estudo.card_id).ef - 1.3) * 10)

        #TODO: Arrumar o ultimo estado_bugando do np.max
        self.q_table[estado, card_ef] = self.q_table[estado, card_ef] + \
                                            self.lr * (
                                                    recompensa +
                                                    self.y * np.max(self.q_table[estado + 1, :]) -
                                                    self.q_table[estado, card_ef]
                                            )

    def atualizar_estudo(self, estudo: Estudo):
        self.__atualizar_ef_card__(estudo)
        estudo = self.__calcular_proxima_repeticao__(estudo)
        self.__gerenciador_estudo__.atualizar_estudo(estudo)

    # O ef será resultante do atualizar política
    def __atualizar_ef_card__(self, estudo: Estudo):
        card = self.__gerenciador_card__.buscar_card(estudo.card_id)
        #atualizar com o Q-learning - Exloration vs Explotation
        estado = estudo.numero_repeticao - 1
        coluna_do_ef = np.argmax(
            self.q_table[estado, :] +
            np.random.randn(1, self.__qtd_possiveis_efs__) * (1. / (estado + 1))
        )
        card.ef = coluna_do_ef * 0.1 + 1.3
        self.__gerenciador_card__.atualizar_card(card)

    def __calcular_proxima_repeticao__(self, estudo: Estudo):
        card_corrente: Card = self.__gerenciador_card__.buscar_card(estudo.card_id)
        if estudo.numero_repeticao is 1:
            estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
        else:
            # Simulando que o tempo passou o tempo e que o card está sendo exibido na data estipulado
            estudo.data_ultima_repeticao = estudo.data_proxima_repeticao  # datetime.now()

        estudo.data_proxima_repeticao = estudo.data_primeira_repeticao + self.__calcular_oi__(card_corrente.ef,
                                                                                              estudo.numero_repeticao)
        estudo.numero_repeticao += 1
        return estudo


# Ambiente
class UserInterface:
    __tempo_inicial__: datetime
    __opcao_correta__: str

    def mostrar_card(self, card: Card):
        print("Digite o número ao lado da qustão para selecionar a resposta")
        print(f'Questão: {card.questao}')
        for index, questao in enumerate(card.opcoes):
            print(f'{index} - {questao}')

        self.__tempo_inicial__ = datetime.now()
        self.__opcao_correta__ = card.opcoes.index(card.opcao_correta)

    def obter_resposta(self):
        resposta_usuario = RespostaUsuario()

        input_invalido = True
        while input_invalido:
            input_do_usuario = input("Selecione a questão:")
            # Caso aperte um caractere indesejado o indice da questão é setado para 1
            try:
                indice_da_questao = int(input_do_usuario)
            except:
                indice_da_questao = 1

            if indice_da_questao >= 0 and indice_da_questao <= 3:
                input_invalido = False
                tempo_final = datetime.now()
                tempo_de_resposta_em_millis = int((tempo_final - self.__tempo_inicial__).total_seconds() * 1000)
                resposta_usuario.tempo_resposta = tempo_de_resposta_em_millis

                if indice_da_questao == self.__opcao_correta__:
                    resposta_usuario.acerto = True
                else:
                    resposta_usuario.acerto = False

        print('---------------------------------------------------------------------------------------')
        return resposta_usuario

    def calcular_recompensa(self, resposta: RespostaUsuario, estudo_corrente: Estudo):
        intervalo = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
        repeticao = estudo_corrente.numero_repeticao
        tempo_resposta = resposta.tempo_resposta
        return intervalo * (repeticao / tempo_resposta)


class Estudante:

    def responderCard(self, card: Card):
        pass


class Controlador:

    def run(self):
        # Inicializando os componentes do algoritmo
        estudante = Estudante()
        agente = Agente()
        user_interface = UserInterface()
        gerenciador_card = GerenciadorCard()
        gerenciador_estudo = GerenciadorEstudo()

        agente.__inicializar_tabela_qlearning__()

        cards = gerenciador_card.buscar_cards('any tag')

        # Criando objetos de estudo
        for card in cards:
            gerenciador_estudo.criar_estudo(card)

        for episodio in range(1, 9):
            for card in cards:
                user_interface.mostrar_card(card)
                resposta_do_usuario = user_interface.obter_resposta()
                estudo_corrente = gerenciador_estudo.buscar_estudo(card.id)

                if estudo_corrente.numero_repeticao is not 1:
                    recompensa = user_interface.calcular_recompensa(resposta_do_usuario, estudo_corrente)
                    print(f'recompensa {recompensa}')
                    # novo_estado = user_interface.gerar_proximo_estado(card.tag, card.ef, estudo_corrente.numero_repeticao)
                    agente.atualizar_politica(recompensa, estudo_corrente)

                # Agente toma ação / Fornece estado do ambiente
                agente.atualizar_estudo(estudo_corrente)

        gerenciador_estudo.imprimir_estudos()
        table = tabulate(agente.q_table,[],tablefmt="fancy_grid")
        print(table)

controlador = Controlador()
controlador.run()
