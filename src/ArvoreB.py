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
        return self._pesquisa(registro, self.raiz)

    def insere(self, registro: int) -> None:
        regRetorno = [None]
        cresceu = [None]
        apRetorno = self._insere(registro, self.raiz, regRetorno, cresceu)
        if cresceu[0]:
            apTemp = Pagina(self.numeroMaximoDeregistros)
            apTemp.registros[0] = regRetorno[0]
            apTemp.paginas[0] = self.raiz
            apTemp.paginas[1] = apRetorno
            self.raiz = apTemp
            self.raiz.qtdRegistros += 1
        else:
            self.raiz = apRetorno

    def _insere(self, registro: int, ap: Pagina, regRetorno: list[int], cresceu: list[bool]) -> Pagina:
        apRetorno = None
        if ap is None:
            cresceu[0] = True
            regRetorno[0] = registro
        else:
            i = 0
            while i < ap.qtdRegistros - 1 and registro > ap.registros[i]:
                i += 1
            if registro == ap.registros[i]:
                print("Erro: registro já existente")
                cresceu[0] = False
            else:
                if registro > ap.registros[i]:
                    i += 1
                apRetorno = self._insere(
                    registro, ap.paginas[i], regRetorno, cresceu)
                if cresceu[0]:
                    if ap.qtdRegistros < self.numeroMaximoDeregistros:
                        # pagina tem espaço
                        self.insereNaPagina(ap, regRetorno[0], apRetorno)
                        cresceu[0] = False
                        apRetorno = ap
                    else:
                        # overflow, pagina tem que ser dividida
                        apTemp = Pagina(self.numeroMaximoDeregistros)
                        apTemp.paginas[0] = None
                        if i <= self.numeroMinimoDeregistros:
                            self.insereNaPagina(
                                apTemp, ap.registros[self.numeroMaximoDeregistros - 1], ap.paginas[self.numeroMaximoDeregistros])
                            ap.qtdRegistros -= 1
                            self.insereNaPagina(ap, regRetorno[0], apRetorno)
                        j = self.numeroMinimoDeregistros + 1
                        while j < self.numeroMaximoDeregistros:
                            self.insereNaPagina(
                                apTemp, ap.registros[j], ap.paginas[j+1])
                            ap.paginas[j+1] = None
                            j += 1
                        ap.qtdRegistros = self.numeroMinimoDeregistros
                        apTemp.paginas[0] = ap.paginas[self.numeroMinimoDeregistros + 1]
                        regRetorno[0] = ap.registros[self.numeroMinimoDeregistros]
                        apRetorno = apTemp
        return apRetorno if cresceu[0] else ap

    def insereNaPagina(self, ap: Pagina, reg: int, apDir: Pagina):
        k = ap.qtdRegistros - 1

        while k >= 0 and reg < ap.registros[k]:
            ap.registros[k + 1] = ap.registros[k]
            ap.paginas[k+2] = ap.paginas[k+1]
            k -= 1
        ap.registros[k + 1] = reg
        ap.paginas[k + 2] = apDir
        ap.qtdRegistros += 1

    def retira(self, registro: int):
        diminuiu = [None]
        self.raiz = self._retira(registro, self.raiz, diminuiu)
        if diminuiu[0] and self.raiz.qtdRegistros == 0:
            self.raiz = self.raiz.paginas[0]

    def _retira(self, registro: int, ap: Pagina, diminuiu: list[bool]) -> Pagina:
        if ap is None:
            print("erro registro nao encontrado")
            diminuiu[0] = False
        else:
            ind = 0
            while ind < ap.qtdRegistros - 1 and registro > ap.registros[ind]:
                ind += 1
            if registro == ap.registros[ind]:
                # achou
                if ap.paginas[ind] is None:
                    # pagina folha
                    ap.qtdRegistros -= 1
                    diminuiu[0] = (ap.qtdRegistros <
                                   self.numeroMinimoDeregistros)

                    j = ind
                    while j < ap.qtdRegistros:
                        ap.registros[j] = ap.registros[j + 1]
                        ap.paginas[j] = ap.paginas[j+1]
                        j += 1

                    ap.paginas[ap.qtdRegistros] = ap.paginas[ap.qtdRegistros + 1]
                    ap.paginas[ap.qtdRegistros + 1] = None
                else:
                    diminuiu[0] = self.antecessor(ap, ind, ap.paginas[ind])
                    if diminuiu[0]:
                        diminuiu[0] = self.reconstitui(
                            ap.paginas[ind], ap, ind)

            else:
                # nao achou
                if registro > ap.registros[ind]:
                    ind += 1
                ap.paginas[ind] = self._retira(
                    registro, ap.paginas[ind], diminuiu)
                if diminuiu[0]:
                    diminuiu[0] = self.reconstitui(ap.paginas[ind], ap, ind)
        return ap

    def antecessor(self, ap: Pagina, ind: int, apPai: Pagina) -> bool:
        diminuiu = True
        if apPai.paginas[apPai.qtdRegistros] is not None:
            diminuiu = self.antecessor(
                ap, ind, apPai.paginas[apPai.qtdRegistros])
            if diminuiu:
                diminuiu = self.reconstitui(
                    apPai.paginas[apPai.qtdRegistros], apPai, apPai.qtdRegistros)
        else:
            ap.registros[ind] = apPai.registros[apPai.qtdRegistros - 1]
            apPai.qtdRegistros -= 1
            diminuiu = apPai.qtdRegistros < self.numeroMinimoDeregistros
        return diminuiu

    def reconstitui(self, apPag: Pagina, apPai: Pagina, posPai: int) -> bool:
        diminuiu = True
        if posPai < apPai.qtdRegistros:
            aux = apPai.paginas[posPai + 1]
            dispAux = (aux.qtdRegistros - self.numeroMinimoDeregistros + 1)//2
            apPag.registros[apPag.qtdRegistros] = apPai.registros[posPai]
            apPag.qtdRegistros += 1
            apPag.paginas[apPag.qtdRegistros] = aux.paginas[0]
            aux.paginas[0] = None

            if dispAux > 0:
                j = 0
                while j < dispAux - 1:
                    self.insereNaPagina(
                        apPag, aux.registros[j], aux.paginas[j + 1])
                    aux.paginas[j + 1] = None
                    j += 1

                apPai.registros[posPai] = aux.registros[dispAux - 1]
                aux.qtdRegistros -= dispAux
                j = 0
                while j < aux.qtdRegistros:
                    aux.registros[j] = aux.registros[j + dispAux]
                    j += 1

                j = 0
                while j <= aux.qtdRegistros:
                    aux.paginas[j] = aux.paginas[j + dispAux]
                    j += 1

                aux.paginas[aux.qtdRegistros + dispAux] = None
                diminuiu = False
            else:
                j = 0
                while j < self.numeroMinimoDeregistros:
                    self.insereNaPagina(
                        apPag, aux.registros[j], aux.paginas[j+1])
                    aux.paginas[j + 1] = None
                    j += 1
                aux = apPai.paginas[posPai + 1] = None

                j = posPai
                while j < apPai.qtdRegistros - 1:
                    apPai.registros[j] = apPai.registros[j + 1]
                    apPai.paginas[j+1] = apPai.paginas[j+2]
                    j += 1
                apPai.paginas[apPai.qtdRegistros - 1] = None
                apPai.qtdRegistros -= 1

                diminuiu = apPai.qtdRegistros < self.numeroMinimoDeregistros
        else:
            aux = apPai.paginas[posPai - 1]
            dispAux = (aux.qtdRegistros - self.numeroMinimoDeregistros + 1)//2

            j = apPag.qtdRegistros - 1
            while j >= 0:
                apPag.registros[j+1] = apPag.registros[j]
                j -= 1

            apPag.registros[0] = apPai.registros[posPai - 1]

            j = apPag.qtdRegistros
            while j >= 0:
                apPag.paginas[j + 1] = apPag.paginas[j]
                j -= 1

            apPag.qtdRegistros += 1

            if dispAux > 0:
                j = 0
                while j < dispAux - 1:
                    self.insereNaPagina(
                        apPag, aux.registros[aux.qtdRegistros - j - 1], aux.paginas[aux.qtdRegistros - j])
                    aux.paginas[aux.qtdRegistros - j] = None
                    j += 1

                apPag.paginas[0] = aux.paginas[aux.qtdRegistros - dispAux + 1]
                aux.paginas[aux.qtdRegistros - dispAux + 1] = None
                apPai.registros[posPai -
                                1] = aux.registros[aux.qtdRegistros - dispAux]
                aux.qtdRegistros = aux.qtdRegistros - dispAux
                diminuiu = False
            else:
                j = 0
                while j < self.numeroMinimoDeregistros:
                    self.insereNaPagina(
                        aux, apPag.registros[j], apPag.paginas[j+1])
                    apPag.paginas[j+1] = None
                    j += 1

                apPag = None
                apPai.paginas[apPai.qtdRegistros - 1] = None
                apPai.qtdRegistros -= 1
                diminuiu = apPai.qtdRegistros < self.numeroMinimoDeregistros

        return diminuiu

    def _pesquisa(self, registro: int, ap: Pagina) -> int:
        if ap is None:
            # nao encontrou o registro
            return None

        i = 0
        while (i < ap.qtdRegistros - 1) and registro > ap.registros[i]:
            # vai pro proximo registro
            i += 1

        if ap.registros[i] == registro:
            # encontrou o registro
            return ap.r[i]

        if ap.registros[i] > registro:
            # vai pra proxima pagina
            return self._pesquisa(registro, ap.paginas[i])

        # vai pra proxima pagina
        return self._pesquisa(registro, ap.paginas[i + 1])
