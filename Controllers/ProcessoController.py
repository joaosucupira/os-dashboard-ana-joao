import threading
import time
from Models.GerenciadorProcessos import GerenciadorProcessos
from Views.TabelaProcessosView import TabelaProcessosView

class ProcessoController:
    def __init__(self, master):
        self.model = GerenciadorProcessos()
        self.view = TabelaProcessosView(master=master)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()  # Semáforo para proteger dados compartilhados
        self._processos = []
        self._thread = threading.Thread(target=self.coletar_processos_em_thread, daemon=True)
        self._thread.start()
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self._atualizar_interface()

    def coletar_processos_em_thread(self):
        while not self._stop_event.is_set():
            processos = self.model.listar_processos_e_usuarios()
            with self._lock:  # Protege o acesso à lista de processos
                self._processos = processos
            time.sleep(2)  # Coleta a cada 2 segundos

    def _atualizar_interface(self):
        with self._lock:
            processos = list(self._processos)  # Cópia segura
        self.view.mostrar_processos(processos)
        if self.view.winfo_exists():
            self.view.after(2000, self._atualizar_interface)

    def fechar(self):
        self._stop_event.set()
        self.view.destroy()