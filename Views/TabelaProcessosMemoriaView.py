import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkTextbox

class TabelaProcessosMemoriaView(ctk.CTkToplevel):
    def __init__(self, master=None, callback_acao_linha=None):
        # Inicializa a janela e configurações iniciais
        super().__init__(master=master)
        self.title("Tabela de Processos")
        self.geometry("1300x520")
        self.monta_tabela()
        self.processos_atuais = []
        self.callback_acao_linha = callback_acao_linha

    def mostrar_processos(self, processos):
        # Atualiza a tabela com a lista de processos recebida
        self.processos_atuais = list(processos)
        scroll_pos = self.tabela.yview()
        self.tabela.configure(state="normal")

        self.tabela.delete("0.0", "end")

        for proc in processos:
            linha_texto = (
                f"{str(proc['pid']):<8}"
                f"{str(proc['nome'])[:25]:<26}"
                f"{str(proc['usuario'])[:18]:<19}"
                f"{str(proc['memoria_alocada_kb']):>12}  "
                f"{str(proc['memoria_alocada_paginas']):>12}  "
                f"{str(proc['codigo_paginas']):>12}  "
                f"{str(proc['heap_paginas']):>12}  "
                f"{str(proc['stack_paginas']):>12}\n"
            )
            self.tabela.insert("end", linha_texto)

        self.tabela.configure(state="disabled")
        self.tabela.yview_moveto(scroll_pos[0])

    def monta_header(self):
        # Definição dos campos e larguras ajustáveis
        header_text = (
            f"{'PID':<8}"
            f"{'Nome':<26}"
            f"{'Usuário':<19}"
            f"{'Memória (kB)':>12}  "
            f"{'Memória (pags.)':>12}  "
            f"{'Código (pags.)':>12}  "
            f"{'Heap (pags.)':>12}  "
            f"{'Stack (pags.)':>12}"
        )
        header = CTkLabel(
                    self,
                    text=header_text,
                    fg_color="white",
                    text_color="black",
                    font=("Courier New", 14, "bold"),
                    anchor="w",
                    width=950,
                    height=30
                    )
        return header

    def monta_tabela(self):
        # Monta o cabeçalho e a área da tabela
        self.header = self.monta_header()
        self.header.pack(fill="x", padx=10, pady=(0, 10))

        # Instancia da tabela
        self.tabela = CTkTextbox(self, width=950, height=520, font=("Courier New", 14))
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 0))
        self.tabela.bind("<Button-1>", self.on_click_linha)

    # Detecção do clique
    def on_click_linha(self, event):
        index = self.tabela.index(f"@{event.x},{event.y}")

        # -1 porque começa do 1
        linha = int(str(index).split('.')[0]) - 1  
        if 0 <= linha < len(self.processos_atuais):
            proc = self.processos_atuais[linha]
            self.acao_linha(proc)

    # Ação que encadeia detalhes
    def acao_linha(self, proc):
        if self.callback_acao_linha:
            self.callback_acao_linha(proc)
        else:
            print(f"Processo clicado: PID={proc['pid']}, Nome={proc['nome']}")