import customtkinter as ctk

class TabelaProcessosView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Processos ativos")
        self.geometry("700x500")
        self.tabela = ctk.CTkTextbox(self, width=650, height=450)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_processos(self, processos):
        self.tabela.delete("0.0", "end")
        header = f"{'PID':<30}{'Usuário':<32}{'Threads':<30}\n"
        self.tabela.insert("end", header)
        self.tabela.insert("end", "-" * 44 + "\n")
        for proc in processos:
            linha = f"{str(proc['pid']):<30}{str(proc['usuario']):<32}{str(proc['threads']):<30}\n"
            self.tabela.insert("end", linha)
