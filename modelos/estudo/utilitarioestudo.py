from datetime import datetime
from collections import defaultdict
from modelos.cards.card import Card
from .estudo import Estudo


class UtilitarioEstudo:

    __lista_estudos__ = defaultdict(list)
    __lista_estudos_aprendidos__ = defaultdict(list)
    __relacao_estudo_aprendido_estudo_pendente__ = defaultdict(list)

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

    def obter_total_repeticoes_cards_aprendidos(self):
        qtd_repeticoes = 0
        for episodio in self.__lista_estudos_aprendidos__.keys():
            estudo = self.__lista_estudos_aprendidos__[episodio]
            qtd_repeticoes += estudo.__qtd_repeticoes__
        return qtd_repeticoes

    def salvar_relacao_estudo_aprendido_estudo_pendente(self, episodio):
        qtd_estudos_aprendidos = len(self.__lista_estudos_aprendidos__)
        qtd_estudos_pendentes = len(self.__lista_estudos__)
        total_estudos = qtd_estudos_aprendidos + qtd_estudos_pendentes
        self.__relacao_estudo_aprendido_estudo_pendente__[episodio] = qtd_estudos_aprendidos/total_estudos

    def obter_relacao_estudos_aprendidos_estudos_repeticao(self, episodio):
        return self.__relacao_estudo_aprendido_estudo_pendente__[episodio]

    def buscar_estudo(self, card_id: int):
        return self.__lista_estudos__[card_id]

    def atualizar_estudo(self, estudo: Estudo):
        self.__lista_estudos__[estudo.card.id] = estudo

    def marcar_estudo_aprendido(self, estudo:Estudo):
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

    def imprimir_estudo_qtd_repeticoes(self):
        for estudo in self.__lista_estudos_aprendidos__:
            print(f"Estudo: {estudo.card.id} | repetições: {estudo.__qtd_repeticoes__}")
