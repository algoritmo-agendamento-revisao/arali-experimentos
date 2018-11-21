from datetime import datetime
import math
from modelos.cards.card import Card
from modelos.resposta_usuario.respostausuario import RespostaUsuario
from modelos.estudo.estudo import Estudo
from modelos_matematicos.simulador_memoria_estudante.simulador_memoria_estudante import obter_acerto_modelo_ebbinghaus, obter_acerto_primeira_repeticao
from modelos_matematicos.simulador_tempo_resposta.simulador_tempo_resposta import distribuicao_normal
# Essa classe é a representação do Ambiente
class UserInterface:

    def __init__(self):
        self.__tempo_inicial__: datetime
        self.__opcao_correta__: str

    def obter_resposta_automatica(self, tempo_resposta_em_millis: int=None, acerto: bool=None, intervalo:int=None):
        if tempo_resposta_em_millis is None:
            tempo_resposta_em_millis = distribuicao_normal(5, 1.5)

        if acerto is None:
            if intervalo is None:
                acerto = obter_acerto_primeira_repeticao()
            else:
                acerto = obter_acerto_modelo_ebbinghaus(intervalo)

        return RespostaUsuario(tempo_resposta_em_millis, acerto)


    def calcular_recompensa(self, resposta: RespostaUsuario, estudo_corrente: Estudo, tipo_formula: str):
        if resposta.acerto is False:
            if tipo_formula is "tipo3":
                return -1/estudo_corrente.numero_repeticao
            else:
                return -1
        else:
            intervalo = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
            repeticao = estudo_corrente.numero_repeticao
            tempo_resposta = resposta.tempo_resposta

            recompensa: float

            if tipo_formula is "tipo1" or tipo_formula is "tipo3":
                recompensa = round((intervalo * (repeticao / tempo_resposta)), 5)

            elif tipo_formula is "tipo2":
                recompensa = round((intervalo * (repeticao / math.pow(tempo_resposta, 2))), 5)

            return recompensa
