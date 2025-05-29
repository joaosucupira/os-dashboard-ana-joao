import threading
import time

from Models.GerenciadorDetalhesMemoria import GerenciadorDetalhesMemoria
from Views.DetalhesMemoriaView import DetalhesMemoriaView

class DetalhesMemoriaController:
    def __init__(self, pid, master):
        self.pid = pid
        self.master = master

        # Instancia do model que puxa os dados de memoria
        self.model = GerenciadorDetalhesMemoria(pid) # Solicita os detalhes do processo identificado por pid
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._detalhes = {}
        self._threads = []
        self._thread = threading.Thread(target=self.coletar_detalhes_em_thread, daemon=True)
        self._thread.start()
        # Aguarda a primeira coleta antes de criar a view
        while not self._detalhes:
            time.sleep(0.05)


        # Passa aqui para a view as informações de processos, threads e o pid
        self.view = DetalhesMemoriaView(master=self.master, detalhes_dict=self._detalhes, threads_list=self._threads, pid=self.pid)
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    # A abertura da thread para coletar os dados de forma segura 
    def coletar_detalhes_em_thread(self):
        while not self._stop_event.is_set():
            detalhes = self.model.carregar_detalhes_processo()
            threads = self.model.get_info_threads()
            with self._lock:
                self._detalhes = detalhes
                self._threads = threads
            time.sleep(1)  # Atualiza a cada 1 segundo

    # Atualização da inferface verificando se a janela está mesmo aberta, respeitando o semaforo e definindo um intervalo justo
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