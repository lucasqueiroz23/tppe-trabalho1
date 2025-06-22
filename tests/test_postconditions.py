from src.ArvoreB import ArvoreB
from typing import List, Optional
import pytest
from src.Pagina import Pagina
import icontract


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
    
def test_pos_condicoes_altura():
    """
    Verifica a pós-condição de variação de altura:
    - altura aumenta em 1 após divisão da raiz,
    - altura diminui em 1 após fusão da raiz,
    - altura permanece inalterada quando não há divisão ou fusão.
    """
    tree = ArvoreB(m=2)
    for key in [10, 20, 5]:
        tree.inserir(key)
    altura_antes = tree.altura()
    tree.inserir(15)
    assert tree.altura() == altura_antes + 1

    folha_esq = make_page(t=2, is_leaf=True, keys=[5])
    folha_dir = make_page(t=2, is_leaf=True, keys=[15])
    raiz = make_page(t=2, is_leaf=False, keys=[10], children=[folha_esq, folha_dir, None])
    raiz.qtdRegistros = 1
    tree.raiz = raiz
    altura_antes = tree.altura()
    tree.remover(10)
    assert tree.altura() == altura_antes - 1

    tree = ArvoreB(m=2)
    tree.inserir(10)
    altura_antes = tree.altura()
    tree.inserir(20)
    assert tree.altura() == altura_antes

    tree.remover(20)
    assert tree.altura() == altura_antes

    tree = ArvoreB(m=2)
    for key in [10, 20, 5, 15, 25]:
        tree.inserir(key)
    altura_antes = tree.altura()
    tree.remover(25)
    assert tree.altura() == altura_antes

def test_violation_num_keys(monkeypatch):
    """
    Pós-condição «número de chaves dentro dos limites»:
    patchamos _inserir_em_pagina_nao_cheia para nada, mantendo um nó
    com 4 chaves (max=3 para t=2), de modo que após insere() _bounds_ok() falhe.
    """
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[1, 2, 3, 4])

    monkeypatch.setattr(ArvoreB, '_inserir_em_pagina_nao_cheia',
                        lambda self, pagina, chave: None)

    with pytest.raises(icontract.ViolationError):
        tree.inserir(5)


def test_violation_num_children(monkeypatch):
    """
    Pós-condição «número de filhos dentro dos limites»:
    patchamos _inserir_em_pagina_nao_cheia para nada, deixando
    a raiz com apenas 1 filho não-nulo (menor que 2), de modo que
    após insere() _children_bounds_ok() falhe.
    """
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[5])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])

    monkeypatch.setattr(ArvoreB, '_inserir_em_pagina_nao_cheia',
                        lambda self, pagina, chave: None)

    with pytest.raises(icontract.ViolationError):
        tree.inserir(15)


def test_violation_height_change(monkeypatch):
    """
    Pós-condição «variação de altura ≤1»:
    monkeypatch em _altura_interna para simular salto >1 após insere().
    """
    tree = ArvoreB(m=2)
    for key in [10, 20, 5]:
        tree.inserir(key)

    real_altura = ArvoreB._altura_interna
    calls = {'count': 0}

    def fake_altura(self):
        calls['count'] += 1
        if calls['count'] == 1:
            return real_altura(self)
        return real_altura(self) + 3

    monkeypatch.setattr(ArvoreB, '_altura_interna', fake_altura)

    with pytest.raises(icontract.ViolationError):
        tree.inserir(15)