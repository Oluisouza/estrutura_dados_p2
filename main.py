from src.arvore import ArvoreBinaria

def teste_arvore():
    print("--- Iniciando Sistema ---")

    arvore = ArvoreBinaria()

    ids_produtos = [45, 10, 7, 90, 12, 50, 13, 39, 57]

    print(f" Inserindo: {ids_produtos}")
    for id_prod in ids_produtos:
        arvore.inserir(id_prod)

    estoque_ordenado = arvore.em_ordem()
    print(f"Estoque organizado (Em Ordem): {estoque_ordenado}")

    busca = 14
    encontrou = arvore.buscar(busca)
    print(f"O produto {busca} esta no estoque? {'Sim' if encontrou else 'Não'}")

if __name__ == "__main__":
    teste_arvore()