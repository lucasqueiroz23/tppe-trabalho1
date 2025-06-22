# test_teste.py

import pytest
import icontract
from src.ArvoreB import ArvoreB
from src.Pagina import Pagina
from typing import List, Optional

def make_page(t: int,
              is_leaf: bool,
              keys: List[int],
              children: Optional[List[Pagina]] = None) -> Pagina:
    """
    Cria uma página de B-Tree para testes.

    Args:
        t (int): Grau mínimo da página.
        is_leaf (bool): Indica se é folha.
        keys (List[int]): Lista de chaves a armazenar.
        children (Optional[List[Pagina]]): Lista de filhos opcionais.

    Returns:
        Pagina: Página configurada com as chaves e filhos.
    """
    page = Pagina(t, is_leaf)
    page.registros = list(keys)
    page.qtdRegistros = len(keys)
    if children is not None:
        page.paginas = list(children)
    return page

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

def test_inserir_pre_falha_com_duplicata():
    """
    Verifica que inserir chave duplicada dispara ViolationError.
    """
    tree = ArvoreB(m=2)
    tree.inserir(10)
    with pytest.raises(icontract.ViolationError):
        tree.inserir(10)

def test_remover_pre_falha_com_inexistente():
    """
    Verifica que remover chave inexistente dispara ViolationError.
    """
    tree = ArvoreB(m=2)
    with pytest.raises(icontract.ViolationError):
        tree.remover(5)

def test_inserir_e_remover_pre_ok():
    """
    Verifica inserção e remoção de chave existente funcionam corretamente.
    """
    tree = ArvoreB(m=2)
    tree.inserir(7)
    assert tree.buscar(7) == 7
    tree.remover(7)
    assert tree.buscar(7) is None

def test_limites_chaves_ok_raiz_valida():
    """
    Verifica _limites_chaves_ok retorna True para raiz com número válido de chaves.
    """
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[10])
    assert tree._limites_chaves_ok()

def test_limites_chaves_ok_raiz_invalida_abaixo():
    """
    Verifica _limites_chaves_ok retorna False para raiz com poucas chaves.
    """
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[])
    assert not tree._limites_chaves_ok()

def test_limites_chaves_ok_raiz_invalida_acima():
    """
    Verifica _limites_chaves_ok retorna False para raiz com chaves acima do máximo.
    """
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[1, 2, 3, 4])
    assert not tree._limites_chaves_ok()

def test_limites_chaves_ok_no_interno_valido():
    """
    Verifica _limites_chaves_ok retorna True para nó interno com chaves válidas.
    """
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[5, 6])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])
    assert tree._limites_chaves_ok()

def test_limites_chaves_ok_no_interno_invalido():
    """
    Verifica _limites_chaves_ok retorna False para nó interno com poucas chaves.
    """
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])
    assert not tree._limites_chaves_ok()

def test_limites_filhos_ok_raiz_valida():
    """
    Verifica _limites_filhos_ok retorna True para raiz com número válido de filhos.
    """
    tree = ArvoreB(m=2)
    child1 = make_page(t=2, is_leaf=True, keys=[5])
    child2 = make_page(t=2, is_leaf=True, keys=[15])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child1, child2, None])
    assert tree._limites_filhos_ok()

def test_limites_filhos_ok_raiz_invalida_abaixo():
    """
    Verifica _limites_filhos_ok retorna False para raiz com poucos filhos.
    """
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[5])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])
    assert not tree._limites_filhos_ok()

def test_limites_filhos_ok_raiz_invalida_acima():
    """
    Verifica _limites_filhos_ok retorna False para raiz com muitos filhos.
    """
    tree = ArvoreB(m=2)
    children = [make_page(t=2, is_leaf=True, keys=[i]) for i in range(5)]
    tree.raiz = make_page(t=2, is_leaf=False, keys=[1, 2, 3, 4], children=children)
    assert not tree._limites_filhos_ok()

def test_limites_filhos_ok_no_interno_valido():
    """
    Verifica _limites_filhos_ok retorna True para nó interno válido.
    """
    tree = ArvoreB(m=2)
    grandchild1 = make_page(t=2, is_leaf=True, keys=[3])
    grandchild2 = make_page(t=2, is_leaf=True, keys=[7])
    child = make_page(t=2, is_leaf=False, keys=[5], children=[grandchild1, grandchild2, None])
    child2 = make_page(t=2, is_leaf=True, keys=[15])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, child2, None])
    assert tree._limites_filhos_ok()

def test_limites_filhos_ok_no_interno_invalido():
    """
    Verifica _limites_filhos_ok retorna False para nó interno com filhos insuficientes.
    """
    tree = ArvoreB(m=2)
    grandchild = make_page(t=2, is_leaf=True, keys=[3])
    child = make_page(t=2, is_leaf=False, keys=[5], children=[grandchild, None])
    child2 = make_page(t=2, is_leaf=True, keys=[15])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, child2, None])
    assert not tree._limites_filhos_ok()

def test_limites_filhos_ok_filhos_nulos_disparam_violacao():
    """
    Verifica _limites_filhos_ok retorna False quando existem filhos nulos.
    """
    tree = ArvoreB(m=2)
    valid_child = make_page(t=2, is_leaf=True, keys=[5])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[valid_child, None])
    assert not tree._limites_filhos_ok()

def test_limites_filhos_ok_filhos_validos_nao_disparam():
    """
    Verifica _limites_filhos_ok retorna True quando filhos são válidos.
    """
    tree = ArvoreB(m=2)
    left = make_page(t=2, is_leaf=True, keys=[5])
    right = make_page(t=2, is_leaf=True, keys=[15])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[left, right, None])
    assert tree._limites_filhos_ok()

def test_altura_aumenta_em_1_ao_dividir_raiz():
    """
    Verifica que a altura da árvore aumenta em 1
    ao inserir chave que causa divisão da raiz.
    """
    tree = ArvoreB(m=2)
    for key in [10, 20, 5]:
        tree.inserir(key)
    altura_antes = tree.altura()

    tree.inserir(15)
    assert tree.altura() == altura_antes + 1

def test_altura_diminui_em_1_ao_fundir_raiz():
    """
    Verifica que a altura da árvore diminui em 1
    ao remover chave que causa fusão da raiz.
    """
    tree = ArvoreB(m=2)
    folha_esq = make_page(t=2, is_leaf=True, keys=[5])
    folha_dir = make_page(t=2, is_leaf=True, keys=[15])
    raiz = make_page(t=2, is_leaf=False, keys=[10], children=[folha_esq, folha_dir, None])
    raiz.qtdRegistros = 1
    tree.raiz = raiz

    altura_antes = tree.altura()
    tree.remover(10)
    assert tree.altura() == altura_antes - 1

def test_altura_nao_muda_em_insercao_sem_divisao():
    """
    Verifica que a altura não muda ao inserir chave
    quando não há divisão de página.
    """
    tree = ArvoreB(m=2)
    tree.inserir(10)
    altura_antes = tree.altura()

    tree.inserir(20)
    assert tree.altura() == altura_antes

def test_altura_nao_muda_em_remocao_sem_fusao():
    """
    Verifica que a altura não muda ao remover chave
    quando não há fusão de página.
    """
    tree = ArvoreB(m=2)
    tree.inserir(10)
    tree.inserir(20)
    altura_antes = tree.altura()

    tree.remover(20)
    assert tree.altura() == altura_antes

def test_altura_nao_muda_quando_raiz_nao_funde():
    """
    Verifica que a altura não muda ao remover chave
    que não causa fusão da raiz.
    """
    tree = ArvoreB(m=2)
    for key in [10, 20, 5, 15, 25]:
        tree.inserir(key)
    altura_antes = tree.altura()

    tree.remover(25)
    assert tree.altura() == altura_antes
    