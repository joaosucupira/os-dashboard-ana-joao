
import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton
from Views.TabelaProcessosView import TabelaProcessosView

class ViewPrincipal(ctk.CTk):
    def __init__(self, abrir_tabela_callback):
        super().__init__()
        self.title("Stich Dashboard - Tela inicial")
        self.geometry("1100x500")

        self.label = CTkLabel(self, text="Bem-vindo ao Stitch Dashboard", font=("Arial", 18, "bold"))
        self.label.pack(pady=(30, 20))

        # processos
        self.btn_tabela = CTkButton(self, text="Ver Tabela de Processos", command=abrir_tabela_callback)
        self.btn_tabela.pack(pady=10)

        # Exemplo de outros botões para requisitos futuros
        self.btn_outro = CTkButton(self, text="Outra funcionalidade", command=self.outra_funcionalidade)
        self.btn_outro.pack(pady=10)


    def outra_funcionalidade(self):
        # Implemente aqui outras funcionalidades conforme os requisitos
        pass