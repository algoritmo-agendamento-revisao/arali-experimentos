class UtilitarioQLearning:

    def mapear_numero_repeticao_em_estado(self, repeticao: int):
        return repeticao - 1

    def mapear_ef_em_acao(self, ef):
        # Mapeia ef de 1.3 a 2.8 em 0 até 15
        return int(round((ef - 1.3), 1) * 10)

    def mapear_acao_em_ef(self, acao):
        #Mapeia acao de 0 a 15 em ef de 1.3 a 2.8
        return round(acao * 0.1 + 1.3, 1)