# src/ArvoreB.py

import icontract
from typing import Optional, List
from .Pagina import Pagina

@icontract.invariant(
    lambda self: self._leaves_same_level(),
    "Todas as folhas estão no mesmo nível"
)
@icontract.invariant(
    lambda self: all(
        node.registros == sorted(node.registros)
        for node in self._all_nodes() if not node.folha
    ),
    "Invariante: nós internos com chaves em ordem crescente"
)
@icontract.invariant(
    lambda self: all(
        node.registros == sorted(node.registros)
        for node in self._all_nodes() if node.folha
    ),
    "Invariante: folhas com valores em ordem crescente"
)
class ArvoreB:
    def __init__(self, m: int):
        self.raiz: Optional[Pagina] = None
        self.t: int = m
        self.min_chaves: int = m - 1
        self.max_chaves: int = 2 * m - 1

    def _height(self) -> int:
        def _h(node: Optional[Pagina]) -> int:
            if node is None:
                return 0
            if node.folha:
                return 1
            return 1 + _h(node.paginas[0])
        return _h(self.raiz)

    def _all_nodes(self) -> List[Pagina]:
        nodes: List[Pagina] = []
        def _collect(node: Optional[Pagina]) -> None:
            if node is None:
                return
            nodes.append(node)
            if not node.folha:
                for c in node.paginas[: node.qtdRegistros + 1]:
                    _collect(c)
        _collect(self.raiz)
        return nodes

    def _leaves_same_level(self) -> bool:
        if self.raiz is None:
            return True
        levels: List[int] = []
        def _traverse(node: Pagina, depth: int) -> None:
            if node.folha:
                levels.append(depth)
            else:
                for c in node.paginas[: node.qtdRegistros + 1]:
                    if c:
                        _traverse(c, depth + 1)
        _traverse(self.raiz, 1)
        return len(set(levels)) == 1

    def _bounds_ok(self) -> bool:
        """
        Retorna True se:
          - raiz: 1 <= qtdRegistros <= max_chaves
          - nós não-raiz: min_chaves <= qtdRegistros <= max_chaves
        """
        for node in self._all_nodes():
            low, high = ((1, self.max_chaves)
                         if node is self.raiz
                         else (self.min_chaves, self.max_chaves))
            if not (low <= node.qtdRegistros <= high):
                return False
        return True

    def _children_bounds_ok(self) -> bool:
        """
        Retorna True se, para cada nó interno (não-folha):
        - raiz: 2 <= numFilhos <= 2*t
        - nós internos não-raiz: t <= numFilhos <= 2*t
        Verifica também que os primeiros (qtdRegistros+1) filhos são não nulos.
        """
        for node in self._all_nodes():
            if not node.folha:
                # Conta apenas filhos não nulos nos primeiros qtdRegistros+1
                num_filhos_nao_nulos = sum(
                    1 for i in range(node.qtdRegistros + 1) 
                    if node.paginas[i] is not None
                )
                num_filhos = num_filhos_nao_nulos
                
                low, high = ((2, 2 * self.t) if node is self.raiz
                            else (self.t, 2 * self.t))
                
                if not (low <= num_filhos <= high):
                    return False
        return True
    
    def altura(self) -> int:
        return self._height()

    # ------------------ busca ------------------

    def pesquisa(self, registro: int) -> Optional[int]:
        return self._pesquisa(self.raiz, registro)

    def _pesquisa(self, no: Optional[Pagina], registro: int) -> Optional[int]:
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

    # ------------------ inserção ------------------

    @icontract.require(
        lambda self, registro: self.pesquisa(registro) is None,
        "Pré-condição: chave a ser inserida não existe na árvore"
    )
    @icontract.ensure(
        lambda self: self._bounds_ok(),
        "Pós-condição: chaves em cada nó dentro dos limites (raiz: 1..max; internos: min..max)"
    )
    @icontract.ensure(
        lambda self: self._children_bounds_ok(),
        "Pós-condição: número de filhos em cada nó dentro dos limites (raiz: 2..2*t; internos: t..2*t)"
    )
    @icontract.snapshot(lambda self: self._height(), name="old_height")
    @icontract.ensure(
        lambda self, OLD: self.altura() == OLD.old_height or 
                          self.altura() == OLD.old_height + 1,
        "Para a raiz, após operação de divisão, nível da árvore aumenta em no máximo uma unidade"
    )
    def insere(self, registro: int) -> None:
        if self.raiz is None:
            # árvore vazia → nova raiz folha
            self.raiz = Pagina(self.t, True)
            self.raiz.registros.append(registro)
            self.raiz.qtdRegistros = 1
            return

        # se raiz cheia, divide e aumenta altura
        if self.raiz.qtdRegistros == self.max_chaves:
            nova_raiz = Pagina(self.t, False)
            nova_raiz.paginas[0] = self.raiz
            self._dividir_filho(nova_raiz, 0)
            self.raiz = nova_raiz

        # insere no nó que não está cheio
        self._inserir_nao_cheio(self.raiz, registro)

    def _inserir_nao_cheio(self, no: Pagina, registro: int) -> None:
        i = no.qtdRegistros - 1
        if no.folha:
            # insere na folha em posição ordenada
            no.registros.append(0)
            while i >= 0 and registro < no.registros[i]:
                no.registros[i + 1] = no.registros[i]
                i -= 1
            no.registros[i + 1] = registro
            no.qtdRegistros += 1
            return

        # desce para o filho correto
        while i >= 0 and registro < no.registros[i]:
            i -= 1
        i += 1
        filho = no.paginas[i]

        # se o filho estiver cheio, tenta empréstimo ou divisão
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

        # recursão
        self._inserir_nao_cheio(filho, registro)

    def _dividir_filho(self, pai: Pagina, index: int) -> None:
        filho = pai.paginas[index]
        novo_filho = Pagina(self.t, filho.folha)
        meio = self.max_chaves // 2
        chave_meio = filho.registros[meio]

        # divide registros
        novo_filho.registros = filho.registros[meio + 1:]
        novo_filho.qtdRegistros = len(novo_filho.registros)
        filho.registros = filho.registros[:meio]
        filho.qtdRegistros = meio

        # se for interno, divide também os ponteiros
        if not filho.folha:
            novo_filho.paginas = filho.paginas[meio + 1:]
            filho.paginas = filho.paginas[:meio + 1]

        # insere chave do meio no pai
        pai.registros.insert(index, chave_meio)
        pai.qtdRegistros += 1
        pai.paginas.insert(index + 1, novo_filho)
        # mantêm tamanho máximo de lista de filhos
        pai.paginas = pai.paginas[:2 * self.t]

    # ------------------ remoção ------------------

    @icontract.require(
        lambda self, registro: self.pesquisa(registro) is not None,
        "Pré-condição: chave a ser removida existe na árvore"
    )
    @icontract.ensure(
        lambda self: self._bounds_ok(),
        "Pós-condição: chaves em cada nó dentro dos limites (raiz: 1..max; internos: min..max)"
    )
    @icontract.ensure(
        lambda self: self._children_bounds_ok(),
        "Pós-condição: número de filhos em cada nó dentro dos limites (raiz: 2..2*t; internos: t..2*t)"
    )
    @icontract.snapshot(lambda self: self._height(), name="old_height")
    @icontract.ensure(
        lambda self, OLD: self._height() == OLD.old_height
                         or self._height() == OLD.old_height - 1,
        "Para a raiz, após operação de fusão, nível da árvore diminui em no máximo uma unidade"
    )
    def retira(self, registro: int) -> None:
        # executa a remoção
        self._retirar(self.raiz, registro)

        # ajusta raiz caso tenha ficado sem chaves
        if self.raiz.qtdRegistros == 0:
            if self.raiz.folha:
                # árvore fica vazia
                self.raiz = None
            else:
                # desce a altura: primeiro filho vira nova raiz
                self.raiz = self.raiz.paginas[0]

    def _retirar(self, no: Pagina, registro: int) -> bool:
        idx = 0
        while idx < no.qtdRegistros and registro > no.registros[idx]:
            idx += 1

        # se encontrado no nó
        if idx < no.qtdRegistros and registro == no.registros[idx]:
            if no.folha:
                # remoção simples na folha
                del no.registros[idx]
                no.qtdRegistros -= 1
                return no.qtdRegistros < self.min_chaves
            # remoção em nó interno
            return self._remover_chave_nao_folha(no, idx)

        # se folha e não achou, nada a fazer
        if no.folha:
            return False

        # caso geral: vai para o filho adequado
        return self._processar_filho(no, idx, registro)

    def _remover_chave_nao_folha(self, no: Pagina, idx: int) -> bool:
        chave = no.registros[idx]
        # se o predecessor cabe, troca e remove recursivamente
        if no.paginas[idx].qtdRegistros > self.min_chaves:
            pred = self._obter_predecessor(no, idx)
            no.registros[idx] = pred
            return self._retirar(no.paginas[idx], pred)

        # se o sucessor cabe, idem
        if no.paginas[idx + 1].qtdRegistros > self.min_chaves:
            succ = self._obter_sucessor(no, idx)
            no.registros[idx] = succ
            return self._retirar(no.paginas[idx + 1], succ)

        # caso de fusão
        self._fundir(no, idx)
        return self._retirar(no.paginas[idx], chave)

    def _obter_predecessor(self, no: Pagina, idx: int) -> int:
        atual = no.paginas[idx]
        while not atual.folha:
            atual = atual.paginas[atual.qtdRegistros]
        return atual.registros[-1]

    def _obter_sucessor(self, no: Pagina, idx: int) -> int:
        atual = no.paginas[idx + 1]
        while not atual.folha:
            atual = atual.paginas[0]
        return atual.registros[0]

    def _processar_filho(self, no: Pagina, idx: int, registro: int) -> bool:
        flag = (idx == no.qtdRegistros)
        filho = no.paginas[idx]
        if filho.qtdRegistros == self.min_chaves:
            self._preencher_filho(no, idx)
        if flag and idx > no.qtdRegistros:
            return self._retirar(no.paginas[idx - 1], registro)
        return self._retirar(no.paginas[idx], registro)

    def _preencher_filho(self, pai: Pagina, idx: int) -> None:
        if idx > 0 and pai.paginas[idx - 1].qtdRegistros > self.min_chaves:
            self._emprestar_anterior(pai, idx)
        elif idx < pai.qtdRegistros and pai.paginas[idx + 1].qtdRegistros > self.min_chaves:
            self._emprestar_posterior(pai, idx)
        else:
            if idx < pai.qtdRegistros:
                self._fundir(pai, idx)
            else:
                self._fundir(pai, idx - 1)

    def _emprestar_anterior(self, pai: Pagina, idx: int) -> None:
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx - 1]
        filho.registros.insert(0, pai.registros[idx - 1])
        filho.qtdRegistros += 1
        if not filho.folha:
            filho.paginas.insert(0, irmao.paginas.pop())
        pai.registros[idx - 1] = irmao.registros.pop()
        irmao.qtdRegistros -= 1

    def _emprestar_posterior(self, pai: Pagina, idx: int) -> None:
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx + 1]
        filho.registros.append(pai.registros[idx])
        filho.qtdRegistros += 1
        if not filho.folha:
            filho.paginas.append(irmao.paginas.pop(0))
        pai.registros[idx] = irmao.registros.pop(0)
        irmao.qtdRegistros -= 1

    def _fundir(self, pai: Pagina, idx: int) -> None:
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx + 1]
        # traz a chave do pai
        filho.registros.append(pai.registros.pop(idx))
        filho.qtdRegistros += 1
        # concatena registros e filhos do irmão
        filho.registros.extend(irmao.registros)
        filho.qtdRegistros += irmao.qtdRegistros
        if not filho.folha:
            filho.paginas.extend(irmao.paginas)
        # remove ponteiro e ajusta contagem no pai
        pai.paginas.pop(idx + 1)
        pai.qtdRegistros -= 1
