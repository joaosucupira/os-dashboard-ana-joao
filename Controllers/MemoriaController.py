from Models.GerenciadorMemoria import GerenciadorMemoria
from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Views.TabelaMemoriaView import TabelaMemoriaView
from Controllers.ProcessosMemoriaController import ProcessosMemoriaController

class MemoriaController:
    def __init__(self, master):
        self.model = GerenciadorMemoria()
        self.view = TabelaMemoriaView(master=master, abrir_tabela_processos_memoria_callback=self.abrir_tabela_processos_memoria)
        self.atualizar_tabela_memoria()

    def abrir_tabela_processos_memoria(self):
        ProcessosMemoriaController(self.view)

    def atualizar_tabela_memoria(self):
        dados_memoria = self.model.atualizaDados()
        self.view.mostrar_memoria(dados_memoria)

    def mostrar(self):
        self.view.deiconify()
        self.atualizar_tabela_memoria()