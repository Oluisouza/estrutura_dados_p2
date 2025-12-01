import matplotlib.pyplot as plt
import networkx as nx
from src.arvore import ArvoreBinaria, No

class VisualizadorArvore:
    def __init__(self, arvore: ArvoreBinaria):
        self.arvore = arvore

    def plotar(self, ax=None):
        """
        Plota a árvore.
        Se 'ax' for fornecido, desenha o grafo dentro desse eixo.
        Se 'ax' for None, cria uma nova janela.
        """
        if ax is None:
            plt.figure(figsize=(10, 6))
            ax = plt.gca()
            mostrar_janela = True
        else:
            ax.clear()
            mostrar_janela = False

        if not self.arvore.raiz:
            print("Árvore vazia, nada para plotar.")
            ax.text(0.5, 0.5, 'Árvore Vazia', ha='center', va='center', fontsize=14)
            if mostrar_janela:
                plt.show()
            return
        
        G = nx.DiGraph()

        self._adicionar_nos_arestas(self.arvore.raiz, G)

        pos = self._posicao_hierarquica(self.arvore.raiz)

        nx.draw_networkx_nodes(G, pos, node_size=600, node_color="#87CEEB", edgecolors="black", ax=ax)

        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=15, ax=ax)

        nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)

        ax.axis('off')

        if mostrar_janela:
            plt.show()

    def _adicionar_nos_arestas(self, no: No, G: nx.DiGraph):
        if no is None:
            return
        
        G.add_node(no.valor)

        if no.esquerda:
            G.add_edge(no.valor, no.esquerda.valor)
            self._adicionar_nos_arestas(no.esquerda, G)

        if no.direita:
            G.add_edge(no.valor, no.direita.valor)
            self._adicionar_nos_arestas(no.direita, G)

    def _posicao_hierarquica(self, raiz, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        """
        Calcula as coordenadas (x, y) de cada nó para ficarem organizados como uma arvore
        """
        pos = {raiz.valor: (xcenter, vert_loc)}

        def _processar(no, curr_x, curr_y, curr_width):
            if no.esquerda:
                pos[no.esquerda.valor] = (curr_x - curr_width / 2, curr_y - vert_gap)
                _processar(no.esquerda, curr_x - curr_width / 2, curr_y - vert_gap, curr_width / 2)
            
            if no.direita:
                pos[no.direita.valor] = (curr_x + curr_width / 2, curr_y - vert_gap)
                _processar(no.direita, curr_x + curr_width / 2, curr_y - vert_gap, curr_width / 2)

        if raiz:
            _processar(raiz, xcenter, vert_loc, width/2)
        
        return pos