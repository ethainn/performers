from tkinter import *
import sqlite3
from PIL import Image, ImageTk
import io


class JanelaBuscaPerformer:

    def __init__(self, master):
        # capa
        cover_busca = Image.open('./cover/saffron_bacchus.jpg')
        cover_busca = cover_busca.resize((484, 484), Image.ANTIALIAS)
        cover_resized = ImageTk.PhotoImage(cover_busca)

        self.__master = master
        self.__master.title('Buscar Performer')
        self.__master.resizable(FALSE, FALSE)

        # self.__master.geometry('500x485')
        self.__cover = cover_resized
        self.label_cover()
        self.label_name()
        self.label_nacionality()
        self.label_ethnicity()
        # entrada de dados
        self.__name_entry = Entry(self.__master, width=20)
        self.__name_entry.grid(row=1, column=0, padx=20)
        self.__natio_entry = Entry(self.__master, width=20)
        self.__natio_entry.grid(row=1, column=1, padx=10)
        self.__ethnicity_entry = Entry(self.__master, width=20)
        self.__ethnicity_entry.grid(row=1, column=2, padx=20)

        self.botao_buscar()
        self.botao_limpar_registros()
        self.label_resultados()

        # Related to the list box
        self.__frame = Frame(self.__master)
        self.__scrollbar = Scrollbar(self.__frame, orient=VERTICAL)
        self.__listbox = Listbox(self.__frame, width=50, height=7, yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.config(command=self.__listbox.yview)
        self.__scrollbar.pack(side=RIGHT, fill=Y)
        self.__frame.grid(row=5, rowspan=4, column=0, columnspan=4, pady=10)
        self.__listbox.pack(pady=20)

        self.botao_abrir_imagem()
        self.botao_info()
        self.__label_info = Label(self.__master, text='')
        self.__label_info.grid(row=12, column=0, columnspan=3, pady=10)

    def label_cover(self):
        """Configuração da capa da janela"""
        capa = Label(self.__master, image=self.__cover)
        capa.image = self.__cover
        capa.grid(row=0, column=3, rowspan=15, columnspan=15)

    def label_name(self):
        nome_performer = Label(self.__master, text='Name')
        nome_performer.grid(row=0, column=0, pady=10, padx=20)

    def label_nacionality(self):
        nationatily_performer = Label(self.__master, text='Nationality')
        nationatily_performer.grid(row=0, column=1, pady=10, padx=20)

    def label_ethnicity(self):
        ethnicity_performer = Label(self.__master, text='Ethnicity')
        ethnicity_performer.grid(row=0, column=2, pady=10, padx=20)

    def botao_buscar(self):
        # botão que exeutará a funcao de buscar dados no banco de dados
        botao_de_busca = Button(self.__master, text='Buscar', width=15)
        botao_de_busca['command'] = lambda: self.buscar_dados_no_banco()
        botao_de_busca.grid(row=2, column=0, pady=20, padx=10)

    def botao_limpar_registros(self):
        botao_limpar_reg = Button(self.__master, text='Limpar Busca', width=15)
        botao_limpar_reg['command'] = lambda: self.limpar_busca()
        botao_limpar_reg.grid(row=2, column=2, pady=20, padx=10)

    def label_resultados(self):
        resultado_busca = Label(self.__master, text='RESULTADO DA BUSCA')
        resultado_busca.grid(row=3, rowspan=2, column=1, pady=10)

    def botao_abrir_imagem(self):
        abrir_imagem = Button(self.__master, width=20, text='Visualizar Foto')
        abrir_imagem['command'] = lambda: self.abrir_imagem()
        abrir_imagem.grid(row=10, column=1, pady=10)

    def botao_info(self):
        # botao para visualizar detalhes da performer selecionada
        info = Button(self.__master, text='Detalhes', width=20)
        info['command'] = lambda: self.mostrar_detalhes()
        info.grid(row=11, column=1, pady=10)

    def buscar_dados_no_banco(self):
        # Busca no banco de dados de acordo com as dados fornecidos
        self.limpar_busca()
        self.limpar_detalhes()

        try:
            conn = sqlite3.connect('./data/goddesses.db')
            my_cursor = conn.cursor()

            sql = """SELECT * FROM tab_performers 
            WHERE name_performer LIKE (?) AND nationality LIKE (?) AND ethnicity LIKE (?)"""

            name = self.__name_entry.get()
            nationality = self.__natio_entry.get()
            ethnicity = self.__ethnicity_entry.get()

            nome_busca = '%' + name + '%'
            naciolidade_busca = '%' + nationality + '%'
            etnia_busca = '%' + ethnicity + '%'

            tupla_dados = (nome_busca, naciolidade_busca, etnia_busca)

            my_cursor.execute(sql, tupla_dados)

            dados = my_cursor.fetchall()

            for dado in range(len(dados)):
                self.__listbox.insert(END, dados[dado][1])

            self.__label_info['text'] = f'{len(dados)} resultado(s) retornado(s)'

            my_cursor.close()
            conn.close()

            self.__name_entry.delete(0, END)
            self.__ethnicity_entry.delete(0, END)
            self.__natio_entry.delete(0, END)

        except Exception as err:
            print(err)

    def limpar_busca(self):
        # limpa a lista de busca
        self.__listbox.delete(0, END)
        self.limpar_detalhes()

    def limpar_detalhes(self):
        # limpa os detalhes da performer
        self.__label_info['text'] = ''

    def abrir_imagem(self):
        # abre a imagem da performer selecionada apos a busca
        try:
            nome_foto = self.__listbox.get(ANCHOR)
            conn = sqlite3.connect('./data/goddesses.db')
            my_cursor = conn.cursor()
            sql = """SELECT picture FROM tab_performers WHERE name_performer = (?)"""

            nome = nome_foto,
            my_cursor.execute(sql, nome)

            dados = my_cursor.fetchall()
            image = io.BytesIO(dados[0][0])
            foto = Image.open(image)
            foto.show()

            my_cursor.close()
            conn.close()

        except Exception as err2:
            print(err2)

    def mostrar_detalhes(self):
        # mostra detalhes da performer selecionada
        try:
            nome_detalhe = self.__listbox.get(ANCHOR)
            conn = sqlite3.connect('./data/goddesses.db')
            my_cursor = conn.cursor()

            sql = """SELECT * FROM tab_performers WHERE name_performer = (?)"""

            nome = nome_detalhe,
            my_cursor.execute(sql, nome)

            dados = my_cursor.fetchall()

            texto = f'ID: {str(dados[0][0])}, Nome: {dados[0][1]}, Etnia: {dados[0][2]}, Nacionalidade: {dados[0][3]}'

            self.__label_info['text'] = texto

            my_cursor.close()
            conn.close()

        except TypeError:
            self.__label_info['text'] = 'Selecione algum registro para ver detalhes'

        except IndexError:
            self.__label_info['text'] = 'Selecione algum registro para ver detalhes'


if __name__ == '__main__':
    print('Este módulo não deve ser executado separadamente.')
