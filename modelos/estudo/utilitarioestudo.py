from datetime import datetime
from collections import defaultdict
from modelos.cards.card import Card
from .estudo import Estudo


class UtilitarioEstudo:

    __lista_estudos__ = defaultdict(list)
    __lista_estudos_aprendidos__ = defaultdict(list)

    def criar_estudo(self, card: Card):
        novo_estudo = Estudo(
            card,
            datetime.utcfromtimestamp(0)
        )
        self.__lista_estudos__[card.id] = novo_estudo

    def obter_estudos(self):
        return list(self.__lista_estudos__.values())

    def obter_estudos_aprendidos(self):
        return list(self.__lista_estudos_aprendidos__.values())

    def obter_media_qtd_repeticoes(self):
        qtd_repeticoes_totais: int = 0
        qtd_estudos: int = len(self.__lista_estudos_aprendidos__)
        for estudo in self.__lista_estudos_aprendidos__:
            qtd_repeticoes_totais += estudo.__qtd_repeticoes__
        return qtd_repeticoes_totais/qtd_estudos

    def buscar_estudo(self, card_id: int):
        return self.__lista_estudos__[card_id]

    def atualizar_estudo(self, estudo: Estudo):
        self.__lista_estudos__[estudo.card.id] = estudo

    def remover_estudo(self, estudo:Estudo):
        self.__lista_estudos__.pop(estudo.card.id, None)
        self.__lista_estudos_aprendidos__[estudo.card.id] = estudo

    def imprimir_estudo(self, estudo:Estudo):
        print(f'Primeira: {estudo.data_primeira_repeticao.date()} |'
              f'Última: {estudo.data_ultima_repeticao.date()} |'
              f'Próxima: {estudo.data_proxima_repeticao.date()} |'
              f'Número repetição: {estudo.numero_repeticao} |'
              f'Card id: {estudo.card.id} |'
              f'Card ef: {estudo.card.ef} |'
              f'Concluido: {estudo.concluido}')
