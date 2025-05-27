from Models.DetalhesProcesso import DetalhesProcesso
from Views.DetalhesProcessoView import DetalhesProcessoView

class DetalhesProcController:
    def __init__(self, pid, master):
        self.model_d =  DetalhesProcesso(pid)
        self.m = master

    def alimenta_view_detalhes(self):
        detalhes = self.model_d.carregar_detalhes_processo()
        threads = self.model_d.carregar_threads()
        view_d = DetalhesProcessoView(self.m, detalhes, threads)        
