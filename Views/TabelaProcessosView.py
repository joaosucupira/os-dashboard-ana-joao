# View da tabela de processos e threads

import customtkinter as ctk
from customtkinter import CTkLabel, CTkTextbox

class TabelaProcessosView(ctk.CTkToplevel):
    # Construtora com o callback que vai chamar a rotina de detalhes ao clique do processo
    def __init__(self, master=None, callback_acao_linha=None):
        super().__init__(master=master)
        self.monta_tabela()
        self.processos_atuais = []
        self.callback_acao_linha = callback_acao_linha 

    # Atualização de interface
    def mostrar_processos(self, processos):
        self.processos_atuais = list(processos)
        scroll_pos = self.tabela.yview()

        self.tabela.configure(state="normal")
        self.tabela.delete("0.0", "end")
        for proc in processos:
            linha_texto = (
                f"{proc['pid']:<10}"
                f"{proc['nome'][:31]:<40}"
                f"{proc['usuario'][:21]:<22}"
                f"{proc['threads']:<10}"
                f"{proc['estado']:<15}"
                f"{proc['cpu_s']:<16}\n"
            )
            self.tabela.insert("end", linha_texto)

        self.tabela.configure(state="disabled")
        self.tabela.yview_moveto(scroll_pos[0])

    def monta_header(self):
        header_text = (
            f"{'PID':<10}"
            f"{'Nome':<40}"
            f"{'Usuário':<22}"
            f"{'Threads':<10}"
            f"{'Estado':<15}"
            f"{'Tempo CPU(s)':<16}"
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
        self.title("Processos ativos")
        self.geometry("1000x520")
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
