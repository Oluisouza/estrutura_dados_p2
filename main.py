import sys
import random
from src.arvore import ArvoreBinaria
from src.visualizadorGrafo import VisualizadorArvore

def limpar_tela():
    print("\n" * 50)

def exibir_menu():
    print("\n=== STOCKINARVORE: SISTEMA DE LOGÌSTICA ===")
    print("1. Inserir novo elemento")
    print("2. Remover elemento")
    print("3. Buscar elemento e Remover")
    print("4. Mostrar Visualização Gráfica")
    print("5. Imprimir lista ordenada (Terminal)")
    print("0. Sair")
    print("===========================================")

def main():
    arvore = ArvoreBinaria()

    print("Bem-vindo ao StockInArvore - Sistema de Logística com Árvore Binária de Busca!")
    entrada = input("Digite os números iniciais separados por vírgula (ou ENTER para gerar 25 aleatórios): ")

    if entrada.strip():
        try:
            lista_inicial = [int(x) for x in entrada.split(",")]
        except ValueError:
            print("Entrada inválida. Certifique-se de digitar apenas números inteiros separados por vírgula.")
            sys.exit(1)
    else:
        lista_inicial = random.sample(range(1, 100), 25)
        print(f"Números gerados aleatoriamente: {lista_inicial}")

    print("Construindo árvore balanceada...")
    arvore.carregar_lote_balanceado(lista_inicial)

    viz = VisualizadorArvore(arvore)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
    
        if opcao == "1":
            try:
                val = int(input("Digite o valor a ser inserido: "))
                arvore.inserir_e_rebalancear(val)
                print(f"Valor {val} inserido com sucesso e árvore rebalanceada.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número inteiro.")
        elif opcao == "2":
            try:
                val = int(input("Digite o valor a ser removido: "))
                if arvore.remover_e_rebalancear(val):
                    print(f"Valor {val} removido com sucesso e árvore rebalanceada.")
                else:
                    print(f"Valor {val} não encontrado na árvore.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número inteiro.")
        elif opcao == "3":
            try:
                val = int(input("Digite o valor a ser buscado e removido: "))
                
                nivel = arvore.buscar_posicao(val)
                if nivel != -1:
                    print(f"\n[ENCONTRADO] O elemento {val} está no nível {nivel} da árvore.)")

                    confirmar = input(f"Deseja remover o {val} agora? (S/N): ").lower()

                    if confirmar == 's':
                        arvore.remover_e_rebalancear(val)
                        print(f"Valor {val} removido com sucesso e árvore rebalanceada.")
                    else:
                        print("Remoção cancelada pelo usuário.")
                else:
                    print(f"\n[NAO ENCONTRADO] O elemento {val} NÃO está na árvore.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número inteiro.")
        elif opcao == "4":
            print("Abrindo janela gráfica... (Feche a janela para voltar ao menu)")
            viz.plotar()
        elif opcao == "5":
            print(f"Lista atual: {arvore.em_ordem()}")
        elif opcao == "0":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()