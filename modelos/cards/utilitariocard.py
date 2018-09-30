from collections import defaultdict

from .mockcards import MockCards
from .card import Card

class UtilitarioCard:

    __cards_na_memoria__ = defaultdict(list)

    def __init__(self):
        mock_cards = MockCards.get_cards()
        for card in mock_cards:
            self.__cards_na_memoria__[card.id] = card

    def buscar_cards(self, tag: str):
        return list(self.__cards_na_memoria__.values())

    def buscar_card(self, card_id):
        return self.__cards_na_memoria__[card_id]

    def atualizar_card(self, card: Card):
        self.__cards_na_memoria__[card.id] = card


