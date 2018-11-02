from datetime import datetime
from collections import defaultdict
from random import randint

from modelos.cards.card import Card
from modelos.estudo.estudo import Estudo

class GerenciadorEstudo:

    __lista_estudos__ = defaultdict(list) # Lista de todos os estudos
    __lista_estudos_correntes__ = defaultdict(list) # Lista dos estudos que usuário está vendo atualmente
    __lista_estudos_aprendidos__ = defaultdict(list) # Lista dos estudos que o usuário já aprendeu
    __qtd_total_cards__: int
    qtd_estudos = 30

    def __init__(self):
        self.__lista_estudos__.clear()
        self.__lista_estudos_correntes__.clear()
        self.__lista_estudos_aprendidos__.clear()


    def criar_estudo(self, card: Card):
        novo_estudo = Estudo(
            card,
            datetime.utcfromtimestamp(0)
        )
        return novo_estudo

    def criar_lista_estudos(self, cards):
        # Cria a lista de estudos e migra os a qtd estudos para os estudos correntes
        for card in cards:
            self.__lista_estudos__[card.id] = self.criar_estudo(card)

        self.__qtd_total_cards__ = len(cards)

        for i in range(0, self.qtd_estudos):
            novo_estudo = self.obter_novo_estudo()
            self.__lista_estudos_correntes__[novo_estudo.card.id] = novo_estudo


    def obter_novo_estudo(self):
        card_id = randint(0, len(self.__lista_estudos__)-1)
        cards_disponiveis = self.__lista_estudos__.keys()

        if card_id not in cards_disponiveis:
            while card_id not in cards_disponiveis:
                card_id += 1
                card_id = card_id % self.__qtd_total_cards__

        novo_estudo = self.__lista_estudos__[card_id]
        self.__lista_estudos__.pop(novo_estudo.card.id, None)
        return novo_estudo

    def obter_estudos(self):
        return list(self.__lista_estudos_correntes__.values())

    def obter_estudos_aprendidos(self):
        return list(self.__lista_estudos_aprendidos__.values())

    def buscar_estudo(self, card_id: int):
        return self.__lista_estudos_correntes__[card_id]

    def mover_estudo_para_aprendidos(self, estudo: Estudo):
        self.__lista_estudos_correntes__.pop(estudo.card.id, None)
        self.__lista_estudos_aprendidos__[estudo.card.id] = estudo

    def substituir_estudo_aprendido_por_novo_estudo(self):
        novo_estudo = self.obter_novo_estudo()
        self.__lista_estudos_correntes__[novo_estudo.card.id] = novo_estudo

    def atualizar_estudo(self, estudo_atualizado: Estudo):
        self.__lista_estudos_correntes__[estudo_atualizado.card.id] = estudo_atualizado