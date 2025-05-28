from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Controllers.DetalhesMemoriaController import DetalhesMemoriaController
from Views.TabelaProcessosMemoriaView import TabelaProcessosMemoriaView

class ProcessosMemoriaController:
    def __init__(self, master):
        self.model = GerenciadorProcessosMemoria()
        self.view = TabelaProcessosMemoriaView(master=master)
        self.atualizar_tabela_processos_memoria()

    def atualizar_tabela_processos_memoria(self):
        dados_processo_memoria = self.model.listar_processos_e_usuarios()
        self.view.mostrar_processos(dados_processo_memoria)

    def mostrar(self):
        self.view.deiconify()
        self.atualizar_tabela_memoria()

    from Models.GerenciadorProcessosMemoria import GerenciadorProcessosMemoria
from Views.TabelaProcessosMemoriaView import TabelaProcessosMemoriaView

class ProcessosMemoriaController:
    def __init__(self, master):
        self.model = GerenciadorProcessosMemoria()
        self.view = TabelaProcessosMemoriaView(master=master)
        self.atualizar_tabela_processos_memoria()

    def atualizar_tabela_processos_memoria(self):
        dados_processo_memoria = self.model.listar_processos_e_usuarios()
        self.view.mostrar_processos(dados_processo_memoria)

    def mostrar(self):
        self.view.deiconify()
        self.atualizar_tabela_memoria()

    def abrir_detalhes_processo(self, proc):
        pid = proc['pid']
        DetalhesMemoriaController(pid, self.view)