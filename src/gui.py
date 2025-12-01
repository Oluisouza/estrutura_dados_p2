import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

from src.arvore import ArvoreBinaria
from src.visualizadorGrafo import VisualizadorArvore

CORES = {
    "bg_sidebar": "#2C3E50",     
    "fg_sidebar": "#ECF0F1",     
    "bg_main":    "#FFFFFF",     
    "btn_add":    "#27AE60",     
    "btn_del":    "#C0392B",     
    "btn_find":   "#2980B9",     
    "btn_new":    "#F39C12",     
    "log_bg":     "#34495E",     
    "log_fg":     "#BDC3C7"      
}

FONTE_TITULO = ("Segoe UI", 16, "bold")
FONTE_TEXTO = ("Segoe UI", 11)
FONTE_BTN = ("Segoe UI", 10, "bold")

class StockInArvoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StockInArvore - Sistema de Logística com Árvore Binária de Busca")
        self.root.geometry("1000x600")

        self.root.configure(bg=CORES["bg_main"])

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
        resposta_aleatoria = messagebox.askyesno(
            "Boas Vindas", 
            "Deseja gerar uma árvore com números ALEATÒRIOS?\n\n(Clique em 'Não' para digitar sua própria lista)"
            )

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
        painel_esquerdo = tk.Frame(self.root, bg=CORES["bg_sidebar"], width=300)
        painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y)

        painel_esquerdo.pack_propagate(False)

        lbl_titulo = tk.Label(
            painel_esquerdo,
            text="Painel de Controle",
            font=FONTE_TITULO,
            bg=CORES["bg_sidebar"],
            fg=CORES["fg_sidebar"]
        )
        lbl_titulo.pack(pady=(30, 20))

        frame_input = tk.Frame(painel_esquerdo, bg=CORES["bg_sidebar"])
        frame_input.pack(fill=tk.X, padx=20)

        tk.Label(frame_input, text="Valor (ID Produto):",font=FONTE_TEXTO, bg=CORES["bg_sidebar"], fg=CORES["fg_sidebar"]).pack(anchor="w")
        
        self.entrada_valor = tk.Entry(
            frame_input,
            font=("Segoe UI", 14),
            bd=0,
            highlightthickness=2,
            highlightbackground="#95a5a6",
            highlightcolor=CORES["btn_find"],
            justify="center")
        self.entrada_valor.pack(fill=tk.X, pady=5, ipady=5)

        tk.Frame(painel_esquerdo, height=1, bg="#7f8c8d").pack(fill=tk.X, padx=20, pady=20)

        self._criar_botao(painel_esquerdo, "✚ Inserir", self.acao_inserir, CORES["btn_add"])
        self._criar_botao(painel_esquerdo, "✖ Remover", self.acao_remover, CORES["btn_del"])
        self._criar_botao(painel_esquerdo, "🔍 Buscar e Deletar", self.acao_buscar_e_deletar, CORES["btn_find"])

        tk.Frame(painel_esquerdo, height=1, bg="#7f8c8d").pack(fill=tk.X, pady=20, padx=20)

        self._criar_botao(painel_esquerdo, "↻ Criar Nova Árvore", self.iniciar_arvore, CORES["btn_new"])

        tk.Label(
            painel_esquerdo,
            text="Log do Sistema:",
            font=("Segoe UI", 9, "bold"),
            bg=CORES["bg_sidebar"],
            fg="#95a5a6").pack(anchor="w", padx=20, pady=(30, 5))
        
        self.log_text = tk.Text(
            painel_esquerdo,
            height=10,
            bg=CORES["log_bg"], 
            fg=CORES["log_fg"],
            font=("Consolas", 9),
            bd=0,
            padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        painel_direito = tk.Frame(self.root, bg=CORES["bg_main"])
        painel_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.figura.patch.set_facecolor(CORES["bg_main"])
        self.ax = self.figura.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figura, master=painel_direito)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(
            painel_direito,
            text="Desenvolvido para o curso de Engenharia de Software - Estrutura de Dados",
            bg=CORES["bg_main"],
            fg="#7f8c8d",
            font=("Segoe UI", 8)
        ).pack(side=tk.BOTTOM, pady=10)

    def _criar_botao(self, pai, texto, comando, cor):
        container = tk.Frame(pai, bg=CORES["bg_sidebar"])
        container.pack(fill=tk.X, padx=20, pady=6)
        
        btn = tk.Button(
            container,
            text=texto,
            command=comando, bg=cor,
            fg="white", 
            font=FONTE_BTN,
            relief="flat",
            cursor="hand2",
            activebackground="white",
            activeforeground=cor,
            bd=0)
        btn.pack(fill=tk.X, ipady=5)

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