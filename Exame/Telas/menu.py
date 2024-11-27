import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from BancoDeDados import *
from Elementos.botoes import *
from PIL import ImageTk, Image

class MainMenu(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#e3e3e3")
        self.app = app
        self.conn = self.app.conn
        
        # Ajustando para tela cheia
        app.root.geometry("700x480")  # Começar com uma resolução padrão
        app.root.state("zoomed")  # Garantir que o app comece em tela cheia

        # Criando a imagem de fundo que se adapta ao tamanho da janela
        self.background_label = tk.Label(self)
        self.background_label.place(relwidth=1, relheight=1)  # Faz com que a imagem ocupe toda a tela

        # Atualizar a imagem de fundo sempre que a janela for redimensionada
        self.bind("<Configure>", self.on_resize)

        # Título
        label_title = tk.Label(self, text=f"Bem-vindo {self.get_usuario_id()}", font=("Archivo", 24, "bold"), bg="#051357", fg="#ffffff", bd=0)
        label_title.pack(pady=20)
        self.label_title = label_title

        # Frame para os botões de opções
        self.options_frame = tk.Frame(self, bg="#ffffff", bd=0)
        self.options_frame.pack(fill="both", expand=True)

        # Botões de opções
        self.create_option_buttons()

        # Variável de controle para o estado do menu lateral
        self.menu_open = False

        self.create_sidebar()

        # Botão que alterna o menu lateral
        self.toggle_btn = tk.Button(self, text="☰", command=self.toggle_sidebar, bg="#601E88", fg="white", padx=10, pady=5, font=("Arial", 16), bd=0)
        self.toggle_btn.place(x=10, y=10)

    # def on_resize(self, event):
    #     # Redimensionar a imagem de fundo conforme o tamanho da janela
    #     largura = event.width
    #     altura = event.height
    #     imagem = Image.open("C:\\Users\\death\\OneDrive\\Documentos\\GitHub\\Exame-CSI-28\\Exame\\Telas\\Imagens\\menu6.jpg", mode="r")
    #     imagem = imagem.resize((largura, altura))  # Redimensionando imagem para cobrir a tela
    #     imagem = ImageTk.PhotoImage(imagem)
    #     self.background_label.config(image=imagem)
    #     self.background_label.image = imagem

    # def create_sidebar(self):
    #     # Criar um frame para o menu lateral
    #     self.sidebar = tk.Frame(self, bg="#601E88", width=200, bd=0)
    #     self.sidebar.place(x=-200, y=0, relheight=1)  # A barra lateral cobre toda a altura da tela

    #     # Imagem para o menu lateral
    #     imagem = Image.open("C:\\Users\\death\\OneDrive\\Documentos\\GitHub\\Exame-CSI-28\\Exame\\Telas\\Imagens\\side_img.png", mode="r")
    #     imagem = imagem.resize((300, 480))  # Ajuste da imagem de fundo da sidebar
    #     imagem = ImageTk.PhotoImage(imagem)
    #     frame = tk.Label(self.sidebar, image=imagem)
    #     frame.image = imagem
    #     frame.place(x=0, y=0)

    #     # Frame para os botões da sidebar
    #     self.box_de_botoes = tk.Frame(self.sidebar, bg="#601E88")
    #     self.box_de_botoes.pack(fill="x", expand=False, pady=75)

    #     # Botões da sidebar
    #     self.btn_logout = tk.Button(self.box_de_botoes, text="Logout", command=self.logout, bg="#601E88", fg="white", font=("Archivo", 12), padx=10, pady=10, bd=0)
    #     self.editar_perfil = tk.Button(self.box_de_botoes, text="Editar Perfil", command=self.editar_perfil, bg="#601E88", fg="white", font=("Archivo", 12), padx=10, pady=10, bd=0)

    #     self.editar_perfil.pack(fill="x", pady=10, padx=20)
    #     self.btn_logout.pack(fill="x", pady=10, padx=20)

    def create_option_buttons(self):
        largura = 300

        # Definir os botões de opções
        btn_consultar = RoundedButton(self.options_frame, text="Consultar Gastos", command=self.show_chart, radius=20, bg="#601E88", hover_bg="#6666ff", fg="white", font=("Archivo", 14, "bold"), width=largura, height=60)
        btn_adicionar_gastos = RoundedButton(self.options_frame, text="Adicionar Gastos", command=self.adicionar_gasto, radius=20, bg="#601E88", hover_bg="#6666ff", fg="white", font=("Archivo", 14, "bold"), width=largura, height=60)
        btn_editar_gastos = RoundedButton(self.options_frame, text="Editar Gastos", command=self.editar_remover_gasto, radius=20, bg="#601E88", hover_bg="#6666ff", fg="white", font=("Archivo", 14, "bold"), width=largura, height=60)
        btn_consultar_investimentos = RoundedButton(self.options_frame, text="Consultar Investimentos", command=self.investimentos, radius=20, bg="#601E88", hover_bg="#6666ff", fg="white", font=("Archivo", 14, "bold"), width=largura, height=60)
        btn_adicionar_investimentos = RoundedButton(self.options_frame, text="Adicionar Investimentos", command=self.add_investimentos, radius=20, bg="#601E88", hover_bg="#6666ff", fg="white", font=("Archivo", 14, "bold"), width=largura, height=60)
        btn_remover_investimentos = RoundedButton(self.options_frame, text="Remover Investimentos", command=self.remover_investimentos, radius=20, bg="#601E88", hover_bg="#6666ff", fg="white", font=("Archivo", 14, "bold"), width=largura, height=60)

        # Usando grid para os botões
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=5)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # Posicionando os botões na grid
        btn_consultar.grid(row=0, column=0, sticky="n", padx=5, pady=20)
        btn_adicionar_gastos.grid(row=0, column=1, sticky="n", padx=5, pady=20)
        btn_editar_gastos.grid(row=1, column=0, sticky="n", padx=5, pady=20)
        btn_consultar_investimentos.grid(row=1, column=1, sticky="n", padx=5, pady=20)
        btn_adicionar_investimentos.grid(row=2, column=0, sticky="n", padx=5, pady=20)
        btn_remover_investimentos.grid(row=2, column=1, sticky="n", padx=5, pady=20)

    def show_chart(self):
        self.app.show_frame("ConsultarGastos")

    def on_resize(self, event):
        # Redimensionar a imagem de fundo conforme o tamanho da janela
        largura = event.width
        altura = event.height

        # Redimensiona a imagem de fundo
        imagem = Image.open("C:\\Users\\death\\OneDrive\\Documentos\\GitHub\\Exame-CSI-28\\Exame\\Telas\\Imagens\\menu6.jpg", mode="r")
        imagem = imagem.resize((largura, altura))  # Redimensionando imagem para cobrir a tela
        imagem = ImageTk.PhotoImage(imagem)
        self.background_label.config(image=imagem)
        self.background_label.image = imagem

        # Redimensionar a imagem da sidebar quando a janela for redimensionada
        if hasattr(self, 'sidebar_image'):  # Verifica se já existe a imagem da sidebar
            sidebar_imagem = Image.open("C:\\Users\\death\\OneDrive\\Documentos\\GitHub\\Exame-CSI-28\\Exame\\Telas\\Imagens\\side_img.png", mode="r")
            sidebar_imagem = sidebar_imagem.resize((200, altura))  # A sidebar tem altura completa, largura fixa
            sidebar_imagem = ImageTk.PhotoImage(sidebar_imagem)
            self.sidebar_image_label.config(image=sidebar_imagem)
            self.sidebar_image_label.image = sidebar_imagem

    def create_sidebar(self):
        # Criar um frame para o menu lateral
        self.sidebar = tk.Frame(self, bg="#601E88", width=200, bd=0)
        self.sidebar.place(x=-200, y=0, relheight=1)  # A barra lateral cobre toda a altura da tela
        largura_tela = self.app.root.winfo_screenwidth()
        altura_tela = self.app.root.winfo_screenheight()
        # Imagem para o menu lateral
        sidebar_imagem = Image.open("C:\\Users\\death\\OneDrive\\Documentos\\GitHub\\Exame-CSI-28\\Exame\\Telas\\Imagens\\side_img.png", mode="r")
        sidebar_imagem = sidebar_imagem.resize((int(largura_tela*0.15), int(altura_tela)))  # Ajuste inicial da imagem de fundo da sidebar
        sidebar_imagem = ImageTk.PhotoImage(sidebar_imagem)
        
        # Adiciona a imagem no label
        self.sidebar_image_label = tk.Label(self.sidebar, image=sidebar_imagem)
        self.sidebar_image_label.image = sidebar_imagem
        self.sidebar_image_label.place(x=0, y=0)

        # Frame para os botões da sidebar
        self.box_de_botoes = tk.Frame(self.sidebar, bg="#601E88")
        self.box_de_botoes.pack(fill="x", expand=False, pady=75)

        # Botões da sidebar
        self.btn_logout = tk.Button(self.box_de_botoes, text="Logout", command=self.logout, bg="#601E88", fg="white", font=("Archivo", 12), padx=10, pady=10, bd=0)
        self.editar_perfil = tk.Button(self.box_de_botoes, text="Editar Perfil", command=self.editar_perfil, bg="#601E88", fg="white", font=("Archivo", 12), padx=10, pady=10, bd=0)

        self.editar_perfil.pack(fill="x", pady=10, padx=20)
        self.btn_logout.pack(fill="x", pady=10, padx=20)

    def toggle_sidebar(self):
        self.sidebar.tkraise()
        self.toggle_btn.tkraise()
        if self.menu_open:
            # Animação para fechar o menu lateral
            for i in range(0, 201, 20):
                self.sidebar.place(x=-i, y=0, relheight=1)
                self.update()
            self.menu_open = False
        else:
            # Animação para abrir o menu lateral
            for i in range(-200, 1, 20):
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update()
            self.menu_open = True

        

    # def toggle_sidebar(self):
    #     self.sidebar.tkraise()
    #     self.toggle_btn.tkraise()
    #     if self.menu_open:
    #         # Animação para fechar o menu lateral
    #         for i in range(0, 201, 20):
    #             self.sidebar.place(x=-i, y=0, relheight=1)
    #             self.update()
    #         self.menu_open = False
    #     else:
    #         # Animação para abrir o menu lateral
    #         for i in range(-200, 1, 20):
    #             self.sidebar.place(x=i, y=0, relheight=1)
    #             self.update()
    #         self.menu_open = True

    def get_usuario_id(self):
        email_usuario = self.app.usuario
        query = f"SELECT nome FROM usuarios WHERE email = '{email_usuario}'"
        cursor = self.conn.cursor()
        cursor.execute(query)
        usuario_id = cursor.fetchone()[0]
        return usuario_id

    def adicionar_gasto(self):
        self.app.show_frame("AdicionarGasto")

    def editar_remover_gasto(self):
        self.app.show_frame("EditarGasto")

    def editar_perfil(self):
        self.app.show_frame("EditarPerfil")

    def investimentos(self):
        self.app.show_frame("Investimentos")

    def add_investimentos(self):
        self.app.show_frame("AdicionarInvestimentos")

    def remover_investimentos(self):
        self.app.show_frame("RemoverInvestimentos")

    def logout(self):
        self.app.usuario = None
        self.app.show_frame("LoginScreen")
