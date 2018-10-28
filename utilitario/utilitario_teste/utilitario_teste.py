from collections import defaultdict

class Metadados:

    recompensa_media: float
    qtd_acerto: int
    qtd_erro: int
    qtd_cards_aprendidos: int

    def __init__(self, recompensa_media: float, qtd_acerto: int, qtd_erro: int, qtd_cards_aprendidos):
        self.recompensa_media = recompensa_media
        self.qtd_acerto = qtd_acerto
        self.qtd_erro = qtd_erro
        self.qtd_cards_aprendidos = qtd_cards_aprendidos


class UtilitarioTeste:

    __metadados_episodio__ = defaultdict(list)

    def salvar_dados(self, episodio: int, recompensa_media: float, qtd_acerto: int, qtd_erro: int, qtd_cards_aprendidos: int):
        self.__metadados_episodio__[episodio] = Metadados(recompensa_media, qtd_acerto, qtd_erro, qtd_cards_aprendidos)

    def obter_recompensa_media_episodio(self, episodio:int):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        return metadado_episodio.recompensa_media

    def obter_recompensa_media(self):
        recompensa_acumulada = 0
        qtd_episodio = len(self.__metadados_episodio__)
        for episodio in self.__metadados_episodio__.keys():
            metadado_episodio_atual: Metadados = self.__metadados_episodio__[episodio]
            recompensa_acumulada += metadado_episodio_atual.recompensa_media
        return recompensa_acumulada/qtd_episodio

    def obter_taxa_acerto_episodio(self, episodio):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        qtd_acerto = metadado_episodio.qtd_acerto
        total = metadado_episodio.qtd_acerto + metadado_episodio.qtd_erro
        return qtd_acerto/total

    def obter_taxa_acerto_media(self):
        qtd_episodio = len(self.__metadados_episodio__)
        taxa_acerto_acumulada = 0
        for episodio in self.__metadados_episodio__.keys():
            taxa_acerto_acumulada += self.obter_taxa_acerto_episodio(episodio)
        return taxa_acerto_acumulada/qtd_episodio

    def obter_qtd_erro_episodio(self, episodio):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        return metadado_episodio.qtd_erro

    def obter_qtd_cards_aprendidos_episodio(self, episodio):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        return metadado_episodio.qtd_cards_aprendidos

    def obter_qtd_cards_aprendidos(self):
        qtd_estudos_aprendidos: int = 0
        for episodio in len(self.__metadados_episodio__):
            qtd_estudos_aprendidos += self.__metadados_episodio__[episodio]
        return qtd_estudos_aprendidos

    def limpar_lista(self):
        self.__metadados_episodio__.clear()

    def imprimir_metadados_episodio(self, episodio):
        recompensa_episodio = self.obter_recompensa_media_episodio(episodio)
        qtd_acerto = self.obter_qtd_acerto_repeticao(episodio)
        qtd_erro = self.obter_qtd_erro_episodio(episodio)
        taxa_acerto_erro = self.obter_taxa_acerto_episodio(episodio)*100
        print(f"Episódio: {episodio} | "
              f"Recompensa {recompensa_episodio} | "
              f"qtd acerto: {qtd_acerto} | "
              f"qtd erro: {qtd_erro} | "
              f"taxa acerto/erro: {taxa_acerto_erro}%")

    def imprimir_metadados(self):
        for episodio in self.__metadados_episodio__:
            self.imprimir_metadados(episodio)

    def obter_numero_episodios(self):
        return len(self.__metadados_episodio__)