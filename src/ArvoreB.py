from Pagina import Pagina

class ArvoreB:
    def __init__(self, m: int):
        self.raiz = None
        self.t = m
        self.min_chaves = m - 1
        self.max_chaves = 2 * m - 1

    def pesquisa(self, registro: int):
        return self._pesquisa(self.raiz, registro)

    def _pesquisa(self, no: Pagina, registro: int):
        if no is None:
            return None
        i = 0
        while i < no.qtdRegistros and registro > no.registros[i]:
            i += 1
        if i < no.qtdRegistros and registro == no.registros[i]:
            return no.registros[i]
        if no.folha:
            return None
        return self._pesquisa(no.paginas[i], registro)

    def insere(self, registro: int) -> None:
        if self.pesquisa(registro) is not None:
            return
        if self.raiz is None:
            self.raiz = Pagina(self.t, True)
            self.raiz.registros.append(registro)
            self.raiz.qtdRegistros = 1
            return
        if self.raiz.qtdRegistros == self.max_chaves:
            nova_raiz = Pagina(self.t, False)
            nova_raiz.paginas[0] = self.raiz
            self._dividir_filho(nova_raiz, 0)
            self.raiz = nova_raiz
        self._inserir_nao_cheio(self.raiz, registro)

    def _inserir_nao_cheio(self, no: Pagina, registro: int):
        i = no.qtdRegistros - 1
        if no.folha:
            no.registros.append(0)
            while i >= 0 and registro < no.registros[i]:
                no.registros[i + 1] = no.registros[i]
                i -= 1
            no.registros[i + 1] = registro
            no.qtdRegistros += 1
            return
        while i >= 0 and registro < no.registros[i]:
            i -= 1
        i += 1
        filho = no.paginas[i]
        if filho.qtdRegistros == self.max_chaves:
            if i > 0 and no.paginas[i - 1].qtdRegistros < self.max_chaves:
                self._emprestar_anterior(no, i)
            elif i < no.qtdRegistros and no.paginas[i + 1].qtdRegistros < self.max_chaves:
                self._emprestar_posterior(no, i)
            else:
                self._dividir_filho(no, i)
                if registro > no.registros[i]:
                    i += 1
            filho = no.paginas[i]
        self._inserir_nao_cheio(filho, registro)

    def _dividir_filho(self, pai: Pagina, index: int):
        filho = pai.paginas[index]
        novo_filho = Pagina(self.t, filho.folha)
        meio = self.max_chaves // 2
        chave_meio = filho.registros[meio]
        novo_filho.registros = filho.registros[meio + 1:]
        novo_filho.qtdRegistros = len(novo_filho.registros)
        filho.registros = filho.registros[:meio]
        filho.qtdRegistros = meio
        if not filho.folha:
            novo_filho.paginas = filho.paginas[meio + 1:]
            filho.paginas = filho.paginas[:meio + 1]
        pai.registros.insert(index, chave_meio)
        pai.qtdRegistros += 1
        pai.paginas.insert(index + 1, novo_filho)
        pai.paginas = pai.paginas[:2 * self.t]

    def retira(self, registro: int) -> None:
        if self.pesquisa(registro) is None:
            return
        self._retirar(self.raiz, registro)
        if self.raiz.qtdRegistros == 0 and not self.raiz.folha:
            self.raiz = self.raiz.paginas[0]

    def _retirar(self, no: Pagina, registro: int) -> bool:
        idx = 0
        while idx < no.qtdRegistros and registro > no.registros[idx]:
            idx += 1
        if idx < no.qtdRegistros and registro == no.registros[idx]:
            if no.folha:
                del no.registros[idx]
                no.qtdRegistros -= 1
                return no.qtdRegistros < self.min_chaves
            return self._remover_chave_nao_folha(no, idx)
        if no.folha:
            return False
        return self._processar_filho(no, idx, registro)

    def _remover_chave_nao_folha(self, no: Pagina, idx: int):
        chave = no.registros[idx]
        if no.paginas[idx].qtdRegistros > self.min_chaves:
            pred = self._obter_predecessor(no, idx)
            no.registros[idx] = pred
            return self._retirar(no.paginas[idx], pred)
        if no.paginas[idx + 1].qtdRegistros > self.min_chaves:
            succ = self._obter_sucessor(no, idx)
            no.registros[idx] = succ
            return self._retirar(no.paginas[idx + 1], succ)
        self._fundir(no, idx)
        return self._retirar(no.paginas[idx], chave)

    def _obter_predecessor(self, no: Pagina, idx: int):
        atual = no.paginas[idx]
        while not atual.folha:
            atual = atual.paginas[atual.qtdRegistros]
        return atual.registros[-1]

    def _obter_sucessor(self, no: Pagina, idx: int):
        atual = no.paginas[idx + 1]
        while not atual.folha:
            atual = atual.paginas[0]
        return atual.registros[0]

    def _processar_filho(self, no: Pagina, idx: int, registro: int):
        flag = (idx == no.qtdRegistros)
        filho = no.paginas[idx]
        if filho.qtdRegistros == self.min_chaves:
            self._preencher_filho(no, idx)
        if flag and idx > no.qtdRegistros:
            return self._retirar(no.paginas[idx - 1], registro)
        return self._retirar(no.paginas[idx], registro)

    def _preencher_filho(self, pai: Pagina, idx: int):
        if idx > 0 and pai.paginas[idx - 1].qtdRegistros > self.min_chaves:
            self._emprestar_anterior(pai, idx)
        elif idx < pai.qtdRegistros and pai.paginas[idx + 1].qtdRegistros > self.min_chaves:
            self._emprestar_posterior(pai, idx)
        else:
            if idx < pai.qtdRegistros:
                self._fundir(pai, idx)
            else:
                self._fundir(pai, idx - 1)

    def _emprestar_anterior(self, pai: Pagina, idx: int):
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx - 1]
        filho.registros.insert(0, pai.registros[idx - 1])
        filho.qtdRegistros += 1
        if not filho.folha:
            filho.paginas.insert(0, irmao.paginas.pop())
        pai.registros[idx - 1] = irmao.registros.pop()
        irmao.qtdRegistros -= 1

    def _emprestar_posterior(self, pai: Pagina, idx: int):
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx + 1]
        filho.registros.append(pai.registros[idx])
        filho.qtdRegistros += 1
        if not filho.folha:
            filho.paginas.append(irmao.paginas.pop(0))
        pai.registros[idx] = irmao.registros.pop(0)
        irmao.qtdRegistros -= 1

    def _fundir(self, pai: Pagina, idx: int):
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx + 1]
        filho.registros.append(pai.registros.pop(idx))
        filho.qtdRegistros += 1
        filho.registros.extend(irmao.registros)
        filho.qtdRegistros += irmao.qtdRegistros
        if not filho.folha:
            filho.paginas.extend(irmao.paginas)
        pai.paginas.pop(idx + 1)
        pai.qtdRegistros -= 1
