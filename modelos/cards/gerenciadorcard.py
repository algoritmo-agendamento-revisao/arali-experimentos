from .mockcards import MockCards
from .card import Card

class GerenciadorCard:

    __cards_na_memoria__: [Card] = MockCards.get_cards()

    def buscar_cards(self, tag: str):
        return self.__cards_na_memoria__

    def buscar_card(self, card_id):
        return list(filter(lambda card: card.id == card_id, self.__cards_na_memoria__))[0]

    def atualizar_card(self, card: Card):
        indice_do_card = self.__cards_na_memoria__.index(card)
        self.__cards_na_memoria__[indice_do_card] = card

    def imprimir_essas_caraia_tudo_dos_card(self):
        for card in self.__cards_na_memoria__:
            print(f'EF:{card.ef}')
