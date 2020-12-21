import sqlite3
from PIL import Image
import io


def busca_registros_performers(performer):

    try:
        conn = sqlite3.connect('./data/goddesses.db')
        mycursor = conn.cursor()

        sql = """SELECT * FROM tab_performers WHERE name_performer LIKE (?)"""

        tupla_dados = '%' + performer + '%',

        mycursor.execute(sql, tupla_dados)

        dados = mycursor.fetchall()
        print('-----------------------------------------------------')
        with open('busca.txt', 'w') as file:
            for dado in range(len(dados)):
                texto = (f'ID: {str(dados[dado][0])}, Nome: {dados[dado][1]}, '
                         f'Etnia: {dados[dado][2]}, Nacionalidade: {dados[dado][3]}')
                print(texto)
                file.write(texto + '\n')

        if len(dados) == 1:
            print('------------------------------------------------------')
            resp = input('Se deseja visualizar imagem aperte "s" e então ENTER: ')
            if resp == 'S' or resp == 's':
                imagem_binaria = io.BytesIO(dados[0][4])
                imagem = Image.open(imagem_binaria)
                imagem.show()

        conn.commit()
        mycursor.close()
        conn.close()

    except Exception as err:
        print(err)

    finally:
        print('-----------------------------------------------------')
        print(f'Busca finalizada, {len(dados)} registros retornados.')


def busca_scena_performer(performer):

    try:
        conn = sqlite3.connect('./data/goddesses.db')

        mycursor = conn.cursor()

        sql = """SELECT p.name_performer, s.title, s.studio, s.style, s.len, s.folder
                FROM tab_performers as p, tab_scene as s, tab_scene_performer as sp
                WHERE p.name_performer LIKE (?) AND p.id_performer = sp.performer AND s.id_scene = sp.scene"""

        tupla_dado = '%' + performer + '%',

        mycursor.execute(sql, tupla_dado)

        dados = mycursor.fetchall()

        with open('busca.txt', 'w') as file:

            print('Performer  -  Scene  -  Studio  -  Style  -  Lenght  -  Folder')
            print('--------------------------------------------------------------')
            for dado in range(len(dados)):
                texto = f'{dados[dado][0]}, {dados[dado][1]}, {dados[dado][2]}, {dados[dado][3]}, ' \
                        f'{dados[dado][4]}, {dados[dado][5]}'
                print(texto)
                file.write(texto + '\n')

        print('--------------------------------------------------------------')
        print(f'Busca finalizada, {len(dados)} resultado(s) foram retornados.')

    except Exception as err:
        print(err)


entrada = None

while entrada != 'SAIR':
    entrada = input('Performer [P]\nScene[S]\n[Sair]: ').upper()
    if entrada != 'SAIR':
        if entrada == 'P':
            nome = input('Informe o nome para busca: ')
            busca_registros_performers(nome)
        if entrada == 'S':
            nome = input('Informe o nome da Performer para busca: ')
            busca_scena_performer(nome)
