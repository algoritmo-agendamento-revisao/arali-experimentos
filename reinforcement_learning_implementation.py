from modelos.cards.card import Card
from modelos.cards.utilitariocard import UtilitarioCard
from modelos.estudo.utilitarioestudo import UtilitarioEstudo
from user_interface.userinterface import UserInterface
from reinforcement_learning.agente.agente import Agente
from utilitario.utilitario_teste.utilitario_teste import UtilitarioTeste
import matplotlib.pyplot as plt

numero_repeticoes_maximo = 36

class Controlador:

    def __init__(self):
        self.__tabela_q_learning__ = None

    def plot_graphic(self, x, y, title, xlabel, ylabel):
        fig1, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel=xlabel, ylabel=ylabel,title=title)
        ax.grid()
        plt.show()

    def __criar_estudos__(self, utilitario_estudo: UtilitarioEstudo, cards: [Card]):
        for card in cards:
            utilitario_estudo.criar_estudo(card)

    def obter_tabela_q_learning(self):
        return self.__tabela_q_learning__

    def testar_algoritmo(self):
        agente = Agente(numero_repeticoes_maximo, 0.1, 0.1, 0.9)
        user_interface = UserInterface() #Ambiente
        utilitario_estudo = UtilitarioEstudo()
        utilitario_card = UtilitarioCard()
        utilitario_teste = UtilitarioTeste()  # Ajuda na obtenção da recompensa média por episodio e qtd de episodios

        agente.__inicializar_tabela_qlearning__(self.__tabela_q_learning__)
        utilitario_card.gerar_cards_aleatorios(2000, 1.3, 'teste')
        cards = utilitario_card.obter_cards('teste')

        #Refatorar essa gambiarra aqui
        self.__criar_estudos__(utilitario_estudo, cards)
        estudos_ativos = utilitario_estudo.obter_estudos()
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
                    utilitario_estudo.marcar_estudo_aprendido(estudo_atualizado)
                else:
                    utilitario_estudo.atualizar_estudo(estudo_atualizado)
                #utilitario_estudo.imprimir_estudo(estudo_atualizado)

                quantidade_acerto += 1 if resposta_do_usuario.acerto else 0
                quantidade_erro += 1 if not resposta_do_usuario.acerto else 0

            utilitario_estudo.salvar_relacao_estudo_aprendido_estudo_pendente(numero_episodio)

            recompensa_media = recompensa_acumulada / len(estudos_ativos)
            utilitario_teste.salvar_dados(numero_episodio, recompensa_media, quantidade_acerto, quantidade_erro)
            estudos_ativos = utilitario_estudo.obter_estudos()  # Se o estudo estiver concluido, ele não é selecionado

        # Não há mais estudos
        self.__tabela_q_learning__ = agente.obter_tabela_q_learing()

        x = []
        y = []

        for episodio in range(1, numero_episodio+1):
            taxa_acerto = utilitario_teste.obter_taxa_acerto_episodio(episodio)
            quantidade_estudos_aprendidos = utilitario_estudo.obter_relacao_estudos_aprendidos_estudos_repeticao(episodio)
            x.append(episodio)
            y.append(quantidade_estudos_aprendidos)
            print(f"Episodio: {episodio} | Taxa de acerto:{taxa_acerto} | Qtd estudos aprendidos: {quantidade_estudos_aprendidos}")

        total_repeticoes = utilitario_estudo.obter_total_repeticoes_cards_aprendidos()
        print(f"Total de repeticoes dos cards {total_repeticoes}")
        self.plot_graphic(x, y, "Quantidade de cards aprendidos por episódio", "Episódio", "% de cards aprendidos")



tabelas = []
controlador = Controlador()
controlador.testar_algoritmo()
tabela_q_learning = controlador.obter_tabela_q_learning()
print("ACABOU!!!!")
"""
for i in range(0, 6):
    controlador = Controlador()
    controlador.testar_algoritmo()
    tabela_q_learning = controlador.obter_tabela_q_learning()
    tabelas.append(tabela_q_learning)
    nome_arquivo = "execução %d" %(i+1) + ".csv"
    np.savetxt(nome_arquivo, tabela_q_learning, delimiter=",")

print("finalizado!")
"""
