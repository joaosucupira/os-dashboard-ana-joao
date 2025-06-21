import threading
import time

# Mudar depois para GerenciadorArquivos!!!
from Models.GerenciadorArquivos import GerenciadorArquivos

# Mudar views!
from Views.TabelaProcessosView import TabelaProcessosView
from Views.TabelaProcessosArquivosView import TabelaProcessosArquivosView

# Mudar depois para detalhesArquivosController!!!
from Controllers.DetalhesProcController import DetalhesProcController

class ArquivosController:
    def __init__(self, master):
        self.inicializa(master)

    def coletar_processos_em_thread(self):
        while not self._stop_event.is_set():
            processos = self.model.listar_processos_e_arquivos()
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
        try:
            
            self.view.destroy()
        except Exception:
            pass

    # Módulo da inicialização do controller: prepara botao, cliques de linha para selecionar processo e thread
    # para rodar a rotina paralelamente
    def inicializa(self, master):
        self.model = GerenciadorArquivos()
        self.view = TabelaProcessosArquivosView(master=master, callback_acao_linha=self.abrir_detalhes_processo)

        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._processos = []

        self._thread = threading.Thread(target=self.coletar_processos_em_thread, daemon=True)
        self._thread.start()

        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_interface()

    def abrir_detalhes_processo(self, proc):
        pid = proc['pid']
        DetalhesProcController(pid, self.view)