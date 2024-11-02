import tkinter as tk
from Telas.loginPage import LoginScreen
from Telas.menu import MainMenu
from Telas.adicionarGastos import AdicionarGasto
from BancoDeDados import *


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App de Finanças")
        self.root.geometry("900x700")
        
        # Iniciar com a tela de login
        self.current_frame = None
        self.show_frame("LoginScreen")
        self.usuario = None

        self.conn = conectar_ao_sql_server()
    
    def show_frame(self, frame_class):
        """Troca as telas."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        if frame_class == "LoginScreen":
            self.current_frame = LoginScreen(self)
        elif frame_class == "MainMenu":
            self.current_frame = MainMenu(self)
        elif frame_class == "AdicionarGasto":
            self.current_frame = AdicionarGasto(self)
        self.current_frame.pack(fill="both", expand=True,)
    
    def run(self):
        self.root.mainloop()

