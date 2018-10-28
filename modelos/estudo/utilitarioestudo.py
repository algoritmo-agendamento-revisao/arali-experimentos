from .estudo import Estudo


class UtilitarioEstudo:

    def obter_media_qtd_repeticoes(self, lista_estudos):
        qtd_repeticoes_totais: int = 0
        qtd_estudos: int = len(lista_estudos)
        for estudo in lista_estudos:
            qtd_repeticoes_totais += estudo.__qtd_repeticoes__
        return qtd_repeticoes_totais/qtd_estudos

    def obter_total_repeticoes(self, lista_estudos):
        qtd_repeticoes = 0
        for estudo in lista_estudos:
            qtd_repeticoes += estudo.__qtd_repeticoes__
        return qtd_repeticoes

    def imprimir_estudo(self, estudo:Estudo):
        print(f'Primeira: {estudo.data_primeira_repeticao.date()} |'
              f'Última: {estudo.data_ultima_repeticao.date()} |'
              f'Próxima: {estudo.data_proxima_repeticao.date()} |'
              f'Número repetição: {estudo.numero_repeticao} |'
              f'Card id: {estudo.card.id} |'
              f'Card ef: {estudo.card.ef} |'
              f'Concluido: {estudo.concluido}')