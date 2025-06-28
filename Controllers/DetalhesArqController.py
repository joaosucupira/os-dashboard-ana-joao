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
        self._arquivos = []
        self._sockets = []
        self._mutexes = []
        self._thread = threading.Thread(target=self.coletar_detalhes_em_thread, daemon=True)
        self._thread.start()
        # Aguarda a primeira coleta antes de criar a view
        while not self._arquivos:
            time.sleep(0.05)

        self.view = DetalhesArquivosView(master=self.master, arquivos_list=self._arquivos, sockets_list=self._sockets, mutexes_list=self._mutexes, pid=self.pid)
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    def coletar_detalhes_em_thread(self):
        while not self._stop_event.is_set():
            self.model.carregar_detalhes_processo()
            arquivos = self.model.get_info_arquivos()
            with self._lock:
                self._arquivos = arquivos
            time.sleep(1)  # Atualiza a cada 1 segundo

    def atualizar_interface(self):
        with self._lock:
            arquivos = list(self._arquivos)
        if hasattr(self.view, "atualizar_detalhes"):
            self.view.atualizar_detalhes(arquivos)
        if self.view.winfo_exists():
            self.view.after(1000, self.atualizar_interface)

    def fechar(self):
        self._stop_event.set()
        self.view.destroy()