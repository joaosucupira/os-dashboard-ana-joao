
import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton
from Views.TabelaProcessosView import TabelaProcessosView

class ViewPrincipal(ctk.CTk):
    def __init__(self, abrir_tabela_callback, abrir_memoria_callback):
        super().__init__()
        self.title("Stich Dashboard - Tela inicial")
        self.geometry("1100x500")

        self.label = CTkLabel(self, text="Bem-vindo ao Stitch Dashboard", font=("Arial", 18, "bold"))
        self.label.pack(pady=(30, 20))

        # processos
        self.btn_tabela = CTkButton(self, text="Ver Tabela de Processos", command=abrir_tabela_callback)
        self.btn_tabela.pack(pady=10)

        # memoria
        self.btn_memoria = CTkButton(self, text="Ver Informacoes de Memoria", command=abrir_memoria_callback)
        self.btn_memoria.pack(pady=10)


    def outra_funcionalidade(self):
        # Implemente aqui outras funcionalidades conforme os requisitos
        pass