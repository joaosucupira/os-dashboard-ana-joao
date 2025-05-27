import customtkinter as ctk

class TabelaProcessosMemoriaView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Tabela de Processos de Memória")
        self.geometry("900x600")
        # Adicione aqui o restante da implementação da tabela de processos de memória