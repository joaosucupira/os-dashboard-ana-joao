import customtkinter as ctk
from customtkinter import CTkLabel

class TabelaMemoriaView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.monta_tabela()

    def mostrar_memoria(self, dados_memoria):
        """
        Exibe os dados de memória na tabela.
        Espera um dicionário com as chaves:
        total, livre, disponivel, cache, swap_total, swap_livre, swap_usada, uso_percent, uso_real_percent
        """
        self.tabela.delete("0.0", "end")
        linhas = [
            f"Memória Física (RAM):\n",
            f"{dados_memoria["mem_used"]:.2f} GB ({dados_memoria["mem_use_perc"]:.2f}%) de {dados_memoria["mem_total"]:.2f} GB utilizados\n",
            f"{dados_memoria["mem_available_perc"]:.2f}% de memória disponível\n",
            f"Memória cache: {dados_memoria["cached"]:.2f} GB\n",
            f"\nMemória Virtual (SWAP):\n",
            f"{dados_memoria["swap_used"]:.2f} kB ({dados_memoria["swap_use_perc"]:.2f}%) de {dados_memoria["swap_total"]:.2f} GB utilizados\n",
        ]
        for linha in linhas:
            self.tabela.insert("end", linha)

    def monta_header(self):
        header_text = "Resumo do Uso de Memória\n"
        header = CTkLabel(
            self,
            text=header_text,
            fg_color="white",
            text_color="black",
            font=("Courier New", 16, "bold"),
            anchor="w",
            width=650,
            height=30
        )
        return header

    def monta_tabela(self):
        self.title("Memória do Sistema")
        self.geometry("600x400")
        self.header = self.monta_header()
        self.header.pack(fill="x", padx=10, pady=(0, 10))
        self.tabela = ctk.CTkTextbox(self, width=550, height=320, font=("Courier New", 14))
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 0))