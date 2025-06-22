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
