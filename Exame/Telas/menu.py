import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root)
        self.app = app

        # Título
        label_title = tk.Label(self, text="Menu Principal", font=("Arial", 16))
        label_title.pack(pady=10)

        # Placeholder de opções
        label_msg = tk.Label(self, text="Aqui irão as opções do menu.")
        label_msg.pack(pady=20)
