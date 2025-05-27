import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton

class TabelaProcessosMemoriaView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Tabela de Processos de Memória")
        self.geometry("900x600")
        self.monta_tabela()
        # Adicione aqui o restante da implementação da tabela de processos de memória

    def mostrar_processos(self, processos):
        self.tabela.delete("0.0", "end")
        
        # Definição dos campos e larguras ajustáveis
        campos = [
            ("pid", 8),
            ("nome", 22),
            ("usuario", 16),
            ("memoria_alocada_kb", 20),
            ("memoria_alocada_paginas", 20),
            ("codigo_paginas", 20),
            ("heap_paginas", 20),
            ("stack_paginas", 20)
        ]
        for proc in processos:
            linha = ""
            for campo, largura in campos:
                valor = str(proc.get(campo, ""))[:largura-1]
                linha += f"{valor:<{largura}}"
            linha += "\n"
            self.tabela.insert("end", linha)

    def monta_header(self):
        # Definição dos campos e larguras ajustáveis
        campos = [
            ("PID", 8),
            ("Nome", 22),
            ("Usuário", 16),
            ("Memória (kB)", 20),
            ("Memória (paginas)", 20),
            ("Código (paginas)", 20),
            ("Páginas (paginas)", 20),
            ("Páginas (paginas)", 20)
        ]
        header_text = ""
        for nome, largura in campos:
            header_text += f"{nome:<{largura}}"
        header_text += "\n"
        header = CTkLabel(
                    self,
                    text=header_text,
                    fg_color="white",
                    text_color="black",
                    font=("Courier New", 14, "bold"),
                    anchor="w",
                    width=1050,
                    height=30
                    )
        return header

    def monta_tabela(self):
        self.title("Informações de Memória dos Processos")
        self.geometry("1100x600")
        self.header = self.monta_header()
        self.header.pack(fill="x", padx=10, pady=(0, 10))
        self.tabela = ctk.CTkTextbox(self, width=1050, height=520, font=("Courier New", 14))
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 0))