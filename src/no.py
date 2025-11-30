class No:
    """
    Nó da Árvore
    """
    def __init__(self, valor: int):
        self.valor = valor
        self.esquerda = 'No' | None = None
        self.direita = 'No' | None = None

    def __repr__(self):
        return f'No({self.valor})'