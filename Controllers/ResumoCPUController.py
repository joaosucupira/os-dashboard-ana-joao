from Models.GerenciadorCPU import GerenciadorCPU
from Views.ResumoCPUView import ResumoCPUView

class ResumoCPUController:
    def __init__(self, master):
        self.model = GerenciadorCPU()
        self.view = ResumoCPUView(master=master)
        self.atualizando = True
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar()

    def atualizar(self):
        if not self.atualizando or not self.view.winfo_exists():
            return
        uso, ocioso = self.model.calcular_percentuais()
        n_proc, n_threads = self.model.contar_processos_threads()
        self.view.atualizar(uso, ocioso, n_proc, n_threads)
        self.view.after(500, self.atualizar)

    def fechar(self):
        self.atualizando = False
        self.view.destroy()