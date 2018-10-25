from collections import defaultdict

class Metadados:

    recompensa_media: float
    quantidade_acerto: int
    quantidade_erro: int

    def __init__(self, recompensa_media: float, quantidade_acerto: int, quantidade_erro: int):
        self.recompensa_media = recompensa_media
        self.quantidade_acerto = quantidade_acerto
        self.quantidade_erro = quantidade_erro

class UtilitarioTeste:

    __metadados_episodio__ = defaultdict(list)

    def salvar_dados(self, episodio: int, recompensa_media: float, quantidade_acerto: int, quantidade_erro: int):
        self.__metadados_episodio__[episodio] = Metadados(recompensa_media, quantidade_acerto, quantidade_erro)

    def obter_recompensa_media_episodio(self, episodio:int):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        return metadado_episodio.recompensa_media

    def obter_recompensa_media(self):
        recompensa_acumulada = 0
        qtd_episodio = len(self.__metadados_episodio__)
        for episodio in self.__metadados_episodio__.keys():
            metadado_episodio_atual: Metadados = self.__episodio_recompensa_media__[episodio]
            recompensa_acumulada += metadado_episodio_atual.recompensa_media
        return recompensa_acumulada/qtd_episodio

    def obter_taxa_acerto_episodio(self, episodio):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        qtd_acerto = metadado_episodio.quantidade_acerto
        total = metadado_episodio.quantidade_acerto + metadado_episodio.quantidade_erro
        return qtd_acerto/total

    def obter_taxa_acerto_media(self):
        qtd_episodio = len(self.__metadados_episodio__)
        taxa_acerto_acumulada = 0
        for episodio in self.__metadados_episodio__.keys():
            taxa_acerto_acumulada += self.obter_taxa_acerto_episodio(episodio)
        return taxa_acerto_acumulada/qtd_episodio

    def obter_qtd_erro_repeticao(self, episodio):
        metadado_episodio: Metadados = self.__metadados_episodio__[episodio]
        return metadado_episodio.quantidade_erro

    def limpar_lista(self):
        self.__metadados_episodio__.clear()

    def imprimir_metadados_episodio(self, episodio):
        recompensa_episodio = self.obter_recompensa_media_episodio(episodio)
        qtd_acerto = self.obter_qtd_acerto_repeticao(episodio)
        qtd_erro = self.obter_qtd_erro_repeticao(episodio)
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