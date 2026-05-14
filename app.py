from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_servicos, add_servico, delete_servico, get_gastos, add_gasto, delete_gasto, relatorio_resumo

app = Flask(__name__)
app.secret_key = 'borracharia123'

@app.route('/')
def index():
    resumo = relatorio_resumo()
    return render_template('index.html', resumo=resumo)

@app.route('/servicos')
def servicos():
    servicos_lista = get_servicos()
    return render_template('servicos.html', servicos=servicos_lista)

@app.route('/add_servico', methods=['POST'])
def add_servico_route():
    servico = request.form['servico']
    valor = float(request.form['valor'])
    qtd = int(request.form.get('quantidade', 1))
    add_servico(servico, valor, qtd)
    flash('✅ Serviço adicionado!')
    return redirect(url_for('servicos'))

@app.route('/delete_servico/<int:id>')
def delete_servico_route(id):
    delete_servico(id)
    flash('🗑️ Serviço removido!')
    return redirect(url_for('servicos'))

@app.route('/gastos')
def gastos():
    gastos_lista = get_gastos()
    return render_template('gastos.html', gastos=gastos_lista)

@app.route('/add_gasto', methods=['POST'])
def add_gasto_route():
    item = request.form['item']
    valor = float(request.form['valor'])
    qtd = int(request.form.get('quantidade', 1))
    add_gasto(item, valor, qtd)
    flash('✅ Gasto adicionado!')
    return redirect(url_for('gastos'))

@app.route('/delete_gasto/<int:id>')
def delete_gasto_route(id):
    delete_gasto(id)
    flash('🗑️ Gasto removido!')
    return redirect(url_for('gastos'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)