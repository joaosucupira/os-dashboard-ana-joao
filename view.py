# Visualização despreocupada com a regra de negócio voltada apenas para receber e
# disponibilizar informações de maneira fluída, correta e interligada.
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Tkinter")
app.geometry("400x400")

label = ctk.CTkLabel(app, text="Funciona!", font=("Arial", 18))
label.pack(pady=50)

# Botão
def clique():
    label.configure(text="Você clicou no botão!")

button = ctk.CTkButton(app, text="Clique Aqui", command=clique)
button.pack(pady=10)

# Caixa de entrada
entry = ctk.CTkEntry(app, placeholder_text="Digite algo...")
entry.pack(pady=10)

# Checkbox
checkbox = ctk.CTkCheckBox(app, text="Ativar algo")
checkbox.pack(pady=10)

# Loop
app.mainloop()



# class View:
#     def __init__(self):
#         pass