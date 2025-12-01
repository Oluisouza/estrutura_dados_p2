import tkinter as tk
from src.gui import StockInArvoreGUI


if __name__ == "__main__":
    try:
        root = tk.Tk()
        
        app = StockInArvoreGUI(root)
        
        root.mainloop()
    
    except KeyboardInterrupt:
        print("Aplicação encerrada.")