from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests
from database import init_db, get_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta-123'
app.config['DEBUG'] = False

init_db()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login para continuar.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def buscar_conselho():
    try:
        resposta = requests.get('https://api.adviceslip.com/advice', timeout=5)
        dados = resposta.json()
        return dados['slip']['advice']
    except:
        return 'Acredite em você e siga em frente!'


@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        if not email or not senha:
            flash('Preencha todos os campos.', 'danger')
            return render_template('login.html')

        conn = get_db()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))

        flash('Email ou senha incorretos.', 'danger')

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'danger')
            return render_template('registro.html')

        if len(senha) < 4:
            flash('A senha deve ter pelo menos 4 caracteres.', 'danger')
            return render_template('registro.html')

        conn = get_db()
        existe = conn.execute('SELECT id FROM usuarios WHERE email = ?', (email,)).fetchone()

        if existe:
            conn.close()
            flash('Este email já está cadastrado.', 'danger')
            return render_template('registro.html')

        senha_hash = generate_password_hash(senha)
        conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                     (nome, email, senha_hash))
        conn.commit()
        conn.close()

        flash('Cadastro realizado! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    conselho = buscar_conselho()
    return render_template('dashboard.html', conselho=conselho)


@app.route('/nova_tarefa', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        status = request.form.get('status', 'pendente')

        if not titulo:
            flash('O título é obrigatório.', 'danger')
            return render_template('nova_tarefa.html')

        conn = get_db()
        conn.execute(
            'INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)',
            (titulo, descricao, status, session['usuario_id'])
        )
        conn.commit()
        conn.close()

        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('nova_tarefa.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    conn = get_db()
    tarefa = conn.execute(
        'SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?',
        (id, session['usuario_id'])
    ).fetchone()

    if not tarefa:
        conn.close()
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        status = request.form.get('status', 'pendente')

        if not titulo:
            flash('O título é obrigatório.', 'danger')
            conn.close()
            return render_template('editar_tarefa.html', tarefa=tarefa)

        conn.execute(
            'UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?',
            (titulo, descricao, status, id)
        )
        conn.commit()
        conn.close()

        flash('Tarefa atualizada!', 'success')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('editar_tarefa.html', tarefa=tarefa)


@app.route('/excluir/<int:id>')
@login_required
def excluir_tarefa(id):
    conn = get_db()
    tarefa = conn.execute(
        'SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?',
        (id, session['usuario_id'])
    ).fetchone()

    if tarefa:
        conn.execute('DELETE FROM tarefas WHERE id = ?', (id,))
        conn.commit()
        flash('Tarefa excluída.', 'info')
    else:
        flash('Tarefa não encontrada.', 'danger')

    conn.close()
    return redirect(url_for('dashboard'))


# rota JSON para filtrar tarefas sem recarregar a pagina
@app.route('/api/tarefas')
@login_required
def api_tarefas():
    status = request.args.get('status', 'todas')

    conn = get_db()
    if status == 'todas':
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC',
            (session['usuario_id'],)
        ).fetchall()
    else:
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC',
            (session['usuario_id'], status)
        ).fetchall()
    conn.close()

    lista = []
    for t in tarefas:
        lista.append({
            'id': t['id'],
            'titulo': t['titulo'],
            'descricao': t['descricao'],
            'status': t['status']
        })

    return jsonify(lista)


# rota JSON para o grafico de progresso
@app.route('/api/stats')
@login_required
def api_stats():
    conn = get_db()
    pendentes = conn.execute(
        "SELECT COUNT(*) as total FROM tarefas WHERE usuario_id = ? AND status = 'pendente'",
        (session['usuario_id'],)
    ).fetchone()['total']

    em_andamento = conn.execute(
        "SELECT COUNT(*) as total FROM tarefas WHERE usuario_id = ? AND status = 'em andamento'",
        (session['usuario_id'],)
    ).fetchone()['total']

    concluidas = conn.execute(
        "SELECT COUNT(*) as total FROM tarefas WHERE usuario_id = ? AND status = 'concluida'",
        (session['usuario_id'],)
    ).fetchone()['total']

    conn.close()

    return jsonify({
        'pendente': pendentes,
        'em andamento': em_andamento,
        'concluida': concluidas
    })


@app.route('/dashboard_stats')
@login_required
def dashboard_stats():
    return render_template('dashboard_stats.html')


if __name__ == '__main__':
    app.run(debug=True)
