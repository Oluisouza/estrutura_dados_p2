import random
from src.arvore import ArvoreBinaria
from src.visualizadorGrafo import VisualizadorArvore

def teste_com_grafo():
    print("--- Teste com Visualização de Grafo ---")

    arvore = ArvoreBinaria()

    lista_numeros = random.sample(range(1, 100), 25)

    print(f"Inserindo lista: {lista_numeros}")

    for val in lista_numeros:
        arvore.inserir(val)

    print("\n[INFO] Árvore montada na memória.")
    print("Abrindo janela de visualização...")

    viz = VisualizadorArvore(arvore)
    viz.plotar()

if __name__ == "__main__":
    teste_com_grafo()