#TODO: Implementar um atributo que indique que o card foi aprendido

class Card:
    id: int
    ef: float
    tag: [str]
    questao: str
    opcoes: [str]
    opcao_correta: str

    def __init__(self, id, ef, tag, questao, opcoes, opcao_correta):
        self.id = id
        self.ef = ef
        self.tag = tag
        self.questao = questao
        self.opcoes = opcoes
        self.opcao_correta = opcao_correta
