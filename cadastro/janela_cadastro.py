from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import filedialog


class JanelaCadastro:
    """Janela onde será feito a inserção de novos dados no banco de dados, aqui também tera uma capa, os campos para
    serem preenchidos pelos usuário, e o botão cadastrar"""
    def __init__(self, master):
        cover_cadastro = Image.open('./cover/adriana.JPG')
        cover_cadastro = cover_cadastro.resize((370, 484), Image.ANTIALIAS)
        cover_resized = ImageTk.PhotoImage(cover_cadastro)
        self.__master = master
        self.__master.resizable(FALSE, FALSE)
        self.__frame = Frame(master).pack()
        self.__master.geometry('820x480')
        self.__master.title('Janela de Cadastro')
        self.__cover = cover_resized
        self.label_cover()
        self.__imagem_binaria = None
        self.__name = Label(self.__master, text='Name*', font=20)
        self.__name.pack(pady=30)
        self.__entrada_nome = Entry(self.__master, width=30, font=15)
        self.__entrada_nome.pack()
        self.__nationality = Label(self.__master, text='Nationality*', font=20)
        self.__nationality.pack(pady=30)
        self.__entrada_nationality = Entry(self.__master, width=20, font=15)
        self.__entrada_nationality.pack()
        self.__ethnicity = Label(self.__master, text='Ethnicity*', font=20)
        self.__ethnicity.pack(pady=30)
        self.__entrada_ethnicity = Entry(self.__master, width=20, font=15)
        self.__entrada_ethnicity.pack()
        self.__explorer = None
        self.botao_buscar_imagem()
        self.botao_cadastrar()

    def label_cover(self):
        """Configuração da capa da janela"""
        capa = Label(self.__master, image=self.__cover)
        capa.image = self.__cover
        capa.pack(side=LEFT)

    def buscar_imagem(self):
        """Abre o explorer em busca da imagem que será convertida e inserida no bando de dados"""
        imagem_escolhida = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                      filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.__explorer = rf'{imagem_escolhida}'
        print(f'Imagem selecionada: {self.__explorer}')

    def botao_buscar_imagem(self):
        botao_busca = Button(self.__master, text='Buscar Imagem', width=20)
        botao_busca['command'] = lambda: self.buscar_imagem()
        botao_busca.pack(pady=30)

    def conversor(self, arquivo):
        """Corversor de arquivos para binário"""
        with open(arquivo, 'rb') as file:
            self.__imagem_binaria = file.read()
            return self.__imagem_binaria

    def cadastrar(self):
        """Função quer irá inserir os dados coletados no banco de dados"""
        try:
            conn = sqlite3.connect('./data/goddesses.db')
            mycursor = conn.cursor()

            sql = """INSERT INTO tab_performers (name_performer, ethnicity, nationality, picture)
            VALUES (?, ?, ?, ?)"""

            nome = self.__entrada_nome.get().title()
            ethnicity = self.__entrada_ethnicity.get().title()
            nationality = self.__entrada_nationality.get().title()
            picture = self.conversor(self.__explorer)

            tupla_dados = (nome, ethnicity, nationality, picture)

            mycursor.execute(sql, tupla_dados)
            print('Dados inseridos com sucesso!')

            conn.commit()
            mycursor.close()
            conn.close()

            self.__entrada_nome.delete(0, 'end')
            self.__entrada_ethnicity.delete(0, 'end')
            self.__entrada_nationality.delete(0, 'end')

        except EXCEPTION as err:
            print(err)

    def botao_cadastrar(self):
        """Botão que invocará a função de cadastro no banco de dados"""
        botao_cadasto = Button(self.__master, text='CADASTRAR', width=20)
        botao_cadasto['command'] = lambda: self.cadastrar()
        botao_cadasto.pack()
        self.__master.bind('<Return>', lambda event=None: botao_cadasto.invoke())


if __name__ == '__main__':
    print('Este módulo não deve ser executado separadamente!')
