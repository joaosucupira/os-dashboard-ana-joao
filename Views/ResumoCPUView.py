import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ResumoCPUView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Resumo do Processador")
        self.geometry("600x400")
        self.label = ctk.CTkLabel(self, text="Resumo do Uso do Processador", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        self.fig, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()
        self.info_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)

    def atualizar(self, uso, ocioso, n_proc, n_threads):
        if not hasattr(self, "ax") or not hasattr(self, "canvas"):
            return
        self.ax.clear()
        self.ax.pie([uso, ocioso], labels=["Uso", "Ocioso"], autopct="%1.1f%%", colors=["#ff9999","#99ff99"])
        self.ax.set_title("CPU")
        self.canvas.draw()
        self.info_label.configure(text=f"Processos: {n_proc} | Threads: {n_threads}")

    def destroy(self):
        # Fecha o canvas do matplotlib antes de destruir a janela
        try:
            self.canvas.get_tk_widget().destroy()
            plt.close(self.fig)
        except Exception:
            pass
        super().destroy()