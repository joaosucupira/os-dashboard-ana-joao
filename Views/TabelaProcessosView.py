import customtkinter as ctk
from customtkinter import CTkLabel, CTkTextbox

class TabelaProcessosView(ctk.CTkToplevel):
    def __init__(self, master=None, callback_acao_linha=None):
        super().__init__(master=master)
        self.monta_tabela()
        self.processos_atuais = []
        self.callback_acao_linha = callback_acao_linha 

    def mostrar_processos(self, processos):
        self.processos_atuais = list(processos)
        scroll_pos = self.tabela.yview()

        self.tabela.configure(state="normal")
        self.tabela.delete("0.0", "end")
        for proc in processos:
            linha_texto = f"{str(proc['pid']):<10}{str(proc['nome'])[:31]:<40}{str(proc['usuario'])[:21]:<22}{str(proc['threads']):<10}{str(proc['estado']):<15}{str(proc['cpu_s']):<16}{proc['mem_kb']/1024:<13.2f}   ●\n"
            self.tabela.insert("end", linha_texto)

        self.tabela.configure(state="disabled")
        self.tabela.yview_moveto(scroll_pos[0])

    def monta_header(self):
        header_text = f"{'PID':<10}{'Nome':<40}{'Usuário':<22}{'Threads':<10}{'Estado':<15}{'Tempo CPU(s)':<16}{'Mem (MB)':<13}"
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
        self.title("Processos ativos")
        self.geometry("1100x600")
        self.header = self.monta_header()
        self.header.pack(fill="x", padx=10, pady=(0, 10))
        self.tabela = CTkTextbox(self, width=1050, height=520, font=("Courier New", 14))
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 0))
        self.tabela.bind("<Button-1>", self.on_click_linha)
    
    def on_click_linha(self, event):

        index = self.tabela.index(f"@{event.x},{event.y}")
        linha = int(str(index).split('.')[0]) - 1  # -1 porque começa do 1
        if 0 <= linha < len(self.processos_atuais):
            proc = self.processos_atuais[linha]
            self.acao_linha(proc)

    def acao_linha(self, proc):
        if self.callback_acao_linha:
            self.callback_acao_linha(proc)
        else:
            print(f"Processo clicado: PID={proc['pid']}, Nome={proc['nome']}")