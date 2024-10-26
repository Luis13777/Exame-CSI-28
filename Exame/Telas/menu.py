import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from BancoDeDados import *
import datetime

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
        # self.btn_edit = tk.Button(self.box_de_botoes, text="Editar Gastos", command=self.editar_gasto,
        #                           bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)
        # self.btn_remove = tk.Button(self.box_de_botoes, text="Remover Gastos", command=self.remover_gasto,
        #                             bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)
        
        self.btn_edit_remove = tk.Button(self.box_de_botoes, text="Editar Gastos", command=self.editar_remover_gasto,
                                    bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)

        self.btn_add.pack(fill="x", pady=10, padx=20)
        self.btn_edit_remove.pack(fill="x", pady=10, padx=20)
        # self.btn_edit.pack(fill="x", pady=10, padx=20)
        # self.btn_remove.pack(fill="x", pady=10, padx=20)

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


    def adicionar_gasto(self):
        # Criar uma nova janela
        self.add_window = tk.Toplevel(self)
        self.add_window.title("Adicionar Gasto")
        self.add_window.geometry("300x200")
        self.add_window.config(bg="#ffffff")
        self.add_window.transient(self)  # Para manter a janela sobre a principal
        self.add_window.grab_set()  # Para bloquear interações com a janela principal

        # Centralizar a janela na tela
        self.add_window.update_idletasks()  # Atualiza informações de geometria
        largura_janela = 300
        altura_janela = 200
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.add_window.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        data_atual = datetime.date.today().strftime("%Y-%m-%d")  # Formato de data "YYYY-MM-DD"

        # Campo de descrição
        label_desc = tk.Label(self.add_window, text="Descrição:", bg="#ffffff", font=("Arial", 12))
        label_desc.pack(pady=10)
        entry_desc = tk.Entry(self.add_window, width=25)
        entry_desc.pack()

        # Campo de valor
        label_valor = tk.Label(self.add_window, text="Valor:", bg="#ffffff", font=("Arial", 12))
        label_valor.pack(pady=10)
        entry_valor = tk.Entry(self.add_window, width=25)
        entry_valor.pack()

        # Botão "OK" para enviar os dados
        def enviar_dados():
            # Recupera os valores dos campos
            descricao = entry_desc.get()
            valor = entry_valor.get()

            # Envia ao banco de dados
            try:
                cursor = self.conn.cursor()
                email_usuario = self.app.usuario
                cursor.execute(f"INSERT INTO gastos (usuario_id, categoria, valor, data) "
                            f"VALUES ((SELECT id FROM usuarios WHERE email='{email_usuario}'), ?, ?, ?)",
                            (descricao, float(valor), data_atual))  # Usa a data atual
                self.conn.commit()
                cursor.close()
                print("Gasto adicionado com sucesso!")
                self.add_window.destroy()  # Fecha a janela
            except Exception as e:
                print(f"Erro ao adicionar gasto: {e}")

        btn_ok = tk.Button(self.add_window, text="OK", command=enviar_dados, bg="#4CAF50", fg="white", font=("Arial", 12))
        btn_ok.pack(pady=20)

    def editar_remover_gasto(self):
        # Criar uma nova janela para edição e remoção
        self.edit_window = tk.Toplevel(self)
        self.edit_window.title("Editar ou Remover Gastos")
        self.edit_window.geometry("500x400")
        self.edit_window.config(bg="#ffffff")
        self.edit_window.transient(self)
        self.edit_window.grab_set()

        # Centralizar a janela na tela
        self.edit_window.update_idletasks()
        largura_janela, altura_janela = 500, 400
        largura_tela, altura_tela = self.winfo_screenwidth(), self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.edit_window.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Título e campos de data para filtrar gastos
        tk.Label(self.edit_window, text="Filtro de Data", bg="#ffffff", font=("Arial", 14, "bold")).pack(pady=10)
        frame_filtro = tk.Frame(self.edit_window, bg="#ffffff")
        frame_filtro.pack(pady=10)

        tk.Label(frame_filtro, text="Data Inicial (YYYY-MM-DD):", bg="#ffffff").grid(row=0, column=0, padx=5)
        entry_data_inicial = tk.Entry(frame_filtro, width=12)
        entry_data_inicial.grid(row=0, column=1)

        tk.Label(frame_filtro, text="Data Final (YYYY-MM-DD):", bg="#ffffff").grid(row=0, column=2, padx=5)
        entry_data_final = tk.Entry(frame_filtro, width=12)
        entry_data_final.grid(row=0, column=3)

        # Função para carregar gastos no período especificado
        def carregar_gastos():
            data_inicial = entry_data_inicial.get()
            data_final = entry_data_final.get()
            
            # Consulta ao banco com filtro de data
            query = ("SELECT id, categoria, valor, data FROM gastos "
                    "WHERE usuario_id = (SELECT id FROM usuarios WHERE email = ?) "
                    "AND data BETWEEN ? AND ?")
            cursor = self.conn.cursor()
            cursor.execute(query, (self.app.usuario, data_inicial, data_final))
            resultados = cursor.fetchall()
            cursor.close()

            # Limpa tabela antes de recarregar
            for widget in frame_tabela.winfo_children():
                widget.destroy()

            # Exibir dados em tabela com botões de ação
            for i, (gasto_id, descricao, valor, data) in enumerate(resultados):
                tk.Label(frame_tabela, text=descricao, bg="#ffffff", width=20).grid(row=i, column=0, padx=5, pady=5)
                tk.Label(frame_tabela, text=f"R${valor:.2f}", bg="#ffffff", width=10).grid(row=i, column=1, padx=5)
                tk.Label(frame_tabela, text=data, bg="#ffffff", width=12).grid(row=i, column=2, padx=5)

                # Botão para editar gasto
                btn_editar = tk.Button(frame_tabela, text="Editar", command=lambda g_id=gasto_id: editar_gasto(g_id), bg="#4CAF50", fg="white", width=8)
                btn_editar.grid(row=i, column=3, padx=5)

                # Botão para remover gasto
                btn_remover = tk.Button(frame_tabela, text="Remover", command=lambda g_id=gasto_id: remover_gasto(g_id), bg="#D9534F", fg="white", width=8)
                btn_remover.grid(row=i, column=4, padx=5)

        # Botão para filtrar
        btn_filtrar = tk.Button(self.edit_window, text="Filtrar", command=carregar_gastos, bg="#4CAF50", fg="white", font=("Arial", 12))
        btn_filtrar.pack(pady=10)

        # Frame para exibir a tabela de gastos
        frame_tabela = tk.Frame(self.edit_window, bg="#ffffff")
        frame_tabela.pack(fill="both", expand=True)

        # Função para editar um gasto
        def editar_gasto(gasto_id):
            def salvar_edicao():
                nova_descricao = entry_editar_desc.get()
                novo_valor = entry_editar_valor.get()
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("UPDATE gastos SET descricao = ?, valor = ? WHERE id = ?", (nova_descricao, float(novo_valor), gasto_id))
                    self.conn.commit()
                    cursor.close()
                    carregar_gastos()
                    janela_edicao.destroy()
                except Exception as e:
                    print(f"Erro ao editar gasto: {e}")

            # Criar uma janela de edição para o gasto
            janela_edicao = tk.Toplevel(self.edit_window)
            janela_edicao.title("Editar Gasto")
            janela_edicao.geometry("250x150")
            janela_edicao.config(bg="#ffffff")

            tk.Label(janela_edicao, text="Nova Descrição:", bg="#ffffff").pack(pady=5)
            entry_editar_desc = tk.Entry(janela_edicao, width=25)
            entry_editar_desc.pack(pady=5)

            tk.Label(janela_edicao, text="Novo Valor:", bg="#ffffff").pack(pady=5)
            entry_editar_valor = tk.Entry(janela_edicao, width=10)
            entry_editar_valor.pack(pady=5)

            btn_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_edicao, bg="#4CAF50", fg="white")
            btn_salvar.pack(pady=10)

        # Função para remover um gasto
        def remover_gasto(gasto_id):
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
                self.conn.commit()
                cursor.close()
                carregar_gastos()
            except Exception as e:
                print(f"Erro ao remover gasto: {e}")


    def remover_gasto(self):
        print("Função de remover gasto chamada")

    def editar_gasto(self):
        print("Função de editar gasto chamada")
