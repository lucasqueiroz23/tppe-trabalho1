from Pagina import Pagina


class ArvoreB:

    raiz: Pagina
    numeroMinimoDeregistros: int
    numeroMaximoDeregistros: int

    def __init__(self, m: int):
        self.raiz = None
        self.numeroMinimoDeregistros = m
        self.numeroMaximoDeregistros = 2 * m

    def pesquisa(self, registro: int) -> int:
        """
        A pesquisa usa polimorfismo. Ou seja, este é o método a utilizar
        para fazer uma pesquisa, mas o método sobrecarregado que vai retornar
        a pesquisa de fato.
        """
        return self.pesquisa(registro, self.raiz)

    def insere(self, registro: int):
        pass

    def retira(self, registroistro: int):
        pass
