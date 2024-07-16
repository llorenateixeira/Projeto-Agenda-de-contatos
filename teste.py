import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import os

class Watcher:
    DIRECTORY_TO_WATCH = r"C://Users//Lorena.CSFDIGITAL//Documents//Teste"
    FILE_TO_WATCH = "2024_Informacoes_csf_centralizadas.v01.xlsx"

    def __init__(self):
        self.observer = Observer()
        self.file_path = os.path.join(self.DIRECTORY_TO_WATCH, self.FILE_TO_WATCH)

    def run(self):
        if not os.path.exists(self.DIRECTORY_TO_WATCH):
            print(f"Erro: O diretório {self.DIRECTORY_TO_WATCH} não existe.")
            return
        
        if os.path.exists(self.file_path):
            update_html(self.file_path)
        else:
            print(f"Erro: O arquivo {self.file_path} não existe.")
        
        event_handler = Handler(self.file_path)
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
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.is_directory:
            return None
        if event.src_path == self.file_path:
            print(f'{event.src_path} foi modificado')
            update_html(self.file_path)

def format_phone_number(phone_number):
    """Formata o número de telefone no formato (XX) XXXXX-XXXX"""
    phone_number = str(phone_number)
    if len(phone_number) == 11:
        return f"({phone_number[:2]}) {phone_number[2:7]}-{phone_number[7:]}"
    return phone_number

def update_html(file_path):
    sheet_name = 'CELULARES'
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    html_header = '''
    <!DOCTYPE html>
    <html lang="pt-br"> 
    <head>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <title>Agenda de Contatos</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <img src="./logo_black.png" alt="Logo" class="d-inline-block align-text-top">
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
                    <form class="d-flex" role="search" onsubmit="return false;">
                        <input id="tableSearchInput" class="form-control me-2" type="search" placeholder="Buscar por nome" aria-label="Search">
                        <button type="button" class="btn btn-danger" onclick="searchTable()">Buscar</button>
                    </form>
                </div>
            </div>
        </nav>

        <div class="container mt-3">    
            <table class="table table-striped" id="contactTable">
                <thead>
                    <tr>
                        <th>Filial</th>
                        <th>Setor</th>
                        <th>Nome</th>
                        <th>Telefone</th> 
                        <th>WhatsApp Link</th>
                    </tr>
                </thead>
                <tbody>
    '''

    html_footer = '''
                </tbody>
            </table>
        </div>
        <script src="script.js"></script>
    </body>
    </html>
    '''

    html_content = ""
    for index, row in df.iterrows():
        phone_number = str(int(row['DDD / LINHA'])) if pd.notna(row['DDD / LINHA']) else 'nan'
        formatted_phone_number = format_phone_number(phone_number)
        whatsapp_link = f"https://wa.me/55{phone_number}" if phone_number.isdigit() else "#"
        html_content += f'''
                <tr>
                    <td>{row['FILIAL']}</td>
                    <td>{row['SETOR']}</td>
                    <td>{row['USUARIO']}</td>
                    <td>{formatted_phone_number}</td>
                    <td><a href="{whatsapp_link}">WhatsApp</a></td>
                </tr>
        '''

    full_html = html_header + html_content + html_footer

    output_path = os.path.join(os.path.dirname(file_path), 'agenda.html')
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(full_html)
        print("Arquivo HTML atualizado com sucesso em:", output_path)
    except Exception as e:
        print(f"Erro ao escrever o arquivo HTML: {e}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
