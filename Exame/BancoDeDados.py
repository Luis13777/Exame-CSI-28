import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

def conectar_ao_sql_server():
    # Carregar as variáveis do arquivo .env
    load_dotenv()

    # Obter os valores das variáveis de ambiente
    server = os.getenv('SERVER_NAME')
    database = os.getenv('DATABASE_NAME')
    
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    try:
        # Tentando estabelecer a conexão
        conn = pyodbc.connect(conn_str)
        print("Conexão estabelecida com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao SQL Server: {e}")
        return None

def adicionar_usuario(conn, nome, email, senha, periodo_relatorio):
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO usuarios (nome, email, senha, periodo_relatorio)
                          VALUES (?, ?, ?, ?)''', (nome, email, senha, periodo_relatorio))
        conn.commit()
        print("Usuário adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")

def adicionar_gasto(conn, usuario_id, categoria, valor, data):
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO gastos (usuario_id, categoria, valor, data)
                          VALUES (?, ?, ?, ?)''', (usuario_id, categoria, valor, data))
        conn.commit()
        print("Gasto adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar gasto: {e}")

def editar_usuario(conn, usuario_id, nome=None, email=None, senha=None, periodo_relatorio=None):
    cursor = conn.cursor()
    updates = []
    params = []
    
    if nome:
        updates.append("nome = ?")
        params.append(nome)
    if email:
        updates.append("email = ?")
        params.append(email)
    if senha:
        updates.append("senha = ?")
        params.append(senha)
    if periodo_relatorio:
        updates.append("periodo_relatorio = ?")
        params.append(periodo_relatorio)
    
    params.append(usuario_id)
    query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
    
    try:
        cursor.execute(query, params)
        conn.commit()
        print("Usuário atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao editar usuário: {e}")

def editar_gasto(conn, gasto_id, categoria=None, valor=None, data=None):
    cursor = conn.cursor()
    updates = []
    params = []
    
    if categoria:
        updates.append("categoria = ?")
        params.append(categoria)
    if valor:
        updates.append("valor = ?")
        params.append(valor)
    if data:
        updates.append("data = ?")
        params.append(data)
    
    params.append(gasto_id)
    query = f"UPDATE gastos SET {', '.join(updates)} WHERE id = ?"
    
    try:
        cursor.execute(query, params)
        conn.commit()
        print("Gasto atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao editar gasto: {e}")

def remover_usuario(conn, usuario_id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        print("Usuário removido com sucesso!")
    except Exception as e:
        print(f"Erro ao remover usuário: {e}")

def remover_gasto(conn, gasto_id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
        conn.commit()
        print("Gasto removido com sucesso!")
    except Exception as e:
        print(f"Erro ao remover gasto: {e}")

def consultar_usuarios(conn, usuario_email):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuario_email,))
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame.from_records(result, columns=columns)
        return df
    except Exception as e:
        print(f"Erro ao consultar usuários: {e}")
        return None
# conn = conectar_ao_sql_server()

# # Adicionando um usuário
# adicionar_usuario(conn, 'Luis Bertuol', 'luis@email.com', 'senha123', 'mensal')

# # Adicionando um gasto
# adicionar_gasto(conn, 1, 'Alimentação', 50.00, '2024-10-22')

# # Editando um usuário
# editar_usuario(conn, 1, nome='Luis F Bertuol', email='novoemail@email.com')

# # Editando um gasto
# editar_gasto(conn, 1, valor=100.00)

# Removendo um usuário
# remover_usuario(conn, 2)

# # Removendo um gasto
# remover_gasto(conn, 1)