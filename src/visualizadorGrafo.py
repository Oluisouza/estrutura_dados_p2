import matplotlib.pyplot as plt
import networkx as nx
from src.arvore import ArvoreBinaria, No

class VisualizadorArvore:
    def __init__(self, arvore: ArvoreBinaria):
        self.arvore = arvore

    def plotar(self):
        if not self.arvore.raiz:
            print("Árvore vazia, nada para plotar.")
            return
        
        G = nx.DiGraph()

        self._adicionar_nos_arestas(self.arvore.raiz, G)

        pos = self._posicao_hierarquica(self.arvore.raiz)

        plt.figure(figsize=(10, 6))
        plt.title("Visualização da Árvore Binária de Busca")

        nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue", edgecolors="black")

        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=20)

        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

        plt.axis("off")
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