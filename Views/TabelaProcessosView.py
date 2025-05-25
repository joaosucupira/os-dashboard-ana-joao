import customtkinter as ctk
from customtkinter import CTkLabel

class TabelaProcessosView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.monta_tabela()


    def mostrar_processos(self, processos):
        self.tabela.delete("0.0", "end")
        for proc in processos:
            linha = f"{str(proc['pid']):<10}{str(proc['nome'])[:31]:<40}{str(proc['usuario'])[:21]:<22}{str(proc['threads']):<10}{str(proc['estado']):<15}{str(proc['cpu_s']):<13}{proc['mem_kb']/1024:<13.2f}\n"
            self.tabela.insert("end", linha)

    def monta_header(self):
        header_text = f"{'PID':<10}{'Nome':<40}{'Usuário':<22}{'Threads':<10}{'Estado':<15}{'CPU (s)':<13}{'Mem (MB)':<13}\n"
        header = CTkLabel(
                    self,
                    text=header_text,
                    fg_color="white",
                    text_color="black",
                    font=("Courier New", 14, "bold"),
                    anchor="w",
                    width=650,
                    height=30
                    )
        return header
    def monta_tabela(self):
        self.title("Processos ativos")
        self.geometry("1100x600")
        self.header = self.monta_header()
        self.header.pack(fill="x", padx=10, pady=(0, 10))
        self.tabela = ctk.CTkTextbox(self, width=1050, height=520, font=("Courier New", 14))
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 0))

