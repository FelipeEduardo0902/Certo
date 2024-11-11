import os
from flask import Flask, make_response, jsonify, request, render_template, redirect, url_for
import mysql.connector
from flask_wtf import CSRFProtect
from markupsafe import escape
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'd0cketT0p')
csrf = CSRFProtect(app)

# Configuração do banco de dados usando variáveis de ambiente
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'root'),
    database=os.getenv('DB_NAME', 'teste')
)

# Cabeçalhos de segurança
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Listagem de currículos
@app.route('/')
def index():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT id, nome, email FROM curriculos')
    curriculos = my_cursor.fetchall()
    return render_template('index.html', curriculos=curriculos)

# Cadastro de currículos
@app.route('/cadastro', methods=['GET', 'POST'])
def create_curriculo():
    if request.method == 'POST':
        nome = escape(request.form.get('nome')).strip()
        telefone = escape(request.form.get('telefone')).strip()
        email = escape(request.form.get('email')).strip()
        endereco_fisico = escape(request.form.get('endereco_fisico')).strip()
        experiencia = escape(request.form.get('experiencia')).strip()

        # Validação básica de entradas
        if not nome or not email or not experiencia:
            return make_response(jsonify(mensagem="Campos obrigatórios não preenchidos"), 400)

        try:
            my_cursor = mydb.cursor()
            sql = """INSERT INTO curriculos (nome, telefone, email, endereco_fisico, experiencia)
                     VALUES (%s, %s, %s, %s, %s)"""
            val = (nome, telefone, email, endereco_fisico, experiencia)
            my_cursor.execute(sql, val)
            mydb.commit()
        except mysql.connector.Error as err:
            return make_response(jsonify(mensagem=f"Erro ao inserir dados: {err}"), 500)

        return redirect(url_for('index'))

    return render_template('cadastro.html')

# Consulta de currículo
@app.route('/curriculo/<int:id>')
def view_curriculo(id):
    my_cursor = mydb.cursor()
    sql = "SELECT * FROM curriculos WHERE id = %s"
    my_cursor.execute(sql, (id,))
    curriculo = my_cursor.fetchone()

    if not curriculo:
        return make_response(jsonify(mensagem="Currículo não encontrado"), 404)

    return render_template('consulta.html', curriculo=curriculo)

# Rota para páginas não encontradas (404)
@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify(mensagem="Página não encontrada"), 404)

if __name__ == '__main__':
    app.run(debug=False)
