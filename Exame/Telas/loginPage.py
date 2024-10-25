import tkinter as tk
from tkinter import messagebox, font
from BancoDeDados import *
from Telas.menu import *


class LoginScreen(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        # Criando uma fonte personalizada
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Frame para a centralização dos elementos
        self.frame = tk.Frame(app.root, bg="#ffffff", padx=20, pady=20, relief="flat", bd=2)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título estilizado
        label_title = tk.Label(self.frame, text="Login", font=self.title_font, bg="#ffffff", fg="#333333")
        label_title.pack(pady=20)

        # Caixa de texto para o nome de usuário
        self.entry_username = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 12), bd=1, relief="flat")
        self.entry_username.pack(pady=10, ipadx=5, ipady=5, fill="x")
        self.entry_username.insert(0, "Email")


        # Caixa de texto para a senha
        self.entry_password = tk.Entry(self.frame, show="*", bg="#f0f0f0", fg="#333333", font=("Arial", 12), bd=1, relief="flat")
        self.entry_password.pack(pady=10, ipadx=5, ipady=5, fill="x")
        self.entry_password.insert(0, "Senha")

        # Botão estilizado com efeito de hover
        self.btn_login = tk.Button(self.frame, text="Entrar", font=self.button_font, bg="#3333cc", fg="#ffffff",
                                   activebackground="#6666ff", activeforeground="#ffffff", bd=0, padx=10, pady=10,
                                   relief="flat", cursor="hand2", command=self.login)
        self.btn_login.pack(pady=20, ipadx=50, ipady=5)

        # Adicionando efeito de hover ao botão
        self.btn_login.bind("<Enter>", self.on_enter)
        self.btn_login.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget['background'] = '#6666ff'  # Cor ao passar o mouse

    def on_leave(self, event):
        event.widget['background'] = '#3333cc'  # Cor normal do botão

    def login(self):

        self.app.usuario = "luis@email.com"
        self.app.show_frame(MainMenu)

        return

        username = self.entry_username.get()
        password = self.entry_password.get()
        # Se o login for bem-sucedido

        conn = conectar_ao_sql_server()

        resultado = consultar_usuarios(conn, username)
        if resultado is not None:
            if resultado['senha'].values[0] == password:
                self.app.usuario = username
                self.app.show_frame(MainMenu)
            else:
                messagebox.showerror("Erro", "Login falhou.")
        else:
            messagebox.showerror("Erro", "Login falhou.")

        conn.close()

    def run(self):
        self.root.mainloop()


