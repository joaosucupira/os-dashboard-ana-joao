import threading
import time

from Models.GerenciadorDetalhesMemoria import GerenciadorDetalhesMemoria
from Views.DetalhesMemoriaView import DetalhesMemoriaView

class DetalhesMemoriaController:
    def __init__(self, pid, master):
        self.pid = pid
        self.master = master
        self.model = GerenciadorDetalhesMemoria(pid) # Solicita os detalhes do processo identificado por pid
        self._stop_event = threading.Event()  # Evento para sinalizar parada da thread
        self._lock = threading.Lock()         # Lock para acesso seguro aos dados compartilhados
        self._detalhes = {}                   # Dicionário para armazenar detalhes do processo
        self._threads = []                    # Lista para armazenar informações das threads
        self._thread = threading.Thread(target=self.coletar_detalhes_em_thread, daemon=True)  # Thread para coleta dos detalhes
        self._thread.start()
        # Aguarda a primeira coleta antes de criar a view
        while not self._detalhes:
            time.sleep(0.05)

        self.view = DetalhesMemoriaView(master=self.master, detalhes_dict=self._detalhes, threads_list=self._threads, pid=self.pid)  # Cria a view
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)  # Define ação ao fechar a janela
        self.atualizar_interface()  # Inicia atualização periódica da interface

    def coletar_detalhes_em_thread(self):
        # Loop para coletar detalhes do processo e threads periodicamente
        while not self._stop_event.is_set():
            detalhes = self.model.carregar_detalhes_processo()
            threads = self.model.get_info_threads()
            with self._lock:
                self._detalhes = detalhes
                self._threads = threads
            time.sleep(1)  # Atualiza a cada 1 segundo

    def atualizar_interface(self):
        # Atualiza a interface gráfica com os dados mais recentes
        with self._lock:
            detalhes = dict(self._detalhes)
            threads = list(self._threads)
        if hasattr(self.view, "atualizar_detalhes"):
            self.view.atualizar_detalhes(detalhes, threads)
        if self.view.winfo_exists():
            self.view.after(1000, self.atualizar_interface)

    def fechar(self):
        self._stop_event.set()  # Sinaliza para parar a thread de coleta
        self.view.destroy()     # Fecha a janela da view