# test_teste.py

import pytest
from src.ArvoreB import ArvoreB
from src.Pagina import Pagina

def _in_order(node: Pagina):
    """Percurso em ordem para coletar todas as chaves."""
    if node is None:
        return []
    result = []
    for i in range(node.qtdRegistros):
        result += _in_order(node.paginas[i])
        result.append(node.registros[i])
    result += _in_order(node.paginas[node.qtdRegistros])
    return result

def test_invariante_folhas_mesmo_nivel():
    tree = ArvoreB(3)
    for x in [10, 20, 5, 6, 12, 30, 7, 17]:
        tree.insere(x)
    # todas as folhas devem estar no mesmo nível
    assert tree._leaves_same_level()

def test_invariante_chaves_internas_ordenadas():
    tree = ArvoreB(3)
    for x in [15, 5, 1, 20, 25, 10]:
        tree.insere(x)
    # em cada nó interno, as chaves devem estar em ordem crescente
    assert tree._internal_keys_ordered()

def test_invariante_valores_folhas_ordenados():
    tree = ArvoreB(3)
    for x in [8, 3, 9, 1, 7, 5]:
        tree.insere(x)
    # em cada folha, os valores devem estar em ordem crescente
    assert tree._leaf_values_ordered()

def test_insercao_duplicada_ignorada():
    tree = ArvoreB(3)
    tree.insere(42)
    before = _in_order(tree.raiz).count(42)
    tree.insere(42)
    after = _in_order(tree.raiz).count(42)
    # inserir duplicata não altera contegem
    assert before == after

def test_remocao_inexistente_sem_erro():
    tree = ArvoreB(3)
    # pesquisar inexistente retorna None
    assert tree.pesquisa(999) is None
    # remover inexistente não lança e continua None
    tree.retira(999)
    assert tree.pesquisa(999) is None

def test_remocao_duplicada_ignorada():
    tree = ArvoreB(3)
    tree.insere(5)
    tree.retira(5)
    # segunda remoção não deve lançar
    tree.retira(5)
    assert tree.pesquisa(5) is None

def test_pos_condicao_aumento_nivel():
    tree = ArvoreB(2)
    h_before = tree._height()
    # forçar split na raiz (árvore de grau 2 suporta até 3 chaves)
    for x in [1, 2, 3, 4]:
        tree.insere(x)
    h_after = tree._height()
    assert h_after == h_before + 1

def test_pos_condicao_diminuicao_nivel():
    tree = ArvoreB(2)
    for x in [1, 2, 3, 4]:
        tree.insere(x)
    h_mid = tree._height()
    for x in [4, 3, 2, 1]:
        tree.retira(x)
    h_after = tree._height()
    # após fusão de raízes vazias, altura cai ou volta a 1
    assert h_after <= h_mid - 1 or h_after == 1

def test_bounds_de_chaves():
    tree = ArvoreB(3)
    for x in range(1, 20):
        tree.insere(x)
    # cada nó deve respeitar número mínimo e máximo de chaves
    assert tree._bounds_ok()

def test_bounds_de_filhos():
    tree = ArvoreB(3)
    for x in range(1, 20):
        tree.insere(x)
    # cada nó interno deve respeitar número mínimo e máximo de filhos
    assert tree._children_bounds_ok()
