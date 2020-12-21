from tkinter import *
from PIL import Image, ImageTk
from janela_busca_performers import JanelaBuscaPerformer
from janela_cadastro import JanelaCadastro
from janela_busca_cena import JanelaBuscaCena


class JanelaPrincipal:
    """Janela inicial da aplicação, nela estará a capa com uma imagem, os botões 'CADASTRAR NOVA MODELO',
     'BUSCAR MODELO' e CANCELAR"""
    def __init__(self, master):
        cover_principal = ImageTk.PhotoImage(Image.open('./cover/janice1.jpg'))
        self.__master = master
        self.__frame = Frame(master).pack()
        self.__master.resizable(FALSE, FALSE)
        self.__master.geometry('1050x450+200+200')
        self.__master.title('Janela Principal')
        self.__new = None
        self.__cover = cover_principal
        self.label_cover()
        self.botao_nova_modelo(JanelaCadastro)
        self.botao_buscar_model(JanelaBuscaPerformer)
        self.botao_buscar_cena(JanelaBuscaCena)
        self.botao_fechar()

    def label_cover(self):
        """Configuração da imagem que será exibida na janela inicial"""
        capa = Label(self.__master, image=self.__cover)
        capa.image = self.__cover
        capa.pack(side=LEFT)

    def new_window(self, _class):
        """Função que inicia uma nova instância/janela"""
        self.__new = Toplevel(self.__master)
        _class(self.__new)

    def botao_nova_modelo(self, _class):
        """Abre a janela de cadastro"""
        nova = Button(self.__master, text='CADASTRAR MODELO', width=20, height=3)
        nova['command'] = lambda: self.new_window(_class)
        nova.pack(pady=20)

    def botao_buscar_model(self, _class):
        """Abre a janela de busca"""
        busca = Button(self.__master, text='BUSCAR MODELO', width=20)
        busca['command'] = lambda: self.new_window(_class)
        busca.pack(pady=20)

    def botao_buscar_cena(self, _class):
        """Abre a jenela de busca de cenas"""
        busca_cena = Button(self.__master, text='BUSCAR CENA', width=20)
        busca_cena['command'] = lambda: self.new_window(_class)
        busca_cena.pack(pady=20)

    def botao_fechar(self):
        """Fecha a janela inicial"""
        fechar = Button(self.__master, text='Close', width=20)
        fechar['command'] = lambda: self.__master.destroy()
        fechar.pack(side=BOTTOM, pady=20)


if __name__ == '__main__':
    print('Este módulo não deve ser executado separadamente!')
