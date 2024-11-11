import tkinter as tk
from tkinter import font
from Elementos.botoes import *

class RegisterScreen(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.mensgem = None

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both",  expand=True)

        # Campo de descrição
        titulo = tk.Label(self.frame, text="Criar nova conta", bg="#ffffff", font=("Arial", 24, "bold"))
        titulo.pack(pady=(25, 50))

        # Campo de descrição
        nome = tk.Label(self.frame, text="Nome:", bg="#ffffff", font=("Arial", 12, "bold"))
        nome.pack()

        entry_nome = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")
        entry_nome.pack(pady=10, ipadx=5, ipady=5)

        email = tk.Label(self.frame, text="Email:", bg="#ffffff", font=("Arial", 12, "bold"))
        email.pack()

        entry_email = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=5, relief="flat", justify="center")
        entry_email.pack(pady=10, ipadx=5, ipady=5)

        
        senha = tk.Label(self.frame, text="Senha:", bg="#ffffff", font=("Arial", 12, "bold"))
        senha.pack()

        entry_senha = tk.Entry(self.frame, show="*", bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=5, relief="flat", justify="center")
        entry_senha.pack(pady=10, ipadx=5, ipady=5)

        confimar_senha = tk.Label(self.frame, text="Confirmar Senha:", bg="#ffffff", font=("Arial", 12, "bold"))
        confimar_senha.pack()

        entry_confimar_senha = tk.Entry(self.frame, show="*", bg="#f0f0f0", fg="#333333", font=("Arial", 10), bd=5, relief="flat", justify="center")
        entry_confimar_senha.pack(pady=10, ipadx=5, ipady=5)



        def criar_nova_conta():
            if self.mensgem:
                self.mensgem.destroy()

            # Recupera os valores dos campos
            nome = entry_nome.get()
            email = entry_email.get()
            senha = entry_senha.get()
            confirmar_senha = entry_confimar_senha.get()

            # Verifica se os campos estão preenchidos
            if nome == "" or email == "" or senha == "" or confirmar_senha == "":
                self.mensgem = tk.Label(self.frame, text="Preencha todos os campos!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                self.mensgem.pack(pady=10)
                return

            # Verifica se as senhas são iguais
            if senha != confirmar_senha:
                self.mensgem = tk.Label(self.frame, text="Senhas não conferem!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                self.mensgem.pack(pady=10)
                return
            
            # Verifica se o email é válido
            if "@" not in email or "." not in email or " " in email:
                self.mensgem = tk.Label(self.frame, text="Email inválido!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                self.mensgem.pack(pady=10)
                return
            
            # Verifica se o email já está cadastrado
            cursor = app.conn.cursor()
            cursor.execute(f"SELECT * FROM usuarios WHERE email='{email}'")
            resultado = cursor.fetchall()
            if len(resultado) > 0:
                self.mensgem = tk.Label(self.frame, text="Email já cadastrado!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                self.mensgem.pack(pady=10)
                return
            
            # Insere o novo usuário no banco de dados
            try:
                api_key = self.gerar_nova_api_key()
                cursor.execute(f"INSERT INTO usuarios (nome, email, senha, api_key) VALUES ('{nome}', '{email}', '{senha}', '{api_key}')")
                app.conn.commit()
                self.mensgem = tk.Label(self.frame, text="Conta criada com sucesso!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="green")
                self.mensgem.pack(pady=10)
            except:
                print("Erro ao criar conta")
                self.mensgem = tk.Label(self.frame, text="Erro ao criar conta!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                self.mensgem.pack(pady=10)

                
                



        altura = 30
        largura = 120

        btn_ok = RoundedButton(self.frame, text="Criar conta", command=criar_nova_conta, radius=altura/3, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 13, "bold"), width=largura, height=altura)
            
        btn_ok.pack(pady=20)

        criarBackButton(self, app, address="LoginScreen")

    def gerar_nova_api_key(self):
        return "RPL2ZTY8XIPB5YFJ"
    
    

    




