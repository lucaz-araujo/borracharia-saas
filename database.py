import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    
    # Tabela SERVIÇOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servico TEXT NOT NULL,
            valor REAL NOT NULL,
            data DATE DEFAULT CURRENT_DATE,
            quantidade INTEGER DEFAULT 1
        )
    ''')
    
    # Tabela GASTOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            valor REAL NOT NULL,
            data DATE DEFAULT CURRENT_DATE,
            quantidade INTEGER DEFAULT 1
        )
    ''')
    
    # Serviços padrão da borracharia
    servicos_padrao = [
        ('Calibragem', 5.00),
        ('Troca de Pneu', 20.00),
        ('Remendo Frio', 20.00),
        ('Remendo Quente', 20.00),
        ('Renovação da Roda', 15.00),
        ('Troca de Óleo', 20.00),
        ('Troca de Pito', 15.00)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO servicos (servico, valor) VALUES (?, ?)', servicos_padrao)
    
    conn.commit()
    conn.close()

# CRUD SERVIÇOS
def get_servicos():
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM servicos ORDER BY data DESC')
    return cursor.fetchall()

def add_servico(servico, valor, quantidade=1):
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO servicos (servico, valor, quantidade) VALUES (?, ?, ?)', 
                   (servico, valor, quantidade))
    conn.commit()
    conn.close()

def delete_servico(id):
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM servicos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# CRUD GASTOS
def get_gastos():
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gastos ORDER BY data DESC')
    return cursor.fetchall()

def add_gasto(item, valor, quantidade=1):
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gastos (item, valor, quantidade) VALUES (?, ?, ?)', 
                   (item, valor, quantidade))
    conn.commit()
    conn.close()

def delete_gasto(id):
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM gastos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# RELATÓRIO
def relatorio_resumo():
    conn = sqlite3.connect('borracharia.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COALESCE(SUM(valor * quantidade), 0) as total_entrada FROM servicos')
    entrada = cursor.fetchone()[0]
    
    cursor.execute('SELECT COALESCE(SUM(valor * quantidade), 0) as total_saida FROM gastos')
    saida = cursor.fetchone()[0]
    
    lucro = entrada - saida
    conn.close()
    
    return {'entrada': entrada, 'saida': saida, 'lucro': lucro}