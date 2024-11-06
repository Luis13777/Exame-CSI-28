import tkinter as tk
from tkinter import font
import datetime
from Elementos.botoes import *

class AdicionarGasto(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.mensgemDeNaoConfirmacao = None

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both",  expand=True)
        # self.frame.place(relx=0.5, rely=0.5, anchor="center")

        data_atual = datetime.date.today().strftime("%Y-%m-%d")  # Formato de data "YYYY-MM-DD"

        # Campo de descrição
        titulo = tk.Label(self.frame, text="Adicionar gasto:", bg="#ffffff", font=("Arial", 24, "bold"))
        titulo.pack(pady=(50, 100))

        # Campo de descrição
        label_desc = tk.Label(self.frame, text="Descrição:", bg="#ffffff", font=("Arial", 12, "bold"))
        label_desc.pack()

        entry_desc = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")
        entry_desc.pack(pady=10, ipadx=5, ipady=5)

        # Campo de valor
        label_valor = tk.Label(self.frame, text="Valor:", bg="#ffffff", font=("Arial", 12, "bold"))
        label_valor.pack()

        entry_valor = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=5, relief="flat", justify="center")
        entry_valor.pack(pady=10, ipadx=5, ipady=5)


        # Botão "OK" para enviar os dados
        def enviar_dados():

            if self.mensgemDeNaoConfirmacao:
                self.mensgemDeNaoConfirmacao.destroy()
            # Recupera os valores dos campos
            descricao = entry_desc.get()
            valor = entry_valor.get()

            # Envia ao banco de dados
            try:
                cursor = app.conn.cursor()
                email_usuario = app.usuario
                cursor.execute(f"INSERT INTO gastos (usuario_id, categoria, valor, data) "
                            f"VALUES ((SELECT usuario_id FROM usuarios WHERE email='{email_usuario}'), ?, ?, ?)",
                            (descricao, float(valor), data_atual))  # Usa a data atual
                cursor.commit()

                # mensagem de confirmação

                self.mensgemDeNaoConfirmacao = tk.Label(self.frame, text="Gasto adicionado com sucesso!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="green")

                self.mensgemDeNaoConfirmacao.pack(pady=10)
                
                print("Gasto adicionado com sucesso!")

            except Exception as e:
                print(f"Erro ao adicionar gasto: {e}")

                self.mensgemDeNaoConfirmacao = tk.Label(self.frame, text="Erro ao adicionar gasto!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")

                self.mensgemDeNaoConfirmacao.pack(pady=10)



        altura = 30
        largura = 100

        btn_ok = RoundedButton(self.frame, text="OK", command=enviar_dados, radius=altura/3, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 13, "bold"), width=largura, height=altura)
            
        btn_ok.pack(pady=20)

        criarBackButton(self, app)



    

    




