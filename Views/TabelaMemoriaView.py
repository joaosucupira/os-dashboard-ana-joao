import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton

class TabelaMemoriaView(ctk.CTkToplevel):
    def __init__(self, master=None, abrir_tabela_processos_memoria_callback=None):
        super().__init__(master=master)
        self.monta_tabela()
        # Botão para abrir a tabela de processos de memória
        self.btn_tabela_processos = CTkButton(
            self,
            text="Ver Tabela de Processos de Memória",
            command=abrir_tabela_processos_memoria_callback
        )
        self.btn_tabela_processos.pack(pady=10)

    def monta_header(self):
        header_text = (
            "Resumo do Uso de Memória\n"
            f"{'PID':<10}{'Nome':<31}{'Usuário':<21}{'Mem (MB)':<13}{'Páginas':<13}"
            f"{'Código':<13}{'Heap':<13}{'Stack':<13}\n"
            + "─" * (10 + 31 + 21 + 13*5) + "\n"
        )
        header = CTkLabel(
            self,
            text=header_text,
            fg_color="white",
            text_color="black",
            font=("Courier New", 16, "bold"),
            anchor="w",
            width=900,
            height=60
        )
        return header

    def monta_tabela(self):
        self.title("Memória do Sistema")
        self.geometry("900x600")
        self.header = self.monta_header()
        self.header.pack(fill="x", padx=10, pady=(0, 10))
        self.tabela = ctk.CTkTextbox(self, width=880, height=480, font=("Courier New", 14))
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 0))

    def mostrar_memoria(self, dados_memoria):
        self.tabela.delete("0.0", "end")
        linhas = [
            f"Memória Física (RAM):\n",
            f"{dados_memoria['mem_used']:.2f} GB ({dados_memoria['mem_use_perc']:.2f}%) de {dados_memoria['mem_total']:.2f} GB utilizados\n",
            f"{dados_memoria['mem_available_perc']:.2f}% de memória disponível\n",
            f"Memória cache: {dados_memoria['cached']:.2f} GB\n",
            f"\nMemória Virtual (SWAP):\n",
            f"{dados_memoria['swap_used']:.2f} kB ({dados_memoria['swap_use_perc']:.2f}%) de {dados_memoria['swap_total']:.2f} GB utilizados\n",
        ]
        for linha in linhas:
            self.tabela.insert("end", linha)