from .card import Card


class MockCards:
    @staticmethod
    def get_cards():
        return [
            Card(1, 1.3, ['adverbios'],
                 "Assinale a alternativa que preenche a lacuna da frase a seguir corretamente: This boat is "
                 "__________small that we can't all get in.",
                 ["very", "so", "many", "much"], 'so'),
            Card(2, 1.3, ['adverbios'], "Qual destas alternativas só contém expressões que indicam tempo:",
                 ["just, suddenly, apparently, all her life", "just, after, all, then;",
                  "any more, apparently, at the same moment;", "right now, all her life, at the same moment, then"],
                 'right now, all her life, at the same moment, then'),
            Card(3, 1.3, ['adverbios'],
                 "Selecione a alternativa que preenche corretamente a lacuna: My mother doesn't drink tea and ...... "
                 "do I.",
                 ["also", "too", "either", "neither"], 'neither'),
            Card(4, 1.3, ['adverbios'],
                 "Assinale a alternativa que preenche corretamente as lacunas: It's.......... difficult to "
                 "find.......... a good wine.",
                 ["so - such", "such - so", "such - such", "so - so"], 'so - such'),
            Card(5, 1.3, ['adverbios'], "Assinale a alternativa correta: The sun______rises in the west.",
                 ["always", "never", "often", "sometimes"], 'always'),
            Card(6, 1.3, ['adverbios'], "Cheque a oração que tem um advérbio de intensidade:",
                 ["I work as a translator, too.", "I also work as a translator.", "I'm too stressed.",
                  "I don't like to work as a translator, either."], "I'm too stressed."),
        ]