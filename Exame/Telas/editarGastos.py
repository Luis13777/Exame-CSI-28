import tkinter as tk
from tkinter import font
from Elementos.botoes import *
import datetime
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class EditarGastos(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.edit_window = tk.Frame(self, bg="#ffffff")
        self.edit_window.pack(fill="both", expand=True)  # Para ocupar todo o espaço

        self.label_no_data = None
        self.frame_tabela = None

        frame_filtro = tk.Frame(self.edit_window, bg="#ffffff")
        frame_filtro.pack(fill="x", pady=10, padx=50)
        self.frame_filtro = frame_filtro

        
        self.frame_filtro.grid_rowconfigure(0, weight=1)
        self.frame_filtro.grid_rowconfigure(1, weight=1)
        self.frame_filtro.grid_rowconfigure(2, weight=1)
        self.frame_filtro.grid_rowconfigure(3, weight=1)
        self.frame_filtro.grid_columnconfigure(0, weight=3)
        self.frame_filtro.grid_columnconfigure(1, weight=3)
        self.frame_filtro.grid_columnconfigure(2, weight=1)
        self.frame_filtro.grid_columnconfigure(3, weight=3)
        self.frame_filtro.grid_columnconfigure(4, weight=3)

        tk.Label(self.frame_filtro, text="Filtro de Data", bg="#ffffff", font=("Arial", 24, "bold")).grid(row=0, column=2, padx=10, pady=20)

        tk.Label(self.frame_filtro, text="Data Inicial (YYYY-MM-DD):", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=1, column=0, padx=5, columnspan=3)

        entry_data_inicial = tk.Entry(self.frame_filtro, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")
        entry_data_inicial.grid(row=2, column=0, columnspan=3, pady=(20, 0))

        tk.Label(self.frame_filtro, text="Data Final (YYYY-MM-DD):", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=1, column=2, padx=5, columnspan=3)

        entry_data_final = tk.Entry(frame_filtro, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")
        entry_data_final.grid(row=2, column=2, columnspan=3, pady=(20, 0))

        criarBackButton(self, app)

        def carregar_gastos():
            data_inicial = entry_data_inicial.get()
            data_final = entry_data_final.get()
            data_inicial = data_inicial.replace(" ", "")
            data_final = data_final.replace(" ", "")

            if self.frame_tabela != None:
                self.frame_tabela.destroy()

            # Frame para exibir a tabela de gastos
            self.frame_tabela = tk.Frame(self.edit_window, bg="#ffffff")
            self.frame_tabela.pack(fill="both", expand=True, padx=100, pady=(50,50))

            if self.label_no_data:
                self.label_no_data.destroy()
                
            try:
                datetime.datetime.strptime(data_inicial, "%Y-%m-%d")
                datetime.datetime.strptime(data_final, "%Y-%m-%d")
            except ValueError:
                self.label_no_data = tk.Label(self.frame_filtro, text="Datas inválidas. Por favor, preencha no formato YYYY-MM-DD.", bg="#f0f4f7", font=("Arial", 12))
                self.label_no_data.grid(row=3, column=0, columnspan=5, pady=10)
                return
            
            if data_inicial == "" or data_final == "":
                self.label_no_data = tk.Label(self.frame_filtro, text="Preencha todos os campos!", bg="#f0f4f7", font=("Arial", 12))
                self.label_no_data.grid(row=3, column=0, columnspan=5, pady=10)
                return

            # Consulta ao banco com filtro de data
            query = ("SELECT id_gasto, categoria, valor, data FROM gastos "
                    "WHERE usuario_id = (SELECT usuario_id FROM usuarios WHERE email = ?) "
                    "AND data BETWEEN ? AND ?")
            cursor = app.conn.cursor()
            cursor.execute(query, (self.app.usuario, data_inicial, data_final))
            resultados = cursor.fetchall()

            # Limpa a tabela antes de recarregar
            for widget in self.frame_tabela.winfo_children():
                widget.destroy()

            # Configura cada coluna da self.frame_tabela para expandir com a janela
            self.frame_tabela.grid_columnconfigure(0, weight=2)  # Coluna Descrição
            self.frame_tabela.grid_columnconfigure(1, weight=1)  # Coluna Valor
            self.frame_tabela.grid_columnconfigure(2, weight=1)  # Coluna Data
            self.frame_tabela.grid_columnconfigure(3, weight=1)  # Coluna Editar
            self.frame_tabela.grid_columnconfigure(4, weight=1)  # Coluna Remover

            # Exibir dados em tabela com botões de ação
            for i, (gasto_id, descricao, valor, data) in enumerate(resultados):
                # Exibe a descrição do gasto
                tk.Label(self.frame_tabela, text=descricao, bg="#ffffff", width=20, anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="ew")
                
                # Exibe o valor do gasto
                tk.Label(self.frame_tabela, text=f"R${valor:.2f}", bg="#ffffff", width=10, anchor="center").grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                
                # Exibe a data do gasto
                tk.Label(self.frame_tabela, text=data, bg="#ffffff", width=12, anchor="center").grid(row=i, column=2, padx=5, pady=5, sticky="ew")

    
                altura = 25
                largura = 80
                btn_editar = RoundedButton(self.frame_tabela, text="Editar", command=lambda g_id=gasto_id: editar_gasto(g_id), radius=altura/2, bg="#4CAF50", hover_bg="#96DF96", fg="white", font=("Arial", 9, "bold"), width=largura, height=altura)
                btn_editar.grid(row=i, column=3, padx=5, pady=5, sticky="ew")


                btn_remover = RoundedButton(self.frame_tabela, text="Remover", command=lambda g_id=gasto_id: remover_gasto(g_id), radius=altura/2, bg="#D9534F", hover_bg="#E08E8B", fg="white", font=("Arial", 9, "bold"), width=largura, height=altura)
                
                btn_remover.grid(row=i, column=4, padx=5, pady=5, sticky="ew")



        altura = 30
        largura = 100

        btn_filtrar = RoundedButton(self.edit_window, text="Filtrar", command=carregar_gastos, radius=altura/2, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 12, "bold"), width=largura, height=altura)
        btn_filtrar.pack(pady=10)



        # Função para editar um gasto
        def editar_gasto(gasto_id):
            def salvar_edicao():
                nova_descricao = entry_editar_desc.get()
                novo_valor = entry_editar_valor.get()
                nova_data = entry_editar_data.get()
                nova_data = nova_data.replace(" ", "")

                if nova_descricao == "" or novo_valor == "" or nova_data == "":
                    tk.messagebox.showinfo('Erro', 'Preencha todos os campos!')
                    janela_edicao.focus_set()
                    return

                
                try:
                    # testar se o valor é um float
                    novo_valor = float(novo_valor)
                except ValueError:
                    tk.messagebox.showinfo('Erro', 'Valor inválido! Insira um valor numérico.')
                    janela_edicao.focus_set()  # Mantém o foco na janela de edição

                # Validação do formato da data
                try:
                    nova_data = datetime.datetime.strptime(nova_data, "%Y-%m-%d").date()

                    
                except ValueError:
                    print("Data inválida! Insira a data no formato YYYY-MM-DD.")
                    tk.messagebox.showinfo('Erro', 'Data inválida! Insira a data no formato YYYY-MM-DD.')
                    janela_edicao.focus_set()  # Mantém o foco na janela de edição
                    return
            


                try:
                    cursor = app.conn.cursor()
                    cursor.execute("UPDATE gastos SET categoria = ?, valor = ?, data = ? WHERE id_gasto = ?", (nova_descricao, float(novo_valor), nova_data, gasto_id))
                    app.conn.commit()
                    carregar_gastos()
                    janela_edicao.destroy()
                except Exception as e:
                    print(f"Erro ao editar gasto: {e}")

            # Criar uma janela de edição para o gasto
            janela_edicao = tk.Toplevel(self.edit_window)
            janela_edicao.title("Editar Gasto")
            janela_edicao.geometry("400x250")
            janela_edicao.config(bg="#ffffff")

            query = f"select categoria, valor, data from gastos where id_gasto = {gasto_id}"

            cursor = app.conn.cursor()
            cursor.execute(query)
            resultado = cursor.fetchone()



            tk.Label(janela_edicao, text="Nova Descrição:", bg="#ffffff").pack(pady=5)
            # entry_editar_desc = tk.Entry(janela_edicao, width=25, justify="center")
            entry_editar_desc = tk.Entry(janela_edicao, bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=1, relief="flat", justify="center", width=25)
            entry_editar_desc.pack(pady=5)
            entry_editar_desc.insert(0, resultado[0])


            tk.Label(janela_edicao, text="Novo Valor:", bg="#ffffff").pack(pady=5)
            # entry_editar_valor = tk.Entry(janela_edicao, width=25, justify="center")
            entry_editar_valor = tk.Entry(janela_edicao, bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=1, relief="flat", justify="center", width=25)
            entry_editar_valor.pack(pady=5)
            entry_editar_valor.insert(0, resultado[1])

            tk.Label(janela_edicao, text="Novo Data:", bg="#ffffff").pack(pady=5)
            # entry_editar_data = tk.Entry(janela_edicao, width=25, justify="center")
            entry_editar_data = tk.Entry(janela_edicao, bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=1, relief="flat", justify="center", width=25)
            entry_editar_data.pack(pady=5)
            entry_editar_data.insert(0, resultado[2])

            # btn_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_edicao, bg="#4CAF50", fg="white")

            janela_edicao.update_idletasks()

            largura = janela_edicao.winfo_width()*0.2
            altura = janela_edicao.winfo_height()*0.1
            
            btn_salvar = RoundedButton(janela_edicao, text="Salvar", command=salvar_edicao, radius=altura/2, bg="#4CAF50", hover_bg="#96DF96", fg="white", font=("Arial", 10, "bold"), width=largura, height=altura)
                
            btn_salvar.pack(pady=(20, 0))

        # Função para remover um gasto
        def remover_gasto(gasto_id):
            try:
                cursor = app.conn.cursor()
                cursor.execute("DELETE FROM gastos WHERE id_gasto = ?", (gasto_id,))
                app.conn.commit()
                carregar_gastos()
            except Exception as e:
                print(f"Erro ao remover gasto: {e}")
               

    