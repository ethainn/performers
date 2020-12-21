from tkinter import *
import io
import sqlite3
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from random import choice


class JanelaBuscaCena:

    def __init__(self, master):

        self.__master = master
        self.__master.title('Buscar Cena')
        self.__master.geometry('1280x720')
        self.__master.resizable(FALSE, FALSE)
        self.__master['bg'] = 'white'

        self.__conexao = None
        self.__cursor = None

        # Frame da capa
        self.__moldura_capa = LabelFrame(self.__master, text=' Hey there ', bg='white')
        self.__moldura_capa.pack(side=RIGHT, pady=10, padx=10, fill=BOTH, expand=YES)

        # Frame da caixa de resultados
        self.__resultados = LabelFrame(self.__master, text=' Resultados ', bg='white')
        self.__resultados.pack(pady=10, padx=10, fill=BOTH, expand=YES)

        # Frame com as entradas e botões de busca
        self.__campos_de_busca = LabelFrame(self.__master, text=' Dados da Cena ', bg='white')
        self.__campos_de_busca.pack(pady=10, padx=10, fill=BOTH, expand=YES)

        self.__label_nome = Label(self.__campos_de_busca, text='Name:', bg='white')
        self.__label_nome.grid(row=0, column=0, padx=10, pady=10)
        self.__entrada_nome = Entry(self.__campos_de_busca, width=30, relief='solid')
        self.__entrada_nome.grid(row=0, column=1, pady=10)

        self.__label_scene = Label(self.__campos_de_busca, text='Scene:', bg='white')
        self.__label_scene.grid(row=1, column=0, pady=10, padx=10)
        self.__entrada_scene = Entry(self.__campos_de_busca, width=30, relief='solid')
        self.__entrada_scene.grid(row=1, column=1, pady=10)

        self.__label_studio = Label(self.__campos_de_busca, text='Studio:', bg='white')
        self.__label_studio.grid(row=2, column=0, pady=10, padx=10)
        self.__entrada_studio = Entry(self.__campos_de_busca, width=30, relief='solid')
        self.__entrada_studio.grid(row=2, column=1, pady=10)

        self.__label_style = Label(self.__campos_de_busca, text='Style:', bg='white')
        self.__label_style.grid(row=3, column=0, pady=10, padx=10)
        self.__entrada_style = Entry(self.__campos_de_busca, width=30, relief='solid')
        self.__entrada_style.grid(row=3, column=1, pady=10)

        self.__botao_buscar = Button(self.__campos_de_busca, width=20, height=3, bg='orange', text='BUSCAR')
        self.__botao_buscar['command'] = self.buscar_dados_no_banco
        self.__botao_buscar.grid(row=4, column=1, pady=20)

        self.__botao_limpar_registros = Button(self.__campos_de_busca,
                                               text='LIMPAR', width=20, height=3, bg='black', fg='white')
        self.__botao_limpar_registros['command'] = self.limpar_dados_da_lista
        self.__botao_limpar_registros.place(rely=0.2, relx=0.5)

        self.__botao_abrir_imagem = Button(self.__campos_de_busca,
                                           width=20, height=3, text='VISUALIZAR MODELO', bg='#B87333')
        self.__botao_abrir_imagem['command'] = self.abrir_imagem
        self.__botao_abrir_imagem.place(rely=0.5, relx=0.5)

        # Montagem da Treeview para os dados
        self.__scrollbar = Scrollbar(self.__resultados, orient=VERTICAL)
        self.__caixa_resultados = ttk.Treeview(self.__resultados,
                                               columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'),
                                               show='headings', height='15', yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.config(command=self.__caixa_resultados.yview)
        self.__scrollbar.pack(side=RIGHT, fill=Y)
        self.caixa_de_resultados()
        self.__caixa_resultados.pack(padx=10, pady=10)

        self.__label_contador = Label(self.__resultados, text='', bg='white')
        self.__label_contador.pack(pady=10)

        # Definição da capa
        self.__escolha = choice(['skin.jpg', 'arya.jpeg'])
        self.__capa = Image.open(f'./cover/{self.__escolha}')
        self.__capa = self.__capa.resize((466, 700), Image.ANTIALIAS)
        self.__capa_completa = ImageTk.PhotoImage(self.__capa)
        self.__label_capa = Label(self.__moldura_capa, image=self.__capa_completa)
        self.__label_capa.pack(fill=BOTH, expand=YES)

    def caixa_de_resultados(self):
        # Definindo os cabeçalhos
        self.__caixa_resultados.heading('#0', text='')
        self.__caixa_resultados.heading('#1', text='Performer')
        self.__caixa_resultados.heading('#2', text='Scene')
        self.__caixa_resultados.heading('#3', text='Studio')
        self.__caixa_resultados.heading('#4', text='Style')
        self.__caixa_resultados.heading('#5', text='Length')
        self.__caixa_resultados.heading('#6', text='Folder')

        # Definindo os tamanhos das colunas
        self.__caixa_resultados.column('#0', width=1)
        self.__caixa_resultados.column('#1', width=110)
        self.__caixa_resultados.column('#2', width=250)
        self.__caixa_resultados.column('#3', width=150)
        self.__caixa_resultados.column('#4', width=90)
        self.__caixa_resultados.column('#5', width=70)
        self.__caixa_resultados.column('#6', width=50)

    def atualizar_dados_da_lista(self, dados):
        # Função que irá adicionar os dados do campo de resultados
        for i in dados:
            self.__caixa_resultados.insert('', END, values=i)
        self.__label_contador['text'] = f'{len(dados)} registros foram retornados'

    def limpar_dados_da_lista(self):
        self.__caixa_resultados.delete(*self.__caixa_resultados.get_children())

    def abrir_imagem(self):

        try:
            cur_item = self.__caixa_resultados.focus()  # a função focus pega o registro que esta selecionado

        # a função item gera um dicionario do registro selecionado, como os valores selecionados estão na chave 'values'
        # utilizanmos a mesma com o índice desejado, neste caso o índice 0 para pegar o nome.
            modelo = self.__caixa_resultados.item(cur_item)['values'][0]

            self.abrir_conexao_db()
            sql = """SELECT picture FROM tab_performers WHERE name_performer = (?)"""

            nome = modelo,
            self.__cursor.execute(sql, nome)

            dados = self.__cursor.fetchall()
            image = io.BytesIO(dados[0][0])
            foto = Image.open(image)
            foto.show()
            self.fechar_conexao_db()

        except IndexError:
            messagebox.showinfo(title='Se liga', message='Selecione algum registro antes')

    def abrir_conexao_db(self):
        # Estabelece conexao com o banco de dados
        self.__conexao = sqlite3.connect('./data/goddesses.db')
        self.__cursor = self.__conexao.cursor()

    def fechar_conexao_db(self):
        # Fecha a conexao do banco de dados
        self.__cursor.close()
        self.__conexao.close()

    def buscar_dados_no_banco(self):
        self.limpar_dados_da_lista()
        self.abrir_conexao_db()

        nome = self.__entrada_nome.get()
        nome_busca = '%' + nome + '%'
        scene = self.__entrada_scene.get()
        scene_busca = '%' + scene + '%'
        studio = self.__entrada_studio.get()
        studio_busca = '%' + studio + '%'
        style = self.__entrada_style.get()
        style_busca = '%' + style + '%'

        self.__cursor.execute("""SELECT p.name_performer, s.title, s.studio, s.style, s.len, s.folder
                    FROM tab_performers as p, tab_scene as s, tab_scene_performer as sp
                    WHERE p.name_performer LIKE (?) AND s.title LIKE (?) AND s.studio LIKE (?) AND s.style LIKE (?)
                    AND p.id_performer = sp.performer AND s.id_scene = sp.scene
                    ORDER BY p.name_performer ASC""", (nome_busca, scene_busca, studio_busca, style_busca))

        dados = self.__cursor.fetchall()

        self.atualizar_dados_da_lista(dados)

        self.__entrada_nome.delete(0, END)
        self.__entrada_scene.delete(0, END)
        self.__entrada_studio.delete(0, END)
        self.__entrada_style.delete(0, END)

        self.fechar_conexao_db()


if __name__ == '__main__':
    print('Este módulo não deve ser executado separadamente!')
