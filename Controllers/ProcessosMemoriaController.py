import threading
import time

from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Views.TabelaProcessosMemoriaView import TabelaProcessosMemoriaView
from Controllers.DetalhesMemoriaController import DetalhesMemoriaController

class ProcessosMemoriaController:
    def __init__(self, master):
        # Inicializa o modelo e a view, conecta o callback de ação de linha
        self.model = GerenciadorProcessosMemoria()
        self.view = TabelaProcessosMemoriaView(master=master, callback_acao_linha=self.abrir_detalhes_processo)

        #parte de semaforo
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._processos = []

        # Cria e inicia a thread de coleta de processos
        self._thread = threading.Thread(target=self.coletar_processos_em_thread, daemon=True)
        self._thread.start()

        # Configura o evento de fechamento da janela
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_tabela_processos_memoria()

    def coletar_processos_em_thread(self):
        # Loop de coleta dos processos enquanto não houver sinal de parada
        while not self._stop_event.is_set():
            processos = self.model.listar_processos_e_usuarios()
            with self._lock:  # protege o acesso a lista de processos
                self._processos = processos

            time.sleep(1)  # coleta a cada 1 segundo

    def atualizar_tabela_processos_memoria(self):
        # Atualiza a tabela da view com os processos coletados
        with self._lock:
            processos = list(self._processos)

        self.view.mostrar_processos(processos)

        # Agenda a próxima atualização se a janela ainda existir
        if self.view.winfo_exists():
            self.view.after(1000, self.atualizar_tabela_processos_memoria)

    def mostrar(self):
        # Exibe a janela e inicia a atualização da tabela
        self.view.deiconify()
        self.atualizar_tabela_processos_memoria()

    def fechar(self):
        # Sinaliza a thread para parar e fecha a janela
        self._stop_event.set()
        self.view.destroy()

    def abrir_detalhes_processo(self, proc):
        # Abre a janela de detalhes do processo selecionado
        pid = proc['pid']
        DetalhesMemoriaController(pid, self.view)