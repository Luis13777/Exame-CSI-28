import tkinter as tk
from tkinter import font
import datetime
from Elementos.botoes import *

class AdicionarGasto(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.frame = tk.Frame(self, bg="#ffffff")
        # self.frame.pack(fill="both",  expand=True)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        data_atual = datetime.date.today().strftime("%Y-%m-%d")  # Formato de data "YYYY-MM-DD"

        # Campo de descrição
        label_desc = tk.Label(self.frame, text="Descrição:", bg="#ffffff", font=("Arial", 12))
        label_desc.pack()
        # entry_desc = tk.Entry(self.frame, width=25, justify="center")
        # entry_desc.pack()

        entry_desc = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 12), bd=1, relief="flat", justify="center")
        entry_desc.pack(pady=10, ipadx=5, ipady=5, fill="x")

        # Campo de valor
        label_valor = tk.Label(self.frame, text="Valor:", bg="#ffffff", font=("Arial", 12))
        label_valor.pack()
        # entry_valor = tk.Entry(self.frame, width=25, justify="center")
        # entry_valor.pack()

        entry_valor = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 12), bd=1, relief="flat", justify="center")
        entry_valor.pack(pady=10, ipadx=5, ipady=5, fill="x")

        # Botão para voltar, inicialmente oculto
        self.back_button = tk.Button(self, text="←", font=("Arial", 20), bg="#333333", fg="white", command=lambda: app.show_frame("MainMenu"))
        
        self.back_button.place(relx=1.0, y=10, x=-10, anchor="ne")

        # Botão "OK" para enviar os dados
        def enviar_dados():
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
                # cursor.close()
                print("Gasto adicionado com sucesso!")

            except Exception as e:
                print(f"Erro ao adicionar gasto: {e}")




        altura = 30
        largura = 100

        btn_ok = RoundedButton(self.frame, text="OK", command=enviar_dados, radius=altura/3, bg="#4CAF50", hover_bg="#96DF96", fg="white", font=("Arial", 13, "bold"), width=largura, height=altura)
            
        btn_ok.pack(pady=20)


        # Botão para voltar
        self.back_button = tk.Button(self, text="←", font=("Arial", 20), bg="#333333", fg="white",
                                command=lambda: self.app.show_frame("MainMenu"))
        self.back_button.place(relx=1.0, y=10, x=-10, anchor="ne")

    

    




