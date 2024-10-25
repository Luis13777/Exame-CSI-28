import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from BancoDeDados import *

class MainMenu(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root)
        self.app = app
        self.conn = conectar_ao_sql_server()

        # Layout principal
        self.config(bg="#ffffff")
        self.pack(fill="both", expand=True)

        # Título
        label_title = tk.Label(self, text=f"Bem vindo {self.get_usuario_id()}", font=("Arial", 24, "bold"), bg="#ffffff")
        label_title.pack(pady=20)

        # Gráfico de gastos
        self.create_gasto_chart()

        # Variável de controle para o estado do menu lateral
        self.menu_open = False

        # Criar um frame para o menu lateral que cobre toda a altura da tela
        self.sidebar = tk.Frame(self, bg="#333", width=200)
        self.sidebar.place(x=-200, y=0, relheight=1)  # Define a altura relativa a 100% da janela

        self.box_de_botoes = tk.Frame(self.sidebar, bg="#333")
        self.box_de_botoes.pack(fill="x", expand=True)
        self.box_de_botoes.place(x=0, y=75, relwidth=1)

        # Adicionar botões no menu lateral com mais espaçamento
        self.btn_add = tk.Button(self.box_de_botoes, text="Adicionar Gastos", command=self.adicionar_gasto,
                                 bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)
        self.btn_edit = tk.Button(self.box_de_botoes, text="Editar Gastos", command=self.editar_gasto,
                                  bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)
        self.btn_remove = tk.Button(self.box_de_botoes, text="Remover Gastos", command=self.remover_gasto,
                                    bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)

        self.btn_add.pack(fill="x", pady=10, padx=20)
        self.btn_edit.pack(fill="x", pady=10, padx=20)
        self.btn_remove.pack(fill="x", pady=10, padx=20)

        # Botão que alterna o menu lateral
        self.toggle_btn = tk.Button(self, text="☰", command=self.toggle_sidebar,
                                    bg="#333", fg="white", padx=10, pady=5, font=("Arial", 16))
        self.toggle_btn.place(x=10, y=10)

    def toggle_sidebar(self):
        if self.menu_open:
            # Animação para fechar o menu
            for i in range(0, 201, 20):
                self.sidebar.place(x=-i, y=0, relheight=1)
                self.update()
            self.menu_open = False
        else:
            # Animação para abrir o menu
            for i in range(-200, 1, 20):
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update()
            self.menu_open = True

    def create_gasto_chart(self):
        """Cria o gráfico de gastos com base nos dados do usuário"""
        gastos = self.fetch_gastos_data()

        if not gastos.empty:
            categorias = gastos['categoria'].unique()
            valores = [gastos[gastos['categoria'] == cat]['valor'].sum() for cat in categorias]

            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            ax.axis('equal')  # Mantém o gráfico circular

            # Desenha o gráfico
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas_widget = canvas.get_tk_widget()

            # Obtém a altura do frame que contém o gráfico (após layout ser atualizado)
            frame_height = self.winfo_height()

            # Calcula 10% da altura do frame
            pady_percent = int(frame_height * 0.10)

            # Aplica o padding calculado
            canvas_widget.pack(pady=pady_percent, fill="both", expand=True)

            # Finalmente desenha o gráfico
            canvas.draw()

        else:
            label_no_data = tk.Label(self, text="Nenhum dado de gasto disponível.", bg="#f0f4f7", font=("Arial", 12))
            label_no_data.pack(pady=20)

    def fetch_gastos_data(self):
        """Busca os dados de gastos do usuário logado"""
        email_usuario = self.app.usuario
        query = f"SELECT g.categoria, g.valor, g.data FROM usuarios u JOIN gastos g ON u.id = g.usuario_id WHERE u.email = '{email_usuario}'"
        cursor = self.conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        if rows:
            data = pd.DataFrame.from_records(rows, columns=['categoria', 'valor', 'data'])
        else:
            data = pd.DataFrame(columns=['categoria', 'valor', 'data'])

        cursor.close()
        return data
    
    def get_usuario_id(self):
        """Busca o ID do usuário logado"""
        email_usuario = self.app.usuario
        query = f"SELECT nome FROM usuarios WHERE email = '{email_usuario}'"
        cursor = self.conn.cursor()
        cursor.execute(query)
        usuario_id = cursor.fetchone()[0]
        cursor.close()
        return usuario_id

    # Métodos de exemplo para ações no menu
    def adicionar_gasto(self):
        print("Função de adicionar gasto chamada")

    def remover_gasto(self):
        print("Função de remover gasto chamada")

    def editar_gasto(self):
        print("Função de editar gasto chamada")
