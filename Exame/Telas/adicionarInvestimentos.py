import tkinter as tk
from Elementos.botoes import *
import requests

class AdicionarInvestimentos(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.mensgemDeNaoConfirmacao = None

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both",  expand=True)
        # self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Campo de descrição
        titulo = tk.Label(self.frame, text="Adicionar Investimento:", bg="#ffffff", font=("Arial", 24, "bold"))
        titulo.pack(pady=(50, 100))

        # Campo de descrição
        label_desc = tk.Label(self.frame, text="Sigla do ativo:", bg="#ffffff", font=("Arial", 12, "bold"))
        label_desc.pack()

        entry_desc = tk.Entry(self.frame, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")
        entry_desc.pack(pady=10, ipadx=5, ipady=5)


        def enviar_dados():

            if self.mensgemDeNaoConfirmacao:
                self.mensgemDeNaoConfirmacao.destroy()

            ativo = entry_desc.get()
            ativo = ativo.replace(" ", "")

            cursor = app.conn.cursor()
            email_usuario = app.usuario
            cursor.execute(f"SELECT * FROM investimentos WHERE usuario_id=(SELECT usuario_id FROM usuarios WHERE email='{email_usuario}') AND simbolo='{ativo}'")
            
            resultado = cursor.fetchall()

            if len(resultado) > 0:
                self.mensgemDeNaoConfirmacao = tk.Label(self.frame, text="Ativo já adicionado!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                self.mensgemDeNaoConfirmacao.pack(pady=10)
            else:
                # verificar se o ativo existe

                api_key = "sua_chave_da_alpha_vantage"  # Substitua pela sua chave de API
                url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ativo}&apikey={api_key}"

                response = requests.get(url)
                data = response.json()


                if not ("bestMatches" in data and len(data["bestMatches"]) > 0):
                    self.mensgemDeNaoConfirmacao = tk.Label(self.frame, text="Ativo não encontrado!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")
                    self.mensgemDeNaoConfirmacao.pack(pady=10)
                    return
                try:
                    cursor = app.conn.cursor()
                    email_usuario = app.usuario
                    cursor.execute(f"INSERT INTO investimentos (usuario_id, simbolo) VALUES ((SELECT usuario_id FROM usuarios WHERE email='{email_usuario}'), '{ativo}')")
                    cursor.commit()

                    # mensagem de confirmação

                    self.mensgemDeNaoConfirmacao = tk.Label(self.frame, text="Ativo adicionado com sucesso!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="green")

                    self.mensgemDeNaoConfirmacao.pack(pady=10)
                    
                    print("Gasto adicionado com sucesso!")

                except Exception as e:
                    print(f"Erro ao adicionar gasto: {e}")

                    self.mensgemDeNaoConfirmacao = tk.Label(self.frame, text="Erro ao adicionar gasto!", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")

                    self.mensgemDeNaoConfirmacao.pack(pady=10)

        altura = 30
        largura = 100

        btn_ok = RoundedButton(self.frame, text="OK", command=enviar_dados, radius=altura/3, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 13, "bold"), width=largura, height=altura)
            
        btn_ok.pack(pady=20)

        criarBackButton(self, app)



    

    




