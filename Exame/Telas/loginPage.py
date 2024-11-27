import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

class LoginScreen(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.aviso = None

        # Criando uma label para a imagem de fundo
        self.image_label = tk.Label(self)
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Criando uma fonte personalizada
        self.title_font = font.Font(family="Archivo", size=24, weight="bold")
        self.button_font = font.Font(family="Archivo", size=12, weight="bold")
        
        # Frame para a centralização dos elementos
        self.frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20, relief="flat", bd=2)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o frame

        # Título estilizado
        label_title = tk.Label(self.frame, text="Login", font=self.title_font, bg="#ffffff", fg="#601E88")
        label_title.pack(pady=20)

        # Caixa de texto para o nome de usuário
        self.entry_username = tk.Entry(self.frame, bg="#e3e3e3", fg="#601E88", font=("Archivo", 12, "bold"), bd=5, relief="flat")
        self.entry_username.pack(pady=10, ipadx=5, ipady=5, fill="x")
        self.entry_username.insert(0, "Email")

        # Caixa de texto para a senha
        self.entry_password = tk.Entry(self.frame, show="*", bg="#e3e3e3", fg="#601E88", font=("Archivo", 12, "bold"), bd=5, relief="flat")
        self.entry_password.pack(pady=10, ipadx=5, ipady=5, fill="x")
        self.entry_password.insert(0, "Senha")

        # Botão estilizado com efeito de hover
        self.btn_login = tk.Button(self.frame, text="Entrar", font=self.button_font, bg="#601E88", fg="#ffffff",
                                   activebackground="#c9c9c9", activeforeground="#ffffff", bd=0, padx=10, pady=10,
                                   relief="flat", cursor="hand2", command=self.login)
        self.btn_login.pack(pady=20, ipadx=50, ipady=5)

        # Adicionando efeito de hover ao botão
        self.btn_login.bind("<Enter>", self.on_enter)
        self.btn_login.bind("<Leave>", self.on_leave)

        # Botão para criar uma nova conta
        self.btn_criar_conta = tk.Button(self.frame, text="Criar conta", font=self.button_font, bg="#ffffff", bd=0, fg="#3333cc",
                                         relief="flat", cursor="hand2", command=lambda: app.show_frame("RegisterScreen"))
        self.btn_criar_conta.pack()

        self.btn_criar_conta.bind("<Enter>", self.on_enter_criar_conta)
        self.btn_criar_conta.bind("<Leave>", self.on_leave_criar_conta)

        # Atualizar a imagem de fundo no redimensionamento da janela
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Redimensionar a imagem de fundo conforme o tamanho da janela
        largura = event.width
        altura = event.height
        imagem = Image.open("C:\\Users\\death\\OneDrive\\Documentos\\GitHub\\Exame-CSI-28\\Exame\\Telas\\Imagens\\side_img.png", mode="r")
        imagem = imagem.resize((largura, altura))
        imagem = ImageTk.PhotoImage(imagem)
        self.image_label.config(image=imagem)
        self.image_label.image = imagem

    def on_enter_criar_conta(self, event):
        event.widget['fg'] = '#6666ff'

    def on_leave_criar_conta(self, event):
        event.widget['fg'] = '#3333cc'

    def on_enter(self, event):
        event.widget['background'] = '#6666ff'  # Cor ao passar o mouse

    def on_leave(self, event):
        event.widget['background'] = '#601E88'  # Cor normal do botão

    def login(self):
        self.app.usuario = "luis@email.com"
        self.app.show_frame("MainMenu")

        return

        if self.aviso:
            self.aviso.destroy()

        username = self.entry_username.get()
        password = self.entry_password.get()
        # Se o login for bem-sucedido

        if username == "" or password == "":
            self.aviso = tk.Label(self.frame, text="Preencha todos os campos", font=("Arial", 12, "bold"), bg="#ffffff", fg="red")
            self.aviso.pack(pady=10)
            return
        
        conn = self.app.conn

        resultado = consultar_usuarios(conn, username)

        if not resultado.empty:
            if resultado['senha'].values[0] == password:
                self.app.usuario = username
                self.app.show_frame("MainMenu")
            else:
                self.aviso = tk.Label(self.frame, text="Email ou senha errada.", font=("Arial", 12, "bold"), bg="#ffffff", fg="red")
                self.aviso.pack(pady=10)
        else:
            self.aviso = tk.Label(self.frame, text="Email ou senha errada.", font=("Arial", 12, "bold"), bg="#ffffff", fg="red")
            self.aviso.pack(pady=10)
