# Exemplo de trecho para DetalhesProcessoView

import customtkinter as ctk
from customtkinter import CTkLabel, CTkTextbox, CTkFrame

class DetalhesProcessoView(ctk.CTkToplevel):
    def __init__(self, master, detalhes_dict, threads_list):
        super().__init__(master=master)
        self.title(f"Detalhes do Processo PID {detalhes_dict.get('pid', '')}")
        self.geometry("700x500")
        self.resizable(False, True)

        # Detalhes principais
        frame_detalhes = CTkFrame(self)
        frame_detalhes.pack(fill="x", padx=20, pady=(20, 10))
        texto = (
            f"Nome: {detalhes_dict.get('nome', '?')}\n"
            f"Usuário: {detalhes_dict.get('usuario', '?')}\n"
            f"Estado: {detalhes_dict.get('estado', '?')}\n"
            f"Prioridade: {detalhes_dict.get('prioridade', '?')}\n"
            f"Threads: {detalhes_dict.get('threads', '?')}\n"
            f"Memória (KB): {detalhes_dict.get('memoria_kb', '?')}\n"
            f"Tempo CPU (s): {detalhes_dict.get('cpu_s', '?')}\n"
            f"%CPU: {detalhes_dict.get('cpu_percent', '?')}\n"
        )
        CTkLabel(frame_detalhes, text=texto, font=("Arial", 14), anchor="w", justify="left").pack(anchor="w")

        # Threads
        frame_threads = CTkFrame(self)
        frame_threads.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        CTkLabel(frame_threads, text="Threads:", font=("Arial", 14, "bold"), anchor="w").pack(anchor="w")

        threads_box = CTkTextbox(frame_threads, width=640, height=300, font=("Courier New", 12))
        threads_box.pack(fill="both", expand=True)
        threads_box.insert("end", f"{'TID':<10}{'Nome':<20}{'Estado':<10}\n")
        threads_box.insert("end", "-"*45 + "\n")
        for t in threads_list:
            threads_box.insert("end", f"{t.get('tid','?'):<10}{t.get('name','?'):<20}{t.get('state','?'):<10}\n")
        threads_box.configure(state="disabled")