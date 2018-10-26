import copy

from modelos.cards.card import Card
from modelos.cards.utilitariocard import UtilitarioCard
from modelos.estudo.utilitarioestudo import UtilitarioEstudo
from user_interface.userinterface import UserInterface
from reinforcement_learning.agente.agente import Agente
from utilitario.utilitario_teste.utilitario_teste import UtilitarioTeste
import matplotlib.pyplot as plt
import numpy as np

numero_repeticoes_maximo = 36

class Controlador:

    utilitario_estudo = None
    utilitario_card = None
    utilitario_teste = None
    __tabela_q_learning__ = None

    def __init__(self):
        self.__tabela_q_learning__ = None
        self.utilitario_estudo = UtilitarioEstudo()
        self.utilitario_card = UtilitarioCard()
        self.utilitario_teste = UtilitarioTeste()  # Ajuda na obtenção da recompensa média por episodio e qtd de episodios

    def plot_graphic(self, x, y, title, xlabel, ylabel):
        fig1, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel=xlabel, ylabel=ylabel,title=title)
        ax.grid()
        plt.xticks(np.arange(0, 200, 25.0))
        plt.yticks(np.arange(0, 1, 0.05))
        plt.show()

    def __criar_estudos__(self, cards: [Card]):
        for card in cards:
            self.utilitario_estudo.criar_estudo(card)

    def obter_tabela_q_learning(self):
        return copy.deepcopy(self.__tabela_q_learning__)

    def imprimir_informacoes(self, numero_episodio, modo):
        #modo - grafico | console | ambos
        episodios = []
        cards_aprendidos = []
        taxas_acerto = []

        for episodio in range(1, numero_episodio+1):
            taxa_acerto = self.utilitario_teste.obter_taxa_acerto_episodio(episodio)
            quantidade_estudos_aprendidos = self.utilitario_estudo.obter_relacao_estudos_aprendidos_estudos_repeticao(episodio)

            episodios.append(episodio)
            cards_aprendidos.append(quantidade_estudos_aprendidos)
            taxas_acerto.append(taxa_acerto)

        if(modo is 'console' or modo is 'ambos'):
            print(f"Episodio: {episodio} | Taxa de acerto:{taxa_acerto} | Qtd estudos aprendidos: {quantidade_estudos_aprendidos}")
        if(modo is 'grafico' or modo is 'ambos'):
            self.plot_graphic(episodios, cards_aprendidos, "Quantidade de cards aprendidos por episódio", "Episódio", "% de cards aprendidos")


    def testar_algoritmo(self, tabela_q_learning=None):
        agente = Agente(numero_repeticoes_maximo, 0.1, 0.1, 0.9, tabela_q_learning)
        user_interface = UserInterface() #Ambiente

        self.utilitario_card.gerar_cards_aleatorios(200, 1.3, 'teste')
        cards = self.utilitario_card.obter_cards('teste')
        self.__criar_estudos__(cards)
        estudos_ativos = self.utilitario_estudo.obter_estudos()

        numero_episodio = 0

        while len(estudos_ativos) != 0:
            numero_episodio += 1
            recompensa_acumulada = 0
            quantidade_erro = 0
            quantidade_acerto = 0

            for estudo_corrente in estudos_ativos:
                if estudo_corrente.numero_repeticao is not 1:
                    # Simulando que o algoritmo sempre mostra o card na data agendada
                    intervalo_em_dias = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
                    resposta_do_usuario = user_interface.obter_resposta_automatica(intervalo=intervalo_em_dias)
                    recompensa = user_interface.calcular_recompensa(resposta_do_usuario, estudo_corrente)
                    recompensa_acumulada += recompensa
                    estudo_corrente.acerto_ultima_repeticao = resposta_do_usuario.acerto
                    estudo_atualizado = agente.tomar_acao(recompensa, estudo_corrente)

                else:
                    resposta_do_usuario = user_interface.obter_resposta_automatica()
                    estudo_corrente.acerto_ultima_repeticao = resposta_do_usuario.acerto
                    estudo_atualizado = agente.tomar_acao(None, estudo_corrente)

                if estudo_atualizado.concluido:
                    self.utilitario_estudo.marcar_estudo_aprendido(estudo_atualizado)
                else:
                    self.utilitario_estudo.atualizar_estudo(estudo_atualizado)
                #utilitario_estudo.imprimir_estudo(estudo_atualizado)

                quantidade_acerto += 1 if resposta_do_usuario.acerto else 0
                quantidade_erro += 1 if not resposta_do_usuario.acerto else 0

            self.utilitario_estudo.salvar_relacao_estudo_aprendido_estudo_pendente(numero_episodio)

            recompensa_media = recompensa_acumulada / len(estudos_ativos)
            self.utilitario_teste.salvar_dados(numero_episodio, recompensa_media, quantidade_acerto, quantidade_erro)
            estudos_ativos = self.utilitario_estudo.obter_estudos()  # Se o estudo estiver concluido, ele não é selecionado

        # Não há mais estudos
        self.__tabela_q_learning__ = agente.obter_tabela_q_learing()
        self.imprimir_informacoes(numero_episodio, 'grafico')

        total_repeticoes = self.utilitario_estudo.obter_total_repeticoes_cards_aprendidos()
        print(f"Total de repeticoes dos cards {total_repeticoes}")




tabelas = []
tabela_q_learning = None

for i in range(0, 5):
    controlador = Controlador()
    controlador.testar_algoritmo(tabela_q_learning)
    tabela_q_learning = controlador.obter_tabela_q_learning()
    tabelas.append(copy.deepcopy(tabela_q_learning))

print("acabou")
"""
for i in range(0, 4):
    print(f"tabela {i} === tabela {i+1} ? --> {np.array_equal(tabelas[i],tabelas[i+1])}")

nome_arquivo = "execução %d" %(i+1) + ".csv"
np.savetxt(nome_arquivo, tabela_q_learning, delimiter=",")
"""
