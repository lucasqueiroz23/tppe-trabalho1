class Pagina:
    """
    A classe Pagina representa um nó da árvore-B.
    """

    def __init__(self, numeroMaximoDeRegistros: int):
        self.qtdRegistros = 0
        self.registros = [None] * numeroMaximoDeRegistros  # array de int
        self.paginas = [None] * \
            (numeroMaximoDeRegistros + 1)  # array de Pagina
