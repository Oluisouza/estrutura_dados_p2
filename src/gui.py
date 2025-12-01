import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

from src.arvore import ArvoreBinaria
from src.visualizadorGrafo import VisualizadorArvore


class StockInArvoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StockInArvore - Sistema de Logística com Árvore Binária de Busca")
        self.root.geometry("1000x600")

        self.arvore = ArvoreBinaria()

        self.viz = None

        self._configurar_layout()

        self.root.after(100, self.iniciar_arvore)

    def iniciar_arvore(self):
        """
        Fluxo inicial para decidir os dados.
        """
        dados = self._obter_dados_usuario()
        self.arvore.carregar_lote_balanceado(dados)
        self.viz = VisualizadorArvore(self.arvore)

        self.atualizar_grafico()
        self.log(f"Árvore iniciada com {len(dados)} elementos.")

    def _obter_dados_usuario(self):
        """
        Abre caixas de diálogo para o usuário escolher entra inserir os dados ou criar aleatórios.
        """
        resposta_aleatoria = messagebox.askyesno("Configuração Inicial", "Deseja gerar uma árvore com números ALEATÒRIOS?\n\n(Clique em 'Não' para digitar sua própria lista)")

        if resposta_aleatoria:
            return random.sample(range(1, 100), 25)
        else:
            entrada = tk.simpledialog.askstring(
                "Entrada de Dados",
                "Digite os números iniciais separados por vírgula: \n(Ex: 10, 50, 30, 90)"
                )

            if entrada and entrada.strip():
                try:
                    lista_user = [int(x.strip()) for x in entrada.split(',')]
                    return lista_user
                except ValueError:
                    messagebox.showerror("Erro", "Entrada inválida. Certifique-se de digitar apenas números inteiros separados por vírgula.")
                    
            return random.sample(range(1, 100), 25)

    def _configurar_layout(self):
        painel_esquerdo = tk.Frame(self.root, bg="#f0f0f0", width=250)
        painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(painel_esquerdo, text="Painel de Controle", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(painel_esquerdo, text="Valor (ID Produto):", bg="#f0f0f0").pack(pady=5)
        self.entrada_valor = tk.Entry(painel_esquerdo, font=("Arial", 12))
        self.entrada_valor.pack(pady=5, padx=10)

        self._criar_botao(painel_esquerdo, "Inserir (+)", self.acao_inserir, "#4CAF50")
        self._criar_botao(painel_esquerdo, "Remover (-)", self.acao_remover, "#F44336")
        self._criar_botao(painel_esquerdo, "Buscar e Deletar (?)", self.acao_buscar_e_deletar, "#2196F3")

        tk.Frame(painel_esquerdo, height=2, bg="#ccc").pack(fill=tk.X, pady=15, padx=10)

        self._criar_botao(painel_esquerdo, "Criar Nova Árvore", self.iniciar_arvore, "#FF9800")

        tk.Label(painel_esquerdo, text="Log do Sistema:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        self.log_text = tk.Text(painel_esquerdo, height=15, width=35, font=("Consolas", 9))
        self.log_text.pack(padx=10, pady=5)

        painel_direito = tk.Frame(self.root, bg="white")
        painel_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figura.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figura, master=painel_direito)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _criar_botao(self, pai, texto, comando, cor):
        btn = tk.Button(pai, text=texto, command=comando, bg=cor, fg="white", font=("Arial", 10, "bold"))
        btn.pack(fill=tk.X, padx=20, pady=5)

    def acao_inserir(self):
        try:
            val_str = self.entrada_valor.get()
            if not val_str: return
            val = int(val_str)

            self.arvore.inserir_e_rebalancear(val)
            self.log(f"Inserido: {val}")
            self.atualizar_grafico()
            self.entrada_valor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número inteiro.")

    def acao_remover(self):
        try:
            val_str = self.entrada_valor.get()
            if not val_str: return
            val = int(val_str)
            
            if self.arvore.remover_e_rebalancear(val):
                self.log(f"Removido: {val}")
                self.atualizar_grafico()
            else:
                self.log(f"Valor {val} não encontrado para remoção.")
                messagebox.showerror("Erro", f"Valor {val} não encontrado na árvore.")
            self.entrada_valor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número inteiro.")

    def acao_buscar_e_deletar(self):
        try:
            val_str = self.entrada_valor.get()
            if not val_str: return
            val = int(val_str)
            
            nivel = self.arvore.buscar_posicao(val)
            
            if nivel != -1:
                self.log(f"Encontrado: {val} (Nível {nivel})")
                resposta = messagebox.askyesno(
                    "Encontrado!",
                    f"O produto {val} está no nível {nivel}. \nDeseja removê-lo agora?"
                )
                if resposta:
                    self.arvore.remover_e_rebalancear(val)
                    self.log(f"-> {val} removido após busca.")
                    self.atualizar_grafico()
                else:
                    self.log(f"-> {val} mantido no estoque")
            else:
                self.log(f"Busca falhou: {val}")
                messagebox.showinfo("Resultado", f"Produto {val} não encontrado na árvore.")

            self.entrada_valor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Por favor, insira um número inteiro.")

    def acao_resetar(self):
        novos_dados = random.sample(range(1, 100), 25)
        self.arvore.carregar_lote_balanceado(novos_dados)
        self.log("Sistema resetado.")
        self.atualizar_grafico()

    def atualizar_grafico(self):
        if self.viz is None:
            return
        
        self.viz.plotar(ax=self.ax)
        self.canvas.draw()

    def log(self, mensagem):
        self.log_text.insert(tk.END, f"> {mensagem}\n")
        self.log_text.see(tk.END)