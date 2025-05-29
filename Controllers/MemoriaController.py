from Models.GerenciadorMemoria import GerenciadorMemoria
from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Views.TabelaMemoriaView import TabelaMemoriaView
from Controllers.ProcessosMemoriaController import ProcessosMemoriaController

class MemoriaController:
    def __init__(self, master):
        # Inicializa o modelo e a view, define o callback para fechar a janela e inicia a atualização da tabela
        self.model = GerenciadorMemoria()
        self.view = TabelaMemoriaView(master=master, abrir_tabela_processos_memoria_callback=self.abrir_tabela_processos_memoria)
        self.view.protocol("WM_DELETE_WINDOW", self.fechar)
        self.atualizar_tabela_memoria()

    def abrir_tabela_processos_memoria(self):
        # Abre a tabela de processos na memória
        ProcessosMemoriaController(self.view)

    def atualizar_tabela_memoria(self):
        # Atualiza os dados da memória na view a cada 1 segundo
        dados_memoria = self.model.atualizaDados()
        self.view.mostrar_memoria(dados_memoria)
        if self.view.winfo_exists():
            self.view.after(1000, self.atualizar_tabela_memoria)

    def mostrar(self):
        # Exibe a janela da view e atualiza a tabela de memória
        self.view.deiconify()
        self.atualizar_tabela_memoria()

    def fechar(self):
        # Fecha a janela da view
        self.view.destroy()

    def mostrar(self):
        # Exibe a janela da view e atualiza a interface (possível duplicidade de método)
        self.view.deiconify()
        self.atualizar_interface()