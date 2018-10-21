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

    def mostrar_card(self, card: Card, imprimir_questao=True):
        if imprimir_questao:
            print("Digite o número ao lado da qustão para selecionar a resposta")
            print(f'Questão: {card.questao}')
            for index, questao in enumerate(card.opcoes):
                print(f'{index} - {questao}')

        self.__tempo_inicial__ = datetime.now()
        self.__opcao_correta__ = card.opcoes.index(card.opcao_correta)

    def obter_resposta(self):
        resposta_usuario = RespostaUsuario()

        input_invalido = True
        while input_invalido:
            input_do_usuario = input("Selecione a questão:")
            # Caso aperte um caractere indesejado o indice da questão é setado para 1
            try:
                indice_da_questao = int(input_do_usuario)
            except:
                indice_da_questao = 1

            if indice_da_questao >= 0 and indice_da_questao <= 3:
                input_invalido = False
                tempo_final = datetime.now()
                tempo_de_resposta_em_millis = int((tempo_final - self.__tempo_inicial__).total_seconds() * 1000)
                resposta_usuario.tempo_resposta = tempo_de_resposta_em_millis

                if indice_da_questao == self.__opcao_correta__:
                    resposta_usuario.acerto = True
                else:
                    resposta_usuario.acerto = False

        print('---------------------------------------------------------------------------------------')
        return resposta_usuario

    def obter_resposta_automatica(self, tempo_resposta_em_millis: int=None, acerto: bool=None, intervalo:int=None):
        if tempo_resposta_em_millis is None:
            tempo_resposta_em_millis = distribuicao_normal(5, 1.5)

        if acerto is None:
            if intervalo is None:
                acerto = obter_acerto_primeira_repeticao()
            else:
                acerto = obter_acerto_modelo_ebbinghaus(intervalo)

        return RespostaUsuario(tempo_resposta_em_millis, acerto)


    def calcular_recompensa(self, resposta: RespostaUsuario, estudo_corrente: Estudo):
        if resposta.acerto is False:
            # TODO: Testar multiplicando o numero de intervalo em dias por -1
            return -1
            #return -10 * (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
        else:
            intervalo = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
            repeticao = estudo_corrente.numero_repeticao
            tempo_resposta = resposta.tempo_resposta
            recompensa: float = round((intervalo * (repeticao / math.pow(tempo_resposta, 2))), 5)
            print(f'Recompensa: {recompensa} do estudo: {estudo_corrente.card.id} | repeticao: {estudo_corrente.numero_repeticao}')
            return recompensa
