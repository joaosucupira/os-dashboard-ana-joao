import threading
import time

from Models.DetalhesProcesso import DetalhesProcesso
from Views.DetalhesProcessoView import DetalhesProcessoView

class DetalhesProcController:
    def __init__(self, pid, master):
        self.pid = pid
        self.master = master
        self.model = DetalhesProcesso(pid)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._detalhes = {}
        self._threads = []
        self._thread = threading.Thread(target=self.coletar_detalhes_em_thread, daemon=True)
        self._thread.start()
        # Aguarda a primeira coleta antes de criar a view
        while not self._detalhes:
            time.sleep(0.05)
        self.view = DetalhesProcessoView(master=self.master, detalhes_dict=self._detalhes, threads_list=self._threads)
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    def coletar_detalhes_em_thread(self):
        while not self._stop_event.is_set():
            detalhes = self.model.carregar_detalhes_processo()
            threads = self.model.get_info_threads()
            with self._lock:
                self._detalhes = detalhes
                self._threads = threads
            time.sleep(1)  # Atualiza a cada 1 segundo

    def atualizar_interface(self):
        with self._lock:
            detalhes = dict(self._detalhes)
            threads = list(self._threads)
        if hasattr(self.view, "atualizar_detalhes"):
            self.view.atualizar_detalhes(detalhes, threads)
        if self.view.winfo_exists():
            self.view.after(1000, self.atualizar_interface)

    def fechar(self):
        self._stop_event.set()
        self.view.destroy()