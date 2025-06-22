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
    page = Pagina(t, is_leaf)
    page.registros    = list(keys)
    page.qtdRegistros = len(keys)
    if children is not None:
        page.paginas = list(children)
    return page

def test_invariante_sucesso_em_arvore_balanceada():
    tree = ArvoreB(m=2)
    for chave in [10, 20, 5, 15, 25, 2, 8]:
        tree.insere(chave)
    # invariantes checadas em métodos públicos
    assert tree.pesquisa(15) == 15
    assert tree.pesquisa(99) is None

def test_invariante_falha_quando_folhas_em_niveis_diferentes():
    tree = ArvoreB(m=2)

    # monta raiz “quebrada”
    tree.raiz = Pagina(t=2, folha=False)
    tree.raiz.qtdRegistros = 1
    tree.raiz.registros   = [50]

    # filho imediato (nível 1)
    left = Pagina(t=2, folha=True)
    left.registros   = [10]
    left.qtdRegistros = 1
    tree.raiz.paginas[0] = left

    # outro ramo mais “profundo” (folha em nível 2)
    mid = Pagina(t=2, folha=False)
    mid.qtdRegistros = 0
    deep_leaf = Pagina(t=2, folha=True)
    deep_leaf.registros   = [60]
    deep_leaf.qtdRegistros = 1
    mid.paginas[0] = deep_leaf
    tree.raiz.paginas[1] = mid

    # chama qualquer método público para disparar a invariante
    with pytest.raises(icontract.ViolationError):
        tree.pesquisa(60)

def test_interna_desordenada_dispara_violacao():
    tree = ArvoreB(m=2)

    # Monta uma raiz interna COM REGISTROS FORA DE ORDEM:
    tree.raiz = Pagina(t=2, folha=False)
    tree.raiz.registros   = [30, 10]  # 30 > 10 → desordenado
    tree.raiz.qtdRegistros = 2

    # É preciso criar 3 filhos (qtdRegistros+1), mesmo vazios, para não ser folha:
    tree.raiz.paginas[0] = Pagina(t=2, folha=True)
    tree.raiz.paginas[1] = Pagina(t=2, folha=True)
    tree.raiz.paginas[2] = Pagina(t=2, folha=True)

    # Qualquer método público dispara a checagem de invariantes
    with pytest.raises(icontract.ViolationError):
        tree.pesquisa(10)


def test_folha_desordenada_dispara_violacao():
    tree = ArvoreB(m=2)

    # Monta a raiz como FOLHA com valores fora de ordem:
    tree.raiz = Pagina(t=2, folha=True)
    tree.raiz.registros   = [5, 2, 8]  # 5 > 2 → desordenado
    tree.raiz.qtdRegistros = 3

    # Inserir qualquer coisa vai invocar o invariant checker
    with pytest.raises(icontract.ViolationError):
        tree.insere(9)


def test_interna_em_ordem_nao_dispara():
    tree = ArvoreB(m=2)

    # Monta raiz interna COM REGISTROS EM ORDEM:
    tree.raiz = Pagina(t=2, folha=False)
    tree.raiz.registros   = [10, 20]
    tree.raiz.qtdRegistros = 2

    # 3 filhos vazios, mas ordenados em profundidade igual
    tree.raiz.paginas[0] = Pagina(t=2, folha=True)
    tree.raiz.paginas[1] = Pagina(t=2, folha=True)
    tree.raiz.paginas[2] = Pagina(t=2, folha=True)

    # Não deve lançar: retorna None pois 15 não está nos registros
    assert tree.pesquisa(15) is None


def test_folha_em_ordem_nao_dispara():
    tree = ArvoreB(m=2)

    # Monta a raiz como FOLHA com valores em ordem:
    tree.raiz = Pagina(t=2, folha=True)
    tree.raiz.registros   = [1, 2, 3]
    tree.raiz.qtdRegistros = 3

    # Inserir um novo valor corretamente mantém tudo em ordem
    tree.insere(4)
    assert tree.pesquisa(4) == 4
    
def test_insere_pre_falha_com_duplicata():
    tree = ArvoreB(m=2)
    tree.insere(10)
    # agora 10 já está, então inserir de novo deve violar a precondição
    with pytest.raises(icontract.ViolationError):
        tree.insere(10)

def test_retira_pre_falha_com_inexistente():
    tree = ArvoreB(m=2)
    # ainda não inserimos nada, logo remover 5 deve falhar
    with pytest.raises(icontract.ViolationError):
        tree.retira(5)

def test_insere_e_retira_pre_ok():
    tree = ArvoreB(m=2)
    # inserir novo funciona
    tree.insere(7)
    assert tree.pesquisa(7) == 7
    # retirar existente também
    tree.retira(7)
    assert tree.pesquisa(7) is None
    
########

def test_bounds_ok_raiz_valida():
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[10])
    assert tree._bounds_ok()  # 1 chave (dentro do limite [1, 3])

def test_bounds_ok_raiz_invalida_abaixo():
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[])
    assert not tree._bounds_ok()  # 0 chaves (abaixo do mínimo)

def test_bounds_ok_raiz_invalida_acima():
    tree = ArvoreB(m=2)
    tree.raiz = make_page(t=2, is_leaf=True, keys=[1, 2, 3, 4])  # 4 chaves
    assert not tree._bounds_ok()  # max=3, 4 > max

def test_bounds_ok_no_interno_valido():
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[5, 6])  # 2 chaves (min=1, max=3)
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])
    assert tree._bounds_ok()

def test_bounds_ok_no_interno_invalido():
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[])  # 0 chaves (abaixo do min=1)
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])
    assert not tree._bounds_ok()
    
def test_children_bounds_ok_raiz_valida():
    tree = ArvoreB(m=2)
    child1 = make_page(t=2, is_leaf=True, keys=[5])
    child2 = make_page(t=2, is_leaf=True, keys=[15])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child1, child2, None])
    assert tree._children_bounds_ok()

def test_children_bounds_ok_raiz_invalida_abaixo():
    tree = ArvoreB(m=2)
    child = make_page(t=2, is_leaf=True, keys=[5])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, None])
    assert not tree._children_bounds_ok()

def test_children_bounds_ok_raiz_invalida_acima():
    tree = ArvoreB(m=2)
    children = [make_page(t=2, is_leaf=True, keys=[i]) for i in range(5)]
    tree.raiz = make_page(t=2, is_leaf=False, keys=[1,2,3,4], children=children)
    assert not tree._children_bounds_ok()

def test_children_bounds_ok_no_interno_valido():
    tree = ArvoreB(m=2)
    grandchild1 = make_page(t=2, is_leaf=True, keys=[3])
    grandchild2 = make_page(t=2, is_leaf=True, keys=[7])
    child = make_page(t=2, is_leaf=False, keys=[5], children=[grandchild1, grandchild2, None])
    child2 = make_page(t=2, is_leaf=True, keys=[15])  # Segundo filho da raiz
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, child2, None])
    assert tree._children_bounds_ok()

def test_children_bounds_ok_no_interno_invalido():
    tree = ArvoreB(m=2)
    grandchild = make_page(t=2, is_leaf=True, keys=[3])
    child = make_page(t=2, is_leaf=False, keys=[5], children=[grandchild, None])
    child2 = make_page(t=2, is_leaf=True, keys=[15])  # Segundo filho da raiz
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[child, child2, None])
    assert not tree._children_bounds_ok()

def test_children_bounds_ok_filhos_nulos_disparam_violacao():
    tree = ArvoreB(m=2)
    valid_child = make_page(t=2, is_leaf=True, keys=[5])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[valid_child, None])
    assert not tree._children_bounds_ok()

def test_children_bounds_ok_filhos_validos_nao_disparam():
    tree = ArvoreB(m=2)
    left = make_page(t=2, is_leaf=True, keys=[5])
    right = make_page(t=2, is_leaf=True, keys=[15])
    tree.raiz = make_page(t=2, is_leaf=False, keys=[10], children=[left, right, None])
    assert tree._children_bounds_ok()
    
# test.py

def test_altura_aumenta_em_1_ao_dividir_raiz():
    tree = ArvoreB(m=2)
    # Inserir até encher a raiz (3 chaves)
    for key in [10, 20, 5]:
        tree.insere(key)
    altura_antes = tree.altura()
    
    # Inserção que causa divisão da raiz
    tree.insere(15)
    
    # Altura deve aumentar em 1
    assert tree.altura() == altura_antes + 1

def test_altura_diminui_em_1_ao_fundir_raiz():
    tree = ArvoreB(m=2)
    # Construir manualmente uma árvore de altura 2 com raiz com apenas 1 chave
    folha_esq = make_page(t=2, is_leaf=True, keys=[5])
    folha_dir = make_page(t=2, is_leaf=True, keys=[15])
    raiz = make_page(t=2, is_leaf=False, keys=[10], children=[folha_esq, folha_dir, None])
    raiz.qtdRegistros = 1
    tree.raiz = raiz

    altura_antes = tree.altura()
    
    # Remoção que causa fusão da raiz
    tree.retira(10)
    
    # Altura deve diminuir em 1
    assert tree.altura() == altura_antes - 1

def test_altura_nao_muda_em_insercao_sem_divisao():
    tree = ArvoreB(m=2)
    tree.insere(10)
    altura_antes = tree.altura()
    
    # Inserção que não causa divisão
    tree.insere(20)
    
    # Altura deve permanecer a mesma
    assert tree.altura() == altura_antes

def test_altura_nao_muda_em_remocao_sem_fusao():
    tree = ArvoreB(m=2)
    tree.insere(10)
    tree.insere(20)
    altura_antes = tree.altura()
    
    # Remoção que não causa fusão da raiz
    tree.retira(20)
    
    # Altura deve permanecer a mesma
    assert tree.altura() == altura_antes

def test_altura_nao_muda_quando_raiz_nao_funde():
    tree = ArvoreB(m=2)
    # Árvore com raiz e 2 filhos
    for key in [10, 20, 5, 15, 25]:
        tree.insere(key)
    altura_antes = tree.altura()
    
    # Remover chave que não causa fusão da raiz
    tree.retira(25)
    
    # Altura deve permanecer a mesma
    assert tree.altura() == altura_antes