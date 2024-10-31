import tkinter as tk
# from traducaoTkInter import *
from Telas.loginPage import LoginScreen


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App de Finanças")
        self.root.geometry("400x300")
        
        # Iniciar com a tela de login
        self.current_frame = None
        self.show_frame(LoginScreen)
        self.usuario = None
    
    def show_frame(self, frame_class):
        """Troca as telas."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True,)
    
    def run(self):
        self.root.mainloop()


# class App:
#     def __init__(self):
#         self.root = tela("App de Finanças", 400, 300).get_tela()
        
#         # Iniciar com a tela de login
#         self.current_frame = None
#         self.show_frame(LoginScreen)
#         self.usuario = None

#     def show_frame(self, frame_class):
#         """Troca as telas."""
#         if self.current_frame is not None:
#             self.current_frame.destroy()
#         self.current_frame = frame_class(self)
#         self.current_frame.pack(fill="both", expand=True)

#     def run(self):
#         self.root.mainloop()