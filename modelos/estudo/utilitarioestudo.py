from datetime import datetime
from collections import defaultdict
from modelos.cards.card import Card
from modelos.cards.utilitariocard import UtilitarioCard
from .estudo import Estudo


class UtilitarioEstudo:

    __estudos_na_memoria__ = defaultdict(list)

    def criar_estudo(self, card: Card):
        novo_estudo = Estudo(
            card.tag,
            card.id,
            datetime.now()
        )
        self.__estudos_na_memoria__[card.id] = novo_estudo

    def obter_estudos(self):
        return list(self.__estudos_na_memoria__.values())

    def buscar_estudo(self, card_id: int):
        return self.__estudos_na_memoria__[card_id]

    def atualizar_estudo(self, estudo: Estudo):
        self.__estudos_na_memoria__[estudo.card_id] = estudo

    def imprimir_estudo(self, estudo:Estudo):
        print(f'primeira: {estudo.data_primeira_repeticao.date()} |'
              f' ultima : {estudo.data_ultima_repeticao.date()} |'
              f' proxima: {estudo.data_proxima_repeticao.date()} |'
              f' numero repeticao: {estudo.numero_repeticao}')
