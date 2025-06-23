import icontract
from typing import Optional, List
from .Pagina import Pagina


@icontract.invariant(
    lambda self: self._folhas_mesmo_nivel(),
    "Nem todas as folhas estão no mesmo nível da árvore"
)
@icontract.invariant(
    lambda self: all(
        node.registros == sorted(node.registros)
        for node in self._todos_nos() if not node.folha
    ),
    "Existe um nó interno com chaves fora de ordem crescente"
)
@icontract.invariant(
    lambda self: all(
        node.registros == sorted(node.registros)
        for node in self._todos_nos() if node.folha
    ),
    "Existe uma folha com valores fora de ordem crescente"
)
class ArvoreB:
    def __init__(self, m: int):
        """
        Inicializa uma nova Árvore B.

        Args:
            m (int): Grau mínimo da árvore (t), define limites de chaves por página.

        Attributes:
            raiz (Optional[Pagina]): Página raiz da árvore.
            t (int): Grau mínimo.
            min_chaves (int): Número mínimo de chaves (t - 1).
            max_chaves (int): Número máximo de chaves (2*t - 1).
        """
        self.raiz: Optional[Pagina] = None
        self.t: int = m
        self.min_chaves: int = m - 1
        self.max_chaves: int = 2 * m - 1

    def _altura_interna(self) -> int:
        """
        Calcula recursivamente a altura da árvore.

        Returns:
            int: Altura total (níveis) da árvore.
        """
        def _h(node: Optional[Pagina]) -> int:
            if node is None:
                return 0
            if node.folha:
                return 1
            return 1 + _h(node.paginas[0])
        return _h(self.raiz)

    def _todos_nos(self) -> List[Pagina]:
        """
        Coleta todas as páginas da árvore em pré-ordem.

        Returns:
            List[Pagina]: Lista de todas as páginas.
        """
        resultado: List[Pagina] = []
        def _coletar(node: Optional[Pagina]) -> None:
            if node is None:
                return
            resultado.append(node)
            if not node.folha:
                for filho in node.paginas[: node.qtdRegistros + 1]:
                    _coletar(filho)
        _coletar(self.raiz)
        return resultado

    def _folhas_mesmo_nivel(self) -> bool:
        """
        Verifica se todas as folhas estão no mesmo nível de profundidade.

        Returns:
            bool: True se todas as folhas têm a mesma profundidade.
        """
        if self.raiz is None:
            return True
        niveis: List[int] = []
        def _percorrer(node: Pagina, profundidade: int) -> None:
            if node.folha:
                niveis.append(profundidade)
            else:
                for filho in node.paginas[: node.qtdRegistros + 1]:
                    if filho:
                        _percorrer(filho, profundidade + 1)
        _percorrer(self.raiz, 1)
        return len(set(niveis)) == 1

    def _limites_chaves_ok(self) -> bool:
        """
        Verifica se cada página respeita os limites de chaves:

          - Raiz: 1 <= qtdRegistros <= max_chaves
          - Demais: min_chaves <= qtdRegistros <= max_chaves

        Returns:
            bool: True se todos estiverem dentro dos limites.
        """
        for no in self._todos_nos():
            minimo, maximo = ((1, self.max_chaves) if no is self.raiz
                              else (self.min_chaves, self.max_chaves))
            if not (minimo <= no.qtdRegistros <= maximo):
                return False
        return True

    def _limites_filhos_ok(self) -> bool:
        """
        Verifica se cada página interna tem número de filhos não-nulos dentro dos limites:

          - Raiz: 2 <= filhos <= 2*t
          - Demais internos: t <= filhos <= 2*t

        Retorna:
            bool: True se todos os internos satisfazem a condição.
        """
        for no in self._todos_nos():
            if not no.folha:
                contagem = sum(
                    1 for i in range(no.qtdRegistros + 1)
                    if no.paginas[i] is not None
                )
                minimo, maximo = ((2, 2 * self.t) if no is self.raiz
                                  else (self.t, 2 * self.t))
                if not (minimo <= contagem <= maximo):
                    return False
        return True

    def altura(self) -> int:
        """
        Retorna a altura da árvore.

        Returns:
            int: Altura atual.
        """
        return self._altura_interna()

    def buscar(self, chave: int) -> Optional[int]:
        """
        Busca uma chave na árvore B.

        Args:
            chave (int): Valor a ser buscado.

        Returns:
            Optional[int]: A chave se encontrada, ou None caso contrário.
        """
        return self._buscar_em_pagina(self.raiz, chave)

    def _buscar_em_pagina(self, pagina: Optional[Pagina], chave: int) -> Optional[int]:
        """
        Busca recursivamente em uma página.

        Args:
            pagina (Optional[Pagina]): Página atual de busca.
            chave (int): Valor buscado.

        Returns:
            Optional[int]: A chave se encontrada, ou None.
        """
        if pagina is None:
            return None
        i = 0
        while i < pagina.qtdRegistros and chave > pagina.registros[i]:
            i += 1
        if i < pagina.qtdRegistros and chave == pagina.registros[i]:
            return pagina.registros[i]
        if pagina.folha:
            return None
        return self._buscar_em_pagina(pagina.paginas[i], chave)

    @icontract.require(
        lambda self, chave: self.buscar(chave) is None,
        "Chave já existe na árvore; duplicatas não são permitidas"
    )
    @icontract.ensure(
        lambda self: self._limites_chaves_ok(),
        "Após inserção, cada página deve respeitar limites de chaves"
    )
    @icontract.ensure(
        lambda self: self._limites_filhos_ok(),
        "Após inserção, cada página interna deve respeitar limites de filhos"
    )
    @icontract.snapshot(lambda self: self._altura_interna(), name="altura_antiga")
    @icontract.ensure(
        lambda self, OLD: self._altura_interna() == OLD.altura_antiga
                        or self._altura_interna() == OLD.altura_antiga + 1,
        "Após divisão da raiz, a altura deve permanecer igual ou aumentar em 1"
    )
    def inserir(self, chave: int) -> None:
        """
        Insere uma chave na árvore B.

        Args:
            chave (int): Valor a inserir (único).

        """
        if self.raiz is None:
            self.raiz = Pagina(self.t, True)
            self.raiz.registros.append(chave)
            self.raiz.qtdRegistros = 1
            return

        if self.raiz.qtdRegistros == self.max_chaves:
            nova = Pagina(self.t, False)
            nova.paginas[0] = self.raiz
            self._dividir_pagina(nova, 0)
            self.raiz = nova

        self._inserir_em_pagina_nao_cheia(self.raiz, chave)

    def _inserir_em_pagina_nao_cheia(self, pagina: Pagina, chave: int) -> None:
        """
        Insere em página que não está cheia.

        Args:
            pagina (Pagina): Página alvo.
            chave (int): Valor a inserir.
        """
        i = pagina.qtdRegistros - 1
        if pagina.folha:
            pagina.registros.append(0)
            while i >= 0 and chave < pagina.registros[i]:
                pagina.registros[i + 1] = pagina.registros[i]
                i -= 1
            pagina.registros[i + 1] = chave
            pagina.qtdRegistros += 1
            return

        while i >= 0 and chave < pagina.registros[i]:
            i -= 1
        i += 1
        filho = pagina.paginas[i]

        if filho.qtdRegistros == self.max_chaves:
            if i > 0 and pagina.paginas[i - 1].qtdRegistros < self.max_chaves:
                self._emprestar_de_anterior(pagina, i)
            elif i < pagina.qtdRegistros and pagina.paginas[i + 1].qtdRegistros < self.max_chaves:
                self._emprestar_de_posterior(pagina, i)
            else:
                self._dividir_pagina(pagina, i)
                if chave > pagina.registros[i]:
                    i += 1
            filho = pagina.paginas[i]

        self._inserir_em_pagina_nao_cheia(filho, chave)

    def _dividir_pagina(self, pai: Pagina, indice: int) -> None:
        """
        Divide uma página cheia e promove chave do meio.

        Args:
            pai (Pagina): Página pai.
            indice (int): Índice da página a dividir.
        """
        filho = pai.paginas[indice]
        novo = Pagina(self.t, filho.folha)
        meio = self.max_chaves // 2
        chave_meio = filho.registros[meio]

        novo.registros = filho.registros[meio + 1:]
        novo.qtdRegistros = len(novo.registros)
        filho.registros = filho.registros[:meio]
        filho.qtdRegistros = meio

        if not filho.folha:
            novo.paginas = filho.paginas[meio + 1:]
            filho.paginas = filho.paginas[:meio + 1]

        pai.registros.insert(indice, chave_meio)
        pai.qtdRegistros += 1
        pai.paginas.insert(indice + 1, novo)
        pai.paginas = pai.paginas[:2 * self.t]

    @icontract.require(
        lambda self, chave: self.buscar(chave) is not None,
        "Chave não existe na árvore"
    )
    @icontract.ensure(
        lambda self: self._limites_chaves_ok(),
        "Após remoção, cada página deve respeitar limites de chaves"
    )
    @icontract.ensure(
        lambda self: self._limites_filhos_ok(),
        "Após remoção, cada página interna deve respeitar limites de filhos"
    )
    @icontract.snapshot(lambda self: self._altura_interna(), name="altura_antiga")
    @icontract.ensure(
        lambda self, OLD: self._altura_interna() == OLD.altura_antiga
                        or self._altura_interna() == OLD.altura_antiga - 1,
        "Após fusão da raiz, a altura deve permanecer igual ou diminuir em 1"
    )
    def remover(self, chave: int) -> None:
        """
        Remove uma chave da árvore B.

        Args:
            chave (int): Valor a remover.
        """
        if self.raiz is None:
            return
        self._remover_em_pagina(self.raiz, chave)
        if self.raiz.qtdRegistros == 0:
            if self.raiz.folha:
                self.raiz = None
            else:
                self.raiz = self.raiz.paginas[0]

    def _remover_em_pagina(self, pagina: Pagina, chave: int) -> bool:
        """
        Remove recursivamente em uma página.

        Args:
            pagina (Pagina): Página atual.
            chave (int): Valor a remover.

        Returns:
            bool: True se ficar abaixo do mínimo de chaves.
        """
        idx = 0
        while idx < pagina.qtdRegistros and chave > pagina.registros[idx]:
            idx += 1

        if idx < pagina.qtdRegistros and chave == pagina.registros[idx]:
            if pagina.folha:
                del pagina.registros[idx]
                pagina.qtdRegistros -= 1
                return pagina.qtdRegistros < self.min_chaves
            return self._remover_chave_em_pagina_interna(pagina, idx)

        if pagina.folha:
            return False

        return self._processar_remocao_em_filho(pagina, idx, chave)

    def _remover_chave_em_pagina_interna(self, pagina: Pagina, idx: int) -> bool:
        """
        Remove chave de página interna, usando predecessores/sucessores ou fusão.

        Args:
            pagina (Pagina): Página interna.
            idx (int): Índice da chave.

        Returns:
            bool: True se abaixo do mínimo após operar.
        """
        chave = pagina.registros[idx]
        if pagina.paginas[idx].qtdRegistros > self.min_chaves:
            pred = self._obter_predecessor(pagina, idx)
            pagina.registros[idx] = pred
            return self._remover_em_pagina(pagina.paginas[idx], pred)

        if pagina.paginas[idx + 1].qtdRegistros > self.min_chaves:
            succ = self._obter_sucessor(pagina, idx)
            pagina.registros[idx] = succ
            return self._remover_em_pagina(pagina.paginas[idx + 1], succ)

        self._fundir_paginas(pagina, idx)
        return self._remover_em_pagina(pagina.paginas[idx], chave)

    def _obter_predecessor(self, pagina: Pagina, idx: int) -> int:
        """
        Obtém predecessor (maior chave à esquerda).

        Args:
            pagina (Pagina): Página interna.
            idx (int): Índice da chave.

        Returns:
            int: Valor do predecessor.
        """
        atual = pagina.paginas[idx]
        while not atual.folha:
            atual = atual.paginas[atual.qtdRegistros]
        return atual.registros[-1]

    def _obter_sucessor(self, pagina: Pagina, idx: int) -> int:
        """
        Obtém sucessor (menor chave à direita).

        Args:
            pagina (Pagina): Página interna.
            idx (int): Índice da chave.

        Returns:
            int: Valor do sucessor.
        """
        atual = pagina.paginas[idx + 1]
        while not atual.folha:
            atual = atual.paginas[0]
        return atual.registros[0]

    def _processar_remocao_em_filho(self, pai: Pagina, idx: int, chave: int) -> bool:
        """
        Desce para o filho adequado para remoção e ajusta se necessário.

        Args:
            pai (Pagina): Página pai.
            idx (int): Índice do filho.
            chave (int): Valor a remover.

        Returns:
            bool: True se o filho ficou abaixo do mínimo.
        """
        vai_direita = (idx == pai.qtdRegistros)
        filho = pai.paginas[idx]
        if filho.qtdRegistros == self.min_chaves:
            self._ajustar_filho(pai, idx)
        if vai_direita and idx > pai.qtdRegistros:
            return self._remover_em_pagina(pai.paginas[idx - 1], chave)
        return self._remover_em_pagina(pai.paginas[idx], chave)

    def _ajustar_filho(self, pai: Pagina, idx: int) -> None:
        """
        Garante que o filho tenha chaves suficientes, fazendo empréstimo ou fusão.

        Args:
            pai (Pagina): Página pai.
            idx (int): Índice do filho a ajustar.
        """
        if idx > 0 and pai.paginas[idx - 1].qtdRegistros > self.min_chaves:
            self._emprestar_de_anterior(pai, idx)
        elif idx < pai.qtdRegistros and pai.paginas[idx + 1].qtdRegistros > self.min_chaves:
            self._emprestar_de_posterior(pai, idx)
        else:
            if idx < pai.qtdRegistros:
                self._fundir_paginas(pai, idx)
            else:
                self._fundir_paginas(pai, idx - 1)

    def _emprestar_de_anterior(self, pai: Pagina, idx: int) -> None:
        """
        Empresta uma chave do irmão anterior para o filho.

        Args:
            pai (Pagina): Página pai.
            idx (int): Índice do filho receptor.
        """
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx - 1]
        filho.registros.insert(0, pai.registros[idx - 1])
        filho.qtdRegistros += 1
        if not filho.folha:
            filho.paginas.insert(0, irmao.paginas.pop())
        pai.registros[idx - 1] = irmao.registros.pop()
        irmao.qtdRegistros -= 1

    def _emprestar_de_posterior(self, pai: Pagina, idx: int) -> None:
        """
        Empresta uma chave do irmão posterior para o filho.

        Args:
            pai (Pagina): Página pai.
            idx (int): Índice do filho receptor.
        """
        filho = pai.paginas[idx]
        irmao = pai.paginas[idx + 1]
        filho.registros.append(pai.registros[idx])
        filho.qtdRegistros += 1
        if not filho.folha:
            filho.paginas.append(irmao.paginas.pop(0))
        pai.registros[idx] = irmao.registros.pop(0)
        irmao.qtdRegistros -= 1

    def _fundir_paginas(self, pai: Pagina, idx: int) -> None:
        """
        Fundir uma página com seu irmão e mover a chave do pai.

        Args:
            pai (Pagina): Página pai.
            idx (int): Índice da página à esquerda da fusão.
        """
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
