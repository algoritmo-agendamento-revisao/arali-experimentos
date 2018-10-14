# Libraries

from modelos.cards.card import Card
from modelos.cards.utilitariocard import UtilitarioCard
from modelos.estudo.utilitarioestudo import UtilitarioEstudo
from modelos.user_interface.userinterface import UserInterface
from modelos.agente.agente import Agente

numero_repeticoes = 9


class Controlador:

    def __init__(self, tabela_q_learning=None, tabela_cards=None, tabela_estudos=None):
        self.__tabela_q_learning__ = tabela_q_learning
        self.__tabela_cards__ = tabela_cards
        self.__tabela_estudos__ = tabela_estudos

    def __obter_cards__(self, utilitario_card: UtilitarioCard):
        cards = utilitario_card.buscar_cards('any tag') if (self.__tabela_cards__ is None) else self.__tabela_cards__
        return cards

    def __criar_estudos__(self, utilitario_estudo: UtilitarioEstudo, cards: [Card]):
        for card in cards:
            utilitario_estudo.criar_estudo(card)

    def __atualizar_dados__(self, tabela_q_learning=None, tabela_cards=None, tabela_estudos=None):
        self.__tabela_q_learning__ = tabela_q_learning
        self.__tabela_cards__ = tabela_cards
        self.__tabela_estudos__ = tabela_estudos

    def obter_tabela_q_learning(self):
        return self.__tabela_q_learning__

    def obter_tabela_cards(self):
        return self.__tabela_cards__

    def obter_tabela_estudos(self):
        return self.__tabela_estudos__

    def run(self):
        agente = Agente(numero_repeticoes)
        user_interface = UserInterface() #Ambiente
        utilitario_estudo = UtilitarioEstudo()
        utilitario_card = UtilitarioCard()

        agente.__inicializar_tabela_qlearning__(self.__tabela_q_learning__)
        cards = self.__obter_cards__(utilitario_card)

        if self.__tabela_estudos__ is None:
            self.__criar_estudos__(utilitario_estudo, cards)

        for episodio in range(1, numero_repeticoes+1):
            for card in cards[-1:]:
                #user_interface.mostrar_card(card)
                resposta_do_usuario = user_interface.obter_resposta_automatica()
                estudo_corrente = utilitario_estudo.buscar_estudo(card.id)

                if estudo_corrente.numero_repeticao is not 1:
                    recompensa = user_interface.calcular_recompensa(resposta_do_usuario, estudo_corrente)
                    agente.atualizar_politica(recompensa, estudo_corrente) #  Atualiza tabela Q Learning
                    agente.atualizar_estudo(estudo_corrente, resposta_do_usuario.acerto)
                else:
                    agente.atualizar_estudo_primeira_repeticao(estudo_corrente, resposta_do_usuario.acerto)

                utilitario_estudo.imprimir_estudo(estudo_corrente)

        self.__atualizar_dados__(
            agente.obter_tabela_q_learing(),
            utilitario_card.buscar_cards('any tag'),
            utilitario_estudo.obter_estudos()
        )

controlador = Controlador()
controlador.run()
for episodios in range(0, 100):
    tabela_q_learning = controlador.obter_tabela_q_learning()
    tabela_cards = controlador.obter_tabela_cards()

    controlador = Controlador(tabela_q_learning, tabela_cards)
    controlador.run()

tabela_q_learning = controlador.obter_tabela_q_learning()
tabela_cards = controlador.obter_tabela_cards()