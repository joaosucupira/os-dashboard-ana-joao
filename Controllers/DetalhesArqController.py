import threading
import time

from Models.GerenciadorDetalhesArq import GerenciadorDetalhesArq
from Views.DetalhesArquivosView import DetalhesArquivosView

class DetalhesArqController:
    def __init__(self, pid, master):
        self.pid = pid
        self.master = master
        self.model = GerenciadorDetalhesArq(pid)
        self._stop_event = threading.Event()

        # Criação da threads voltada para exibir os arquivos do processo
        self._lock = threading.Lock()
        self._infos = []
        self._thread = threading.Thread(target=self.coletar_detalhes_em_thread, daemon=True)
        self._thread.start()
        # Aguarda a primeira coleta antes de criar a view
        while not self._infos:
            time.sleep(0.05)

        self.view = DetalhesArquivosView(master=self.master, infos_list=self._infos, pid=self.pid)
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    def coletar_detalhes_em_thread(self):
        while not self._stop_event.is_set():
            self.infos = self.model.carregar_detalhes_processo()

            with self._lock:
                self._infos = self.infos
            time.sleep(1)  # Atualiza a cada 1 segundo

    def atualizar_interface(self):
        with self._lock:
            infos = list(self._infos)
        if hasattr(self.view, "atualizar_detalhes"):
            self.view.atualizar_detalhes(infos)
        if self.view.winfo_exists():
            self.view.after(1000, self.atualizar_interface)

    def fechar(self):
        self._stop_event.set()
        self.view.destroy()