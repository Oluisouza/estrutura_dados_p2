from src.no import No

class ArvoreBinaria:
    """
    Árvore Binária de Busca
    """
    def __init__(self):
        self.raiz: No | None = None

    def inserir(self, valor: int) -> None:
        """
        Insere um valor na árvore
        """
        if not self.raiz:
            self.raiz = No(valor)
        else:
            self._inserir_recursivo(self.raiz, valor)

    def _inserir_recursivo(self, no_atual: No, valor: int) -> None:
        if valor < no_atual.valor:
            if no_atual.esquerda is None:
                no_atual.esquerda = No(valor)
            else:
                self._inserir_recursivo(no_atual.esquerda, valor)
        elif valor > no_atual.valor:
            if no_atual.direita is None:
                no_atual.direita = No(valor)
            else:
                self._inserir_recursivo(no_atual.direita, valor)
        else:
            print(f"Produto {valor} já cadastrado no estoque.")

    def buscar(self, valor: int) -> bool:
        """
        Busca um valor na árvore, retorna True se o valor Existe, retorna False caso contrário.
        """
        return self._buscar_recursivo(self.raiz, valor)
    

    def _buscar_recursivo(self, no_atual: No, valor: int) -> bool:
        if no_atual is None:
            return False
        
        if valor == no_atual.valor:
            return True
        elif valor < no_atual.valor:
            return self._buscar_recursivo(no_atual.esquerda, valor)
        else:
            return self._buscar_recursivo(no_atual.direita, valor)

    def buscar_posicao(self, valor: int) -> int:
        """
        Retorna o Nível do nó (Profundidade).
        Raiz = 0, Filhos da Raiz = 1, etc.
        Retorna -1 se não encontrar.
        """
        return self._buscar_posicao_rec(self.raiz, valor, nivel=0)
    
    def _buscar_posicao_rec(self, no: No, valor: int, nivel: int) -> int:
        if no is None:
            return -1
        
        if valor == no.valor:
            return nivel
        elif valor < no.valor:
            return self._buscar_posicao_rec(no.esquerda, valor, nivel + 1)
        else:
            return self._buscar_posicao_rec(no.direita, valor, nivel + 1)

    def em_ordem(self) -> list:
        """
        Retorna uma lista com os valores da árvore em ordem 
        """
        elementos = []
        self._em_ordem_recursivo(self.raiz, elementos)
        return elementos

    def _em_ordem_recursivo(self, no: No, lista: list):
        if no:
            self._em_ordem_recursivo(no.esquerda, lista)
            lista.append(no.valor)
            self._em_ordem_recursivo(no.direita, lista)



    def carregar_lote_balanceado(self, lista_numeros: list[int]):
        """
        recebe a lista, ordena e constroi a árvore de forma balanceada.
        """

        lista_ordenada = sorted(list(set(lista_numeros)))

        self.raiz = None

        self.construir_balanceada(lista_ordenada)


    def remover_e_rebalancear(self, valor: int) -> bool:
        """
        Remove um valor da árvore e rebalanceia a árvore
        Retorna True se o valor foi removido, False caso contrário
        """
        if not self.buscar(valor):
            return False
        
        lista_atual = self.em_ordem()
        lista_atual.remove(valor)

        self.carregar_lote_balanceado(lista_atual)
        return True
    
    def inserir_e_rebalancear(self, valor: int):
        """
        Insere um valor na árvore e rebalanceia a árvore
        """
        lista_atual = self.em_ordem()
        lista_atual.append(valor)

        self.carregar_lote_balanceado(lista_atual)

    def construir_balanceada(self, lista_ordenada: list[int]):
        """
        Constrói uma árvore balanceada a partir de uma lista ordenada
        """
        if not lista_ordenada:
            return 
        
        meio = len(lista_ordenada) // 2
        valor_meio = lista_ordenada[meio]

        self.inserir(valor_meio)

        self.construir_balanceada(lista_ordenada[:meio])
        self.construir_balanceada(lista_ordenada[meio + 1:])