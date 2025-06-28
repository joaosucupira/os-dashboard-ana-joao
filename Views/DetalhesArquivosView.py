import customtkinter as ctk
from customtkinter import CTkLabel, CTkTextbox, CTkFrame

class DetalhesArquivosView(ctk.CTkToplevel):
    def __init__(self, master, arquivos_list, sockets_list, mutexes_list, pid):
        super().__init__(master=master)
        self.title(f'Detalhes do processo {str(pid)}')
        self.geometry("1000x500")
        self.resizable(False, True)

        frame_arquivos = CTkFrame(self)
        frame_arquivos.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        CTkLabel(frame_arquivos, text="Arquivos:", font=("Arial", 14, "bold"), anchor="w").pack(anchor="w")
        arquivos_box = CTkTextbox(frame_arquivos, width=640, height=300, font=("Courier New", 12))
        arquivos_box.pack(fill="both", expand=True)

        header = f"{'FD':<10}{'CAMINHO'}\n"
        arquivos_box.insert("end", header)
        arquivos_box.insert("end", "="*130 + "\n")

        for a in arquivos_list:
            arquivos_box.insert("end", f"{a.get('fd','?'):<10}{a.get('caminho','?')}\n")
        arquivos_box.configure(state="disabled")