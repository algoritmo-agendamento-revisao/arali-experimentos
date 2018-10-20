from datetime import datetime
from collections import defaultdict
from modelos.cards.card import Card
from .estudo import Estudo


class UtilitarioEstudo:

    __lista_estudos__ = defaultdict(list)

    def criar_estudo(self, card: Card):
        novo_estudo = Estudo(
            card,
            datetime.now()
        )
        self.__lista_estudos__[card.id] = novo_estudo

    def obter_estudos(self):
        return list(self.__lista_estudos__.values())

    def buscar_estudo(self, card_id: int):
        return self.__lista_estudos__[card_id]

    def atualizar_estudo(self, estudo: Estudo):
        self.__lista_estudos__[estudo.card.id] = estudo

    def remover_estudo(self, estudo:Estudo):
        self.__lista_estudos__.pop(estudo.card.id, None)

    def imprimir_estudo(self, estudo:Estudo):
        print(f'Primeira: {estudo.data_primeira_repeticao.date()} |'
              f'Última: {estudo.data_ultima_repeticao.date()} |'
              f'Próxima: {estudo.data_proxima_repeticao.date()} |'
              f'Número repetição: {estudo.numero_repeticao} |'
              f'Card id: {estudo.card.id} |'
              f'Card ef: {estudo.card.ef} |'
              f'Concluido: {estudo.concluido}')
