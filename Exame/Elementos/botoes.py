import tkinter as tk

class RoundedButton(tk.Frame):
    def __init__(self, parent, text, command=None, radius=25, width=200, height=50, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 14, "bold")):
        super().__init__(parent, bg=parent["bg"])
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.fg = fg
        self.radius = radius
        self.width = width
        self.height = height
        self.text = text
        self.font = font


        # Canvas para desenhar o botão arredondado
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, highlightthickness=0, bg=self["bg"])
        self.canvas.pack(expand=True)

        # Desenhando o botão com bordas arredondadas
        self.draw_rounded_rectangle(self.bg)

        # Eventos de clique e hover
        self.canvas.bind("<Button-1>", lambda e: self.on_click())
        self.canvas.bind("<Enter>", lambda e: self.on_hover())
        self.canvas.bind("<Leave>", lambda e: self.on_leave())

    def draw_rounded_rectangle(self, fill):
        """Desenha um retângulo com bordas arredondadas."""
        self.canvas.delete("all")   
        x0 = self.radius
        y0 = 0
        x1 = self.width - self.radius
        y1 = self.height
        
        # Criando o retângulo com bordas arredondadas
        self.button_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="")
        self.canvas.create_oval(0, 0, self.radius * 2, self.radius * 2, fill=fill, outline="")
        self.canvas.create_oval(0, y1 - self.radius * 2, self.radius * 2, y1, fill=fill, outline="")
        self.canvas.create_oval(x1 - self.radius, 0, x1 + self.radius, self.radius * 2, fill=fill, outline="")
        self.canvas.create_oval(x1 - self.radius, y1, x1 + self.radius, y1 - self.radius*2, fill=fill, outline="")

        # Criando a parte superior e inferior
        self.canvas.create_rectangle(0, self.radius, self.radius, y1 - self.radius, fill=fill, outline="")
        self.canvas.create_rectangle(x1 + self.radius, self.radius, x1, y1 - self.radius, fill=fill, outline="")

        # Redesenhando o texto após desenhar o botão
        self.canvas.create_text(self.width // 2, self.height // 2, text=self.text, fill=self.fg, font=self.font)

    def on_click(self):
        if self.command:
            self.command()

    def on_hover(self):
        self.draw_rounded_rectangle(self.hover_bg)

    def on_leave(self):
        self.draw_rounded_rectangle(self.bg)

def criarBackButton(parent, app):
    back_button = RoundedButton(parent, text="←", command=lambda: app.show_frame("MainMenu"), radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 20, "bold"), width=40, height=40)
        
    back_button.place(relx=1.0, y=10, x=-10, anchor="ne")

