import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

class ResumoCPUView(ctk.CTkToplevel):
    def __init__(self, master=None, max_pontos=60):
        super().__init__(master=master)
        self.title("Resumo do Processador")
        self.geometry("700x450")
        self.label = ctk.CTkLabel(self, text="Resumo do Uso do Processador", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        self.fig, self.ax = plt.subplots(figsize=(6, 3.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=5)
        self.info_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.info_label.pack(pady=5)
        self.uptime_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.uptime_label.pack(pady=5)

        # Histórico do uso de CPU (percentual)
        self.max_pontos = max_pontos
        self.historico_uso = deque([0]*max_pontos, maxlen=max_pontos)
        self.tempo = deque(range(-max_pontos+1, 1), maxlen=max_pontos)

    def atualizar(self, uso, ocioso, n_proc, n_threads, uptime=None):
        # Atualiza histórico
        self.historico_uso.append(uso)
        self.tempo.append(self.tempo[-1] + 1 if self.tempo else 0)

        self.ax.clear()
        self.ax.plot(self.tempo, self.historico_uso, color="#ff9999", label="Uso CPU (%)")
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(self.tempo[0], self.tempo[-1])
        self.ax.set_xlabel("Tempo (atualizações)")
        self.ax.set_ylabel("Uso CPU (%)")
        self.ax.set_title("Uso total de CPU ao longo do tempo")
        self.ax.legend(loc="upper left", fontsize=10, frameon=True)
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.canvas.draw()
        # Info label agora mostra processos, threads e uptime juntos
        info_text = f"Processos: {n_proc} | Threads: {n_threads}"
        if uptime is not None:
            info_text += f" | Uptime do sistema: {self.formatar_uptime(uptime)}"
        else:
            info_text += " | Uptime do sistema: ?"
        self.info_label.configure(text=info_text)

    def formatar_uptime(self, segundos):
        dias = int(segundos // 86400)
        horas = int((segundos % 86400) // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos = int(segundos % 60)
        partes = []
        if dias > 0:
            partes.append(f"{dias}d")
        if horas > 0 or dias > 0:
            partes.append(f"{horas}h")
        if minutos > 0 or horas > 0 or dias > 0:
            partes.append(f"{minutos}m")
        partes.append(f"{segundos}s")
        return " ".join(partes)
    
    def destroy(self):
        try:
            self.canvas.get_tk_widget().destroy()
            plt.close(self.fig)
        except Exception:
            pass
        super().destroy()