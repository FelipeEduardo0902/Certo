from flask import Flask, make_response, jsonify, request, render_template, redirect, url_for
import mysql.connector
from flask_wtf import CSRFProtect
from markupsafe import escape

app = Flask(__name__, static_folder='static')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'd0cketT0p'
csrf = CSRFProtect(app)

# Configuração do banco de dados
mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='teste'
)

#listagem de curriculos
@app.route('/')
def index():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT id, nome, email FROM curriculos')
    curriculos = my_cursor.fetchall()
    return render_template('index.html', curriculos=curriculos)

#cadastro de
@app.route('/cadastro', methods=['GET', 'POST'])
@csrf.exempt
def create_curriculo():
    if request.method == 'POST':
        nome = escape(request.form.get('nome'))
        telefone = escape(request.form.get('telefone'))
        email = escape(request.form.get('email'))
        endereco_fisico = escape(request.form.get('endereco_fisico'))  # Alterado para endereço físico
        experiencia = escape(request.form.get('experiencia'))

        # Validação de campos obrigatórios
        if not nome or not email or not experiencia:
            return make_response(jsonify(mensagem="Campos obrigatórios não preenchidos"), 400)

        my_cursor = mydb.cursor()
        sql = "INSERT INTO curriculos (nome, telefone, email, endereco_fisico, experiencia) VALUES (%s, %s, %s, %s, %s)"
        val = (nome, telefone, email, endereco_fisico, experiencia)
        my_cursor.execute(sql, val)
        mydb.commit()

        return redirect(url_for('index'))

    return render_template('cadastro.html')

# Tela 3 - Consulta de Currículo
@app.route('/curriculo/<int:id>')
def view_curriculo(id):
    my_cursor = mydb.cursor()
    sql = "SELECT * FROM curriculos WHERE id = %s"
    my_cursor.execute(sql, (id,))
    curriculo = my_cursor.fetchone()
    
    if not curriculo:
        return make_response(jsonify(mensagem="Currículo não encontrado"), 404)

    return render_template('consulta.html', curriculo=curriculo)

if __name__ == '__main__':
    app.run(debug=True)
