from flask import Flask, request, render_template, send_file, redirect, flash, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import datetime
import magic
from flask_mail import Mail, Message



app = Flask(__name__)
mail=Mail(app)
app.secret_key = '123456789'

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'Glocheck@outlook.com'
app.config['MAIL_PASSWORD'] = 'Glosa1234'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)
# caminho da pasta na hospedagem
# UPLOAD_FOLDER = '/home/Rasantis/mysite/repositorio'
# UPLOAD_FOLDER = 'repositorio' #Caminho máquina local
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'repositorio')


# Definindo a lista de usuarios e senhas validos
users = [
    {"username": "admin", "password": "1234", "is_admin": True},
    {"username": "user1", "password": "abcd", "is_admin": False},
    {"username": "user2", "password": "efgh", "is_admin": False},
]

# Rota para exibir o formulario de login


@app.route("/login", methods=["GET"])
def login_form():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login_submit():
    input_username = request.form["username"]
    input_password = request.form["password"]

    user_found = False
    for user in users:
        if input_username == user["username"] and input_password == user["password"]:
            user_found = True
            session["username"] = input_username
            if user["is_admin"]:
                return redirect(url_for("show_repository"))

    if user_found:
        return render_template("repositorio.html", username=session["username"])
    else:
        return render_template("error.html")

@app.route('/repositorio', methods=['POST'])
def upload():
    # Obtendo o nome do usuário logado
    username = session["username"]
    # Criando o caminho da pasta do usuário
    user_folder = os.path.join(os.path.dirname(UPLOAD_FOLDER), username)

    # Criando a pasta se ela ainda não existir
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    # Salvando o arquivo na pasta do usuário
    file = request.files['imagem']
    save_path = os.path.join(user_folder, secure_filename(file.filename))
    file.save(save_path)
    save_path_repo = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.seek(0)
    file.save(save_path_repo)
    Nome = request.form.get("Nome")
    Email = request.form.get("email")
    Destino = request.form.get("Destino")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('submissions.txt', 'a+') as f:
        f.write('{} - {} - {} - {} - {}\n'.format(Nome, Email, Destino, file.filename, time))
    return render_template("repositorio.html", username=username)


@app.route('/get-file/<filename>')
def get_file(filename):
    file = os.path.join(UPLOAD_FOLDER, filename)
    file_type = magic.from_file(file)
    return send_file(file, mimetype=file_type)
# return send_file(file, mimetype="image/png|image/jpeg|text/csv|application/vnd.ms-excel|text/plain|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# Rota
@app.route('/arquivos', methods=['GET', 'POST'])
def show_repository():
    if request.method == 'GET':
        # Obtém uma lista de tuplas, onde cada tupla contém o nome do arquivo e a data de criação
        files = [(f, os.stat(os.path.join(UPLOAD_FOLDER, f)).st_ctime) for f in os.listdir(UPLOAD_FOLDER)]

        # Ordena a lista de tuplas pelo elemento de índice 1 (data de criação) em ordem crescente
        files.sort(key=lambda x: x[1])

        # Extrai apenas o nome dos arquivos da lista de tuplas
        files = [f[0] for f in files]

        # Lê o conteúdo dos arquivos e armazena em um dicionário, como feito anteriormente
        file_contents = {}
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            with open(file_path, 'r', encoding='latin-1') as f:
                file_contents[file] = f.read()

        # Renderiza a página HTML com os arquivos ordenados por data de criação
        return render_template('arquivos.html', files=files, os=os, UPLOAD_FOLDER=UPLOAD_FOLDER, file_contents=file_contents)

    elif request.method == 'POST':
        # Obter o nome do arquivo e o arquivo enviado pelo usuário
        file = request.form['filename']
        file_path = os.path.join(UPLOAD_FOLDER, file)
        new_content = request.form['texto']

        # Grava o novo conteúdo do arquivo
        with open(file_path, 'w', encoding='latin-1') as f:
            f.write(new_content)
        
        if os.path.exists(file_path):
            flash('Arquivo editado com sucesso!')
    else:
            flash('Erro ao editar o arquivo')

    return redirect(url_for('show_repository'))


@app.route("/results", methods=['POST', 'GET'])
def result():
    if request.method == "POST":
        # Obtém os detalhes do formulário
        name = request.form['Name']
        subject = request.form['Subject']
        email = request.form['Email']

        # Obtém o arquivo enviado
        file = request.files['file']

        # Cria a mensagem usando os valores do formulário
        msg = Message(subject, sender='Glocheck@outlook.com', recipients=[email])
        msg.body = f"{name} ({email}) enviou uma mensagem:\n\n{subject}"

        # Adiciona o arquivo à mensagem como um anexo
        msg.attach(file.filename, file.content_type, file.read())

        # Envia a mensagem
        mail.send(msg)
        
        return "arquivo enviado com sucesso"


@app.route('/download/<path:filename>')
def download(filename):
  # Verifique se o arquivo existe e tem permissão de leitura
  file_path = os.path.join(UPLOAD_FOLDER, filename)
  if os.path.exists(file_path) and os.access(file_path, os.R_OK):
    # Retorne o arquivo como resposta
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
  else:
    # Retorne uma mensagem de erro se o arquivo não existir ou não tiver permissão de leitura
    return 'Erro: arquivo não encontrado ou sem permissão de leitura'


@app.route('/submissions')
def show_submissions():
    with open('submissions.txt', 'r') as f:
        submissions = f.read()
    submissions = "<pre>" + submissions + "</pre>"
    return submissions


if __name__ == "__main__":
    app.run(debug=True)