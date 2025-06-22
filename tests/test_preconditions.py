import pytest
import icontract
from src.ArvoreB import ArvoreB


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

