import copy

from collections import defaultdict
from modelos.cards.utilitariocard import UtilitarioCard
from modelos.estudo.utilitarioestudo import UtilitarioEstudo
from user_interface.userinterface import UserInterface
from reinforcement_learning.agente.agente import Agente
from utilitario.gerenciador_estudo.gerenciador_estudo import GerenciadorEstudo
from utilitario.utilitario_teste.utilitario_teste import UtilitarioTeste
import matplotlib.pyplot as plt
import numpy as np

numero_repeticoes_maximo = 36

class Controlador:

    utilitario_estudo = None
    utilitario_card = None
    utilitario_teste = None
    gerenciador_estudo = None
    __tabela_q_learning__ = None

    def __init__(self):
        self.__tabela_q_learning__ = None
        self.utilitario_estudo = UtilitarioEstudo()
        self.utilitario_card = UtilitarioCard()
        self.utilitario_teste = UtilitarioTeste()  # Ajuda na obtenção da recompensa média por episodio e qtd de episodios
        self.gerenciador_estudo = GerenciadorEstudo()

    def plot_graphic(self, x, y, title, xlabel, ylabel):
        fig1, ax = plt.subplots()

        y_media = [np.mean(y)]*len(x)
        y_max = [np.max(y)]*len(x)
        y_min = [np.min(y)]*len(x)

        media = "Média: {:.2f}".format(y_media[0])
        max = "Máximo: {:.2f}".format(y_max[0])
        min = "Mínimo: {:.2f}".format(y_min[0])

        ax.plot(x, y)
        ax.plot(x, y_media, label=media, linestyle='-.')
        ax.plot(x, y_max, label=max, linestyle='-.')
        ax.plot(x, y_min, label=min, linestyle='-.')
        ax.legend(loc='upper right')
        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        ax.grid()
        plt.show()

    def __criar_estudos__(self, qtd_estudos):
        self.utilitario_card.gerar_cards_aleatorios(qtd_estudos, 1.3, 'teste')
        cards = self.utilitario_card.obter_cards('teste')
        self.gerenciador_estudo.criar_lista_estudos(cards)

    def __obter_estudos__(self, qtd_maxima_cards):
        lista_estudos = defaultdict(list)
        for i in range(0, qtd_maxima_cards):
            novo_estudo = self.gerenciador_estudo.obter_novo_estudo()
            lista_estudos.append(novo_estudo)
        return lista_estudos

    def obter_tabela_q_learning(self):
        return copy.deepcopy(self.__tabela_q_learning__)

    def imprimir_informacoes(self, numero_episodio, modo):
        #modo - grafico | console | ambos
        episodios = []
        taxas_acerto = []

        for episodio in range(1, numero_episodio+1):
            taxa_acerto = self.utilitario_teste.obter_taxa_acerto_episodio(episodio) * 100
            episodios.append(episodio)
            taxas_acerto.append(taxa_acerto)

        if(modo is 'console' or modo is 'ambos'):
            print(f"Episodio: {episodio} | Taxa de acerto:{taxa_acerto} | Qtd estudos aprendidos: {quantidade_estudos_aprendidos}")
        if(modo is 'grafico' or modo is 'ambos'):
            self.plot_graphic(episodios, taxas_acerto, "Taxa de acerto por episódio", "Episódio", "Taxa de acerto (em %)")

    def testar_algoritmo(self, tabela_q_learning=None):
        agente = Agente(numero_repeticoes_maximo, 0.1, 0.1, 0.9, tabela_q_learning)
        user_interface = UserInterface()  # Ambiente

        self.__criar_estudos__(1000)

        for numero_episodio in range(0, 101):
            recompensa_acumulada = 0
            qtd_erro = 0
            qtd_acerto = 0
            qtd_estudos_aprendidos = 0
            estudos_correntes = self.gerenciador_estudo.obter_estudos()

            for estudo_corrente in estudos_correntes:
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
                    self.gerenciador_estudo.mover_estudo_para_aprendidos(estudo_atualizado)
                    self.gerenciador_estudo.substituir_estudo_aprendido_por_novo_estudo()
                    qtd_estudos_aprendidos += 1
                else:
                    self.gerenciador_estudo.atualizar_estudo(estudo_atualizado)

                qtd_acerto += 1 if resposta_do_usuario.acerto else 0
                qtd_erro += 1 if not resposta_do_usuario.acerto else 0

            recompensa_media = recompensa_acumulada / self.gerenciador_estudo.qtd_estudos
            self.utilitario_teste.salvar_dados(numero_episodio, recompensa_media, qtd_acerto, qtd_erro, qtd_estudos_aprendidos)

        # Não há mais estudos
        self.__tabela_q_learning__ = agente.obter_tabela_q_learing()
        self.imprimir_informacoes(numero_episodio, 'grafico')

        estudos_aprendidos = self.gerenciador_estudo.obter_estudos_aprendidos()
        estudos_correntes = self.gerenciador_estudo.obter_estudos()
        total_repeticoes = self.utilitario_estudo.obter_total_repeticoes(estudos_aprendidos)
        total_repeticoes += self.utilitario_estudo.obter_total_repeticoes(estudos_correntes)
        print(f"Total de repeticoes dos cards: {total_repeticoes} | total de cards aprendidos: {len(estudos_aprendidos)}")


tabelas = []
tabela_q_learning = None

for i in range(0, 5):
    controlador = Controlador()
    controlador.testar_algoritmo(tabela_q_learning)
    tabela_q_learning = controlador.obter_tabela_q_learning()
    tabelas.append(copy.deepcopy(tabela_q_learning))

print("acabou")

"""
nome_arquivo = "execução %d" %(i+1) + ".csv"
np.savetxt(nome_arquivo, tabela_q_learning, delimiter=",")
"""
