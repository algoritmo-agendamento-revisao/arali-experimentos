import copy
import os
from collections import defaultdict
from utilitario.utilitario_card.utilitariocard import UtilitarioCard
from utilitario.utilitario_estudo.utilitario_estudo import UtilitarioEstudo
from user_interface.userinterface import UserInterface
from reinforcement_learning.agente.agente import Agente
from gerenciador.gerenciador_estudo.gerenciador_estudo import GerenciadorEstudo
from utilitario.utilitario_teste.utilitario_teste import UtilitarioTeste
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class ConfigTeste:

    def __init__(self, taxa_aprendizagem, taxa_exploracao, fator_desconto, tabela_qlearning_atual, tipo_recompensa, modo_aleatorio=None):
        self.taxa_aprendizagem = taxa_aprendizagem
        self.taxa_exploracao = taxa_exploracao
        self.fator_desconto = fator_desconto
        self.tabela_qlearning_atual = tabela_qlearning_atual
        self.tipo_recompensa = tipo_recompensa
        self.modo_aleatorio = modo_aleatorio

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

    def salvar_grafico(self, x, yq, ya, title, xlabel, ylabel, path, name):
        fig, ax = plt.subplots()

        q_mean = np.mean(yq)
        a_mean = np.mean(ya)
        q_mean_line = [q_mean]*len(x)
        a_mean_line = [a_mean]*len(x)

        ax.plot(x, yq, label="Q Learning")
        ax.plot(x, ya, label="Aleatório")
        ax.plot(x, q_mean_line, label="Média Q Learning", linestyle='--')
        ax.plot(x, a_mean_line, label="Média Aleatória", linestyle='--')

        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        ax.grid()
        ax.margins(x=0)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                  fancybox=True, shadow=True, ncol=4)

        fig.savefig(path + name + ".png", dpi=400)
        #plt.show()

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

    def __gerar_nome_arquivo__(self, configuracao: ConfigTeste):
        a = configuracao.taxa_aprendizagem if configuracao.taxa_aprendizagem is not None else 'linear'
        e = configuracao.taxa_exploracao if configuracao.taxa_exploracao is not None else 'linear'
        y = configuracao.fator_desconto
        r = configuracao.tipo_recompensa
        return 'aprendizagem_{a}_exploracao_{e}_fdesconto_{y}_recompensa_{r}'.format(a=a, e=e, y=y, r=r)

    def testar_algoritmo(self, configuracao: ConfigTeste):

        agente = Agente(
            configuracao.fator_desconto,
            configuracao.modo_aleatorio,
            configuracao.taxa_aprendizagem,
            configuracao.taxa_exploracao,
            configuracao.tabela_qlearning_atual
        )
        user_interface = UserInterface()  # Ambiente

        self.__criar_estudos__(2000)

        qtd_estudos_aprendidos_totais = 0

        for passo in range(0, 200):
            estudos_correntes = self.gerenciador_estudo.obter_estudos()

            for estudo_corrente in estudos_correntes:
                if estudo_corrente.numero_repeticao is not 1:
                    # Simulando que o algoritmo sempre mostra o card na data agendada
                    intervalo_em_dias = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
                    resposta_do_usuario = user_interface.obter_resposta_automatica(intervalo=intervalo_em_dias)
                    recompensa = user_interface.calcular_recompensa(resposta_do_usuario, estudo_corrente, configuracao.tipo_recompensa)
                    estudo_corrente.acerto_ultima_repeticao = resposta_do_usuario.acerto
                    estudo_atualizado = agente.tomar_acao(recompensa, estudo_corrente)

                else:
                    resposta_do_usuario = user_interface.obter_resposta_automatica()
                    estudo_corrente.acerto_ultima_repeticao = resposta_do_usuario.acerto
                    estudo_atualizado = agente.tomar_acao(None, estudo_corrente)

                if estudo_atualizado.concluido:
                    self.gerenciador_estudo.mover_estudo_para_aprendidos(estudo_atualizado)
                    self.gerenciador_estudo.substituir_estudo_aprendido_por_novo_estudo()
                    qtd_estudos_aprendidos_totais += 1
                else:
                    self.gerenciador_estudo.atualizar_estudo(estudo_atualizado)

        # Não há mais estudos
        self.__tabela_q_learning__ = agente.obter_tabelas_q_learing()

        return qtd_estudos_aprendidos_totais

    def run(self):
        tabela_qlearning_atual = None
        nome_diretorio = "resultado_experimento/"

        #taxa_aprendizagem, taxa_exploracao, fator_desconto
        configuracoes_teste = [
            ConfigTeste(0.1, 0.1, 0.1, None, "tipo1"),
            ConfigTeste(0.1, 0.1, 0.1, None, "tipo2"),
            ConfigTeste(0.1, 0.1, 0.1, None, "tipo3"),
            ConfigTeste(0.1, 0.1, 0.5, None, "tipo1"),
            ConfigTeste(0.1, 0.1, 0.5, None, "tipo2"),
            ConfigTeste(0.1, 0.1, 0.5, None, "tipo3"),
            ConfigTeste(0.1, 0.1, 0.9, None, "tipo1"),
            ConfigTeste(0.1, 0.1, 0.9, None, "tipo2"),
            ConfigTeste(0.1, 0.1, 0.9, None, "tipo3"),
            ConfigTeste(0.1, 0.9, 0.1, None, "tipo1"),
            ConfigTeste(0.1, 0.9, 0.1, None, "tipo2"),
            ConfigTeste(0.1, 0.9, 0.1, None, "tipo3"),
            ConfigTeste(0.1, 0.9, 0.5, None, "tipo1"),
            ConfigTeste(0.1, 0.9, 0.5, None, "tipo2"),
            ConfigTeste(0.1, 0.9, 0.5, None, "tipo3"),
            ConfigTeste(0.1, 0.9, 0.9, None, "tipo1"),
            ConfigTeste(0.1, 0.9, 0.9, None, "tipo2"),
            ConfigTeste(0.1, 0.9, 0.9, None, "tipo3"),
            ConfigTeste(0.1, None, 0.1, None, "tipo1"),
            ConfigTeste(0.1, None, 0.1, None, "tipo2"),
            ConfigTeste(0.1, None, 0.1, None, "tipo3"),
            ConfigTeste(0.1, None, 0.5, None, "tipo1"),
            ConfigTeste(0.1, None, 0.5, None, "tipo2"),
            ConfigTeste(0.1, None, 0.5, None, "tipo3"),
            ConfigTeste(0.1, None, 0.9, None, "tipo1"),
            ConfigTeste(0.1, None, 0.9, None, "tipo2"),
            ConfigTeste(0.1, None, 0.9, None, "tipo3"),
            ConfigTeste(0.9, 0.1, 0.1, None, "tipo1"),
            ConfigTeste(0.9, 0.1, 0.1, None, "tipo2"),
            ConfigTeste(0.9, 0.1, 0.1, None, "tipo3"),
            ConfigTeste(0.9, 0.1, 0.5, None, "tipo1"),
            ConfigTeste(0.9, 0.1, 0.5, None, "tipo2"),
            ConfigTeste(0.9, 0.1, 0.5, None, "tipo3"),
            ConfigTeste(0.9, 0.1, 0.9, None, "tipo1"),
            ConfigTeste(0.9, 0.1, 0.9, None, "tipo2"),
            ConfigTeste(0.9, 0.1, 0.9, None, "tipo3"),
            ConfigTeste(0.9, 0.9, 0.1, None, "tipo1"),
            ConfigTeste(0.9, 0.9, 0.1, None, "tipo2"),
            ConfigTeste(0.9, 0.9, 0.1, None, "tipo3"),
            ConfigTeste(0.9, 0.9, 0.5, None, "tipo1"),
            ConfigTeste(0.9, 0.9, 0.5, None, "tipo2"),
            ConfigTeste(0.9, 0.9, 0.5, None, "tipo3"),
            ConfigTeste(0.9, 0.9, 0.9, None, "tipo1"),
            ConfigTeste(0.9, 0.9, 0.9, None, "tipo2"),
            ConfigTeste(0.9, 0.9, 0.9, None, "tipo3"),
            ConfigTeste(0.9, None, 0.1, None, "tipo1"),
            ConfigTeste(0.9, None, 0.1, None, "tipo2"),
            ConfigTeste(0.9, None, 0.1, None, "tipo3"),
            ConfigTeste(0.9, None, 0.5, None, "tipo1"),
            ConfigTeste(0.9, None, 0.5, None, "tipo2"),
            ConfigTeste(0.9, None, 0.5, None, "tipo3"),
            ConfigTeste(0.9, None, 0.9, None, "tipo1"),
            ConfigTeste(0.9, None, 0.9, None, "tipo2"),
            ConfigTeste(0.9, None, 0.9, None, "tipo3"),
            ConfigTeste(None, 0.1, 0.1, None, "tipo1"),
            ConfigTeste(None, 0.1, 0.1, None, "tipo2"),
            ConfigTeste(None, 0.1, 0.1, None, "tipo3"),
            ConfigTeste(None, 0.1, 0.5, None, "tipo1"),
            ConfigTeste(None, 0.1, 0.5, None, "tipo2"),
            ConfigTeste(None, 0.1, 0.5, None, "tipo3"),
            ConfigTeste(None, 0.1, 0.9, None, "tipo1"),
            ConfigTeste(None, 0.1, 0.9, None, "tipo2"),
            ConfigTeste(None, 0.1, 0.9, None, "tipo3"),
            ConfigTeste(None, 0.9, 0.1, None, "tipo1"),
            ConfigTeste(None, 0.9, 0.1, None, "tipo2"),
            ConfigTeste(None, 0.9, 0.1, None, "tipo3"),
            ConfigTeste(None, 0.9, 0.5, None, "tipo1"),
            ConfigTeste(None, 0.9, 0.5, None, "tipo2"),
            ConfigTeste(None, 0.9, 0.5, None, "tipo3"),
            ConfigTeste(None, 0.9, 0.9, None, "tipo1"),
            ConfigTeste(None, 0.9, 0.9, None, "tipo2"),
            ConfigTeste(None, 0.9, 0.9, None, "tipo3"),
            ConfigTeste(None, None, 0.1, None, "tipo1"),
            ConfigTeste(None, None, 0.1, None, "tipo2"),
            ConfigTeste(None, None, 0.1, None, "tipo3"),
            ConfigTeste(None, None, 0.5, None, "tipo1"),
            ConfigTeste(None, None, 0.5, None, "tipo2"),
            ConfigTeste(None, None, 0.5, None, "tipo3"),
            ConfigTeste(None, None, 0.9, None, "tipo1"),
            ConfigTeste(None, None, 0.9, None, "tipo2"),
            ConfigTeste(None, None, 0.9, None, "tipo3")

        ]

        for index, configuracao in enumerate(configuracoes_teste):
            print(f"Experimento número:{index+1}")
            qtd_cards_por_episodio_aleatorio = self.__experimentar__(configuracao, True)
            qtd_cards_por_episodio_qlearning = self.__experimentar__(configuracao, False)

            # Montando a estrutura do csv
            tabela = []
            for i in range(0, len(qtd_cards_por_episodio_aleatorio)):
                tabela.append(
                    [i+1, qtd_cards_por_episodio_qlearning[i], qtd_cards_por_episodio_aleatorio[i]]
                )

            # Cria diretório novo para salvar a tabela e o gráfico
            path = nome_diretorio+"experimento{:.0f}".format(index+1)+"/"
            if not os.path.exists(path):
                os.makedirs(path)

            # Transforma a tabela para salvar em um csv
            df = pd.DataFrame(tabela)
            df.to_csv(path+"tabela.csv", index=False, header=["Episódio", "Quantidade de cards aprendidos - Q Learning", "Quantidade de cards aprendidos - Política aleatória"])

            # Imprimir e salva o gráfico
            self.salvar_grafico(
                range(1, len(qtd_cards_por_episodio_aleatorio)+1),
                qtd_cards_por_episodio_qlearning,
                qtd_cards_por_episodio_aleatorio,
                "Performance aprendizagem: Q Learning x Política aleatória",
                "Número episódio",
                "Quantidade de cards aprendidos",
                path,
                self.__gerar_nome_arquivo__(configuracao)
            )


    def __experimentar__(self, configuracao_teste, modo_aleatorio):
        cards_aprendidos_experimento = []
        qtd_experimento = 3
        qtd_episodios = 100

        for n_experimento in range(0, qtd_experimento):

            configuracao_teste.tabela_qlearning_atual = None
            configuracao_teste.modo_aleatorio = modo_aleatorio

            cards_aprendidos_episodio = []

            for episodio in range(0, qtd_episodios):
                print(f"Sub-Experimento:{n_experimento+1} de 3 | Episódio: {episodio} de 100")

                controlador = Controlador()
                qtd_cards_aprendidos = controlador.testar_algoritmo(configuracao_teste)
                cards_aprendidos_episodio.append(qtd_cards_aprendidos)
                tabela_qlearning_atual = controlador.obter_tabela_q_learning()
                configuracao_teste.tabela_qlearning_atual = tabela_qlearning_atual

            cards_aprendidos_experimento.append(cards_aprendidos_episodio)

        qtd_media_cards_aprendidos_experimento = []

        for n_episodio in range(0, qtd_episodios):
            qtd_media_cards_episodio = 0

            for n_experimento in range(0, qtd_experimento):
                qtd_media_cards_episodio += cards_aprendidos_experimento[n_experimento][n_episodio]

            qtd_media_cards_episodio = round(qtd_media_cards_episodio/qtd_experimento)
            qtd_media_cards_aprendidos_experimento.append(qtd_media_cards_episodio)

        return qtd_media_cards_aprendidos_experimento


Controlador().run()
