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
            f"{'Memória Física Total:':<30}{dados_memoria.get('total', 0):>10.2f} GB\n",
            f"{'Memória Física Livre:':<30}{dados_memoria.get('livre', 0):>10.2f} GB\n",
            f"{'Memória Física Disponível:':<30}{dados_memoria.get('disponivel', 0):>10.2f} GB\n",
            f"{'Memória Cache:':<30}{dados_memoria.get('cache', 0):>10.2f} GB\n",
            f"{'Swap Total:':<30}{dados_memoria.get('swap_total', 0):>10.2f} GB\n",
            f"{'Swap Livre:':<30}{dados_memoria.get('swap_livre', 0):>10.2f} GB\n",
            f"{'Swap Usada:':<30}{dados_memoria.get('swap_usada', 0):>10.2f} GB\n",
            f"{'Uso de Memória (%):':<30}{dados_memoria.get('uso_percent', 0):>10.2f} %\n",
            f"{'Uso Real de Memória (%):':<30}{dados_memoria.get('uso_real_percent', 0):>10.2f} %\n",
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