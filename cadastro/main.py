import tkinter as tk
from janela_principal import JanelaPrincipal
from janela_cadastro import JanelaCadastro
from janela_busca_cena import JanelaBuscaCena
from janela_busca_performers import JanelaBuscaPerformer
from PIL import Image, ImageTk
import os

root = tk.Tk()
app = JanelaPrincipal(root)
if os.name == 'nt':
    root.iconbitmap(True, './cover/icone.ico')
    
root.mainloop()
