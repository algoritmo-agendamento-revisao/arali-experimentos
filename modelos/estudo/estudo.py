from datetime import datetime
from datetime import timedelta

class Estudo:
    tag: str
    card_id: int
    data_primeira_repeticao: datetime
    data_ultima_repeticao: datetime
    data_proxima_repeticao: datetime
    numero_repeticao: int

    def __init__(self, tag: str, card_id: int, data_primeira_repeticao: datetime):
        self.tag = tag
        self.card_id = card_id
        self.data_primeira_repeticao = data_primeira_repeticao
        self.data_ultima_repeticao = None
        self.data_proxima_repeticao = None
        self.numero_repeticao = 1