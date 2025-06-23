
class Pagina:
    def __init__(self, t: int, folha: bool = False):
        self.folha = folha
        self.registros = []
        self.paginas = [None] * (2 * t)
        self.qtdRegistros = 0
