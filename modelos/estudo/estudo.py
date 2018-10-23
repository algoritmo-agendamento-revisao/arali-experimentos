from datetime import datetime
from modelos.cards.card import Card

class Estudo:
    tag: str
    card: Card
    data_primeira_repeticao: datetime
    data_ultima_repeticao: datetime
    data_proxima_repeticao: datetime
    numero_repeticao: int
    concluido: bool
    acerto_ultima_repeticao: bool
    #  Metadados
    __qtd_repeticoes__: int


    def __init__(self, card: Card, data_primeira_repeticao: datetime):
        self.tag = card.tag
        self.card = card
        self.data_primeira_repeticao = data_primeira_repeticao
        self.data_ultima_repeticao = None
        self.data_proxima_repeticao = None
        self.numero_repeticao = 1
        self.concluido = False
        self.acerto_ultima_repeticao = None
        self.__qtd_repeticoes__ = 1
