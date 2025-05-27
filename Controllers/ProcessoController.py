import threading
import time

from Models.GerenciadorProcessos import GerenciadorProcessos
from Views.TabelaProcessosView import TabelaProcessosView

from Controllers.DetalhesProcController import DetalhesProcController
from Views.DetalhesProcessoView import DetalhesProcessoView

class ProcessoController:
    def __init__(self, master):
        self.inicializa(master)

    def coletar_processos_em_thread(self):
        while not self._stop_event.is_set():
            processos = self.model.listar_processos_e_usuarios()
            with self._lock:  # protege o acesso a lista de processos
                self._processos = processos
            time.sleep(0.5)  # coleta a cada 2 segundos

    def atualizar_interface(self):
        with self._lock:
            processos = list(self._processos)  # copia segura
            
        self.view.mostrar_processos(processos)
        
        if self.view.winfo_exists():
            self.view.after(500, self.atualizar_interface)

    def fechar(self):
        self._stop_event.set()
        self.view.destroy()

    def inicializa(self, master):
        self.model = GerenciadorProcessos()
        self.view = TabelaProcessosView(master=master)

        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._processos = []

        self._thread = threading.Thread(target=self.coletar_processos_em_thread, daemon=True)
        self._thread.start()

        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    def exibir_detalhes_processo(self, pid, master):
        DetalhesProcController(pid, master)