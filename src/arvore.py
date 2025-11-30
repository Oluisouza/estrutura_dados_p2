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
        
    def _em_ordem_recursivo(self, no: No, lista: list):
        if no:
            self._em_ordem_recursivo(no.esquerda, lista)
            lista.append(no.valor)
            self._em_ordem_recursivo(no.direita, lista)