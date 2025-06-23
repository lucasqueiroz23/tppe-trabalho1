import pytest
import icontract
from src.ArvoreB import ArvoreB
from src.Pagina import Pagina


def test_invariante_sucesso_em_arvore_balanceada():
    """
    Verifica que em uma árvore balanceada:
    - buscar chave existente retorna o valor.
    - buscar chave inexistente retorna None.
    """
    tree = ArvoreB(m=2)
    for chave in [10, 20, 5, 15, 25, 2, 8]:
        tree.inserir(chave)
    assert tree.buscar(15) == 15
    assert tree.buscar(99) is None

def test_invariante_falha_quando_folhas_em_niveis_diferentes():
    """
    Verifica que ao montar manualmente folhas em níveis distintos,
    a busca dispara ViolationError por invariante de nível das folhas.
    """
    tree = ArvoreB(m=2)
    tree.raiz = Pagina(t=2, folha=False)
    tree.raiz.qtdRegistros = 1
    tree.raiz.registros = [50]

    left = Pagina(t=2, folha=True)
    left.registros = [10]
    left.qtdRegistros = 1
    tree.raiz.paginas[0] = left

    mid = Pagina(t=2, folha=False)
    mid.qtdRegistros = 0
    deep_leaf = Pagina(t=2, folha=True)
    deep_leaf.registros = [60]
    deep_leaf.qtdRegistros = 1
    mid.paginas[0] = deep_leaf
    tree.raiz.paginas[1] = mid

    with pytest.raises(icontract.ViolationError):
        tree.buscar(60)

def test_interna_desordenada_dispara_violacao():
    """
    Verifica que uma raiz interna com registros fora de ordem
    dispara ViolationError ao buscar.
    """
    tree = ArvoreB(m=2)
    tree.raiz = Pagina(t=2, folha=False)
    tree.raiz.registros = [30, 10]
    tree.raiz.qtdRegistros = 2
    tree.raiz.paginas[0] = Pagina(t=2, folha=True)
    tree.raiz.paginas[1] = Pagina(t=2, folha=True)
    tree.raiz.paginas[2] = Pagina(t=2, folha=True)

    with pytest.raises(icontract.ViolationError):
        tree.buscar(10)

def test_folha_desordenada_dispara_violacao():
    """
    Verifica que uma folha com registros fora de ordem
    dispara ViolationError ao inserir nova chave.
    """
    tree = ArvoreB(m=2)
    tree.raiz = Pagina(t=2, folha=True)
    tree.raiz.registros = [5, 2, 8]
    tree.raiz.qtdRegistros = 3

    with pytest.raises(icontract.ViolationError):
        tree.inserir(9)

def test_interna_em_ordem_nao_dispara():
    """
    Verifica que uma raiz interna ordenada não dispara erro
    e busca retorna None para chave ausente.
    """
    tree = ArvoreB(m=2)
    tree.raiz = Pagina(t=2, folha=False)
    tree.raiz.registros = [10, 20]
    tree.raiz.qtdRegistros = 2
    tree.raiz.paginas[0] = Pagina(t=2, folha=True)
    tree.raiz.paginas[1] = Pagina(t=2, folha=True)
    tree.raiz.paginas[2] = Pagina(t=2, folha=True)

    assert tree.buscar(15) is None

def test_folha_em_ordem_nao_dispara():
    """
    Verifica que inserir em folha ordenada mantém ordem
    e busca retorna valor inserido.
    """
    tree = ArvoreB(m=2)
    tree.raiz = Pagina(t=2, folha=True)
    tree.raiz.registros = [1, 2, 3]
    tree.raiz.qtdRegistros = 3

    tree.inserir(4)
    assert tree.buscar(4) == 4
