# Visualização despreocupada com a regra de negócio voltada apenas para receber e
# disponibilizar informações de maneira fluída, correta e interligada.

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class DashboardUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.cria_layout()

        self.cria_botoes()

        self.mostra_mem_cpu()

    def limpar(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostra_mem_cpu(self):
        self.limpar()

        ctk.CTkLabel(self.main_frame, text="CPU e Memória", font=("Arial", 24)).pack(pady=10)

        self.cpu_usage_label = ctk.CTkLabel(self.main_frame, text="Uso de CPU: --%")
        self.cpu_usage_label.pack(pady=5)

        self.cpu_idle_label = ctk.CTkLabel(self.main_frame, text="Tempo Ocioso: --%")
        self.cpu_idle_label.pack(pady=5)

        self.memory_usage_label = ctk.CTkLabel(self.main_frame, text="Uso de Memória: -- MB / -- MB")
        self.memory_usage_label.pack(pady=5)

        self.total_process_label = ctk.CTkLabel(self.main_frame, text="Total de Processos: --")
        self.total_process_label.pack(pady=5)

        self.total_threads_label = ctk.CTkLabel(self.main_frame, text="Total de Threads: --")
        self.total_threads_label.pack(pady=5)

    def lista_processos(self):
        self.limpar()

        ctk.CTkLabel(self.main_frame, text="Lista de Processos", font=("Arial", 24)).pack(pady=10)

        process_listbox = ctk.CTkTextbox(self.main_frame, width=750, height=500)
        process_listbox.pack(pady=10)
        process_listbox.insert("0.0", "PID\tUsuário\tNome do Processo\n")
        process_listbox.insert("end", "--------------------------------------------\n")

    def mostra_detalhes_processo(self):
        self.limpar()

        ctk.CTkLabel(self.main_frame, text="Detalhes do Processo", font=("Arial", 24)).pack(pady=10)

        details_box = ctk.CTkTextbox(self.main_frame, width=750, height=500)
        details_box.pack(pady=10)
        details_box.insert("0.0", "Selecione um processo para ver detalhes...\n")

    def mostra_threads(self):
        self.limpar()

        ctk.CTkLabel(self.main_frame, text="Threads do Processo", font=("Arial", 24)).pack(pady=10)

        threads_box = ctk.CTkTextbox(self.main_frame, width=750, height=500)
        threads_box.pack(pady=10)
        threads_box.insert("0.0", "TID\tStatus\tUso de CPU\n")
        threads_box.insert("end", "-------------------------------\n")

    def cria_layout(self):
        self.title("Dashboard - Sistemas Operacionais S73")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.sidebar_frame = ctk.CTkFrame(self, width=200)
        self.sidebar_frame.pack(side="left", fill="y")
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

    def cria_botoes(self):
        ctk.CTkLabel(self.sidebar_frame, text="Menu", font=("Arial", 20)).pack(pady=10)
        self.cpu_button = ctk.CTkButton(self.sidebar_frame, text="CPU e Memória", command=self.mostra_mem_cpu)
        self.cpu_button.pack(pady=10)
        self.process_button = ctk.CTkButton(self.sidebar_frame, text="Processos", command=self.lista_processos)
        self.process_button.pack(pady=10)
        self.details_button = ctk.CTkButton(self.sidebar_frame, text="Detalhes do Processo", command=self.mostra_detalhes_processo)
        self.details_button.pack(pady=10)
        self.threads_button = ctk.CTkButton(self.sidebar_frame, text="Threads", command=self.mostra_threads)
        self.threads_button.pack(pady=10)

if __name__ == "__main__":
    app = DashboardUI()
    app.mainloop()
