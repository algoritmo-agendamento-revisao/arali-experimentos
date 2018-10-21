from modelos.cards.card import Card
from modelos.cards.utilitariocard import UtilitarioCard
from modelos.estudo.utilitarioestudo import UtilitarioEstudo
from user_interface.userinterface import UserInterface
from reinforcement_learning.agente.agente import Agente

numero_repeticoes_maximo = 36

class Controlador:

    def __init__(self):
        self.__tabela_q_learning__ = None

    def __obter_cards__(self, utilitario_card: UtilitarioCard):
        cards = utilitario_card.buscar_cards('any tag')
        return cards

    def __criar_estudos__(self, utilitario_estudo: UtilitarioEstudo, cards: [Card]):
        for card in cards:
            utilitario_estudo.criar_estudo(card)

    def obter_tabela_q_learning(self):
        return self.__tabela_q_learning__

    def testar_algoritmo(self):
        agente = Agente(numero_repeticoes_maximo)
        user_interface = UserInterface() #Ambiente
        utilitario_estudo = UtilitarioEstudo()
        utilitario_card = UtilitarioCard()

        agente.__inicializar_tabela_qlearning__(self.__tabela_q_learning__)
        cards = self.__obter_cards__(utilitario_card)

        #Refatorar essa gambiarra aqui
        self.__criar_estudos__(utilitario_estudo, cards)
        estudos_ativos = utilitario_estudo.obter_estudos()
        qtd_episodios = 0

        while len(estudos_ativos) != 0:
            for estudo_corrente in estudos_ativos:
                #user_interface.mostrar_card(card)

                if estudo_corrente.numero_repeticao is not 1:
                    # Simulando que o algoritmo sempre mostra o card na data agendada
                    intervalo_em_dias = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
                    resposta_do_usuario = user_interface.obter_resposta_automatica(intervalo=intervalo_em_dias)
                    recompensa = user_interface.calcular_recompensa(resposta_do_usuario, estudo_corrente)
                    estudo_corrente.acerto_ultima_repeticao = resposta_do_usuario.acerto
                    estudo_atualizado = agente.tomar_acao(recompensa, estudo_corrente)

                else:
                    resposta_do_usuario = user_interface.obter_resposta_automatica()
                    estudo_corrente.acerto_ultima_repeticao = resposta_do_usuario.acerto
                    estudo_atualizado = agente.tomar_acao(None, estudo_corrente)

                if estudo_atualizado.concluido:
                    utilitario_estudo.remover_estudo(estudo_atualizado)
                else:
                    utilitario_estudo.atualizar_estudo(estudo_atualizado)
                utilitario_estudo.imprimir_estudo(estudo_atualizado)

            qtd_episodios += 1
            estudos_ativos = utilitario_estudo.obter_estudos()  # Se o estudo estiver concluido, ele não é selecionado

        self.__tabela_q_learning__ = agente.obter_tabela_q_learing()
        print(f"qtd episodios= {qtd_episodios}")


controlador = Controlador()
controlador.testar_algoritmo()
tabela_q_learning = controlador.obter_tabela_q_learning()
pass