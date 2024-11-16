import tkinter as tk
from Elementos.botoes import *
from BancoDeDados import *
import pandas as pd

class editarPerfil(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both",  expand=True)

        # Campo de descrição
        self.label = tk.Label(self.frame, text="Editar Perfil:", bg="#ffffff", font=("Arial", 24, "bold"))
        self.label.pack(fill="x", pady=20)

        # Carregar dados
        informacoes = self.carregarDados()

        self.frame_com_informacoes = tk.Frame(self.frame, bg="#ffffff")
        self.frame_com_informacoes.pack()

        self.inputs = {}
        self.aviso = None


        for i, info in enumerate(informacoes):
            self.frame_com_informacoes.grid_rowconfigure(2*i, weight=1)
            self.frame_com_informacoes.grid_rowconfigure(2*i+1, weight=1)

        for i, info in enumerate(informacoes):
            self.label = tk.Label(self.frame_com_informacoes, text=info, bg="#ffffff", font=("Arial", 12, "bold"))
            self.label.grid(row = 2*i,sticky="", pady=(10,5))

            if info == "Senha":
                self.entry = tk.Entry(self.frame_com_informacoes, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center", show="*")

            else:
                self.entry = tk.Entry(self.frame_com_informacoes, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")

            self.entry.insert(0, informacoes[info])
            self.entry.grid(row = 2*i+1, sticky="w", pady=(0,5), ipadx=100)

            self.inputs[info] = self.entry

        self.btn_salvar = RoundedButton(self.frame, text="Salvar", command=self.salvar, radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 14, "bold"), width=100, height=40)

        self.btn_salvar.pack(pady=20)



        criarBackButton(self, app)



    def salvar(self):
        cursor = self.app.conn.cursor()

        nome = self.inputs["Nome"].get()
        email = self.inputs["Email"].get()
        senha = self.inputs["Senha"].get()

        # checar se o email ja nao existe no banco de dados

        query = f"SELECT * FROM usuarios WHERE email = '{email}'"
        cursor.execute(query)
        resultado = cursor.fetchall()

        if self.aviso:
            self.aviso.destroy()

        if len(resultado) > 0 and resultado[0][2] != self.app.usuario:
            self.aviso = tk.Label(self.frame, text="Email já cadastrado", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
            self.aviso.pack(pady=20)
            return

        if not nome or not email or not senha:
            self.aviso = tk.Label(self.frame, text="Preencha todos os campos", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
            self.aviso.pack(pady=20)
            return
        
        if "@" not in email or "." not in email or " " in email:
            self.aviso = tk.Label(self.frame, text="Email inválido", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
            self.aviso.pack(pady=20)
            return
        
            
        query = f"UPDATE usuarios SET nome = '{nome}', email = '{email}', senha = '{senha}' WHERE email = '{self.app.usuario}'"
        cursor.execute(query)
        cursor.commit()

        self.aviso = tk.Label(self.frame, text="Dados salvos com sucesso", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="green")
        self.aviso.pack(pady=20)
        


    def carregarDados(self):
        query = f"SELECT * FROM usuarios WHERE email = '{self.app.usuario}'"

        cursor = self.app.conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        return {"Nome": resultado[0][1], "Email": resultado[0][2], "Senha": resultado[0][3]}