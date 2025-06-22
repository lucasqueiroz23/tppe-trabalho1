# main.py

from src.ArvoreB import ArvoreB

def imprimir_arvore(no, nivel=0):
    if no is None:
        return
    indent = '    ' * nivel
    print(f"{indent}Nível {nivel} | Registros: {no.registros}")
    if not no.folha:
        for filho in no.paginas[: no.qtdRegistros + 1]:
            imprimir_arvore(filho, nivel + 1)

if __name__ == '__main__':
    arv = ArvoreB(3)

    for chave in [10, 20, 5, 6, 12, 30, 7, 17]:
        arv.inserir(chave)

    print("[Estado inicial]\n")
    print(f"Altura da árvore: {arv.altura()}\n")
    print("Estrutura interna da Árvore B:")
    imprimir_arvore(arv.raiz)

    print("\n[Remoção da chave 6]\n")
    try:
        arv.remover(6)
        print("Chave 6 removida com sucesso.")
    except Exception as e:
        print(f"Erro ao remover a chave 6: {e}")

    print("\n[Após remoção]\n")
    print(f"Altura da árvore: {arv.altura()}\n")
    print("Estrutura interna da Árvore B:")
    imprimir_arvore(arv.raiz)

    print("\n[Inserção da chave 3]\n")
    try:
        arv.inserir(3)
        print("Chave 3 inserida com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir a chave 3: {e}")

    print("\n[Após inserção da chave 3]\n")
    print(f"Altura da árvore: {arv.altura()}\n")
    print("Estrutura interna da Árvore B:")
    imprimir_arvore(arv.raiz)

    print("\n[Inserção da chave 25]\n")
    try:
        arv.inserir(25)
        print("Chave 25 inserida com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir a chave 25: {e}")

    print("\n[Após inserção da chave 25]\n")
    print(f"Altura da árvore: {arv.altura()}\n")
    print("Estrutura interna da Árvore B:")
    imprimir_arvore(arv.raiz)
