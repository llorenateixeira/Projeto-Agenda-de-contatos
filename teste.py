import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import os
import re

class Watcher:
    DIRECTORY_TO_WATCH = r"C://Users//Lorena.CSFDIGITAL//Documents//Teste"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        if not os.path.exists(self.DIRECTORY_TO_WATCH):
            print(f"Erro: O diretório {self.DIRECTORY_TO_WATCH} não existe.")
            return

        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        print(f"Observando o diretório: {self.DIRECTORY_TO_WATCH}")
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observador parado.")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        if event.is_directory:
            return None

        if event.src_path.endswith("2024_Informacoes_csf_centralizadas.v01.xlsx"):
            print(f'{event.src_path} foi modificado')
            update_html(event.src_path)

def update_html(file_path):
    sheet_name = 'CELULARES'

    if not os.path.exists(file_path):
        print(f"Erro: O arquivo {file_path} não existe.")
        return

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agenda de Contatos</title>
        <style>
          table {
            font-family: Arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        h2 {
            color: #333333;
            font-size: 24px;
            margin-bottom: 20px;
        }

        a {
            color: #007bff; 
            text-decoration: none; 
        }

        a:hover {
            text-decoration: underline; 
        }
        </style>
    </head>
    <body>

    <h2>Agenda de Contatos</h2>

    <table>
      <tr>
        <th>Filial</th>
        <th>Setor</th>
        <th>Nome</th>
        <th>Telefone</th> 
        <th>WhatsApp Link</th>
      </tr>
    '''

    for index, row in df.iterrows():
        phone_number =  str(int(row['DDD / LINHA'])) if pd.notna(row['DDD / LINHA']) else 'nan'
        html += f'''
        <tr>
            <td>{row['FILIAL']}</td>
            <td>{row['SETOR']}</td>
            <td>{row['USUARIO']}</td>
            <td>{phone_number}</td>
            <td><a href="https://wa.me/55{phone_number}">WhatsApp</a></td>
        </tr>
        '''

    html += '''
    </table>
    </body>
    </html>
    '''

    try:
        with open('C://Users//Lorena.CSFDIGITAL//Documents//Teste//agenda.html', 'w', encoding='utf-8') as file:
            file.write(html)
        print("Arquivo HTML atualizado com sucesso.")
    except Exception as e:
        print(f"Erro ao escrever o arquivo HTML: {e}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
