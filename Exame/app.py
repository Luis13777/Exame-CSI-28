import tkinter as tk
from Telas.loginPage import LoginScreen
from Telas.menu import MainMenu
from Telas.adicionarGastos import AdicionarGasto
from Telas.editarGastos import EditarGastos
from Telas.consultarGastos import consultarGastos
from Telas.editarPerfil import editarPerfil
from Telas.investimentos import ConsultaAcoes
from Telas.adicionarInvestimentos import AdicionarInvestimentos
from Telas.removerInvestimentos import RemoverInvestimentos
from Telas.registerPage import RegisterScreen
from BancoDeDados import *


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App de Finanças")
        self.root.geometry("900x700")
        
        # Iniciar com a tela de login
        self.current_frame = None
        self.usuario = None

        self.conn = conectar_ao_sql_server()

        self.show_frame("LoginScreen")
    
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        if frame_class == "LoginScreen":
            self.current_frame = LoginScreen(self)
        elif frame_class == "MainMenu":
            self.current_frame = MainMenu(self)
        elif frame_class == "AdicionarGasto":
            self.current_frame = AdicionarGasto(self)
        elif frame_class == "EditarGasto":
            self.current_frame = EditarGastos(self)
        elif frame_class == "ConsultarGastos":
            self.current_frame = consultarGastos(self)
        elif frame_class == "EditarPerfil":
            self.current_frame = editarPerfil(self)
        elif frame_class == "Investimentos":
            self.current_frame = ConsultaAcoes(self)
        elif frame_class == "AdicionarInvestimentos":
            self.current_frame = AdicionarInvestimentos(self)
        elif frame_class == "RemoverInvestimentos":
            self.current_frame = RemoverInvestimentos(self)
        elif frame_class == "RegisterScreen":
            self.current_frame = RegisterScreen(self)

        self.current_frame.pack(fill="both", expand=True)

    
    def run(self):
        self.root.mainloop()