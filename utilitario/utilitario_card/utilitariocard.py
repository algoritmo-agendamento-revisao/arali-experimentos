from collections import defaultdict

from modelos.cards.mockcards import MockCards
from modelos.cards.card import Card
from random import randint

class UtilitarioCard:

    __lista_cards__ = defaultdict(list)

    def obter_cards(self, tag: str):
        return list(self.__lista_cards__.values())

    def buscar_card(self, card_id):
        return self.__lista_cards__[card_id]

    def atualizar_card(self, card: Card):
        self.__lista_cards__[card.id] = card


    def gerar_cards_aleatorios(self, quantidade: int, ef_padrao: float, tag: str):
        self.__lista_cards__.clear()
        for i in range(0, quantidade):
            novo_card = Card(i, ef_padrao, tag, "Some question", ["1", "2", "3", "4"], str(randint(1, 4)))
            self.__lista_cards__[i] = novo_card


    def gerar_cards_mockados(self):
        self.__lista_cards__.clear()
        mock_cards = MockCards.get_cards()
        for card in mock_cards:
            self.__lista_cards__[card.id] = card